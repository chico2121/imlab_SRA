import problemreader
import action, solution
import math
import random

class ActionGenerator(object):

    def loca_calculate(self, index, size_h, size_v):

        loca = []

        if math.floor(index / (size_h * size_v)) == 0:
            loca.append(int(math.floor(index / (size_h * size_v))))
            loca.append(int(math.floor(index / size_v)))
            loca.append(int(index % size_v))

        else:
            loca.append(int(math.floor(index / (size_h * size_v))))
            loca.append(int(math.floor((index - size_h * size_v) / size_v)))
            loca.append(int((index - (size_h * size_v)) % size_v))

        return loca

    def change_to_two_dimension1(self, rack_status, columnNum, floorNum):
        result = [[0.0 for col in range(columnNum)] for row in range(floorNum)]
        for row in range(floorNum):
            for col in range(columnNum):
                result[row][col] = rack_status[row * floorNum + col]
        return result

    def change_to_two_dimension2(self, rack_status, columnNum, floorNum):
        result = [[0.0 for col in range(columnNum)] for row in range(floorNum)]
        for row in range(floorNum):
            for col in range(columnNum):
                result[row][col] = rack_status[columnNum * floorNum + row * floorNum + col]
        return result

    def right_search(self, rack, column, floor, sol, idx):
        # rightward direction search
        new_sol = sol
        target_loc = new_sol.loc[idx]
        target_seq = new_sol.oper[idx]
        target_type = new_sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and new_sol.oper[temp1] == target_seq:
                other_loc = new_sol.loc[temp1]

        excep_num = other_loc[0]*column*floor + other_loc[1]*column + other_loc[2]

        lot = []
        max_col = column - 1
        max_flo = floor - 1
        dif_col = max_col - target_loc[1]
        dif_flo = max_flo - target_loc[2]

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] > target_loc[1]:
                    if loca1[2] == target_loc[2]:
                        lot.append(loca1)
                    elif loca1[2] > target_loc[2]:
                        upper_slope = float(dif_flo) / dif_col
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if target_slope < upper_slope:
                            lot.append(loca1)
                    elif loca1[2] < target_loc[2]:
                        lower_slope = float(-target_loc[2]) / dif_col
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if lower_slope < target_slope:
                            lot.append(loca1)

        if lot == []:
            return new_sol
        else:

            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def left_search(self, rack, column, floor, sol, idx):
        # leftward direction search

        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []
        max_flo = floor - 1
        dif_col = - target_loc[1]
        dif_flo = max_flo - target_loc[2]

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] < target_loc[1]:
                    if loca1[2] == target_loc[2]:
                        lot.append(loca1)
                    elif loca1[2] > target_loc[2]:
                        upper_slope = float(dif_flo) / dif_col
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if upper_slope < target_slope:
                            lot.append(loca1)
                    elif loca1[2] < target_loc[2]:
                        lower_slope = float(-target_loc[2]) / dif_col
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if lower_slope > target_slope:
                            lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def top_search(self, rack, column, floor, sol, idx):
        # top direction search

        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []
        max_col = column - 1
        max_flo = floor - 1
        dif_col = max_col - target_loc[1]
        dif_flo = max_flo - target_loc[2]

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[2] > target_loc[2]:
                    if loca1[1] == target_loc[1]:
                        lot.append(loca1)
                    elif loca1[1] > target_loc[1]:
                        right_slope = float(dif_flo) / dif_col
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if target_slope > right_slope:
                            lot.append(loca1)
                    elif loca1[1] < target_loc[1]:
                        left_slope = float(dif_flo) / (- target_loc[1])
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if left_slope < target_slope:
                            lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def bottom_search(self, rack, column, floor, sol, idx):
        # bottom direction search

        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []
        max_col = column - 1
        dif_col = max_col - target_loc[1]

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[2] < target_loc[2]:
                    if loca1[1] == target_loc[1]:
                        lot.append(loca1)
                    elif loca1[1] > target_loc[1]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        right_slope = float(- target_loc[2]) / dif_col
                        if target_slope > right_slope:
                            lot.append(loca1)
                    elif loca1[1] < target_loc[1]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        left_slope = float(- target_loc[2]) / (- target_loc[1])
                        if left_slope < target_slope:
                            lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def right_top_search(self, rack, column, floor, sol, idx):
        # upper right search
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] > target_loc[1] and loca1[2] > target_loc[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def right_bottom_search(self, rack, column, floor, sol, idx):
        # below right search
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] > target_loc[1] and loca1[2] < target_loc[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def left_top_search(self, rack, column, floor, sol, idx):
        # upper left search
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] < target_loc[1] and loca1[2] > target_loc[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def left_bottom_search(self, rack, column, floor, sol, idx):
        # below left search
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] < target_loc[1] and loca1[2] < target_loc[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def before_search(self, rack, column, floor, sol, idx):
        # close to after point
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []

        if idx == 0:
            before_node = [0, 0, 0]
        else:
            before_node = sol.loc[idx - 1]

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if min(target_loc[1], before_node[1]) < loca1[1] < max(target_loc[1], before_node[1]) \
                        and min(target_loc[2], before_node[2]) < loca1[2] < max(target_loc[2], before_node[2]):
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def next_search(self, rack, column, floor, sol, idx):
        # close to after point
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []

        if idx == 3:
            next_node = [0, 0, 0]
        else:
            next_node = sol.loc[idx + 1]

        for a, item1 in enumerate(rack):
            if item1 == target_num and a != excep_num:
                loca1 = self.loca_calculate(a, column, floor)
                if min(target_loc[1], next_node[1]) < loca1[1] < max(target_loc[1], next_node[1]) \
                        and min(target_loc[2], next_node[2]) < loca1[2] < max(target_loc[2], next_node[2]):
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1]-target_loc[1]), 2) + math.pow((lot[b][2]-target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[b]
                    distance = new_distance
            return new_sol

    def item_search(self, rack, column, floor, sol, idx):
        # close to median value of the item
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        # target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            return sol

        for temp1 in range(4):
            if idx != temp1 and sol.oper[temp1] == target_seq:
                other_loc = sol.loc[temp1]

        excep_num = other_loc[0] * column * floor + other_loc[1] * column + other_loc[2]

        lot = []
        sublot = []

        for a, item1 in enumerate(rack):
            if item1 == sol.type[idx]:
                loca1 = self.loca_calculate(a, column, floor)
                sublot.append(loca1)

        target_to = [0, 0, 0]
        target_to_go = [0, 0, 0]

        for b in range(len(sublot)):
            target_to[1] += sublot[b][1]
            target_to[2] += sublot[b][2]

        target_to_go[1] = float(target_to[1]) / len(sublot)
        target_to_go[2] = float(target_to[2]) / len(sublot)

        for c, item1 in enumerate(rack):
            if item1 == target_num and c != excep_num:
                loca1 = self.loca_calculate(c, column, floor)
                if min(target_loc[1], target_to_go[1]) < loca1[1] < max(target_loc[1], target_to_go[1]) \
                        and min(target_loc[2], target_to_go[2]) < loca1[2] < max(target_loc[2], target_to_go[2]):
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            new_sol = sol
            distance = 10000
            for d in range(len(lot)):
                new_distance = math.pow((lot[d][1] - target_loc[1]), 2) + math.pow((lot[d][2] - target_loc[2]), 2)
                if distance > new_distance:
                    new_sol.loc[idx] = lot[d]
                    distance = new_distance
            return new_sol

    def generating_idx(self, rack, column, floor, sol, idx, iter):
        # idx means action type
        # iter means operate time

        if idx == 0:  # original solution
            return sol

        elif idx == 1:  # right search solution
            new_sol = self.right_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 2:  # left search solution
            new_sol = self.left_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 3:  # top search solution
            new_sol = self.top_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 4:  # bottom search solution
            new_sol = self.bottom_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 5:  # right top search solution
            new_sol = self.right_top_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 6:  # right bottom search solution
            new_sol = self.right_bottom_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 7:  # left top search solution
            new_sol = self.left_top_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 8:  # left bottom search solution
            new_sol = self.left_bottom_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 9:  # before node search solution
            new_sol = self.before_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 10:  # next node search solution
            new_sol = self.next_search(rack, column, floor, sol, iter)
            return new_sol

        elif idx == 11:  # target item search solution
            new_sol = self.item_search(rack, column, floor, sol, iter)
            return new_sol

    def full_random_action(self, rack, column, floor, sol):
        # fully random selection

        action = []

        for a in range(4):
            idx = random.randrange(0, 12)
            result = self.generating_idx(rack, column, floor, sol, idx, a)
            action.append(idx)

        return result, action

    def action_fixed_action(self, rack, column, floor, sol, idx):
        # generate each operation with fixed action

        for iter in range(4):
            result = self.generating_idx(rack, column, floor, sol, idx, iter)

        return result

    def oper_fixed_random_action(self, rack, column, floor, sol, iter):
        # generate random action with fixed operation
        # unnecessary

        result = []
        temp = sol

        for idx in range(12):
            result.append(self.generating_idx(rack, column, floor, temp, idx, iter).loc)

        return result

if __name__ == '__main__':

    test = problemreader.ProblemReader(20)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor

    make = ActionGenerator()

    # for a in range(floor):
    #    print (floor - a - 1), make.change_to_two_dimension1(rs, column, floor)[floor - a - 1], '    ', \
    #        make.change_to_two_dimension2(rs, column, floor)[floor - 1 - a]

    ts = action.action()
    sol = ts.dijk(rs, column, floor, [18, 24], [23, 25])[0]
    temp = solution.solution(sol.loc, sol.type, sol.oper)

    print column, floor, sol.type, sol.oper
    print sol.loc
    print

    print make.generating_idx(rs, column, floor, sol, 1, 1)

    # result = make.full_random_action(rs, column, floor, sol)
    # result = make.action_fixed_action(rs, column, floor, sol, 11)
    # result = make.oper_fixed_random_action(rs, column, floor, sol, 0)

    # print result.loc
