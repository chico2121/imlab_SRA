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


    def make_table_dijk(self,tidx):
        tablename = 'dijk_'+str(tidx)+'density'
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `%s`" \
              "(" \
              "idx int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT," \
              "iteridx int(10) NULL," \
              "rs TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "act int(2) NULL DEFAULT NULL," \
              "inp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "outp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "reward float(5,2) NULL DEFAULT NULL," \
              "rsprime TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "terminal TEXT NULL COLLATE utf8mb4_unicode_ci" \
              ")" % (tablename)
        cur.execute(sql)



    def insert_ob_dijk(self, tidx, pidx):

        test = problemreader.ProblemReader(tidx)
        rs = test.get_problem(pidx).rack.status
        column = test.get_problem(pidx).rack.column
        floor = test.get_problem(pidx).rack.floor
        input = test.get_problem(pidx).input
        output = test.get_problem(pidx).output

        tablename = 'dijk_'+str(tidx)+'density'
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        simul = nextstate.simul()


        for iter in range(1,1001):
            rs1 = test.get_problem(pidx).rack.status

            for i in range(len(input) / 2):
                k = i + 1
                inputs = input[(k * 2 - 2):k * 2]
                outputs = output[(k * 2 - 2):k * 2]
                ac = action.action()
                idx = random.randrange(0,8)
                sol, cycletime = ac.dijk_density(rs1, column, floor, inputs, outputs, idx)
                #rs2 = simul.change_rs(rs1, column, floor, sol)
                if i == ((len(input) / 2) - 1):
                    cur.execute("""INSERT INTO """ + """%s""" % (
                    tablename) + """ (iteridx,rs,act,inp,outp,reward,rsprime,terminal) VALUES (%s,%s,%s,%s,%s,%s,%s,'O')""",
                                (iter, str(rs1), idx, str(inputs), str(outputs), cycletime, str(simul.change_rs(rs1, column, floor, sol))))
                    con.commit()
                    rs1 = rs
                else:
                    cur.execute("""INSERT INTO """ + """%s""" % (
                    tablename) + """ (iteridx,rs,act,inp,outp,reward,rsprime) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                                (iter, str(rs1), idx, str(inputs), str(outputs), cycletime, str(simul.change_rs(rs1, column, floor, sol))))
                    con.commit()
                    rs1 = simul.change_rs(rs1, column, floor, sol)


    def make_data_dijk(self, tidx, pidx):
        self.make_table_dijk(tidx)
        self.insert_ob_dijk(tidx,pidx)

    def make_table_selected_action(self, tidx):
        tablename = 'selected_action'+str(tidx)
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `%s`" \
              "(" \
              "idx int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT," \
              "iteridx int(10) NULL," \
              "rs TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "act int(2) NULL DEFAULT NULL," \
              "inp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "outp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "reward float(5,2) NULL DEFAULT NULL," \
              "rsprime TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "terminal TEXT NULL COLLATE utf8mb4_unicode_ci" \
              ")" % (tablename)
        cur.execute(sql)

    def insert_ob_selected_aciton(self, tidx, pidx):

        test = problemreader.ProblemReader(tidx)
        rs = test.get_problem(pidx).rack.status
        column = test.get_problem(pidx).rack.column
        floor = test.get_problem(pidx).rack.floor
        input = test.get_problem(pidx).input
        output = test.get_problem(pidx).output

        tablename = 'selected_action'+str(tidx)
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        simul = nextstate.simul()

        for iter in range(1, 1001):
            rs1 = test.get_problem(pidx).rack.status

            for i in range(len(input) / 2):
                k = i + 1
                inputs = input[(k * 2 - 2):k * 2]
                outputs = output[(k * 2 - 2):k * 2]
                ac = action.action()
                idxlist = [2,4,8,9,10,11]
                idx = random.choice(idxlist)
                sol, cycletime = ac.dijk_density(rs1, column, floor, inputs, outputs, idx)
                # rs2 = simul.change_rs(rs1, column, floor, sol)
                if i == ((len(input) / 2) - 1):
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (iteridx,rs,act,inp,outp,reward,rsprime,terminal) VALUES (%s,%s,%s,%s,%s,%s,%s,'O')""",
                                (iter, str(rs1), idx, str(inputs), str(outputs), cycletime,
                                 str(simul.change_rs(rs1, column, floor, sol))))
                    con.commit()
                    rs1 = rs
                else:
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (iteridx,rs,act,inp,outp,reward,rsprime) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                                (iter, str(rs1), idx, str(inputs), str(outputs), cycletime,
                                 str(simul.change_rs(rs1, column, floor, sol))))
                    con.commit()
                    rs1 = simul.change_rs(rs1, column, floor, sol)

    def make_data_selected_action(self, tidx, pidx):
        self.make_table_selected_action(tidx)
        self.insert_ob_selected_aciton(tidx, pidx)



    def make_table_fixed_operation(self, fixed_oper):
        tablename = 'fixed_operation_'+str(fixed_oper)
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `%s`" \
              "(" \
              "idx int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT," \
              "iteridx int(10) NULL," \
              "rs TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "act int(2) NULL DEFAULT NULL," \
              "inp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "outp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "reward float(5,2) NULL DEFAULT NULL," \
              "rsprime TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "terminal TEXT NULL COLLATE utf8mb4_unicode_ci" \
              ")" % (tablename)

        cur.execute(sql)

    def insert_ob_fixed_operation(self, tidx, pidx, fixed_oper): #fixed_oper : 0~3

        test = problemreader.ProblemReader(tidx)
        rs = test.get_problem(pidx).rack.status
        column = test.get_problem(pidx).rack.column
        floor = test.get_problem(pidx).rack.floor
        input = test.get_problem(pidx).input
        output = test.get_problem(pidx).output

        tablename = 'fixed_operation_'+str(fixed_oper)
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        simul = nextstate.simul()
        acg = actiongenerator.ActionGenerator()
        rw = reward.reward()
        ac = action.action()

        for iter in range(1,1001):
            rs1 = test.get_problem(pidx).rack.status
            for j in range(len(input) / 2):
                k = j + 1
                inputs = input[(k * 2 - 2):k * 2]
                outputs = output[(k * 2 - 2):k * 2]
                i = random.randrange(1, 12)
                sol, cycletime = ac.dijk(rs1, column, floor, inputs, outputs)
                new_sol = acg.generating_idx(rs1,column,floor,sol,i,fixed_oper)
                cycletime = rw.get_cycletime(new_sol)

                #rs2 = simul.change_rs(rs1, column, floor, new_sol)
                if j == ((len(input) / 2) - 1):
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (iteridx,rs,act,inp,outp,reward,rsprime,terminal) VALUES (%s,%s,%s,%s,%s,%s,%s,'O')""",
                                (iter, str(rs1), i, str(inputs), str(outputs), cycletime, str(simul.change_rs(rs1, column, floor, new_sol))))
                    con.commit()

                else:
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (iteridx,rs,act,inp,outp,reward,rsprime) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                                (iter, str(rs1), i, str(inputs), str(outputs), cycletime, str(simul.change_rs(rs1, column, floor, new_sol))))
                    con.commit()
                    rs1 = simul.change_rs(rs1, column, floor, new_sol)

    def make_data_fixed_operation(self, tidx, pidx):
        for i in range(4):
            self.make_table_fixed_operation(i)
            self.insert_ob_fixed_operation(tidx,pidx,i)

    def make_table_fixed_action(self, fixed_act):
        tablename = 'fixed_action_' + str(fixed_act)
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `%s`" \
              "(" \
              "idx int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT," \
              "iteridx int(10) NULL," \
              "rs TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "act int(2) NULL DEFAULT NULL," \
              "operation int(1) NULL DEFAULT NULL," \
              "inp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "outp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "reward float(5,2) NULL DEFAULT NULL," \
              "rsprime TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "terminal TEXT NULL COLLATE utf8mb4_unicode_ci" \
              ")" % (tablename)

        cur.execute(sql)

    def insert_ob_fixed_action(self, tidx, pidx, fixed_act):  # fixed_act : 1~11

        test = problemreader.ProblemReader(tidx)
        rs = test.get_problem(pidx).rack.status
        column = test.get_problem(pidx).rack.column
        floor = test.get_problem(pidx).rack.floor
        input = test.get_problem(pidx).input
        output = test.get_problem(pidx).output

        tablename = 'fixed_action_' + str(fixed_act)
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        simul = nextstate.simul()
        acg = actiongenerator.ActionGenerator()
        rw = reward.reward()
        ac = action.action()


        for iter in range(1, 1001):
            rs1 = test.get_problem(pidx).rack.status
            for j in range(len(input) / 2):
                k = j + 1
                inputs = input[(k * 2 - 2):k * 2]
                outputs = output[(k * 2 - 2):k * 2]
                i = random.randrange(0,4)
                sol, cycletime = ac.dijk(rs1, column, floor, inputs, outputs)
                new_sol = acg.generating_idx(rs1, column, floor, sol, fixed_act, i)
                cycletime = rw.get_cycletime(new_sol)
                #rs2 = simul.change_rs(rs1, column, floor, new_sol)

                if j == ((len(input) / 2) - 1):
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (iteridx,rs,act,operation,inp,outp,reward,rsprime,terminal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'O')""",
                                (iter, str(rs1), fixed_act, i, str(inputs), str(outputs), cycletime, str(simul.change_rs(rs1, column, floor, new_sol))))
                    con.commit()

                else:
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (iteridx,rs,act,operation,inp,outp,reward,rsprime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                                (iter, str(rs1), fixed_act, i, str(inputs), str(outputs), cycletime, str(simul.change_rs(rs1, column, floor, new_sol))))
                    con.commit()
                    rs1 = simul.change_rs(rs1, column, floor, new_sol)

    def make_data_fixed_action(self, tidx, pidx):
         for i in range(1,12):
            self.make_table_fixed_action(i)
            self.insert_ob_fixed_action(tidx,pidx,i)

    def make_table_action6(self):
        tablename = 'action6'
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `%s`" \
              "(" \
              "idx int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT," \
              "iteridx int(10) NULL," \
              "rs TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "act int(2) NULL DEFAULT NULL," \
              "inp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "outp TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "reward float(5,2) NULL DEFAULT NULL," \
              "rsprime TEXT NULL COLLATE utf8mb4_unicode_ci," \
              "terminal TEXT NULL COLLATE utf8mb4_unicode_ci" \
              ")" % (tablename)

        cur.execute(sql)

    def insert_ob_action6(self, tidx, pidx, fixed_oper):  # fixed_oper : 0~3

        test = problemreader.ProblemReader(tidx)
        rs = test.get_problem(pidx).rack.status
        column = test.get_problem(pidx).rack.column
        floor = test.get_problem(pidx).rack.floor
        input = test.get_problem(pidx).input
        output = test.get_problem(pidx).output

        tablename = 'fixed_operation_' + str(fixed_oper)
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        simul = nextstate.simul()
        acg = actiongenerator.ActionGenerator()
        rw = reward.reward()
        ac = action.action()

        for iter in range(1, 1001):
            rs1 = test.get_problem(pidx).rack.status
            for j in range(len(input) / 2):
                k = j + 1
                inputs = input[(k * 2 - 2):k * 2]
                outputs = output[(k * 2 - 2):k * 2]
                i = random.randrange(1, 12)
                sol, cycletime = ac.dijk(rs1, column, floor, inputs, outputs)
                new_sol = acg.generating_idx(rs1, column, floor, sol, i, fixed_oper)
                cycletime = rw.get_cycletime(new_sol)

                # rs2 = simul.change_rs(rs1, column, floor, new_sol)
                if j == ((len(input) / 2) - 1):
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (iteridx,rs,act,inp,outp,reward,rsprime,terminal) VALUES (%s,%s,%s,%s,%s,%s,%s,'O')""",
                                (iter, str(rs1), i, str(inputs), str(outputs), cycletime,
                                 str(simul.change_rs(rs1, column, floor, new_sol))))
                    con.commit()

                else:
                    cur.execute("""INSERT INTO """ + """%s""" % (
                        tablename) + """ (iteridx,rs,act,inp,outp,reward,rsprime) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                                (iter, str(rs1), i, str(inputs), str(outputs), cycletime,
                                 str(simul.change_rs(rs1, column, floor, new_sol))))
                    con.commit()
                    rs1 = simul.change_rs(rs1, column, floor, new_sol)

    def make_data_fixed_operation(self, tidx, pidx):
        for i in range(4):
            self.make_table_fixed_operation(i)
            self.insert_ob_fixed_operation(tidx, pidx, i)


if __name__ == '__main__':
    a = ObservationGenerator()
    a.make_data_dijk(23,1)
    #a.make_data_selected_action(23,1)
    #a.make_data_fixed_operation(23,1)
    #a.make_data_fixed_action(20,1)
