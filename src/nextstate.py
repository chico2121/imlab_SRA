from problemIO import problemreader
from learner import solution
from learner import action
from learner import actiongenerator



class simul(object):


    def change_rs_from_problem(self, tidx, pidx, order_raw):  # order_raw format : [[59,51,68,1],[[1,0,0],[1,0,1],[1,0,1],[1,4,1]],['S','R','S','R']]
        test = problemreader.ProblemReader(tidx)
        rs2 = test.get_problems(pidx)[pidx - 1].rack.status
        rack_size_h = test.get_problems(pidx)[pidx - 1].rack.column
        rack_size_v = test.get_problems(pidx)[pidx - 1].rack.floor
        one_cycle_act = 4

        for action in range(one_cycle_act):
            loca = (rack_size_h * rack_size_v * order_raw[action + 1][0]) + (rack_size_v * order_raw[action + 1][1]) + \
                   order_raw[action + 1][2]

            if action % one_cycle_act == 0:  # one_cylce_act = 4
                if order_raw[5][action] == 'S':
                    rs2[loca] = order_raw[0][action]

                elif order_raw[5][action] == 'R':
                    rs2[loca] = -1

            else:
                if order_raw[5][action] == 'S':
                    rs2[loca] = order_raw[0][action]

                elif order_raw[5][action] == 'R':
                    rs2[loca] = -1

        return rs2


    def change_rs(self, rs, column, floor, sol):
                  # rs format : [-1,1,2,3,4,2,-1]

        rs2 = rs
        rack_size_h = column
        rack_size_v = floor

        for action in range(len(sol.loc)):
            loca = (rack_size_h * rack_size_v * sol.loc[action][0]) + (rack_size_v * sol.loc[action][1]) + \
                   sol.loc[action][2]

            if sol.oper[action] == 'S':

                rs2.insert(loca,sol.type[action])
                rs2.pop(loca+1)

            elif sol.oper[action] == 'R':

                rs2.insert(loca, -1)
                rs2.pop(loca + 1)

        return rs2


if __name__ == '__main__':
    test = problemreader.ProblemReader(20)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor
    input = test.get_problem(1).input
    output = test.get_problem(1).output
    solu,ct = action.action().dijk(rs,column,floor,input[0:2],output[0:2])


