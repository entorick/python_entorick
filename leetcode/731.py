# https://leetcode.cn/problems/my-calendar-ii/

class MyCalendarTwo:

    def __init__(self):
        self.idx = 0
        self.lst = {}
        self.start = {}
        self.end = {}

    def book(self, start: int, end: int) -> bool:
        self.idx += 1
        tmp = {}

        for k, v in self.start.items():
            if k < start:
                continue
            if k >= end:
                break
            if start <= k < end:
                for vv in v:
                    tmp[vv] = True

        for k, v in self.end.items():
            if k <= start:
                continue
            if k >= end:
                break
            if start < k < end:
                for vv in v:
                    if vv in tmp:
                        del (tmp[vv])
                    else:
                        tmp[vv] = True

        if len(tmp) == 2:
            return False

        if start in self.start:
            self.start[start].append(self.idx)
        else:
            self.start[start] = [self.idx]
        self.start = self.sort_dict(self.start)

        if end in self.end:
            self.end[end].append(self.idx)
        else:
            self.end[end] = [self.idx]
        self.end = self.sort_dict(self.end)
        self.lst[self.idx] = [start, end]

        return True

    def sort_dict(self, dct: dict) -> dict:
        ret = {}
        if len(dct.keys()) == 0:
            return ret
        for k in sorted(dct.keys()):
            ret[k] = dct[k]
        return ret


# Your MyCalendarTwo object will be instantiated and called as such:
obj = MyCalendarTwo()
# obj.book(10, 15)
# exit()

# xx = [[28, 46], [9, 21], [21, 39], [37, 48], [38, 50], [22, 39], [45, 50], [1, 12], [40, 50], [31, 44]]
xx = [[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
for v in xx:
    # if v == [45, 50]:
    #     print([(k, obj.lst[k]) for k in sorted(obj.lst.keys())])
    #     exit()
    param_1 = obj.book(v[0], v[1])
    print(param_1)
