#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wx import *
import interfaceResources
import wxPython
from interfaceResources import panelData
import datetime
import time
import os
import matplotlib
import math

class frameANuCla(interfaceResources.frameANuCla):
    def __init__( self, controller, parent, app):
        self.controller = controller
        self.app = app
        self.rawEventsSelected = {}
        self.rawDataTableNeedsUpdate = False
        self.rawLineGraphNeedsUpdate = False
        self.rawHistogramNeedsUpdate = False
        self.mfEventsSelected = {}
        self.mfDataTableNeedsUpdate = False
        self.mfLineGraphNeedsUpdate = False
        self.mfHistogramNeedsUpdate = False
        self.normEventsSelected = {}
        self.normDataTableNeedsUpdate = False
        self.coords = None
        self.dataSource = 'raw'     # data source for calculations
        status = super(frameANuCla, self).__init__(parent)
        # Add tabs
        self.tabRawData = panelData(self.tabMain, self)
        self.tabMain.AddPage(self.tabRawData, 'RAW data')
        self.tabRawData.tabMain.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChanged_tabMain)
        self.tabMedianFilter = panelData(self.tabMain, self)
        self.tabMain.AddPage(self.tabMedianFilter, 'Median filter')
        self.tabMedianFilter.tabMain.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChanged_tabMain)
        self.tabMedianFilter.Show(False)
        self.tabNormalization = panelNormalization(self.tabMain, self)
        self.tabMain.AddPage(self.tabNormalization, 'Normalized')
        self.tabNormalization.Show(False)
        # Draw compass rose in map
        compassImageData = [(0, 0, os.path.join(self.controller.appPath, 'resources', 'compass_rose.png'), {'placement': 'ne'})]
        self.ctlGeneralMap.AddImageLayer(compassImageData, map_rel=False, visible=True, name='<compass_layer>')
        # Bind events
        #self.ctlGeneralMap.Bind(pyslip.EVT_PYSLIP_RIGHTSELECT, self.onRightSelect_ctlGeneralMap)
        #self.ctlGeneralMap.Bind(pyslip.EVT_PYSLIP_SELECT, self.onRightSelect_ctlGeneralMap)
        #self.ctlGeneralMap.Bind(pyslip.EVT_PYSLIP_POSITION, self.onRightSelect_ctlGeneralMap)
        #self.ctlGeneralMap.Bind(pyslip.EVT_PYSLIP_LEVEL, self.onRightSelect_ctlGeneralMap)
        return status

    def initInterface(self):
        # Enable or disable controls
        enabled = not self.controller.data is None
        self.tabGeneral.Enable(enabled)
        self.tabRawData.Enable(enabled)
        self.lstAvailableTimes.Enable(enabled)
        self.calendarControl.Enable(enabled)
        self.menuImportFile.Enable(enabled)
        self.menuImportFolder.Enable(enabled)
        self.menuDeleteDay.Enable(enabled)
        self.menuMedianFilterDay.Enable(enabled)
        self.menuMedianFilterAll.Enable(enabled)
        self.menuRelevantWindowMaxIntensityDay.Enable(enabled)
        self.menuRelevantWindowMaxIntensityAll.Enable(enabled)
        self.menuRelevantWindowDifIntensityDay.Enable(enabled)
        self.menuRelevantWindowDifIntensityAll.Enable(enabled)
        self.menuNormalizationDay.Enable(enabled)
        self.menuNormalizationAll.Enable(enabled)
        self.menuResetTrainingKmeans.Enable(enabled)
        self.menuImportTrainingKmeans.Enable(enabled)
        self.menuClassificationKmeans.Enable(enabled)
        # Empty controls
        self.txtGeneralName.SetValue("")
        self.txtGeneralLocation.SetValue("")
        self.txtGeneralPath.SetValue("")
        self.lstAvailableTimes.Set([])

    ############## EVENTS ##################
    
    def on_menuQuit(self, event):
        self.Close()

    def on_menuAbout(self, event):
        """
        Shows about dialog.
        """
        dlg = dialogAbout(self)
        dlg.ShowModal()
        dlg.Destroy()
        
    def on_menuNew(self, event):
        """
        Prompts for a name and path for new DB.
        """
        dlg = wx.FileDialog(self, message="Select file name", wildcard="*.anc", style=wx.SAVE | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if not path.endswith('.anc'): path += '.anc' 
            self.controller.newDb(path)
        dlg.Destroy()

    def on_menuOpen(self, event):
        """
        Prompts for a path for opening DB.
        """
        dlg = wx.FileDialog(self, "Select a file to open", "", "", wildcard="*.anc|*.*", style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            busyDlg = wx.BusyInfo('Opening file...', self)
            while self.app.Pending(): self.app.Dispatch() # ensure correct display
            self.controller.openDb(dlg.GetPath())
            del busyDlg
        dlg.Destroy()

    def on_menuImportFile(self, event):
        self.app.importFile()
    
    def on_buttonImportFile(self, event):
        self.app.importFile()
        self.onCalendarSelChange_calendarControl(None)

    def on_menuImportFolder(self, event):
        self.app.importFolder()
    
    def on_menuDeleteDay(self, event):
        dlg = wx.MessageDialog(self, 'Do you want to delete selected day?', 'Warning', wx.YES_NO or wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.controller.data.deleteDayData(self.calendarControl.PyGetDate(), 'mf')
            self.controller.data.deleteDayData(self.calendarControl.PyGetDate(), 'norm')
            self.controller.data.deleteDayData(self.calendarControl.PyGetDate(), 'raw')
            self.app.updateCalendar()
            self.onCalendarSelChange_calendarControl(None)
        dlg.Destroy()
    
    def on_menuMedianFilterDay(self, event):
        dlg = dialogMedianFilter(self)
        if dlg.ShowModal() == wx.ID_OK:
            busyDlg = wx.BusyInfo('Calculating median filter...', self)
            while self.app.Pending(): self.app.Dispatch() # ensure correct display
            self.controller.medianFilterOneDay(self.calendarControl.PyGetDate(), [dlg.spinHorWindowSize.GetValue(), dlg.spinVerWindowSize.GetValue()] )
            del busyDlg
        dlg.Destroy()

    def on_menuMedianFilterAll(self, event):
        dlg = dialogMedianFilter(self)
        if dlg.ShowModal() == wx.ID_OK:
            dlg2 = wx.MessageDialog(self, 'WARNING: All previous median filter data will be deleted. Do you want to continue?', 'Warning', wx.YES_NO or wx.ICON_QUESTION)
            if dlg2.ShowModal() == wx.ID_YES:
                maximum = self.controller.data.getDayNumber()
                progressDlg = wx.ProgressDialog('Calculating median filter...', 'Calculating day 0/%s' %(maximum), maximum=maximum, parent=self, style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
                while self.app.Pending(): self.app.Dispatch() # ensure correct display
                self.controller.medianFilterAll( [dlg.spinHorWindowSize.GetValue(), dlg.spinVerWindowSize.GetValue()], progressDlg, maximum )
                progressDlg.Destroy()
            dlg2.Destroy()
        dlg.Destroy()
    
    def on_menuRelevantWindowMaxIntensityDay(self, event):
        busyDlg = wx.BusyInfo('Calculating relevant data window...', self)
        while self.app.Pending(): self.app.Dispatch() # ensure correct display
        self.controller.relevantWindowDay(self.calendarControl.PyGetDate(), self.controller.relevantWindowSize, method='max', source=self.dataSource)
        del busyDlg
        self.rawDataTableNeedsUpdate = True
        self.mfDataTableNeedsUpdate = True
        self._updateTables()

    def on_menuRelevantWindowMaxIntensityAll(self, event):
        maximum = self.controller.data.getDayNumber()
        progressDlg = wx.ProgressDialog('Calculating relevant window...', 'Calculating day 0/%s' %(maximum), maximum=maximum, parent=self, style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
        while self.app.Pending(): self.app.Dispatch() # ensure correct display
        self.controller.relevantWindowAll(self.controller.relevantWindowSize, 'max', self.dataSource, progressDlg, maximum)
        progressDlg.Destroy()
        self.rawDataTableNeedsUpdate = True
        self.mfDataTableNeedsUpdate = True
        self._updateTables()

    def on_menuRelevantWindowDifIntensityDay(self, event):
        busyDlg = wx.BusyInfo('Calculating relevant data window...', self)
        while self.app.Pending(): self.app.Dispatch() # ensure correct display
        self.controller.relevantWindowDay(self.calendarControl.PyGetDate(), self.controller.relevantWindowSize, method='dif', source=self.dataSource)
        del busyDlg
        self.rawDataTableNeedsUpdate = True
        self.mfDataTableNeedsUpdate = True
        self._updateTables()

    def on_menuRelevantWindowDifIntensityAll(self, event):
        maximum = self.controller.data.getDayNumber()
        progressDlg = wx.ProgressDialog('Calculating relevant window...', 'Calculating day 0/%s' %(maximum), maximum=maximum, parent=self, style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
        while self.app.Pending(): self.app.Dispatch() # ensure correct display
        self.controller.relevantWindowAll(self.controller.relevantWindowSize, 'dif', self.dataSource, progressDlg, maximum)
        progressDlg.Destroy()
        self.rawDataTableNeedsUpdate = True
        self.mfDataTableNeedsUpdate = True
        self._updateTables()
    
    def on_menuNormalizationDay(self, event):
        busyDlg = wx.BusyInfo('Normalizing...', self)
        while self.app.Pending(): self.app.Dispatch() # ensure correct display
        self.controller.normalizationDay(self.calendarControl.PyGetDate(), source=self.dataSource)
        del busyDlg
        self._updateInterfaceAfterNormalization()
    
    def on_menuNormalizationAll(self, event):
        maximum = self.controller.data.getDayNumber()
        progressDlg = wx.ProgressDialog('Normalizing...', 'Calculating day 0/%s' %(maximum), maximum=maximum, parent=self, style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
        while self.app.Pending(): self.app.Dispatch() # ensure correct display
        self.controller.normalizationAll(self.dataSource, progressDlg, maximum)
        progressDlg.Destroy()
        self._updateInterfaceAfterNormalization()
    
    def _updateInterfaceAfterNormalization(self):
        # Hide/show normalized tab depending on data
        self.tabNormalization.Show(self._checkNormalizedData(self.calendarControl.PyGetDate()))
        self.normDataTableNeedsUpdate = True
        self._updateTables()

    def on_menuDataSourceRaw(self, event):
        self.dataSource = 'raw'
        self.menuDataSourceRaw.Check(True)
        self.menuDataSourceMf.Check(False)
    
    def on_menuDataSourceMf(self, event):
        self.dataSource = 'mf'
        self.menuDataSourceRaw.Check(False)
        self.menuDataSourceMf.Check(True)

    def on_menuResetTrainingKmeans(self, event):
        self.controller.data.deleteTrainingData()
        dlg = wx.MessageDialog(self, 'Training data has been deleted.', 'Info', wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    def on_menuImportTrainingKmeans(self, event):
        dlg = wx.FileDialog(self, message="Select CSV file", wildcard="*.csv", style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            busyDlg = wx.BusyInfo('Importing training...', self)
            while self.app.Pending(): self.app.Dispatch() # ensure correct display
            self.controller.importTraining(dlg.GetPath())
            del busyDlg
        dlg.Destroy()
    
    def on_menuClassificationKmeans(self, event):
        busyDlg = wx.BusyInfo('Performing classification...', self)
        while self.app.Pending(): self.app.Dispatch() # ensure correct display
        self.controller.performKmeans()
        del busyDlg
    
    def on_buttonImportFolder(self, event):
        self.app.importFolder()

    def onTextEnter_txtGeneralName(self, event):
        if self.controller.data:
            self.controller.data.setGeneralInformation(self.txtGeneralName.GetValue(), self.txtGeneralLocation.GetValue(), self.coords)

    def onTextEnter_txtGeneralLocation(self, event):
        if self.controller.data:
            self.controller.data.setGeneralInformation(self.txtGeneralName.GetValue(), self.txtGeneralLocation.GetValue(), self.coords)

    def onCalendarSelChange_calendarControl(self, event):
        times = self.controller.data.getDayTimes(self.calendarControl.PyGetDate())
        # Disable event handling, because is invoked each time an element is removed
        self.lstAvailableTimes.SetEvtHandlerEnabled(False)
        # Set new list of elements
        self.lstAvailableTimes.Set(times)
        # Select all times by default
        i = 0
        while i < len(times):
            self.lstAvailableTimes.Select(i)
            i += 1
        # Enable event handling again
        self.lstAvailableTimes.SetEvtHandlerEnabled(True)
        # Hide/show median filter tab depending on data
        testMf = self.controller.data.getDayData(self.calendarControl.PyGetDate(), 'mf')
        self.tabMedianFilter.Show(len(testMf))
        self.tabNormalization.Show(self._checkNormalizedData(self.calendarControl.PyGetDate())) # Hide/show normalized tab depending on data
        # Force grid update
        self.onListBox_lstAvailableTimes(None)

    def onMonthYear_calendarControl(self, event):
        self.app.updateCalendar()

    def onListBox_lstAvailableTimes(self, eventList):
        if not self.calendarControl: return
        # Get selected times
        times = []
        for index in self.lstAvailableTimes.GetSelections():
            times.append(self.lstAvailableTimes.GetString(index))
        date = self.calendarControl.PyGetDate()
        # Get data for that date and times
        self.rawEventsSelected = {}
        self.mfEventsSelected = {}
        self.normEventsSelected = {}
        for time in times:
            self.rawEventsSelected[time] = self.controller.data.getDayHourData(date, time, 'raw')
            self.mfEventsSelected[time] = self.controller.data.getDayHourData(date, time, 'mf')
        self.normEventsSelected = self.controller.data.getDayData(date, 'norm')
        # Mark interface to update
        self.rawDataTableNeedsUpdate = True
        self.mfDataTableNeedsUpdate = True
        self.normDataTableNeedsUpdate = True
        self._updateTables()
        self.rawLineGraphNeedsUpdate = True
        self.mfLineGraphNeedsUpdate = True
        self._updateLineGraphs()
        self.rawHistogramNeedsUpdate = True
        self.mfHistogramNeedsUpdate = True
        self._updateHistograms()

    def _checkNormalizedData(self, date):
        return len(self.controller.data.getDayData(date, 'norm'))

    def _updateTables(self):
        """
        Check for table tabs visibility and update data if so.
        """
        if self.controller.data and self.calendarControl:
            relevantWindow = self.controller.data.getDayRelevantWindow(self.calendarControl.PyGetDate())
            if self.rawDataTableNeedsUpdate and self.tabMain.Selection == 1 and self.tabRawData.tabMain.Selection == 0:
                self.app.updateTableGrid(self.rawEventsSelected, self.tabRawData.gridTable, self.tabRawData.labelTableInfo, relevantWindow)
                self.rawDataTableNeedsUpdate = False
            if self.mfDataTableNeedsUpdate and self.tabMain.Selection == 2 and self.tabMedianFilter.tabMain.Selection == 0:
                self.app.updateTableGrid(self.mfEventsSelected, self.tabMedianFilter.gridTable, self.tabMedianFilter.labelTableInfo, relevantWindow)
                self.mfDataTableNeedsUpdate = False
            if self.normDataTableNeedsUpdate and self.tabMain.Selection == 3:
                self.app.updateTableGrid(self.normEventsSelected, self.tabNormalization.gridNormalization)
                self.normDataTableNeedsUpdate = False

    def _updateLineGraphs(self):
        """
        Check for line graphs visibility and update data if so.
        """
        if self.rawLineGraphNeedsUpdate and self.tabMain.Selection == 1 and self.tabRawData.tabMain.Selection == 1:
            self.app.updateLineGraph(self.rawEventsSelected, self.tabRawData.lineGraphFigure)
            self.rawLineGraphNeedsUpdate = False
        if self.mfLineGraphNeedsUpdate and self.tabMain.Selection == 2 and self.tabMedianFilter.tabMain.Selection == 1:
            self.app.updateLineGraph(self.mfEventsSelected, self.tabMedianFilter.lineGraphFigure)
            self.mfLineGraphNeedsUpdate = False

    def _updateHistograms(self):
        """
        Check for histograms visibility and update data if so.
        """
        if self.controller.data and self.calendarControl:
            relevantWindow = self.controller.data.getDayRelevantWindow(self.calendarControl.PyGetDate())
        if self.rawHistogramNeedsUpdate and self.tabMain.Selection == 1 and self.tabRawData.tabMain.Selection == 2:
            self.app.updateHistogram(self.rawEventsSelected, self.tabRawData.histogramFigure, relevantWindow)
            self.rawHistogramNeedsUpdate = False
        if self.mfHistogramNeedsUpdate and self.tabMain.Selection == 2 and self.tabMedianFilter.tabMain.Selection == 2:
            self.app.updateHistogram(self.mfEventsSelected, self.tabMedianFilter.histogramFigure, relevantWindow)
            self.mfHistogramNeedsUpdate = False

    def onPageChanged_tabMain(self, event):
        self._updateTables()
        self._updateLineGraphs()
        self._updateHistograms()

    def onRightSelect_ctlGeneralMap(self, event):
        pass

class dialogAbout(interfaceResources.dialogAbout):
    #TODO: Poner para cargar imagen: os.path.join(self.controller.appPath, 'resources', 'uclm.png')
    def on_buttonClose(self, event):
        self.Close()
        
class panelData(interfaceResources.panelData):
    def __init__( self, parent, app):
        self.app = app
        return super(panelData, self).__init__(parent)

class panelNormalization(interfaceResources.panelNormalization):
    def __init__( self, parent, app):
        self.app = app
        return super(panelNormalization, self).__init__(parent)    

class dialogMedianFilter(interfaceResources.dialogMedianFilter):
    def on_OkButton(self, event):
        self.EndModal(wx.ID_OK)
        self.Close()

    def on_CancelButton(self, event):
        self.Close()
        
class ANuClaApp(wx.App):
    def __init__(self, controller, *args):
        self.controller = controller
        status = wx.App.__init__(self, 0, *args)
        self.frameANuCla = frameANuCla(controller, None, self)
        self.SetTopWindow(self.frameANuCla)
        self.frameANuCla.Show()
        return status

    ############# UPDATE METHODS ############################

    def initInterface(self):
        self.frameANuCla.initInterface()
        self.updateCalendar()

    def updateGeneralInformation(self):
        if self.controller.data:
            generalInfo = self.controller.data.getGeneralInformation()
            self.frameANuCla.coords = generalInfo[2]
            self.frameANuCla.txtGeneralName.SetValue(generalInfo[0])
            self.frameANuCla.txtGeneralLocation.SetValue(generalInfo[1])
            self.frameANuCla.txtGeneralPath.SetValue(self.controller.data.path)
            # Coordinates
            if self.frameANuCla.coords:
                coordsString = self.frameANuCla.coords.split('-')
                coords = (float(coordsString[1]), float(coordsString[0]))
                arrowImageData = [(coords[0], coords[1], os.path.join(self.controller.appPath, 'resources', 'arrow.png'))]
                self.frameANuCla.ctlGeneralMap.AddImageLayer(arrowImageData, map_rel=True, visible=True, name='<arrow_layer>')
                self.frameANuCla.ctlGeneralMap.GotoLevelAndPosition(3, coords)

    def updateStats(self):
        self.frameANuCla.labelNumberDays.Label = "Number of days imported: %s days" %(self.controller.data.getDayNumber(),)
        self.frameANuCla.labelNumberEvents.Label = "Number of data: %s measures" %(self.controller.data.getEventNumber(),)
    
    def _setEventsDays(self, eventsDays, calendar):
        """
        Reset calendar attributes and sets holidays for days given.
        @param eventsDays: List of integers that represent day numbers with events
        @param calendar: WxCalendarCtrl that is going to be modified  
        """
        # Reset attributes of all days
        i = 1
        while i < 32:
            calendar.ResetAttr(i)
            i += 1
        # Mark as holidays days with events
        for eventDay in eventsDays:
            calendar.SetHoliday(eventDay)

    def updateCalendar(self):
        if self.frameANuCla.calendarControl:
            date = self.frameANuCla.calendarControl.PyGetDate()
            activeDays = self.controller.data.getActiveDays(date.year, date.month) if self.controller.data else [] 
            self._setEventsDays(activeDays, self.frameANuCla.calendarControl)
            self.frameANuCla.calendarControl.Refresh()

    def importFile(self):
        """
        Shows a file open dialog to select file to import and call controller to import it
        """
        dlg = wx.FileDialog(self.frameANuCla, "Select SUM file", "", "", "*.sum", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            busyDlg = wx.BusyInfo('Importing file...', self.frameANuCla)
            while self.Pending(): self.Dispatch() # ensure correct display
            self.controller.importSUM(dlg.GetPath(), self.frameANuCla.calendarControl.PyGetDate())
            self.updateStats()
            del busyDlg
        dlg.Destroy()
    
    def importFolder(self):
        #TODO: Comprobar que el patrÃ³n es correcto (contiene fecha, mes y dÃ­a al menos)
        dlg = wx.DirDialog(self.frameANuCla, "Select folder to import:")
        if dlg.ShowModal() == wx.ID_OK:
            dlg2 = wx.MessageDialog(self.frameANuCla, 'WARNING: Folder import process may take a long time to accomplish, giving the appearance of the program not responding. Besides, all previous data that overlap imported one will be deleted. Do you want to continue?', 'Warning', wx.YES_NO or wx.ICON_QUESTION)
            if dlg2.ShowModal() == wx.ID_YES:
                # get total number of files
                maximum = self.controller.getNumberFiles(dlg.GetPath(), self.frameANuCla.txtPatternImportFolder.GetValue())
                progressDlg = wx.ProgressDialog('Importing folder...', 'Importing file 0/%s' %(maximum), maximum=maximum, parent=self.frameANuCla, style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
                while self.Pending(): self.Dispatch() # ensure correct display
                self.controller.importFolder(dlg.GetPath(), self.frameANuCla.txtPatternImportFolder.GetValue(), progressDlg, maximum)
                self.updateStats()
                progressDlg.Destroy()
            dlg2.Destroy()
        dlg.Destroy()

    def showImportResult(self, result):
        if result:
            dlg = wx.MessageDialog(self.frameANuCla, 'Import process has been sucessfully completed.', 'Done', wx.ICON_INFORMATION)
        else:
            dlg = wx.MessageDialog(self.frameANuCla, 'There was an error in the import process.', 'Error', wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    def showDayPresentDialog(self):
        dlg = wx.MessageDialog(self.frameANuCla, 'Selected day already exists. If you go on with the process, previous data will be deleted. Do you want to continue?', 'Warning', wx.YES_NO or wx.ICON_QUESTION)
        result = dlg.ShowModal()       
        dlg.Destroy()
        return result == wx.ID_YES

    def updateTableGrid(self, events, grid, label=None, relevantWindow=None):
        """
        Updates data in visualization grid with given data.
        @param events: Dictionary with times as keys and events as values. Each event value is also a dictionary
        with size as key and amount as value.  
        """
        # Clean previous data
        if grid.GetNumberCols(): grid.DeleteCols(0, grid.GetNumberCols())
        if grid.GetNumberRows(): grid.DeleteRows(0, grid.GetNumberRows())
        if len(events):
            # Generate header
            sizes = events.values()[0].keys()
            sizes.sort()
            times = events.keys()
            times.sort()
            grid.AppendRows(len(times))
            grid.AppendCols(len(sizes))
            i = 0
            for size in sizes:
                grid.SetColLabelValue(i, "%s" %size)
                i += 1
            # Fill data
            count = 0
            nrow = 0
            for time in times:
                grid.SetRowLabelValue(nrow, time)
                ncol = 0
                for size in sizes:
                    value = events[time][size]
                    if not value is None: count += 1
                    grid.SetCellValue(nrow, ncol, "%s" %value)
                    grid.SetCellAlignment(nrow, ncol, wxPython._core.wxALIGN_RIGHT, wxPython._core.wxALIGN_CENTRE)
                    ncol += 1
                nrow += 1
            # Adjust column width
            grid.AutoSizeColumns(20)
            # Highlight relevant window
            # TODO: Cuando la selecciÃ³n de eventos no es completa, seguir resaltando correctamente
            if relevantWindow:
                for i in range(relevantWindow[2], relevantWindow[3]):
                    for j in range(relevantWindow[0], relevantWindow[1]):
                        grid.SetCellBackgroundColour(i, j, wx.GREEN)
            # Set general info
            if label:
                label.Label = "NÂº capture times: %s - NÂº sizes: %s - Total number data: %s" %(len(times), len(sizes), count)

    def updateLineGraph(self, events, figure):
        busyDlg = wx.BusyInfo('Creating graph...', self.frameANuCla)
        while self.Pending(): self.Dispatch() # ensure correct display
        figure.clear()
        axes = figure.gca()
        axes.set_xlabel("Dp/m")
        axes.set_ylabel("dN/dlogDp(cm-3)")
        # More resolution to units in x scale
        minorLocator = matplotlib.ticker.LogLocator()
        axes.xaxis.set_minor_locator(minorLocator)
        times = events.keys()
        # Line for nucleation mode
        axes.axvline(x=self.controller.nucleationSizeLimit, c="red", linestyle='--', zorder=0, label='Nucleation limit')
        # Graph
        times.sort()
        for eventHour in times:
            event = events[eventHour]
            sizes = event.keys()
            sizes.sort()
            axes.plot(sizes, map(lambda x: event[x], sizes), 'o-')
            axes.set_xscale('log')
        if len(times):
            times.insert(0, 'Nucleation limit') 
            axes.legend(times)
        figure.canvas.draw()
        del busyDlg

    def updateHistogram(self, events, figure, relevantWindow=None):
        busyDlg = wx.BusyInfo('Creating histogram...', self.frameANuCla)
        while self.Pending(): self.Dispatch() # ensure correct display
        figure.clear()
        if len(events) > 1:
            # Prepare data
            eventTimes = events.keys()
            eventTimes.sort()
            sizes = events[eventTimes[0]].keys()
            sizes.sort()
            x = [] ; y = [] ; c = []
            axes = figure.gca()
            for eventTime in eventTimes:
                event = events[eventTime]
                for size in sizes:
                    x.append(matplotlib.dates.date2num(datetime.datetime.strptime(eventTime, '%H:%M:%S')))
                    y.append(size)
                    c.append(event[size])
            # More resolution to units in y scale
            minorLocator = matplotlib.ticker.LogLocator()
            axes.yaxis.set_minor_locator(minorLocator)
            # Hour in y axis
            hourLocator = matplotlib.dates.HourLocator(interval=2)
            axes.xaxis.set_major_locator(hourLocator)
            majorFormatter = matplotlib.dates.DateFormatter('%H:%M')
            axes.xaxis.set_major_formatter(majorFormatter)
            minuteLocator = matplotlib.dates.MinuteLocator(interval=10)
            axes.xaxis.set_minor_locator(minuteLocator)
            # Plot
            mappable = axes.hexbin(x, y, C=c, yscale='log', gridsize=(len(eventTimes), int(len(sizes) * 0.4))) #len(sizes)))
            # Line for nucleation mode and relevant window
            axes.axhline(y=self.controller.nucleationSizeLimit, c="red", linestyle='--', label='Nucleation limit')
            if relevantWindow:
                axes.axvline(x=matplotlib.dates.date2num(datetime.datetime.strptime(eventTimes[relevantWindow[2]], '%H:%M:%S')), c="yellow", linestyle='--', label='Start time')
                axes.axvline(x=matplotlib.dates.date2num(datetime.datetime.strptime(eventTimes[relevantWindow[3]], '%H:%M:%S')), c="yellow", linestyle='--', label='End time')
            figure.colorbar(mappable)
            #cb.set_label('counts')
        figure.canvas.draw()
        del busyDlg        
