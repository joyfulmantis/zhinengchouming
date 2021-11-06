from  itertools import cycle, islice
from random import SystemRandom
from typing import Counter, List

class NameList:
    def __init__(self, nameList: List[str], nameListCounter: Counter[str]) -> None:
        self.name = None
        self.nameList = nameList
        self.nameListCounter = nameListCounter
        self.myRandom = SystemRandom()

    def randomNames(self) -> List[str]:
        animationNames = cycle(self.myRandom.sample(self.nameList,
                                             len(self.nameList)))
        return list(islice(animationNames, 20))

    def newName(self) -> str:
        leastCommon = self.nameListCounter.most_common()[-1][1]
        name = self.myRandom.choice(seq = [k for k, v in self.nameListCounter.items() if v == leastCommon and k != self.name])

        print(self.nameListCounter)
        print(name)
        
        self.nameListCounter[name] += 1
        self.name = name
        return name

    def resetCounter(self) -> None:
        self.nameListCounter: Counter = Counter({k: 1 for k, v in self.nameListCounter.items()})