from typing import Counter, List


class ScoreKeeper():
    def __init__(self):
        self.counter: Counter[str] = Counter()
        self.isNotSaved = True

    def isNotEmpty(self) -> bool:
        return (len(list(self.counter)) > 0)

    def getScoreFor(self, name) -> int:
        return self.counter[name]
    
    def increaseScoreFor(self, name) -> None:
        self.counter[name] += 1
        self.isNotSaved = True
    
    def decreaseScoreFor(self, name) -> None:
        self.counter[name] -= 1
        self.isNotSaved = True
    
    def saveScores(self, filename: str, orderedList: List[str]) -> str:
        file = f"{filename} 分数记录\n"
        for item in orderedList:
            if(item in self.counter):
                file += f"{item} : {self.counter[item]}\n"
        self.isNotSaved = False
        return file