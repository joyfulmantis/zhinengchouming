
from chardet import detect
from codecs import decode
from datetime import datetime
from csv import DictReader
from typing import Optional

from wx import Panel, EVT_CLOSE, BoxSizer, VERTICAL, HORIZONTAL, Size, EVT_BUTTON, Choice, EVT_CHOICE, SizerFlags, FileDialog, FD_OPEN, FD_FILE_MUST_EXIST, ID_CANCEL, MessageBox, ICON_ERROR, OK, FD_SAVE, FD_OVERWRITE_PROMPT, CallAfter, YES_NO, NO_DEFAULT, ICON_QUESTION, MessageDialog, ID_YES
from wx.svg import SVGimage
from wx.lib.buttons import GenBitmapButton

from models.class_csv import ClassCSV
from widgets.main_menu import MainMenu
from widgets.name_score_combo import NameScoreCombo

from resources.icons8_menu_svg import icons8_menu_svg

class MainPanel(Panel):
    def __init__(self, parent) -> None:
        super(MainPanel, self).__init__(parent)

        self.parent = parent

        self.Bind(EVT_CLOSE, self.onQuit)

        self.classCSV: Optional[ClassCSV] = None

        self.showScore: bool = False
        self.enableGroupToIndividual: bool = False

        self.mainSizer = BoxSizer(VERTICAL)

        controlsSizer = BoxSizer(HORIZONTAL)

        self.mainMenu = MainMenu(self)

        img = SVGimage.CreateFromBytes(icons8_menu_svg.encode('utf-8'))
        bmp = img.ConvertToScaledBitmap(Size(24, 24), self)
        self.button = GenBitmapButton(self, bitmap=bmp)

        self.button.Bind(EVT_BUTTON, self.menuButton)

        controlsSizer.Add(self.button)

        self.choices = Choice(self)
        choicesFont = self.choices.GetFont()
        choicesFont.PointSize = 14
        self.choices.SetFont(choicesFont)

        self.Bind(EVT_CHOICE, self.selectChoice, self.choices)

        self.choices.Disable()

        controlsSizer.Add(
            self.choices, SizerFlags().Proportion(1).Expand())

        self.mainNameBox = NameScoreCombo(self)

        self.secondaryNameBox = NameScoreCombo(self)

        self.secondaryNameBox.hide()

        self.mainSizer.Add(controlsSizer, SizerFlags().Expand())
        self.mainSizer.Add(self.mainNameBox, SizerFlags().Expand())
        self.mainSizer.Add(self.secondaryNameBox, SizerFlags().Expand())
        self.mainSizer.AddStretchSpacer()

        self.SetSizer(self.mainSizer)
        self.Fit()

    """Event handlers"""

    def openFile(self, event) -> None:
        self.closeFile()

        with FileDialog(self,
                        "打开 CSV 文件",
                        wildcard="CSV 文件 (*.csv)|*.csv",
                        style=FD_OPEN | FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    fileBytes = file.read()
                    encoding: str = detect(fileBytes)['encoding']

                    csvData = DictReader(decode(fileBytes, encoding).splitlines())

                    self.parent.SetTitle(
                        f"智能抽名 - '{fileDialog.GetFilename()}")
                    self.classCSV = ClassCSV(csvData, fileDialog.GetFilename())

                    self.mainNameBox.loadNames(
                        self.classCSV.returnListFor(self.classCSV.fields[0]))

                    self.mainNameBox.loadScoreKeeper(self.classCSV.scoreKeeper)
                    self.secondaryNameBox.loadScoreKeeper(
                        self.classCSV.scoreKeeper)

                    self.choices.Enable()
                    self.choices.Set(self.classCSV.fieldsPlus)
                    self.choices.SetSelection(0)

                    self.mainMenu.enableScoreItem()
                    self.mainMenu.enableSaveScores()
                    self.mainMenu.enableCloseFile()

                    if(len(self.classCSV.fields) > 1):
                        self.mainMenu.enableGroupToIndividualItem()
            except AssertionError:
                MessageBox("无法解读您文件的格式",
                                "Error",
                                OK | ICON_ERROR)
            except Exception as e:
                MessageBox("出现错误 \n {str(e)}",
                                        "Error",
                                        OK | ICON_ERROR)


    def closeFile(self, event=None) -> None:
        try:
            if(self.classCSV is not None and
                    self.classCSV.scoreKeeper.isNotEmpty() and
                    self.classCSV.scoreKeeper.isNotSaved):
                self.promptSaveScores()

            if(self.showScore == True):
                self.toggleScore()
            if(self.enableGroupToIndividual == True):
                self.toggleGroupToIndividual()

            self.parent.SetTitle("智能抽名 - 请打开文件")
            self.classCSV = None

            self.choices.Clear()
            self.choices.Disable()

            self.mainNameBox.loadNames(None)
            self.secondaryNameBox.loadNames(None)
            self.mainNameBox.loadScoreKeeper(None)
            self.secondaryNameBox.loadScoreKeeper(None)
            
            self.mainMenu.disableScoreItem()
            self.mainMenu.disableSaveScores()
            self.mainMenu.disableGroupToIndividualItem()
            self.mainMenu.disableCloseFile()

        except Exception as e:
            MessageBox("出现错误 \n {str(e)}",
                                    "Error",
                                    OK | ICON_ERROR)

    def saveScores(self, event=None) -> None:
        if(self.classCSV is not None):
            with FileDialog(self,
                            "保存班级分数",
                            defaultFile=f"{self.classCSV.filename.replace('.', '-')}-{datetime.now().isoformat(timespec='minutes').replace(':', '-')}.txt",
                            wildcard="TXT 文件 (*.txt)|*.txt",
                            style=FD_SAVE | FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == ID_CANCEL:
                    return

                pathname = fileDialog.GetPath()
                try:
                    with open(pathname, "w") as text_file:
                        text_file.write(
                            self.classCSV.scoreKeeper.saveScores(
                                self.classCSV.filename, self.classCSV.orderedList))
                except IOError:
                    MessageBox(f"无法写到 {pathname}",
                                    "Error",
                                    OK | ICON_ERROR)
                except Exception as e:
                                MessageBox("出现错误 \n {str(e)}",
                                    "Error",
                                    OK | ICON_ERROR)

    def selectChoice(self, event) -> None:
        if(self.classCSV is not None):
            self.mainNameBox.loadNames(
                self.classCSV.returnListFor(event.GetString()))

    def menuButton(self, event) -> None:
        self.PopupMenu(self.mainMenu)

    def toggleScore(self, event=None) -> None:
        self.showScore = not self.showScore
        self.mainNameBox.toggleScore()
        if(self.enableGroupToIndividual):
            self.secondaryNameBox.toggleScore()

    def toggleGroupToIndividual(self, event=None) -> None:
        if(self.classCSV is not None):
            self.enableGroupToIndividual = not self.enableGroupToIndividual

            if(self.enableGroupToIndividual):
                self.choices.Set(self.classCSV.fields[1:])
                self.mainNameBox.defineSetLabelCallback(self.callSecondaryBox)
            else:
                self.choices.Set(self.classCSV.fieldsPlus)
                self.mainNameBox.defineSetLabelCallback(None)

            self.choices.SetSelection(0)
            self.mainNameBox.loadNames(
                self.classCSV.returnListFor(self.choices.GetString(0)))

            self.secondaryNameBox.toggle()

    def onQuit(self, event):
        try:
            self.closeFile()
        finally:
            del event
            CallAfter(self.parent.Destroy)

    """Other functions"""

    def promptSaveScores(self) -> None:
        with MessageDialog(
            self,
            '你是否想保存您的分数?',
            '确认',
                YES_NO | NO_DEFAULT | ICON_QUESTION) as dlg:
            if dlg.ShowModal() == ID_YES:
                self.saveScores()

    def callSecondaryBox(self) -> None:
        if(self.classCSV is not None):
            self.secondaryNameBox.loadNames(
                self.classCSV.returnListFor(self.mainNameBox.getCurrentLabel()))
            self.secondaryNameBox.newText()

    def Fit(self):
        self.mainSizer.Fit(self.parent)
