import MySQLdb
import problem
from simulator import rack

class ProblemReader(object):

    # DB Configuration
    DBAdress = 'imlab-ws2.snu.ac.kr'
    DBName = 'ASRS'
    DBID = 'ioasrs'
    DBPassward = '1wjdqhruddud'

    def __init__(self, table_idx):
        self.table_idx = table_idx

    def get_problem(self, problem_idx):
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = 'SELECT aisleNum, columnNum, floorNum, itemTypeNum,  requestLength, shuttleNum FROM problemConfigNew WHERE idx = '+str(self.table_idx)
        cur.execute(sql)
        row = cur.fetchone()
        p = problem.Problem(row[0], row[1], row[2], row[3], row[4], row[5])
        column = row[1]
        floor = row[2]

        sql = 'SELECT rack, input, output FROM problemSet_c'+str(self.table_idx)+ ' WHERE idx = '+str(problem_idx)
        cur.execute(sql)
        #for i in range(cur.rowcount):
        row = cur.fetchone()
        ra = rack.rack(map(int, row[0].split(", ")), column, floor)
        p.set_problem(ra, map(int, row[1].split(", ")), map(int, row[2].split(", ")))
        con.close()
        return p


    def get_problems(self, NO_of_problem):
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = 'SELECT aisleNum, columnNum, floorNum, itemTypeNum,  requestLength, shuttleNum FROM problemConfigNew WHERE idx = ' + str(
            self.table_idx)
        cur.execute(sql)
        row = cur.fetchone()
        a0, a1, a2, a3, a4, a5 = row[0], row[1], row[2], row[3], row[4], row[5]

        ps = []

        sql = 'SELECT rack, input, output FROM problemSet_c' + str(self.table_idx) + ' LIMIT ' + str(NO_of_problem)
        cur.execute(sql)
        for i in range(cur.rowcount):
            row = cur.fetchone()
            p = problem.Problem(a0, a1, a2, a3, a4, a5)
            ra = rack.rack(map(int, row[0].split(", ")), a1, a2)
            p.set_problem(ra, map(int, row[1].split(", ")), map(int, row[2].split(", ")))
            ps.append(p)
        con.close()
        return ps


class ProblemWithSolutionReader(ProblemReader):

    DBName = 'ASRS.solver'

    def get_problem_with_solution(self):
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = 'SELECT aisleNum, columnNum, floorNum, itemTypeNum,  requestLength, shuttleNum FROM problemConfig WHERE idx = ' + str(
            self.table_idx)
        cur.execute(sql)
        row = cur.fetchone()
        pws = problem.ProblemWithSolution(row[0], row[1], row[2], row[3], row[4], row[5])

        sql = 'SELECT rack, input, output, NN_sol, RNN_sol FROM problemSet_c' + str(self.table_idx) + ' WHERE idx = ' + str(
            self.problem_idx)
        cur.execute(sql)
        # for i in range(cur.rowcount):
        row = cur.fetchone()
        pws.set_problem_with_solution(row[0], row[1], row[2], row[3], row[4])
        con.close()
        return pws

if __name__ == '__main__':
    test = ProblemReader(20)
    print len(test.get_problem(1).output)