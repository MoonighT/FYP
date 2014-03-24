import wx
import os



class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''
        super(MainWindow, self).__init__(parent, title=title, size=(450, 450))
        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        self.InitGUI()
        self.Centre()
        self.Show()

    def InitGUI(self):

        # MENUS
        fileMenu = wx.Menu()  # create menu for file
        viewMenu = wx.Menu()  # create a menu for view
        helpMenu = wx.Menu()  # create a menu for help

        # FILE MENU
        menuOpen = fileMenu.Append(wx.ID_OPEN,
                        "&Open", " Open a file to edit")  # add open to File
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit",
                                " Terminate the program")  # add exit to File

        # VIEW MENU
        menuView = viewMenu.Append(wx.ID_ANY, "TODO:", "Still to do")

        # HELP MENU
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About",
                                "About this program")  # add about menu item

        # MENUBAR
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")  # Adding the "filemenu" to the MenuBar
        menuBar.Append(viewMenu, "&View")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        '''#TOOLBAR
        toolbar = self.CreateToolBar()
        toolOpen = toolbar.AddLabelTool(wx.ID_OPEN, "Open", wx.Bitmap("open.png"))
        toolExit = toolbar.AddLabelTool(wx.ID_EXIT, "Exit", wx.Bitmap("blah.png"))'''

        # MENU EVENTS
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        '''#TOOLBAR EVENTS
        self.Bind(wx.EVT_TOOL, self.OnExit, toolExit)
        self.Bind(wx.EVT_TOOL, self.OnOpen, toolOpen)'''


        # PANEL
        panel = wx.Panel(self)

        panel.SetBackgroundColour('#ededed')
        vBox = wx.BoxSizer(wx.VERTICAL)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(wx.StaticText(panel, label="File:"), flag=wx.TOP, border=3)
        hBox.Add(wx.TextCtrl(panel), 1, flag=wx.LEFT, border=10)
        checkBtn = wx.Button(panel, -1, "Check")
        self.Bind(wx.EVT_BUTTON, self.checkBtnClick)
        hBox.Add(checkBtn, 0, flag=wx.LEFT, border=10)
        vBox.Add(hBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vBox.Add((-1, 10))

        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(wx.StaticText(panel, label="URLs:"))
        vBox.Add(hBox2, flag=wx.LEFT, border=10)
        vBox.Add((-1, 5))

        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.urlFld = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 295))
        hBox3.Add(self.urlFld, 1, flag=wx.EXPAND)
        vBox.Add(hBox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)


        panel.SetSizer(vBox)

    # GUI EVENTS
    def checkBtnClick(self, e):
        self.urlFld.SetValue("blahh")

    # MENU ITEM EVENTS
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A small text editor",
                               "My test editor", wx.OK)  # create a dialog (dlg) box to display the message, and ok button
        dlg.ShowModal()  # show the dialog box, modal means cannot do anything on the program until clicks ok or cancel
        dlg.Destroy()  # destroy the dialog box when its not needed

    def OnExit(self, e):
        self.Close(True)  # on menu item select, close the app frame.

    def OnOpen(self, e):
        self.file_open()
        e.Skip()

    def file_open(self):  # 9
        with wx.FileDialog(self, "Choose a file to open", self.dirname,
                           "", "*.*", wx.OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                self.urlFld.LoadFile('/'.join((directory, filename)))
                self.SetTitle(filename)

app = wx.App(False)  # creates a new app
MainWindow(None, "URL Checker")  # give the frame a title
app.MainLoop()  # start the apps mainloop which handles app events