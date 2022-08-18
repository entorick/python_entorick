# https://leetcode.cn/problems/asteroid-collision/

class Solution(object):
    def asteroidCollision(self, asteroids):
        """
        :type asteroids: List[int]
        :rtype: List[int]
        """
        if len(asteroids) == 0:
            return asteroids

        remain_flag = None
        cur_flag = None

        remain = []
        for v in asteroids:
            cur_flag = True if v > 0 else False

            if len(remain) == 0:
                remain.append(v)
                remain_flag = cur_flag
                continue

            if cur_flag == remain_flag:
                # 相同
                remain.append(v)
                continue
            elif cur_flag:
                # 负正不撞
                remain_flag = cur_flag
                remain.append(v)
                continue

            while len(remain) > 0:
                pop = remain.pop()
                remain_flag = True if pop > 0 else False
                if remain_flag == cur_flag:
                    # 撞到方向相同
                    remain.append(pop)
                    remain.append(v)
                    break
                if (pop + v) > 0 and cur_flag:
                    continue
                if (pop + v) > 0 and not cur_flag:
                    remain.append(pop)
                    break
                if (pop + v) < 0 and cur_flag:
                    remain.append(pop)
                    break
                if (pop + v) < 0 and not cur_flag:
                    continue
                if (pop + v) == 0:
                    break

            if len(remain) == 0 and (pop + v) != 0:
                remain.append(v)
                remain_flag = cur_flag

        return remain


asteroids = [5, 10, -5]
print(Solution().asteroidCollision(asteroids))
asteroids = [8, -8]
print(Solution().asteroidCollision(asteroids))
asteroids = [10, 2, -5]
print(Solution().asteroidCollision(asteroids))
asteroids = [-2, -1, 1, 2]
print(Solution().asteroidCollision(asteroids))
asteroids = [-2, -2, 1, -2]
print(Solution().asteroidCollision(asteroids))
asteroids = [1, -2, -2, -2]
print(Solution().asteroidCollision(asteroids))