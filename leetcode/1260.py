from typing import List
from collections import deque

# https://leetcode.cn/problems/shift-2d-grid/


class Solution:

    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        x = deque()
        n_len = len(grid[0])
        for v in grid:
            for vv in v:
                x.append(vv)
        x.rotate(k)

        ret = []
        tmp = []
        for v in x:
            if len(tmp) == n_len:
                ret.append(tmp)
                tmp = []
            tmp.append(v)
        ret.append(tmp)
        return ret


a = Solution()
print(a.shiftGrid([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1))
