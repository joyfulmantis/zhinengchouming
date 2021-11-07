from os import name
from typing import Callable, List, Optional
from wx import BoxSizer, HORIZONTAL, EVT_LEFT_DOWN, EVT_RIGHT_DOWN, SizerFlags, Timer
from wx.core import ALIGN_CENTER, ALIGN_CENTRE_HORIZONTAL, ST_NO_AUTORESIZE
from wx.lib.stattext import GenStaticText

from models.name_list import NameList
from models.score_keeper import ScoreKeeper

class NameScoreCombo(BoxSizer):
    def __init__(self,
                 parent, 
                 scoreKeeper: Optional[ScoreKeeper] = None, 
                 nameList: Optional[NameList] = None, 
                 initialText: str = "？",
                 intialTextExtent: str = "某某某",
                 initialScore: str = "0"):

        super().__init__(orient=HORIZONTAL)

        self.parent = parent
        self.scoreKeeper: Optional[ScoreKeeper] = scoreKeeper

        self.nameList: Optional[NameList] = nameList
        self.intialText: str = initialText
        self.intialScore: str = initialScore

        self.setLabelCallback: Optional[Callable] = None

        self.textBox = GenStaticText(parent, label=initialText, style=ALIGN_CENTER|ST_NO_AUTORESIZE)

        textBoxFont = self.textBox.GetFont()
        textBoxFont.PointSize = 60
        font = textBoxFont.Bold()
        self.textBox.SetFont(font)

        self.textBox.Bind(EVT_LEFT_DOWN, self.newText)
        self.textBox.SetInitialSize(self.textBox.GetTextExtent(intialTextExtent))

        self.scoreBox = GenStaticText(parent, label=initialScore, )

        scoreBoxFont = self.scoreBox.GetFont()
        scoreBoxFont.PointSize = 40
        scoreBoxFont = scoreBoxFont.Bold()
        self.scoreBox.SetFont(scoreBoxFont)

        self.scoreBox.Bind(EVT_LEFT_DOWN, self.scorePP)
        self.scoreBox.Bind(EVT_RIGHT_DOWN, self.scoreMM)

        self.scoreBox.Hide()

        self.Add(self.textBox, SizerFlags())
        self.AddStretchSpacer()
        self.Add(self.scoreBox, SizerFlags().DoubleHorzBorder().CenterVertical())

    """ Event Handlers """
    def newText(self, event = None):
        del event
        if(self.nameList is not None):
            self.timer = RandomNameAnimation(self,
                                             self.nameList.newName(),
                                             self.nameList.randomNames(),
                                             self.textBox)
            self.timer.Start(25)

    def scorePP(self, event):
        if(self.scoreKeeper is not None and
            self.getCurrentLabel() != self.intialText):
            self.scoreKeeper.increaseScoreFor(self.getCurrentLabel())
            self.scoreBox.SetLabel(
                str(self.scoreKeeper.getScoreFor(self.getCurrentLabel())))
            self.Fit()

    def scoreMM(self, event):
        if(self.scoreKeeper is not None and
            self.getCurrentLabel() != self.intialText):
            self.scoreKeeper.decreaseScoreFor(self.getCurrentLabel())
            self.scoreBox.SetLabel(
                str(self.scoreKeeper.getScoreFor(self.getCurrentLabel())))
            self.Fit()

    """Other Functions"""
    def getCurrentLabel(self) -> str:
        return self.textBox.GetLabelText()

    def setCurrentLabel(self, name: str) -> None:
        self.textBox.SetLabel(name)
        if(self.scoreKeeper is not None):
            self.scoreBox.SetLabel(str(self.scoreKeeper.getScoreFor(name)))

        self.Fit()

        if(self.setLabelCallback is not None):
            self.setLabelCallback()

    def setTextExtent(self, extent: str) -> None:
        self.textBox.SetInitialSize(self.textBox.GetTextExtent(extent))
        self.Fit()

    def loadNames(self, nameList: Optional[NameList]) -> None:
        if(self.nameList is not None and self.parent.classCSV is not None):
            self.parent.classCSV.mergeCalledCounts(self.nameList.nameListCounter)
        self.nameList = nameList
        self.resetLabel()

    def loadScoreKeeper(self, scoreKeeper: Optional[ScoreKeeper]) -> None:
        self.scoreKeeper = scoreKeeper

    def defineSetLabelCallback(self, function: Optional[Callable]) -> None:
        self.setLabelCallback = function

    def resetLabel(self) -> None:
        self.textBox.SetLabel(self.intialText)
        self.scoreBox.SetLabel(self.intialScore)
        self.Fit()

    def toggleScore(self) -> None:
        if(self.scoreBox.IsShownOnScreen()):
            self.scoreBox.Hide()
        else:
            self.scoreBox.Show()
        self.Fit()

    def toggle(self) -> None:
        if(self.textBox.IsShownOnScreen()):
            self.hide()
        else:
            self.show()

    def hide(self) -> None:
        self.textBox.Hide()
        self.scoreBox.Hide()
        self.Fit()

    def show(self) -> None:
        self.textBox.Show()
        if(self.parent.showScore):
            self.scoreBox.Show()
        self.Fit()

    def Fit(self):
        self.Layout()
        self.parent.Fit()


class RandomNameAnimation(Timer):
    def __init__(self, parent, name: str, animationNames: List[str], label: GenStaticText, *args, **kw):
        self.name = name
        self.animationNames = animationNames
        self.label = label
        self.parent = parent
        super().__init__(*args, **kw)

    def Notify(self):
        if(len(self.animationNames) > 0):
            self.label.SetLabel(self.animationNames.pop())
        else:
            self.Stop()
            self.parent.setCurrentLabel(self.name)

        return super().Notify()
