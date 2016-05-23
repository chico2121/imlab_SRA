import MySQLdb
from collections import deque
import reward
import state
import numpy as np

class OBSfromDB(object):
    # DB Configuration
    DBAdress = 'imlab-ws2.snu.ac.kr'
    DBName = 'ASRS_RL_DATA'
    DBID = 'ioasrs'
    DBPassward = '1wjdqhruddud'

    def __init__(self, table_idx):
        self.table_idx = table_idx


    def get_obs(self, no_obs):

        observations = deque()

        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        clm = 25
        flr = 20
        sht = 2
        ACTIONS_COUNT = 8

        sql = 'SELECT rs, act, inp, outp, reward, rsprime, terminal FROM dijk_23density limit ' + str(no_obs)
        cur.execute(sql)
        for i in range(cur.rowcount):
            row = cur.fetchone()

            last_state = map(int, row[0][1:-1].split(", "))
            last_action = np.zeros([ACTIONS_COUNT])
            last_action[row[1]] = 1
            input = map(int, row[2][1:-1].split(", "))
            output = map(int, row[3][1:-1].split(", "))
            rwd = - row[4] / reward.reward().get_maxtime(clm, flr, sht)
            current_state = map(int, row[5][1:-1].split(", "))
            if row[6] == 'O':
                terminal = True
            else:
                terminal = False

            foe = state.get_rack_full_or_empty(last_state)
            foe = self.change_to_two_dimension(foe, clm, flr)
            son_in = state.get_rack_same_or_not(last_state, input)
            son_out = state.get_rack_same_or_not(last_state, output)

            for i in range(len(son_in)):
                foe = np.append(foe, self.change_to_two_dimension(son_in[i], clm, flr), axis=2)
            for i in range(len(son_out)):
                foe = np.append(foe, self.change_to_two_dimension(son_out[i], clm, flr), axis=2)
            ls = foe[:,:,:]

            foe = state.get_rack_full_or_empty(current_state)
            foe = self.change_to_two_dimension(foe, clm, flr)
            son_in = state.get_rack_same_or_not(current_state, input)
            son_out = state.get_rack_same_or_not(current_state, output)

            for i in range(len(son_in)):
                foe = np.append(foe, self.change_to_two_dimension(son_in[i], clm, flr), axis=2)
            for i in range(len(son_out)):
                foe = np.append(foe, self.change_to_two_dimension(son_out[i], clm, flr), axis=2)
            cs = foe[:,:,:]

            observations.append((ls, last_action, rwd, cs, terminal))
        con.close()
        return observations


    def change_to_two_dimension(self, rack_status, columnNum, floorNum):
        leftrack = [[0.0 for flr in range(floorNum)] for clm in range(columnNum)]
        for clm in range(columnNum):
            for flr in range(floorNum):
                leftrack[clm][flr] = rack_status[clm * floorNum + flr]
        rightrack = [[0.0 for flr in range(floorNum)] for clm in range(columnNum)]
        for clm in range(columnNum):
            for flr in range(floorNum):
                rightrack[clm][flr] = rack_status[columnNum * floorNum + clm * floorNum + flr]

        result = np.append(np.reshape(np.array(leftrack), (columnNum, floorNum, 1)),
                           np.reshape(np.array(rightrack), (columnNum, floorNum, 1)), axis=2)
        return result


if __name__ == '__main__':
    obs = OBSfromDB(20)
    obs.get_obs(32)
