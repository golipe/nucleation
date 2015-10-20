# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.calendar
import pyslip
import os
import wx.grid
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx

###########################################################################
## Class frameANuCla
###########################################################################

class frameANuCla ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ANuCla - Aerosols nucleation classifier", pos = wx.DefaultPosition, size = wx.Size( 900,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.menubar = wx.MenuBar( 0 )
		self.menuFile = wx.Menu()
		self.menuNew = wx.MenuItem( self.menuFile, wx.ID_ANY, u"&New"+ u"\t" + u"Ctrl+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuNew )
		
		self.menuOpen = wx.MenuItem( self.menuFile, wx.ID_ANY, u"&Open"+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuOpen )
		
		self.menuFile.AppendSeparator()
		
		self.menuImportFile = wx.MenuItem( self.menuFile, wx.ID_ANY, u"Import &file", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuImportFile )
		self.menuImportFile.Enable( False )
		
		self.menuImportFolder = wx.MenuItem( self.menuFile, wx.ID_ANY, u"Im&port folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuImportFolder )
		self.menuImportFolder.Enable( False )
		
		self.menuDeleteDay = wx.MenuItem( self.menuFile, wx.ID_ANY, u"&Delete day", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuDeleteDay )
		self.menuDeleteDay.Enable( False )
		
		self.menuFile.AppendSeparator()
		
		self.menuQuit = wx.MenuItem( self.menuFile, wx.ID_ANY, u"&Quit"+ u"\t" + u"Ctrl+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuQuit )
		
		self.menubar.Append( self.menuFile, u"&File" ) 
		
		self.menuDataProcessing = wx.Menu()
		self.menuMedianFilter = wx.Menu()
		self.menuMedianFilterDay = wx.MenuItem( self.menuMedianFilter, wx.ID_ANY, u"For selected &day", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuMedianFilter.AppendItem( self.menuMedianFilterDay )
		
		self.menuMedianFilterAll = wx.MenuItem( self.menuMedianFilter, wx.ID_ANY, u"For &all days", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuMedianFilter.AppendItem( self.menuMedianFilterAll )
		
		self.menuDataProcessing.AppendSubMenu( self.menuMedianFilter, u"&Median filter" )
		
		self.menuRelevantWindow = wx.Menu()
		self.menuRelevantWindowMaxIntensity = wx.Menu()
		self.menuRelevantWindowMaxIntensityDay = wx.MenuItem( self.menuRelevantWindowMaxIntensity, wx.ID_ANY, u"For selected &day", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuRelevantWindowMaxIntensity.AppendItem( self.menuRelevantWindowMaxIntensityDay )
		self.menuRelevantWindowMaxIntensityDay.Enable( False )
		
		self.menuRelevantWindowMaxIntensityAll = wx.MenuItem( self.menuRelevantWindowMaxIntensity, wx.ID_ANY, u"For &all days", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuRelevantWindowMaxIntensity.AppendItem( self.menuRelevantWindowMaxIntensityAll )
		self.menuRelevantWindowMaxIntensityAll.Enable( False )
		
		self.menuRelevantWindow.AppendSubMenu( self.menuRelevantWindowMaxIntensity, u"With &maximum intensity" )
		
		self.menuRelevantWindowDifIntensity = wx.Menu()
		self.menuRelevantWindowDifIntensityDay = wx.MenuItem( self.menuRelevantWindowDifIntensity, wx.ID_ANY, u"For selected &day", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuRelevantWindowDifIntensity.AppendItem( self.menuRelevantWindowDifIntensityDay )
		self.menuRelevantWindowDifIntensityDay.Enable( False )
		
		self.menuRelevantWindowDifIntensityAll = wx.MenuItem( self.menuRelevantWindowDifIntensity, wx.ID_ANY, u"For &all days", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuRelevantWindowDifIntensity.AppendItem( self.menuRelevantWindowDifIntensityAll )
		self.menuRelevantWindowDifIntensityAll.Enable( False )
		
		self.menuRelevantWindow.AppendSubMenu( self.menuRelevantWindowDifIntensity, u"With &differential intensity" )
		
		self.menuDataProcessing.AppendSubMenu( self.menuRelevantWindow, u"Calculate &relevant window" )
		
		self.menuNormalization = wx.Menu()
		self.menuNormalizationDay = wx.MenuItem( self.menuNormalization, wx.ID_ANY, u"For selected &day", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuNormalization.AppendItem( self.menuNormalizationDay )
		self.menuNormalizationDay.Enable( False )
		
		self.menuNormalizationAll = wx.MenuItem( self.menuNormalization, wx.ID_ANY, u"For &all days", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuNormalization.AppendItem( self.menuNormalizationAll )
		self.menuNormalizationAll.Enable( False )
		
		self.menuDataProcessing.AppendSubMenu( self.menuNormalization, u"&Normalization" )
		
		self.menuDataSource = wx.Menu()
		self.menuDataSourceRaw = wx.MenuItem( self.menuDataSource, wx.ID_ANY, u"&RAW data", wx.EmptyString, wx.ITEM_CHECK )
		self.menuDataSource.AppendItem( self.menuDataSourceRaw )
		self.menuDataSourceRaw.Check( True )
		
		self.menuDataSourceMf = wx.MenuItem( self.menuDataSource, wx.ID_ANY, u"&Median filter data", wx.EmptyString, wx.ITEM_CHECK )
		self.menuDataSource.AppendItem( self.menuDataSourceMf )
		
		self.menuDataProcessing.AppendSubMenu( self.menuDataSource, u"Data &source" )
		
		self.menubar.Append( self.menuDataProcessing, u"Data &pre-processing" ) 
		
		self.menuClassification = wx.Menu()
		self.menuKmeans = wx.Menu()
		self.menuResetTrainingKmeans = wx.MenuItem( self.menuKmeans, wx.ID_ANY, u"&Reset training", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuKmeans.AppendItem( self.menuResetTrainingKmeans )
		self.menuResetTrainingKmeans.Enable( False )
		
		self.menuImportTrainingKmeans = wx.MenuItem( self.menuKmeans, wx.ID_ANY, u"Import &training data", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuKmeans.AppendItem( self.menuImportTrainingKmeans )
		self.menuImportTrainingKmeans.Enable( False )
		
		self.menuClassificationKmeans = wx.MenuItem( self.menuKmeans, wx.ID_ANY, u"Perform &classification", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuKmeans.AppendItem( self.menuClassificationKmeans )
		self.menuClassificationKmeans.Enable( False )
		
		self.menuClassification.AppendSubMenu( self.menuKmeans, u"&K-means" )
		
		self.menubar.Append( self.menuClassification, u"&Classification" ) 
		
		self.menuHelp = wx.Menu()
		self.menuAbout = wx.MenuItem( self.menuHelp, wx.ID_ANY, u"&About", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuHelp.AppendItem( self.menuAbout )
		
		self.menubar.Append( self.menuHelp, u"&Help" ) 
		
		self.SetMenuBar( self.menubar )
		
		sizerMain = wx.BoxSizer( wx.HORIZONTAL )
		
		sizerVerticalMain = wx.BoxSizer( wx.VERTICAL )
		
		self.calendarControl = wx.calendar.CalendarCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( 265,-1 ), wx.calendar.CAL_MONDAY_FIRST|wx.calendar.CAL_SHOW_HOLIDAYS )
		sizerVerticalMain.Add( self.calendarControl, 0, wx.TOP, 5 )
		
		self.labelAvailableTimes = wx.StaticText( self, wx.ID_ANY, u"Available times", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelAvailableTimes.Wrap( -1 )
		sizerVerticalMain.Add( self.labelAvailableTimes, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		lstAvailableTimesChoices = []
		self.lstAvailableTimes = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstAvailableTimesChoices, wx.LB_EXTENDED|wx.LB_MULTIPLE )
		self.lstAvailableTimes.SetMinSize( wx.Size( 100,-1 ) )
		
		sizerVerticalMain.Add( self.lstAvailableTimes, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		sizerMain.Add( sizerVerticalMain, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.tabMain = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tabGeneral = wx.Panel( self.tabMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerGeneral = wx.BoxSizer( wx.VERTICAL )
		
		sizerGeneralA = wx.BoxSizer( wx.HORIZONTAL )
		
		
		sizerGeneralA.AddSpacer( ( 0, 0), 0, wx.LEFT, 15 )
		
		sizerGeneralA1 = wx.BoxSizer( wx.VERTICAL )
		
		self.labelGeneralName = wx.StaticText( self.tabGeneral, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelGeneralName.Wrap( -1 )
		sizerGeneralA1.Add( self.labelGeneralName, 0, wx.TOP|wx.BOTTOM, 7 )
		
		self.labelGeneralLocation = wx.StaticText( self.tabGeneral, wx.ID_ANY, u"Location", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelGeneralLocation.Wrap( -1 )
		sizerGeneralA1.Add( self.labelGeneralLocation, 0, wx.TOP|wx.BOTTOM, 7 )
		
		self.labelGeneralPath = wx.StaticText( self.tabGeneral, wx.ID_ANY, u"Path", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelGeneralPath.Wrap( -1 )
		sizerGeneralA1.Add( self.labelGeneralPath, 0, wx.TOP|wx.BOTTOM, 7 )
		
		sizerGeneralA.Add( sizerGeneralA1, 0, wx.EXPAND|wx.RIGHT, 25 )
		
		sizerGeneralB2 = wx.BoxSizer( wx.VERTICAL )
		
		self.txtGeneralName = wx.TextCtrl( self.tabGeneral, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.txtGeneralName.SetToolTipString( u"Press Enter for accepting changes" )
		
		sizerGeneralB2.Add( self.txtGeneralName, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 2 )
		
		self.txtGeneralLocation = wx.TextCtrl( self.tabGeneral, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.txtGeneralLocation.SetToolTipString( u"Press Enter for accepting changes" )
		
		sizerGeneralB2.Add( self.txtGeneralLocation, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 2 )
		
		self.txtGeneralPath = wx.TextCtrl( self.tabGeneral, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtGeneralPath.Enable( False )
		
		sizerGeneralB2.Add( self.txtGeneralPath, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 2 )
		
		sizerGeneralA.Add( sizerGeneralB2, 1, wx.EXPAND|wx.RIGHT, 10 )
		
		sizerGeneral.Add( sizerGeneralA, 0, wx.EXPAND|wx.TOP, 10 )
		
		sizerGeneralB = wx.BoxSizer( wx.HORIZONTAL )
		
		self.labelNumberDays = wx.StaticText( self.tabGeneral, wx.ID_ANY, u"Number of days imported: 0 days", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelNumberDays.Wrap( -1 )
		sizerGeneralB.Add( self.labelNumberDays, 0, wx.RIGHT|wx.LEFT, 40 )
		
		self.labelNumberEvents = wx.StaticText( self.tabGeneral, wx.ID_ANY, u"Number of data: 0 measures", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelNumberEvents.Wrap( -1 )
		sizerGeneralB.Add( self.labelNumberEvents, 0, wx.RIGHT|wx.LEFT, 40 )
		
		sizerGeneral.Add( sizerGeneralB, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 10 )
		
		sizerGeneralC = wx.BoxSizer( wx.HORIZONTAL )
		
		self.buttonImportFile = wx.Button( self.tabGeneral, wx.ID_ANY, u"Import &day", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.buttonImportFile.SetToolTipString( u"With this button, you can import one single file to database in the selected day of the calendar" )
		
		sizerGeneralC.Add( self.buttonImportFile, 0, wx.ALL, 5 )
		
		
		sizerGeneralC.AddSpacer( ( 0, 0), 0, wx.LEFT, 150 )
		
		self.lblPatternImportFolder = wx.StaticText( self.tabGeneral, wx.ID_ANY, u"Pattern", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblPatternImportFolder.Wrap( -1 )
		sizerGeneralC.Add( self.lblPatternImportFolder, 0, wx.TOP, 10 )
		
		self.txtPatternImportFolder = wx.TextCtrl( self.tabGeneral, wx.ID_ANY, u"dm%y%m%d.sum", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.txtPatternImportFolder.SetToolTipString( u"CODES: \n%yyy - Year with four digits; %y - Year with two digits;\n%m - Month with two digits; %d - Day with two digits\nNOTE: The rest of the characters are not case sensitive." )
		
		sizerGeneralC.Add( self.txtPatternImportFolder, 0, wx.ALL, 5 )
		
		self.buttonImportFolder = wx.Button( self.tabGeneral, wx.ID_ANY, u"Import &folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.buttonImportFolder.SetToolTipString( u"With this button, you can import all contents of one folder, detecting date for each file trough the pattern." )
		
		sizerGeneralC.Add( self.buttonImportFolder, 0, wx.ALL, 5 )
		
		sizerGeneral.Add( sizerGeneralC, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.TOP, 20 )
		
		self.panelGeneralMap = wx.Panel( self.tabGeneral, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbGeneralMap = wx.StaticBoxSizer( wx.StaticBox( self.panelGeneralMap, wx.ID_ANY, u"Map" ), wx.VERTICAL )
		
		self.ctlGeneralMap = pyslip.PySlip(self.panelGeneralMap, tile_dir=os.path.join(self.controller.appPath, 'resources', 'tiles'), min_level=0, max_level=4, start_level=0)
		self.ctlGeneralMap.SetToolTipString( u"Right click to set new coordinates." )
		
		sbGeneralMap.Add( self.ctlGeneralMap, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.panelGeneralMap.SetSizer( sbGeneralMap )
		self.panelGeneralMap.Layout()
		sbGeneralMap.Fit( self.panelGeneralMap )
		sizerGeneral.Add( self.panelGeneralMap, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.tabGeneral.SetSizer( sizerGeneral )
		self.tabGeneral.Layout()
		sizerGeneral.Fit( self.tabGeneral )
		self.tabMain.AddPage( self.tabGeneral, u"General", True )
		
		sizerMain.Add( self.tabMain, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( sizerMain )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.Bind( wx.EVT_MENU, self.on_menuNew, id = self.menuNew.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuOpen, id = self.menuOpen.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuImportFile, id = self.menuImportFile.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuImportFolder, id = self.menuImportFolder.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuDeleteDay, id = self.menuDeleteDay.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuQuit, id = self.menuQuit.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuMedianFilterDay, id = self.menuMedianFilterDay.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuMedianFilterAll, id = self.menuMedianFilterAll.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuRelevantWindowMaxIntensityDay, id = self.menuRelevantWindowMaxIntensityDay.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuRelevantWindowMaxIntensityAll, id = self.menuRelevantWindowMaxIntensityAll.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuRelevantWindowDifIntensityDay, id = self.menuRelevantWindowDifIntensityDay.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuRelevantWindowDifIntensityAll, id = self.menuRelevantWindowDifIntensityAll.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuNormalizationDay, id = self.menuNormalizationDay.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuNormalizationAll, id = self.menuNormalizationAll.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuDataSourceRaw, id = self.menuDataSourceRaw.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuDataSourceMf, id = self.menuDataSourceMf.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuResetTrainingKmeans, id = self.menuResetTrainingKmeans.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuImportTrainingKmeans, id = self.menuImportTrainingKmeans.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuClassificationKmeans, id = self.menuClassificationKmeans.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menuAbout, id = self.menuAbout.GetId() )
		self.calendarControl.Bind( wx.calendar.EVT_CALENDAR_MONTH, self.onMonthYear_calendarControl )
		self.calendarControl.Bind( wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.onCalendarSelChange_calendarControl )
		self.calendarControl.Bind( wx.calendar.EVT_CALENDAR_YEAR, self.onMonthYear_calendarControl )
		self.lstAvailableTimes.Bind( wx.EVT_LISTBOX, self.onListBox_lstAvailableTimes )
		self.tabMain.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChanged_tabMain )
		self.txtGeneralName.Bind( wx.EVT_TEXT_ENTER, self.onTextEnter_txtGeneralName )
		self.txtGeneralLocation.Bind( wx.EVT_TEXT_ENTER, self.onTextEnter_txtGeneralLocation )
		self.buttonImportFile.Bind( wx.EVT_BUTTON, self.on_buttonImportFile )
		self.buttonImportFolder.Bind( wx.EVT_BUTTON, self.on_buttonImportFolder )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onClose( self, event ):
		event.Skip()
	
	def on_menuNew( self, event ):
		event.Skip()
	
	def on_menuOpen( self, event ):
		event.Skip()
	
	def on_menuImportFile( self, event ):
		event.Skip()
	
	def on_menuImportFolder( self, event ):
		event.Skip()
	
	def on_menuDeleteDay( self, event ):
		event.Skip()
	
	def on_menuQuit( self, event ):
		event.Skip()
	
	def on_menuMedianFilterDay( self, event ):
		event.Skip()
	
	def on_menuMedianFilterAll( self, event ):
		event.Skip()
	
	def on_menuRelevantWindowMaxIntensityDay( self, event ):
		event.Skip()
	
	def on_menuRelevantWindowMaxIntensityAll( self, event ):
		event.Skip()
	
	def on_menuRelevantWindowDifIntensityDay( self, event ):
		event.Skip()
	
	def on_menuRelevantWindowDifIntensityAll( self, event ):
		event.Skip()
	
	def on_menuNormalizationDay( self, event ):
		event.Skip()
	
	def on_menuNormalizationAll( self, event ):
		event.Skip()
	
	def on_menuDataSourceRaw( self, event ):
		event.Skip()
	
	def on_menuDataSourceMf( self, event ):
		event.Skip()
	
	def on_menuResetTrainingKmeans( self, event ):
		event.Skip()
	
	def on_menuImportTrainingKmeans( self, event ):
		event.Skip()
	
	def on_menuClassificationKmeans( self, event ):
		event.Skip()
	
	def on_menuAbout( self, event ):
		event.Skip()
	
	def onMonthYear_calendarControl( self, event ):
		event.Skip()
	
	def onCalendarSelChange_calendarControl( self, event ):
		event.Skip()
	
	
	def onListBox_lstAvailableTimes( self, event ):
		event.Skip()
	
	def onPageChanged_tabMain( self, event ):
		event.Skip()
	
	def onTextEnter_txtGeneralName( self, event ):
		event.Skip()
	
	def onTextEnter_txtGeneralLocation( self, event ):
		event.Skip()
	
	def on_buttonImportFile( self, event ):
		event.Skip()
	
	def on_buttonImportFolder( self, event ):
		event.Skip()
	

###########################################################################
## Class dialogMedianFilter
###########################################################################

class dialogMedianFilter ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Select window size for algorithm", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		sizerMain = wx.FlexGridSizer( 2, 2, 0, 0 )
		sizerMain.SetFlexibleDirection( wx.BOTH )
		sizerMain.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
		
		self.labelHorWindowSize = wx.StaticText( self, wx.ID_ANY, u"Value for horizontal window size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelHorWindowSize.Wrap( -1 )
		sizerMain.Add( self.labelHorWindowSize, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 10 )
		
		self.spinHorWindowSize = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 3, 300, 3 )
		sizerMain.Add( self.spinHorWindowSize, 0, wx.ALL, 5 )
		
		self.labelVerWindowSize = wx.StaticText( self, wx.ID_ANY, u"Value for vertical window size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelVerWindowSize.Wrap( -1 )
		sizerMain.Add( self.labelVerWindowSize, 0, wx.ALL, 10 )
		
		self.spinVerWindowSize = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 3, 300, 3 )
		sizerMain.Add( self.spinVerWindowSize, 0, wx.ALL, 5 )
		
		
		sizerMain.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		sizerOkCancel = wx.StdDialogButtonSizer()
		self.sizerOkCancelOK = wx.Button( self, wx.ID_OK )
		sizerOkCancel.AddButton( self.sizerOkCancelOK )
		self.sizerOkCancelCancel = wx.Button( self, wx.ID_CANCEL )
		sizerOkCancel.AddButton( self.sizerOkCancelCancel )
		sizerOkCancel.Realize();
		sizerMain.Add( sizerOkCancel, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, 15 )
		
		self.SetSizer( sizerMain )
		self.Layout()
		sizerMain.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.sizerOkCancelCancel.Bind( wx.EVT_BUTTON, self.on_CancelButton )
		self.sizerOkCancelOK.Bind( wx.EVT_BUTTON, self.on_OkButton )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_CancelButton( self, event ):
		event.Skip()
	
	def on_OkButton( self, event ):
		event.Skip()
	

###########################################################################
## Class dialogAbout
###########################################################################

class dialogAbout ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"About", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		sizerAbout = wx.BoxSizer( wx.HORIZONTAL )
		
		self.bitmapUclm = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		sizerAbout.Add( self.bitmapUclm, 0, wx.TOP, 15 )
		
		sizerLabelsAbout = wx.BoxSizer( wx.VERTICAL )
		
		self.labelPFC = wx.StaticText( self, wx.ID_ANY, u"DEGREE PROJECT", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelPFC.Wrap( -1 )
		self.labelPFC.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		sizerLabelsAbout.Add( self.labelPFC, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.labelNombre = wx.StaticText( self, wx.ID_ANY, u"Pedro Manuel Baeza Romero", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelNombre.Wrap( -1 )
		sizerLabelsAbout.Add( self.labelNombre, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.labelTitle = wx.StaticText( self, wx.ID_ANY, u"Tool for automatic classification of atmosferic particles", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTitle.Wrap( -1 )
		self.labelTitle.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString ) )
		
		sizerLabelsAbout.Add( self.labelTitle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.buttonClose = wx.Button( self, wx.ID_ANY, u"&Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerLabelsAbout.Add( self.buttonClose, 0, wx.ALIGN_RIGHT|wx.ALL, 8 )
		
		sizerAbout.Add( sizerLabelsAbout, 1, wx.ALL|wx.FIXED_MINSIZE, 5 )
		
		self.SetSizer( sizerAbout )
		self.Layout()
		sizerAbout.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.buttonClose.Bind( wx.EVT_BUTTON, self.on_buttonClose )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_buttonClose( self, event ):
		event.Skip()
	

###########################################################################
## Class panelData
###########################################################################

class panelData ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,700 ), style = wx.TAB_TRAVERSAL )
		
		sizerData = wx.BoxSizer( wx.VERTICAL )
		
		self.tabMain = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_TOP )
		self.tabTable = wx.Panel( self.tabMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerTable = wx.BoxSizer( wx.VERTICAL )
		
		self.gridTable = wx.grid.Grid( self.tabTable, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.gridTable.CreateGrid( 0, 0 )
		self.gridTable.EnableEditing( False )
		self.gridTable.EnableGridLines( True )
		self.gridTable.EnableDragGridSize( False )
		self.gridTable.SetMargins( 0, 0 )
		
		# Columns
		self.gridTable.AutoSizeColumns()
		self.gridTable.EnableDragColMove( False )
		self.gridTable.EnableDragColSize( False )
		self.gridTable.SetColLabelSize( 30 )
		self.gridTable.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.gridTable.AutoSizeRows()
		self.gridTable.EnableDragRowSize( False )
		self.gridTable.SetRowLabelSize( 80 )
		self.gridTable.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.gridTable.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		sizerTable.Add( self.gridTable, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.labelTableInfo = wx.StaticText( self.tabTable, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTableInfo.Wrap( -1 )
		sizerTable.Add( self.labelTableInfo, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.tabTable.SetSizer( sizerTable )
		self.tabTable.Layout()
		sizerTable.Fit( self.tabTable )
		self.tabMain.AddPage( self.tabTable, u"Table", True )
		self.tabLineGraph = wx.Panel( self.tabMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerLineGraph = wx.BoxSizer( wx.VERTICAL )
		
		self.panelLineGraph = wx.Panel( self.tabLineGraph, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerPanelLineGraph = wx.BoxSizer( wx.VERTICAL )
		
		self.lineGraphFigure = matplotlib.figure.Figure(figsize=(2, 2))
		self.lineGraphCanvas = FigureCanvasWxAgg(self.panelLineGraph, -1, self.lineGraphFigure)
		
		sizerPanelLineGraph.Add( self.lineGraphCanvas, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.lineGraphToolbar = NavigationToolbar2Wx(self.lineGraphCanvas)
		self.lineGraphToolbar.Realize()
		sizerPanelLineGraph.Add( self.lineGraphToolbar, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.panelLineGraph.SetSizer( sizerPanelLineGraph )
		self.panelLineGraph.Layout()
		sizerPanelLineGraph.Fit( self.panelLineGraph )
		sizerLineGraph.Add( self.panelLineGraph, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.tabLineGraph.SetSizer( sizerLineGraph )
		self.tabLineGraph.Layout()
		sizerLineGraph.Fit( self.tabLineGraph )
		self.tabMain.AddPage( self.tabLineGraph, u"Line graph", False )
		self.tabHistogram = wx.Panel( self.tabMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerHistogram = wx.BoxSizer( wx.HORIZONTAL )
		
		self.panelHistogram = wx.Panel( self.tabHistogram, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerPanelHistogram = wx.BoxSizer( wx.VERTICAL )
		
		self.histogramFigure = matplotlib.figure.Figure(figsize=(2, 2))
		self.histogramCanvas = FigureCanvasWxAgg(self.panelHistogram,  -1, self.histogramFigure)
		
		sizerPanelHistogram.Add( self.histogramCanvas, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.histogramToolbar = NavigationToolbar2Wx(self.histogramCanvas)
		self.histogramToolbar.Realize()
		sizerPanelHistogram.Add( self.histogramToolbar, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.panelHistogram.SetSizer( sizerPanelHistogram )
		self.panelHistogram.Layout()
		sizerPanelHistogram.Fit( self.panelHistogram )
		sizerHistogram.Add( self.panelHistogram, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.tabHistogram.SetSizer( sizerHistogram )
		self.tabHistogram.Layout()
		sizerHistogram.Fit( self.tabHistogram )
		self.tabMain.AddPage( self.tabHistogram, u"Histogram", False )
		
		sizerData.Add( self.tabMain, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( sizerData )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class panelNormalization
###########################################################################

class panelNormalization ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		sizerNormalization = wx.BoxSizer( wx.VERTICAL )
		
		self.gridNormalization = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.gridNormalization.CreateGrid( 0, 0 )
		self.gridNormalization.EnableEditing( False )
		self.gridNormalization.EnableGridLines( True )
		self.gridNormalization.EnableDragGridSize( False )
		self.gridNormalization.SetMargins( 0, 0 )
		
		# Columns
		self.gridNormalization.AutoSizeColumns()
		self.gridNormalization.EnableDragColMove( False )
		self.gridNormalization.EnableDragColSize( False )
		self.gridNormalization.SetColLabelSize( 30 )
		self.gridNormalization.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.gridNormalization.AutoSizeRows()
		self.gridNormalization.EnableDragRowSize( False )
		self.gridNormalization.SetRowLabelSize( 80 )
		self.gridNormalization.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.gridNormalization.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		sizerNormalization.Add( self.gridNormalization, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( sizerNormalization )
		self.Layout()
	
	def __del__( self ):
		pass
