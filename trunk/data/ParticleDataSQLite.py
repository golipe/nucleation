# -*- coding: utf-8 -*-
import sqlite3
import unittest
import os
import datetime
import math
from IParticleData import IParticleData
from argparse import ArgumentError
import numpy

# Métodos para manejar datos complejos con SQLite fácilmente
def dateAdapt(date):
    return date.strftime('%Y-%m-%d')
def dateConvert(text):
    return text.strptime('%Y-%m-%d')
sqlite3.register_adapter(datetime.date, dateAdapt)
sqlite3.register_converter("event_date", dateConvert)
def timeAdapt(time):
    return time.strftime('%H:%M:%S')
def timeConvert(text):
    return text.strptime('%H:%M:%S')
sqlite3.register_adapter(datetime.time, timeAdapt)
sqlite3.register_converter("hour", timeConvert)

class ParticleDataSQLite(IParticleData):
    """"
    Clase que contiene todos los datos de eventos de nucleacion
    """
    def __init__(self, path):
        self.path = path
        isNewDb = not os.path.exists(path) 
        self.connection = sqlite3.connect(path, detect_types = sqlite3.PARSE_DECLTYPES or sqlite3.PARSE_COLNAMES)
        self.cursor = self.connection.cursor()
        self._modifyDb()
        self.cacheHours = {}
        self.cacheDates = {}
        self.cacheSizes = {}
        if isNewDb: self._newDb()

    def _modifyDb(self):
        """
        For existing DBs, to update to last definition
        """
        try:
            self.cursor.execute("ALTER TABLE dates ADD size_min INTEGER") 
            self.cursor.execute("ALTER TABLE dates ADD size_max INTEGER")
            self.cursor.execute("ALTER TABLE dates ADD time_min INTEGER")
            self.cursor.execute("ALTER TABLE dates ADD time_max INTEGER")
            self.cursor.commit()
        except:
            pass
        try:
            self.cursor.execute('CREATE TABLE eventsN (id INTEGER PRIMARY KEY, date_id INTEGER, hour_id INTEGER, size_id INTEGER, value REAL)')
            self.cursor.execute('CREATE INDEX indexEventsN ON eventsN (date_id, hour_id)')
        except:
            pass
        try:
            self.cursor.execute('CREATE TABLE classes (id INTEGER PRIMARY KEY, name TEXT)')        
            self.cursor.execute("INSERT INTO classes VALUES (?, ?)", (0, "Event class 1"))
            self.cursor.execute("INSERT INTO classes VALUES (?, ?)", (1, "Event class 2"))
            self.cursor.execute("INSERT INTO classes VALUES (?, ?)", (2, "Event class 3"))
            self.cursor.execute("INSERT INTO classes VALUES (?, ?)", (3, "Event class 0"))
            self.cursor.execute("INSERT INTO classes VALUES (?, ?)", (4, "Non event"))

            self.cursor.execute('CREATE TABLE centroids (id INTEGER PRIMARY KEY, class_id INTEGER, hour_index INTEGER, size_index INTEGER, value REAL)')
        except:
            pass

    def _newDb(self):
        """
        Performs needed operations in a new DB.
        """
        self.cursor.execute('CREATE TABLE general (id INTEGER PRIMARY KEY, name TEXT, location TEXT, coords TEXT)')
        self.cursor.execute("INSERT INTO general VALUES (?, ?, ?)", (0, "", ""))
        self.cursor.execute('CREATE TABLE dates (id INTEGER PRIMARY KEY, date TEXT UNIQUE, size_min INTEGER, size_max INTEGER, time_min INTEGER, time_max INTEGER)')
        self.cursor.execute('CREATE TABLE hours (id INTEGER PRIMARY KEY, hour TEXT UNIQUE)')
        self.cursor.execute('CREATE TABLE hoursDay (date_id INTEGER, hour_id INTEGER)')
        self.cursor.execute('CREATE TABLE sizes (id INTEGER PRIMARY KEY, size REAL UNIQUE)')
        self.cursor.execute('CREATE TABLE events (id INTEGER PRIMARY KEY, date_id INTEGER, hour_id INTEGER, size_id INTEGER, value REAL)')
        self.cursor.execute('CREATE INDEX hoursDayEvents ON hoursDay (date_id, hour_id)')
        self.cursor.execute('CREATE INDEX indexEvents ON events (date_id, hour_id)')
        # Tablas para el filtro de mediana
        self.cursor.execute('CREATE TABLE eventsMF (id INTEGER PRIMARY KEY, date_id INTEGER, hour_id INTEGER, size_id INTEGER, value REAL)')
        self.cursor.execute('CREATE INDEX indexEventsMF ON eventsMF (date_id, hour_id)')
        # Tablas para los datos normalizados
        self.cursor.execute('CREATE TABLE eventsN (id INTEGER PRIMARY KEY, date_id INTEGER, hour_id INTEGER, size_id INTEGER, value REAL)')
        self.cursor.execute('CREATE INDEX indexEventsN ON eventsN (date_id, hour_id)')
        # Tablas para el entrenamiento
        self.cursor.execute('CREATE TABLE classes (id INTEGER PRIMARY KEY, name TEXT)')        
        self.cursor.execute('CREATE TABLE centroids (id INTEGER PRIMARY KEY, class_id INTEGER, hour_index INTEGER, size_index INTEGER, value REAL)')
        self.cursor.execute('CREATE INDEX indexCentroids ON centroids (class_id)')
        self.cursor.execute("INSERT INTO classes VALUES (?, ?, ?)", (0, "Event class 1"))
        self.cursor.execute("INSERT INTO classes VALUES (?, ?, ?)", (1, "Event class 2"))
        self.cursor.execute("INSERT INTO classes VALUES (?, ?, ?)", (2, "Event class 3"))
        self.cursor.execute("INSERT INTO classes VALUES (?, ?, ?)", (4, "Event class 0"))
        self.cursor.execute("INSERT INTO classes VALUES (?, ?, ?)", (5, "Non event"))

        self.connection.commit()
    
    def __del__(self):
        self.connection.close()
    
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
        if second == 60:
            minute += 1
            second = 0
        if (hour > 23) or (minute > 59) or (second > 59):
            print "Tiempo incorrecto: %s:%s:%s" %(hour, minute, second)
            return None
        else:
            return datetime.time(hour, minute, second)
    
    def _getDateId(self, date):
        """
        Obtiene el ID de la tabla 'dates' para la fecha dada, recuperándolo de la BD.
        @return: El ID del día dado, None en caso de que no se encuentre. 
        """
        date_id = self.cacheDates.get(date) 
        if date_id:
            return date_id
        else:
            self.cursor.execute("SELECT * FROM dates WHERE date = ?", (date, ))
            row = self.cursor.fetchone()
            if row:
                self.cacheDates[date] = row[0]
                return row[0]
            else:
                return None

    def _getCreateDateId(self, date):
        """
        Obtiene el ID de la tabla 'dates' para la fecha dada, recuperándolo de la BD
        si ya existe, y si no, creándolo nuevo
        @return: El ID del día dado. 
        """
        date_id = self._getDateId(date)
        if date_id:
            return date_id
        else:
            self.cursor.execute("INSERT INTO dates VALUES (NULL, ?)", (date, ))
            self.connection.commit()            
            self.cacheDates[date] = self.cursor.lastrowid 
            return self.cursor.lastrowid

    def _getCreateSizeId(self, size):
        """
        Obtiene el ID de la tabla 'sizes' para el tamaño dado, recuperándolo de la BD 
        si ya existe, y si no, creándolo nuevo.
        @param size: Tamaño a buscar/crear en la BD. 
        """
        size_id = self.cacheSizes.get(size)
        if size_id:
            return size_id
        else:
            self.cursor.execute("SELECT * FROM sizes WHERE size = ?", (size, ))
            row = self.cursor.fetchone()
            if row:
                self.cacheSizes[size] = row[0]
                return row[0]
            else:
                self.cursor.execute("INSERT INTO sizes VALUES (NULL, ?)", (size, ))
                self.connection.commit()
                self.cacheSizes[size] = self.cursor.lastrowid
                return self.cursor.lastrowid

    def _getHourId(self, hour):
        hour_id = self.cacheHours.get(hour) 
        if hour_id:
            return hour_id
        else:
            self.cursor.execute("SELECT * FROM hours WHERE hour = ?", (hour, ))
            row = self.cursor.fetchone()
            if row:
                self.cacheHours[hour] = row[0]
                return row[0]
            else:
                return None

    def _getCreateHourId(self, time):
        """
        Obtiene el ID de la tabla 'hours' para el tamaño dado, recuperándolo de la BD 
        si ya existe, y si no, creándolo nuevo.
        @param time: Tiempo a buscar/crear en la BD. 
        """
        hour_id = self._getHourId(time)
        if hour_id:
            return hour_id
        else:
            self.cursor.execute("INSERT INTO hours VALUES (NULL, ?)", (time, ))
            self.connection.commit()            
            self.cacheHours[time] = self.cursor.lastrowid
            return self.cursor.lastrowid

    def importSumFile(self, path, fecha):
        """
        Imports a SUM file to DB.
        @param path: Path to SUM file
        @date: Date in which file is going to be imported
        """
        try:
            eventFile = open(path, 'r')
        except:
            return False
        # Añadir registro de fecha
        self.cursor.execute("INSERT INTO dates VALUES (NULL, ?, NULL, NULL, NULL, NULL)", (fecha, ))
        date_id = self.cursor.lastrowid
        # Leer primera línea
        firstLine = eventFile.readline()
        size_columns = firstLine.split()
        sizes_id = []
        for size_column in size_columns:
            sizes_id.append(self._getCreateSizeId(float(size_column)))
        # Leer resto de líneas
        for linea in eventFile.readlines():
            event_columns = linea.split()
            # Obtener hora
            if len(event_columns):
                time = self._getTimeFromJulianDate(event_columns[0])
                if time:
                    time_id = self._getCreateHourId(time)
                    # Añadir registro de la hora para ese día
                    self.cursor.execute("INSERT INTO hoursDay VALUES (?, ?)", (date_id, time_id))
                    i = 2
                    while i < len(event_columns):
                        val = float(event_columns[i])
                        self.cursor.execute("INSERT INTO events VALUES (NULL, ?, ?, ?, ?)", (date_id, time_id, sizes_id[i], 0.0 if math.isnan(val) else val))
                        i += 1
                else:
                    print path
        eventFile.close()
        self.connection.commit()
        return True

    def getGeneralInformation(self):
        """
        Extracts from DB general information of the station.
        @return: tuple with name, location and coordinates as string elements.
        """
        self.cursor.execute("SELECT * FROM general WHERE id=0")
        row = self.cursor.fetchone()
        return (row[1], row[2], row[3])

    def setGeneralInformation(self, name, location, coords):
        """
        Save into DB general information of the station.
        @param name: Name of the station.
        @param location: Location in text of the station.
        @param coords: Coordinates in text of the station.
        """
        self.cursor.execute("UPDATE general SET name=?, location=?, coords=? WHERE id=0", (name, location, coords))
        self.connection.commit()

    def getDayNumber(self):
        """
        Gets the number of days with data that DB contains.
        @return: Long value with the number of days 
        """
        self.cursor.execute("SELECT COUNT(id) FROM dates")
        row = self.cursor.fetchone()
        return row[0]

    def getEventNumber(self):
        """
        Gets the number of events that DB contains.
        @return: Long value with the number of events 
        """
        self.cursor.execute("SELECT COUNT(id) FROM events")
        row = self.cursor.fetchone()
        return row[0]

    def getDayTimes(self, date):
        """
        Obtiene los tiempos para los que hay datos para un día dado.
        @param date: Día para el que se van a obtener las horas de los datos. 
        @return: Lista con los tiempos de los datos del día dado.
        """
        times = []
        date_id = self._getDateId(date)
        if date_id:
            self.cursor.execute("SELECT hours.hour FROM hoursDay, hours WHERE hoursDay.hour_id = hours.id AND date_id = ?", (date_id,))
            for row in self.cursor:
                times.append(row[0])
        times.sort()
        return times
    
    def getDayData(self, date, source):
        """
        Get all events for an specific date, organiced by time and size.
        @param date: Fecha para la que se quieren obtener los eventos
        @param source: Data source. 'raw' for raw data. 'mf' for median filter.
        @return: Dictionary with one entry for each time, containing another dictionary with particle sizes as keys. 
        """
        times = self.getDayTimes(date)
        events = {}
        for time in times:
            eventsTime = self.getDayHourData(date, time, source)
            if len(eventsTime): events[time] = eventsTime
        return events

    def getDayHourData(self, date, time, source):
        """
        Obtiene todos los eventos para una date y una time concreta.
        @param date: Fecha para la que se quieren obtener los eventos
        @param time: Hora para la que se quieren obtener los eventos
        @param source: Data source. 'raw' for raw data. 'mf' for median filter.
        @return: Diccionario con una entrada para cada tamaño de partículas. 
        """
        date_id = self._getDateId(date)
        hour_id  = self._getHourId(time)
        events = {}
        if date_id and hour_id:
            if source == 'raw':
                srcTable = 'events' 
            elif source == 'mf':
                srcTable = 'eventsMF'
            elif source == 'norm':
                srcTable = 'eventsN'
            else:
                raise ArgumentError('source', 'Invalid value for argument.')
            self.cursor.execute("SELECT sizes.size, %s.value FROM %s, sizes WHERE date_id = ? AND hour_id = ? AND sizes.id = %s.size_id" %(srcTable, srcTable, srcTable), (date_id, hour_id))
            for row in self.cursor:
                events[row[0]] = row[1]
        return events

    def getAllActiveDays(self):
        """
        Gets all days that have events.
        @return: List with dates that have events.
        """
        self.cursor.execute("SELECT date FROM dates")
        days = []
        for row in self.cursor:
            days.append(row[0])
        return days        
        
    def getActiveDays(self, year, month):
        """
        Obtiene los días en los que hay eventos para el mes y año especificados.
        @param year: Año para el que se quieren saber los días de eventos.
        @param month: Mes para el que se quieren saber los días de eventos.
        @return: Lista con los cardinales de los días que hay eventos.
        """
        fechaMin = datetime.date(year, month, 1)
        fechaMax = datetime.date(year, month + 1, 1) if month < 12 else datetime.date(year + 1, 1, 1)
        self.cursor.execute("SELECT date FROM dates WHERE date >= ? AND date < ?", (fechaMin, fechaMax))
        days = []
        for row in self.cursor:
            #TODO: Conseguir que funcione dateConvert para no tener que coger el día de esta forma 
            days.append(int(row[0].split('-')[2]))
        return days
        
    def isDayPresent(self, fecha):
        """
        Comprueba si en la BD hay eventos para el día dado.
        @param fecha: Fecha a comprobar.
        @return: True si hay eventos, False en caso contrario.
        """
        self.cursor.execute("SELECT date FROM dates WHERE date = ?", (fecha,))
        return self.cursor.fetchone()

    def deleteDayData(self, date, source):
        """
        Borra todos los datos para la fecha indicada.
        @param date: Fecha para la que se van a borrar los datos. 
        @param source: Data source. 'raw' for raw data. 'mf' for median filter.
        """
        date_id = self._getDateId(date)
        if date_id: 
            if source == 'raw':
                self.cursor.execute("DELETE FROM events WHERE date_id = ?", (date_id,))
                self.cursor.execute("DELETE FROM eventsMF WHERE date_id = ?", (date_id,))
                self.cursor.execute("DELETE FROM hoursDay WHERE date_id = ?", (date_id,))
                self.cursor.execute("DELETE FROM dates WHERE id = ?", (date_id,))
                # remove cache
                self.cacheDates.pop(date)
            elif source == 'mf':
                self.cursor.execute("DELETE FROM eventsMF WHERE date_id = ?", (date_id,))                
            elif source == 'norm':
                self.cursor.execute("DELETE FROM eventsN WHERE date_id = ?", (date_id,))                
            else:
                raise ArgumentError('source', 'Invalid value for argument.')
            self.connection.commit()
        return

    def addData(self, date, time, size, value, target):
        """
        Añade un dato de nº de partículas para un tamaño, fecha y momento de tiempo dados. 
        @param date: Fecha del dato. 
        @param time: Momento del día (hora) del dato, dado como cadena.
        @param size: Tamaño de partículas del dato.
        @param value: Nº de partículas.           
        @param target: Data target: 'raw' for raw data; 'mf' for median filter; 'norm' for normalized data.
        """
        date_id = self._getCreateDateId(date)
        size_id = self._getCreateSizeId(size)
        hour_id = self._getCreateHourId(time)
        # Añadir la entrada de la hora para el día en concreto, si es necesario
        if target == 'raw':
            self.cursor.execute("SELECT * FROM hoursDay WHERE date_id = ? AND hour_id = ?", (date_id, hour_id))
            row = self.cursor.fetchone()
            if not row:
                self.cursor.execute("INSERT INTO hoursDay VALUES (?, ?)", (date_id, hour_id))
            self.cursor.execute("INSERT INTO events VALUES (NULL, ?, ?, ?, ?)", (date_id, hour_id, size_id, value))
        elif target == 'mf':
            self.cursor.execute("INSERT INTO eventsMF VALUES (NULL, ?, ?, ?, ?)", (date_id, hour_id, size_id, value))
        elif target == 'norm':
            self.cursor.execute("INSERT INTO eventsMF VALUES (NULL, ?, ?, ?, ?)", (date_id, hour_id, size_id, value))
        else:
            raise ArgumentError('target', 'Invalid value for argument.')
        self.connection.commit()

    def addDayData(self, date, times, sizes, values, target):
        """
        Add a bunch of data for one day.
        @param date: Date for which data is going to be added.
        @param times: List of times of the day when exists data.
        @param sizes: List of sizes for which data are been measured.
        @param values: ndarray or list of lists with data to fit with times as rows and sizes as columns.  
        @param target: Data target: 'raw' for raw data; 'mf' for median filter; 'norm' for normalized data.
        """
        date_id = self._getCreateDateId(date)
        sizes_id = []
        times_id = []
        # Prepare ids
        for size in sizes:
            sizes_id.append(self._getCreateSizeId(float(size)))
        for time in times:
            times_id.append(self._getCreateHourId(time))
        # Select target table
        if target == 'raw':
            targetTable = 'events' 
        elif target == 'mf':
            targetTable = 'eventsMF'
        elif target == 'norm':
            targetTable = 'eventsN'
        else:
            raise ArgumentError('target', 'Invalid value for argument.')
        # insert data
        for i in range(len(times)):
            for j in range(len(sizes)):
                self.cursor.execute("INSERT INTO %s VALUES (NULL, ?, ?, ?, ?)" %(targetTable), (date_id, times_id[i], sizes_id[j], values[i][j]))
        self.connection.commit()      

    def getDayRelevantWindow(self, date):
        self.cursor.execute("SELECT size_min, size_max, time_min, time_max FROM dates WHERE date = ?", (date, ))
        row = self.cursor.fetchone()
        if row and not row[0] is None:
            return (row[0], row[1], row[2], row[3])
        else:
            return None
    
    def setDayRelevantWindow(self, date, size_min, size_max, time_min, time_max):
        self.cursor.execute("UPDATE dates SET size_min=?, size_max=?, time_min=?, time_max=? WHERE date = ?", (size_min, size_max, time_min, time_max, date))
        self.connection.commit()

    def deleteTrainingData(self, date=None):
        """
        Deletes training data from DB for an specific date or all data.
        @param date: Date which data is going to be deleted. If None, all dates will be deleted.
        """
        if date is None:
            self.cursor.execute("DELETE FROM centroids")
        else:
            date_id = self._getDateId(date)
            self.cursor.execute("DELETE FROM centroids WHERE date_id=?", (date_id,))
        self.connection.commit()

    def getTrainingData(self, class_id):
        """
        Get training data for an specific class.
        @param class_id: Id of the class to retrieve.
        @return: array with class training data. 
        """
        self.cursor.execute("SELECT MAX(hour_index) FROM centroids WHERE class_id = ?", (class_id, ))
        time_size = self.cursor.fetchone()[0]
        data = numpy.zeros((time_size + 1, 14), dtype=numpy.float64)
        self.cursor.execute("SELECT hour_index, size_index, value FROM centroids WHERE class_id = ?", (class_id, ))
        for row in self.cursor:
            data[row[0]][row[1]] = row[2]
        return data
    
    def addTrainingData(self, class_id, values):
        """
        Add a bunch of training data.
        @param class_id: ID of the class to store.
        @param values: ndarray or list of lists with training data.  
        """
        values_range = values.shape
        # insert data
        for i in range(values_range[0]):
            for j in range(values_range[1]):
                self.cursor.execute("INSERT INTO centroids VALUES (NULL, ?, ?, ?, ?)", (class_id, i, j, values[i][j]))
        self.connection.commit()

if __name__ == '__main__':
    unittest.main()
    #TODO: Crear tests unitarios
