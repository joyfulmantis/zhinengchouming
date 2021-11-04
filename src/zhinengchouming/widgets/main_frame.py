from wx import Frame, STAY_ON_TOP, RESIZE_BORDER, MAXIMIZE_BOX, DEFAULT_FRAME_STYLE, EVT_CLOSE

from widgets.main_panel import MainPanel


class MainFrame(Frame):
    def __init__(self):
        super(MainFrame, self).__init__(None,
                                        style=DEFAULT_FRAME_STYLE & 
                                        ~(RESIZE_BORDER | MAXIMIZE_BOX))
                                        
        self.Title: str = '智能抽名 - 请打开文件'

        self.mainPanel = MainPanel(self)

        self.Bind(EVT_CLOSE, self.mainPanel.onQuit)

        self.Centre()
        self.Show()

    def toggleStyle(self, event):
        if(self.WindowStyle == STAY_ON_TOP):
            self.WindowStyle = DEFAULT_FRAME_STYLE & ~(RESIZE_BORDER |
                                                          MAXIMIZE_BOX)
            self.mainPanel.Fit()
        else:
            self.WindowStyle = STAY_ON_TOP
            self.mainPanel.Fit()

