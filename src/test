import MySQLdb
import random
import actiongenerator
import action
import reward
import problemreader
import nextstate


class ObservationGenerator(object):

    # DB Configuration
    DBAdress = 'imlab-ws2.snu.ac.kr'
    DBName = 'ASRS_RL_DATA'
    DBID = 'ioasrs'
    DBPassward = '1wjdqhruddud'


    def make_table_exercise(self, percent):
        tablename = 'exercise' + str(percent[0])
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `%s`" \
              "(" \
              "idx int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT," \
              "pidx int(10) NULL," \
              "rs TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "act int(2) NULL DEFAULT NULL," \
              "inp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "outp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "reward float(5,2) NULL DEFAULT NULL," \
              "cum_reward float(8,2) NULL DEFAULT NULL," \
              "rsprime TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "terminal TEXT NULL COLLATE utf8mb4_unicode_ci" \
              ")" % (tablename)

        cur.execute(sql)

    def insert_ob_exercise(self, tidx, percent):

        per = []
        for a in range(len(percent)-1):
            for b in range(percent[a+1]):
                per.append(a + 1)

        tablename = 'exercise' + str(percent[0])
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        simul = nextstate.simul()
        acg = actiongenerator.ActionGenerator()
        rw = reward.reward()
        ac = action.action()

        for pidx in range(1, 21):
            print pidx
            test = problemreader.ProblemReader(tidx)
            rs = test.get_problem(pidx).rack.status
            column = test.get_problem(pidx).rack.column
            floor = test.get_problem(pidx).rack.floor
            input = test.get_problem(pidx).input
            output = test.get_problem(pidx).output

            rs1 = test.get_problem(pidx).rack.status
            cum_cycletime = 0
            for j in range(len(input) / 2):
                k = j + 1
                inputs = input[(k * 2 - 2):k * 2]
                outputs = output[(k * 2 - 2):k * 2]

                i = random.randrange(0, 100)
                sol, cycletime = ac.dijk(rs1, column, floor, inputs, outputs)
                selected_action = per[i]
                new_sol = acg.action_fixed_action(rs1, column, floor, sol, selected_action)
                cycletime = rw.get_cycletime(new_sol)
                cum_cycletime += cycletime

                # rs2 = simul.change_rs(rs1, column, floor, new_sol)
                if j == ((len(input) / 2) - 1):
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (pidx,rs,act,inp,outp,reward,cum_reward,rsprime,terminal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'O')""",
                                (pidx, str(rs1), selected_action, str(inputs), str(outputs), cycletime, cum_cycletime,
                                 str(simul.change_rs(rs1, column, floor, new_sol))))
                    con.commit()

                else:
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (pidx,rs,act,inp,outp,reward,cum_reward,rsprime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                                (pidx, str(rs1), selected_action, str(inputs), str(outputs), cycletime, cum_cycletime,
                                 str(simul.change_rs(rs1, column, floor, new_sol))))
                    con.commit()
                    rs1 = simul.change_rs(rs1, column, floor, new_sol)

    def make_data_exercise(self, tidx, percent):

        self.make_table_exercise(percent)
        self.insert_ob_exercise(tidx, percent)

if __name__ == '__main__':
    Ob = ObservationGenerator()
    # a.make_data_dijk(20,1)
    # a.make_data_fixed_operation(20,1)
    per = ['21', 55, 15, 15, 15]
    Ob.make_data_exercise(20, per)
    per = ['22', 15, 55, 15, 15]
    Ob.make_data_exercise(20, per)
    per = ['23', 15, 15, 55, 15]
    Ob.make_data_exercise(20, per)
    per = ['24', 15, 15, 15, 55]
    Ob.make_data_exercise(20, per)


    # for c in range(20):
    #    test = random.randrange(0, 100)
    #    print percent[test]



