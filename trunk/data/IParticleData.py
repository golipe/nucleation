# -*- coding: utf-8 -*-

class IParticleData():
    def importSumFile(self, path, date):
        """
        Imports a SUM file to DB.
        @param path: Path to SUM file
        @date: Date in which file is going to be imported
        """
        raise NotImplementedError
        
    def getDayTimes(self, date):
        """Obtiene los momentos (horas) para las que hay datos para una fecha dada.
        @param date: Día para el que se van a obtener las horas de los datos. 
        @return: Lista con las horas de los datos del día dado.
        """
        raise NotImplementedError

    def getDayData(self, date, source):
        """Obtiene todos los datos para una fecha concreta, organizados por tiempo y por tamaño.
        @param date: Fecha para la que se quieren obtener los datos.
        @param source: Data source: 'raw' for raw data; 'mf' for median filter; 'norm' for normalized data.
        @return: Dictionary with one entry for each time, containing another dictionary with particle sizes as keys. 
        """
        raise NotImplementedError

    def getDayHourData(self, date, time, source):
        """
        Obtiene todos los eventos para una date y una htimeconcreta.
        @param date: Fecha para la que se quieren obtener los eventos
        @param time: Hora para la que se quieren obtener los eventos
        @param source: Data source: 'raw' for raw data; 'mf' for median filter; 'norm' for normalized data.
        @return: Diccionario con una entrada para cada tamaño de partículas. 
        """
        raise NotImplementedError

    def getAllActiveDays(self):
        """
        Gets all days that have events.
        @return: List with dates that have events.
        """
        raise NotImplementedError
        
    def getActiveDays(self, year, month):
        """
        Obtiene los días en los que hay eventos para el mes y año especificados.
        @param year: Año para el que se quieren saber los días de eventos.
        @param month: Mes para el que se quieren saber los días de eventos.
        @return: Lista con los cardinales de los días que hay eventos.
        """
        raise NotImplementedError
        
    def isDayPresent(self, fecha):
        """
        Comprueba si en la BD hay eventos para el día dado.
        @param fecha: Fecha a comprobar.
        @return: True si hay eventos, False en caso contrario.
        """
        raise NotImplementedError

    def deleteDayData(self, date, source):
        """
        Borra todos los datos para la fecha indicada.
        @param date: Fecha para la que se van a borrar los datos. 
        @param source: Data source: 'raw' for raw data; 'mf' for median filter; 'norm' for normalized data.
        """
        raise NotImplementedError

    def getGeneralInformation(self):
        """
        Extracts from DB general information of the station.
        @return: tuple with name, location and coordinates as string elements.
        """
        raise NotImplementedError        

    def setGeneralInformation(self, name, location, coords):
        """
        Save into DB general information of the station.
        @param name: Name of the station.
        @param location: Location in text of the station.
        @param coords: Coordinates in text of the station.
        """
        raise NotImplementedError        

    def addDayData(self, date, times, sizes, values, target):
        """
        Add a bunch of data for one day.
        @param date: Date for which data is going to be added.
        @param times: List of times of the day when exists data.
        @param sizes: List of sizes for which data are been measured.
        @param values: ndarray with data to fit with times as rows and sizes as columns.  
        @param target: Data target: 'raw' for raw data; 'mf' for median filter; 'norm' for normalized data.
        """

    def addData(self, date, time, size, value, target):
        """
        Añade un dato de nº de partículas para un tamaño, fecha y momento de tiempo dados. 
        @param date: Fecha del dato. 
        @param time: Momento del día (hora) del dato, dado como cadena.
        @param size: Tamaño de partículas del dato.
        @param value: Nº de partículas.           
        @param target: Data target: 'raw' for raw data; 'mf' for median filter; 'norm' for normalized data.
        """
        raise NotImplementedError

    def getDayNumber(self):
        """
        Gets the number of days with data that DB contains.
        @return: Long value with the number of days 
        """
        raise NotImplementedError

    def getEventNumber(self):
        """
        Gets the number of events that DB contains.
        @return: Long value with the number of events 
        """
        raise NotImplementedError

    def deleteTrainingData(self, date=None):
        """
        Deletes training data from DB for an specific date or all data.
        @param date: Date which data is going to be deleted. If None, all dates will be deleted.
        """
        raise NotImplementedError

    def getTrainingData(self, class_id):
        """
        Get training data for an specific class.
        @param class_id: Id of the class to retrieve.
        @return: array with class training data. 
        """
        raise NotImplementedError
    
    def addTrainingData(self, class_id, values):
        """
        Add a bunch of training data.
        @param class_id: ID of the class to store.
        @param values: ndarray or list of lists with training data.  
        """
        raise NotImplementedError        
