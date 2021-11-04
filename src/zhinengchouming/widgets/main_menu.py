from wx import Menu, ID_ANY, ID_OPEN, ID_SAVEAS, ID_EXIT, EVT_MENU
from wx.core import ID_CLOSE


class MainMenu(Menu):
    def __init__(self, parent):
        super(MainMenu, self).__init__()

        self.toggleStyle = self.AppendCheckItem(ID_ANY, "隐藏标题栏")
        self.toggleScore = self.AppendCheckItem(ID_ANY, "打开记分数功能")
        self.toggleGroupToIndividual = self.AppendCheckItem(ID_ANY, "小组点到人")

        self.toggleScore.Enable(False)
        self.toggleGroupToIndividual.Enable(False)

        self.AppendSeparator()
        self.openfile = self.Append(ID_OPEN, "&打开...", " 打开文件")
        self.saveScores = self.Append(ID_SAVEAS, "&保存分数...", "保存分数")
        self.saveScores.Enable(False)
        self.closeFile = self.Append(ID_CLOSE, "&关闭文件", "关闭文件")
        self.closeFile.Enable(False)
        self.quit = self.Append(ID_EXIT, '退出', '退出软件')

        self.Bind(EVT_MENU, parent.parent.toggleStyle, self.toggleStyle)
        self.Bind(EVT_MENU, parent.toggleScore, self.toggleScore)
        self.Bind(EVT_MENU, parent.toggleGroupToIndividual, self.toggleGroupToIndividual)
        self.Bind(EVT_MENU, parent.openFile, self.openfile)
        self.Bind(EVT_MENU, parent.saveScores, self.saveScores)
        self.Bind(EVT_MENU, parent.closeFile, self.closeFile)
        self.Bind(EVT_MENU, parent.onQuit, self.quit)

    def enableScoreItem(self) -> None:
        self.toggleScore.Enable(True)

    def disableScoreItem(self) -> None:
        self.toggleScore.Enable(False)
        self.toggleScore.Check(False)

    def enableGroupToIndividualItem(self) -> None:
        self.toggleGroupToIndividual.Enable(True)
    
    def disableGroupToIndividualItem(self) -> None:
        self.toggleGroupToIndividual.Enable(False)
        self.toggleGroupToIndividual.Check(False)

    def enableSaveScores(self) -> None:
        self.saveScores.Enable(True)

    def disableSaveScores(self) -> None:
        self.saveScores.Enable(False)

    def enableCloseFile(self) -> None:
        self.closeFile.Enable(True)

    def disableCloseFile(self) -> None:
        self.closeFile.Enable(False)