from wx import Menu, ID_ANY, ID_OPEN, ID_SAVEAS, ID_EXIT, EVT_MENU
from wx.core import ID_CLOSE


class MainMenu(Menu):
    def __init__(self, parent):
        super(MainMenu, self).__init__()

        self.toggleStyle = self.AppendCheckItem(ID_ANY, "隐藏标题栏")
        self.Bind(EVT_MENU, parent.parent.toggleStyle, self.toggleStyle)

        self.toggleScore = self.AppendCheckItem(ID_ANY, "打开记分数功能")
        self.toggleScore.Enable(False)
        self.Bind(EVT_MENU, parent.toggleScore, self.toggleScore)

        self.toggleGroupToIndividual = self.AppendCheckItem(ID_ANY, "小组点到人")
        self.toggleGroupToIndividual.Enable(False)
        self.Bind(EVT_MENU, parent.toggleGroupToIndividual, self.toggleGroupToIndividual)

        self.resetCounter = self.Append(ID_ANY, "重置轮次")
        self.resetCounter.Enable(False)
        self.Bind(EVT_MENU, parent.resetCounter, self.resetCounter)

        self.AppendSeparator()

        self.openfile = self.Append(ID_OPEN, "&打开...", " 打开文件")
        self.Bind(EVT_MENU, parent.openFile, self.openfile)

        self.saveScores = self.Append(ID_SAVEAS, "&保存分数...", "保存分数")
        self.saveScores.Enable(False)
        self.Bind(EVT_MENU, parent.saveScores, self.saveScores)

        self.closeFile = self.Append(ID_CLOSE, "&关闭文件", "关闭文件")
        self.closeFile.Enable(False)
        self.Bind(EVT_MENU, parent.closeFile, self.closeFile)

        self.quit = self.Append(ID_EXIT, '退出', '退出软件')
        self.Bind(EVT_MENU, parent.onQuit, self.quit)


    def fileOpenedEnable(self) -> None:
        self.toggleScore.Enable(True)

        self.saveScores.Enable(True)

        self.resetCounter.Enable(True)

        self.closeFile.Enable(True)


    def fileClosedDisable(self) -> None:
        self.toggleScore.Enable(False)
        self.toggleScore.Check(False)

        self.toggleGroupToIndividual.Enable(False)
        self.toggleGroupToIndividual.Check(False)

        self.saveScores.Enable(False)

        self.resetCounter.Enable(False)

        self.closeFile.Enable(False)

    def enableGroupToIndividualItem(self) -> None:
        self.toggleGroupToIndividual.Enable(True)
    
