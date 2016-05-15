import solution

class reward(object):
    ySpeed = 2.5
    zSpeed = 0.6666667

    def get_maxtime(self, columnNum, floorNum, shuttleNum):
        return (shuttleNum * 2 + 1) * self.get_time([0,0,0], [0, columnNum-1, floorNum-1])

    def get_cycletime(self, solution):
        cycletime = 0.0
        for i in range(len(solution.loc)):
            if i == 0:
                cycletime += self.get_time([0,0,0], solution.loc[i])
            else:
                cycletime += self.get_time(solution.loc[i], solution.loc[i-1])

        cycletime += self.get_time([0,0,0], solution.loc[len(solution.loc)-1])
        return cycletime

    def get_time(self, start, end):
        return max(abs((float(start[1]) - float(end[1])) / self.ySpeed),
                   abs((float(start[2]) - float(end[2])) / self.zSpeed))

if __name__ == '__main__':
    test = reward()
    sol = solution.solution([[0,1,0],[0,2,0]], [1,2], ['S','R'])
    print test.get_cycletime(sol)
    print test.get_maxtime(2, 3, 2)
