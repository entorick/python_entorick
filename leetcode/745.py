from typing import List

# https://leetcode.cn/problems/prefix-and-suffix-search/

class WordFilter:

    def __init__(self, words: List[str]):
        self.pref_dict_tree = DictTree()
        self.suff_dict_tree = DictTree()
        for idx, word in enumerate(words):
            self.pref_dict_tree.append(word, idx)
            self.suff_dict_tree.append(word[::-1], idx)

    def f(self, pref: str, suff: str) -> int:
        pref_find_lst = self.pref_dict_tree.pref_find(pref)
        suff_find_lst = self.suff_dict_tree.pref_find(suff[::-1])
        ret = -1
        if len(pref_find_lst) == 0 or len(suff_find_lst) == 0:
            return ret

        pref_key_lst = pref_find_lst.copy()
        suff_key_lst = suff_find_lst.copy()
        pref_point = pref_key_lst.pop(-1)
        suff_point = suff_key_lst.pop(-1)
        while True:
            if pref_point == suff_point:
                return pref_point
            if pref_point > suff_point and len(pref_key_lst) == 0:
                break
            if pref_point < suff_point and len(suff_key_lst) == 0:
                break
            if pref_point > suff_point:
                pref_point = pref_key_lst.pop(-1)
                continue
            if pref_point < suff_point:
                suff_point = suff_key_lst.pop(-1)
                continue

        # for k, value in pref_find_lst.items():
        #     if k in suff_find_lst and k > ret:
        #         ret = k

        return ret


class DictTree:

    def __init__(self):
        self.tree = {}
        self.id_lst = []

    def append(self, word: str, idx: int):
        char = word[0]
        if char in self.tree:
            # 当前节点已经有了
            node: DictTree = self.tree[char]
            if len(word) == 1:
                # 最后一个
                node.id_lst.append(idx)
                return

            node.id_lst.append(idx)
            node.append(word[1:], idx)
        else:
            sub_tree = DictTree()
            sub_tree.id_lst.append(idx)
            if len(word) != 1:
                sub_tree.append(word[1:], idx)
            self.tree.update({char: sub_tree})

    def pref_find(self, pref: str):
        cur_tree = self
        for char in pref:
            if char in cur_tree.tree:
                cur_tree = cur_tree.tree[char]
            else:
                return []
        return cur_tree.id_lst


# Your WordFilter object will be instantiated and called as such:
# obj = WordFilter(["apple"])
# obj = WordFilter(["apple", "apologize"])
# obj = WordFilter(["abbba", "abba"])
# obj = DictTree()
# obj.append("apple", 0)
# obj.append("apologize", 1)
# print(obj.pref_find("apo"))

# print(obj.f("a", "e"))
# print(obj.f("a", "e"))
# print(obj.f("b", "e"))

# import time
from tmp import data, params
#
# x = time.time()
obj = WordFilter(data)
print(data[1597])
print(obj.f("ukfjp", "fjp"))
# print(str(time.time() - x))
# for v in params:
#     obj.f(v[0], v[1])
#
# print(str(time.time() - x))
