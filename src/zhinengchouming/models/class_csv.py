from collections import Sequence
from csv import DictReader
from typing import Counter, Deque, Dict, List, Tuple

from models.name_list import NameList
from models.score_keeper import ScoreKeeper

class ClassCSV:
    def __init__(self, csvData: DictReader, filename: str) -> None:

        assert csvData.fieldnames is not None
        self.fields : List = list(filter(lambda x: x, csvData.fieldnames))
        
        print(self.fields)
        listOfData: List[Dict] = list(csvData)
        fieldsPlusDict, self.dictOfKey = makeDictOfKeys(self.fields[0], self.fields, listOfData) 
        print(fieldsPlusDict)
        self.fieldsPlus = [item for sublist in fieldsPlusDict.values() for item in sublist]

        print(self.fieldsPlus)
        print(self.dictOfKey)

        self.orderedList = self.fieldsPlus[1:] + self.dictOfKey[self.fields[0]]

        self.calledCount: Counter = Counter([item for sublist in self.dictOfKey.values() for item in sublist])
        self.calledCount: Counter = Counter({k: 1 for k, v in self.calledCount.items()})

        self.filename = filename
        self.scoreKeeper = ScoreKeeper()

    def returnNameListFor(self, key: str) -> NameList:
        names = self.dictOfKey[key]
        filteredCounter = Counter({k: v for k, v in self.calledCount.items() if k in names})
        return NameList(names, filteredCounter)

    def returnListFor(self, key: str) -> List[str]:
        return self.dictOfKey[key]

    def mergeCalledCounts(self, calledCount2: Counter) -> None:
        self.calledCount = self.calledCount | calledCount2
    
    def resetCounter(self) -> None:
        self.calledCount: Counter = Counter({k: 1 for k, v in self.calledCount.items()})


def makeDictOfKeys(nameField: str, listOfKeys: List, csvData: List[Dict]) -> Tuple[Dict, Dict]:
    fieldsPlus: Dict = {"": listOfKeys}
    dictOfKeys: Dict = {}

    for key in listOfKeys:
        values = isolateValuesFor(key, csvData)
        if(key is not nameField):
            modifiedValues = (list(map(lambda x: f"{key}: {x}", values)))
            dictOfKeys[key] = modifiedValues
            fieldsPlus[key] = modifiedValues
            for value in values:
                dictOfKeys[f"{key}: {value}"] = isolateNamesFor(nameField, key, value, csvData)
        else:
            dictOfKeys[key] = values

    return fieldsPlus, dictOfKeys


def isolateValuesFor(key: str, csvData: List) -> List[str]:
    values: list = []
    for line in csvData:
        if(line[key] in values or not line[key]):
            pass
        else:
            list.append(values, line[key])
    return values


def isolateNamesFor(nameField: str, key: str, tag: str, csvData: List[Dict]) -> List[str]:
    names: list = []
    for line in csvData:
        if(tag == line[key]):
            names.append(line[nameField])
    return names
