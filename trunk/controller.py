# -*- coding: utf-8 -*-
import datetime
import math         # Basic maths
import os           # OS operations
import re           # Regular expressions
from data.ParticleDataSQLite import ParticleDataSQLite
import scipy.signal
import numpy
import csv
import scipy.cluster.vq

class Controller():
    def __init__(self, appPath):
        self.data = None
        self.view = None
        self.operations = {}
        self.appPath = appPath
        self.nucleationSizeLimit = 0.000000025 # 25 nm
        self.relevantWindowSize = 12
    
    def setView(self, view):
        """
        Set view instance for calling interface update methods
        """
        self.view = view
        self.initInterface()

    def newDb(self, path):
        if os.path.exists(path): os.remove(path)
        self.data = ParticleDataSQLite(path)
        self.initInterface()

    def openDb(self, path):
        self.data = ParticleDataSQLite(path)
        self.initInterface()
        self.view.updateGeneralInformation()
        self.view.updateStats()
        self.view.updateCalendar()

    def initInterface(self):
        """
        Llama a los procedimientos necesarios del interfaz para resetear el mismo.
        """
        self.view.initInterface()

    def _getDateTimeFromJulianDate(self, julianDate):
        X = float(julianDate)
        Z = math.floor(X)
        F = X - Z
        Y = math.floor((Z - 1867216.25) / 36524.25)
        A = Z + 1 + Y - math.floor(Y / 4)
        B = A + 1524
        C = math.floor((B - 122.1)/365.25)
        D = math.floor(365.25 * C)
        G = math.floor((B - D) / 30.6001)
        month = (G - 1) if (G < 13.5) else (G - 13)
        year = (C - 4715) if (month < 2.5) else (C - 4716)
        UT = B - D - math.floor(30.6001 * G) + F
        day = int(math.floor(UT))
        UT -= math.floor(UT)
        UT *= 24
        hour = int(math.floor(UT))
        UT -= math.floor(UT)
        UT *= 60
        minute = int(math.floor(UT))
        UT -= math.floor(UT)
        UT *= 60
        second = int(round(UT))
        return datetime.datetime(int(year), int(month), day, hour, minute, second)

    def _getTimeFromJulianDate(self, julianDate):
        julianDate = float(julianDate)
        UT = julianDate - math.floor(julianDate)
        UT -= math.floor(UT)
        UT *= 24
        hour = int(math.floor(UT))
        UT -= math.floor(UT)
        UT *= 60
        minute = int(math.floor(UT))
        UT -= math.floor(UT)
        UT *= 60
        second = int(round(UT))
        return datetime.time(hour, minute, second)

    def importSUM(self, path, date):
        """
        Imports a SUM file and update interface consequently.
        """
        if self.data.isDayPresent(date):
            if self.view.showDayPresentDialog():
                self.data.deleteDayData(date, 'norm')
                self.data.deleteDayData(date, 'mf')
                self.data.deleteDayData(date, 'raw')
            else:
                return
        result = self.data.importSumFile(path, date)
        self.view.showImportResult(result)
        if result:
            self.view.updateCalendar()

    def importTraining(self, path):
        self.reader = csv.DictReader(open(path, "r"), delimiter=',')
        classes = {}
        # Delete previous training data
        self.data.deleteTrainingData()
        # Perform sum of all elements of the class 
        for record in self.reader:
            date = datetime.datetime(int(record['YEAR']), 1, 1) + datetime.timedelta(int(record['DAY']) - 1)
            date = date.date()
            measures = self.data.getDayData(date, 'norm')
            if len(measures):
                class_id = int(record['CLASS'])
                times = measures.keys()
                times.sort()
                sizes = measures[times[0]].keys()
                sizes.sort()
                if classes.get(class_id):
                    hits_count, class_measures = classes.get(class_id)
                    hits_count += 1
                else:
                    hits_count = 1
                    class_measures = numpy.zeros((len(times), 14), dtype=numpy.float64)
                offset = 14 - len(sizes)
                for i in range(len(times)):
                    for j in range(len(sizes)):
                        class_measures[i][offset + j] += measures[times[i]][sizes[j]]
                classes[class_id] = (hits_count, class_measures)
            else:
                print "No normalized data for %s" %(date)
        # Compute average
        class_ids = classes.keys()
        for class_id in class_ids:
            hits_count, class_measures = classes[class_id]
            class_range = class_measures.shape
            for i in range(class_range[0]): 
                for j in range(class_range[1]):
                    class_measures[i][j] /= hits_count
            # Store training data
            self.data.addTrainingData(class_id, class_measures)

    def performKmeans(self):
        # Construct centroid array
        centroids = []
        max_classes = 5
        for i in range(max_classes): # TODO: Coger de la BD el nº de clases
            centroid = self.data.getTrainingData(i)
            shape = centroid.shape
            centroids.append([item for sublist in centroid for item in sublist])
        centroids = numpy.array(centroids) 
        dates = self.data.getAllActiveDays()
        observations = []
        for i in range(len(dates)):
            measures = self.data.getDayData(dates[i], 'norm')
            if len(measures): 
                times = measures.keys()
                times.sort()
                sizes = measures[times[0]].keys()
                sizes.sort()
                offset = shape[1] - len(sizes)
                observation = numpy.zeros(shape[0] * shape[1], numpy.float64)
                for i in range(len(times)):
                    for j in range(len(sizes)):
                        observation[i * shape[1] + offset + j] += measures[times[i]][sizes[j]]
            observations.append(observation)
        observations = numpy.array(observations)
        centroid, labels = scipy.cluster.vq.kmeans2(observations, centroids, iter=10, thresh=1e-05, minit='matrix')
        # Evaluation
        classes = {}
        rank_classes = {}
        for i in range(max_classes):
            classes[i] = []
            rank_classes[i] = [0, 0]
            for j in range(len(labels)):
                if labels[j] == i:
                    classes[i].append(dates[j]) 
            print "Clase %s - Total: %s" %(i, len(classes[i]))
            #print classes[i]
        self.reader = csv.DictReader(open(os.path.join(self.appPath, 'hyde_clean_06.csv'), "r"), delimiter=',')
        for record in self.reader:
            date = datetime.datetime(int(record['year']), 1, 1) + datetime.timedelta(int(record['day']) - 1)
            date = date.strftime('%Y-%m-%d')
            owner_class = None
            if record['event_1'] == '1':
                owner_class = 0
            elif record['event_2'] == '1':
                owner_class = 1
            elif record['event_3'] == '1':
                owner_class = 2
            elif record['event_0'] == '1':
                owner_class = 3
            elif record['non_event'] == '1':
                owner_class = 4
            if not owner_class is None:
                rank_classes[owner_class][0] += 1
                for date_class in classes[i]:
                    if date_class == date:
                        rank_classes[owner_class][1] += 1
                        break
        for i in range(max_classes):
            print "Clase %s. Nº elementos manual: %s - Bien clasificados: %s" %(i, rank_classes[i][0], rank_classes[i][1])

    def _constructReExpression(self, pattern):
        regexPattern = pattern.replace('%y', '[0-9][0-9]')
        regexPattern = regexPattern.replace('%yyy', '[0-9][0-9][0-9][0-9]')
        regexPattern = regexPattern.replace('%m', '[0-9][0-9]')
        regexPattern = regexPattern.replace('%d', '[0-9][0-9]')
        regexPattern = '^' + regexPattern + '$'
        return re.compile(regexPattern, re.IGNORECASE)

    def importFolder(self, path, pattern, progressDialog, numberFiles):
        """
        Preparan el patrón RegEx para pasarlo como patrón a un método recursivo que examina los posibles
        archivos a importar.
        @param path: Ruta de la carpeta raíz a importar
        @param pattern: Patrón para obtener la fecha a través del nombre de archivo.
        Códigos:
        - %yyy - Año con cuatro cifras
        - %y - Año con dos cifras
        - %m - Mes con dos cifras
        - %d - Día con dos cifras
        """
        expression = self._constructReExpression(pattern)
        result = True
        count = 0
        # Walk trough entire path
        for dirname, dirnames, filenames in os.walk(path):
            for filename in filenames:
                # See if filename match the pattern
                if expression.match(filename):
                    count += 1
                    # Extract date
                    index = pattern.find('%yyy')
                    if index > -1:
                        year = int(filename[index : index + 4])
                    else:
                        index = pattern.find('%y')
                        year = int(filename[index : index + 2])
                        # Ajuste a cuatro cifras
                        year += 2000 if year < 70 else 1900
                    index = pattern.find('%m')
                    month = int(filename[index : index + 2])
                    index = pattern.find('%d')
                    day = int(filename[index : index + 2])
                    date = datetime.date(year, month, day)
                    if self.data.isDayPresent(date): 
                        self.data.deleteDayData(date, 'norm')
                        self.data.deleteDayData(date, 'mf')
                        self.data.deleteDayData(date, 'raw')
                    result = self.data.importSumFile(os.path.join(dirname, filename), date)
                    result = result and progressDialog.Update(count, 'Importing file %s/%s' %(count, numberFiles))[0]
                    while self.view.Pending(): self.view.Dispatch() # assure correct display
                    if not result: break
            if not result: break
        self.view.showImportResult(result)
        return

    def getNumberFiles(self, path, pattern):
        expression = self._constructReExpression(pattern)
        count = 0
        for dirname, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if expression.match(filename): count += 1
        return count
        
    def medianFilterOneDay(self, date, window):
        """
        Makes a median filter of given date and stores in DB.
        @param date: Date for which median filter is going to be calculated.
        @param window: List of two elements specifying window size for the algorithm.
        """
        result = self._medianFilter(self.data.getDayData(date, 'raw'), window)
        if result:
            times, sizes, values = result
            # Delete previous data if any
            self.data.deleteDayData(date, 'mf')
            # Add new data
            self.data.addDayData(date, times, sizes, values, 'mf')
        else:
            print "Incorrect data for date: %s" %(date)
        return bool(result)

    def medianFilterAll(self, window, progressDialog, numberDays):
        """
        Makes a median filter of all dates and stores in DB.
        @param window: List of two elements specifying window size for the algorithm.
        """
        dates = self.data.getAllActiveDays()
        count = 0
        for date in dates:
            count += 1
            self.medianFilterOneDay(date, window)
            if not progressDialog.Update(count, 'Calculating day %s/%s' %(count, numberDays))[0]: break
            while self.view.Pending(): self.view.Dispatch() # assure correct display

    def _medianFilter(self, events, window):
        """
        Makes a median filter of given data.
        @param events: Data for doing median filter.
        @param window: List of two elements specifying window size for the algorithm.
        @return: array with data filter by median 
        """
        if len(events):
            # Build array from events dictionary
            sizes = events.values()[0].keys()
            sizes.sort()
            times = events.keys()
            times.sort()
            eventsMatrix = []
            for time in times:
                rowTime = []
                for size in sizes:
                    rowTime.append(events[time][size])
                eventsMatrix.append(rowTime)
            # Do median filter
            try:
                result = scipy.signal.medfilt2d(eventsMatrix, window)
            except:
                return None
            return (times, sizes, result)
        else:
            return None
        
    def relevantWindowDay(self, date, windowSize, method, source):
        size_max, time_max = self._relevantWindow(date, windowSize, method=method, source=source)
        if size_max:
            self.data.setDayRelevantWindow(date, 0, size_max, time_max - windowSize + 1, time_max)

    def relevantWindowAll(self, windowSize, method, source, progressDialog, numberDays):
        dates = self.data.getAllActiveDays()
        count = 0
        for date in dates:
            count += 1
            self.relevantWindowDay(date, windowSize, method=method, source=source)
            if not progressDialog.Update(count, 'Calculating day %s/%s' %(count, numberDays))[0]: break
            while self.view.Pending(): self.view.Dispatch() # assure correct display
        
    def _relevantWindow(self, date, windowSize, method='max', source='raw'):
        """
        Calculates relevant data window of given date.
        @param date: Date for which relevant window is going to be calculated.
        @param windowSize: Vertical size of the window (time lapse). Horizontal window size is calculated 
        automatically from nucleationSizeLimit variable.
        @param metod: 'max' for maximum intensity, 'dif' for differential intensity.
        @return: tuple with left, right, top and bottom indexes of the window. 
        """
        captures = self.data.getDayData(date, source)
        if len(captures):
            times = captures.keys()
            times.sort()
            # Determine particle size interval relevant from first capture of the day
            capture = captures[times[0]]
            size_upper_limit = 0
            sizes = capture.keys()
            sizes.sort()
            while sizes[size_upper_limit] < self.nucleationSizeLimit:
                size_upper_limit += 1 # keep this value instead minus 1 to get index of next bin after nucleation mode size limit 
            windowSize -= 1 # Adjust window size for 0-base index issue
            time_upper_limit = windowSize
            max_sum = 0
            for time_pos in range(0, len(times) - windowSize - 1):
                local_sum = 0
                for i in range(time_pos, time_pos + windowSize):
                    dataTime = captures[times[i]]
                    if dataTime:
                        for j in range(0, size_upper_limit):
                            if dataTime[sizes[j]]:
                                if method == 'max': 
                                    # Calculate sum of the values of the window
                                    local_sum += dataTime[sizes[j]]
                                elif method == 'dif':
                                    # Calculate sum of the increments of the window
                                    if i > 0 and captures[times[i-1]][sizes[j]]: local_sum += dataTime[sizes[j]] - captures[times[i-1]][sizes[j]]
                if local_sum > max_sum:
                    max_sum = local_sum
                    time_upper_limit = time_pos + windowSize
            return size_upper_limit, time_upper_limit
        else:
            return (None, None)

    def normalizationDay(self, date, source='raw'):
        self.data.deleteDayData(date, 'norm')
        # Get data
        captures = self.data.getDayData(date, source)
        relevantWindow = self.data.getDayRelevantWindow(date)
        if relevantWindow and len(captures):
            times = captures.keys()
            times.sort()
            sizes = captures[times[0]].keys()
            sizes.sort()
            # Reduce keys to relevant window frame
            times = times[relevantWindow[2]:relevantWindow[3]+1]
            sizes = sizes[relevantWindow[0]:relevantWindow[1]+1]
            # Get maximum value of the window
            maximum = 0
            for time in times:
                for size in sizes:
                    if captures[time][size] > maximum:
                        maximum = captures[time][size]
            # Normalize
            normalizedData = []
            for time in times:
                timeData = []
                for size in sizes:
                    if captures[time][size]:
                        timeData.append(captures[time][size] / maximum)
                    else:
                        timeData.append(0.0)
                normalizedData.append(timeData)
            self.data.addDayData(date, times, sizes, normalizedData, 'norm')
        else:
            # TODO: Informar del error de otra forma
            print "No data or relevant window for date %s" %(date)

    def normalizationAll(self, source, progressDialog, numberDays):
        dates = self.data.getAllActiveDays()
        count = 0
        for date in dates:
            count += 1
            self.normalizationDay(date, source=source)
            if not progressDialog.Update(count, 'Calculating day %s/%s' %(count, numberDays))[0]: break
            while self.view.Pending(): self.view.Dispatch() # assure correct display
