# https://leetcode.cn/problems/qIsx9U/


class MovingAverage:

    def __init__(self, size: int):
        """
        Initialize your data structure here.
        """
        self.total = 0
        self.max = size
        self.lst = []

    def next(self, val: int) -> float:
        if len(self.lst) < self.max:
            self.total += val
            self.lst.append(val)
            return float(self.total) / len(self.lst)
        else:
            self.total -= self.lst.pop(0)
            self.total += val
            self.lst.append(val)
            return float(self.total) / len(self.lst)