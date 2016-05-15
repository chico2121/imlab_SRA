from problemIO import problemreader
import networkx as nx
import math
import solution
import matplotlib.pyplot as plt

class action(object):

    yspeed = 2.5
    zspeed = 0.6666667

    def loca_calculate(self,index,size_h,size_v):

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

    def get_time(self, start, end):

        return max(abs((start[1] - end[1]) / self.yspeed), abs((start[2] - end[2]) / self.zspeed))

    def adjust_rs(self, rs1):
        rs1 = rs1.replace(" ", "")
        rs1 = rs1.split(",")

        return rs1

    def adjust_list(self, lst):
        for i,j in enumerate(lst):
            for k in range(len(j)):
                lst[i][k] = int(lst[i][k])
        return lst

    def print_dijk(self,G): # G = nx.graph()
        path = nx.dijkstra_path(G,'start','end')
        sol_of_loca = path[1][:-3] + "/" + path[2][:-3] + "/" \
                      + path[3][:-3] + "/" + path[4][:-3]
        sol_of_loca = sol_of_loca.replace("[","")
        sol_of_loca = sol_of_loca.replace("]","")
        sol_of_loca = sol_of_loca.replace(" ","")
        list_sol_of_loca = sol_of_loca.split("/")
        list_sol_of_loca = [x.split(',') for x in list_sol_of_loca]
        list_sol_of_loca = self.adjust_list(list_sol_of_loca)
        return list_sol_of_loca


    def dijk_ssr1r2(self, rs, column, floor, outputs):# ex :outputs = [10,18]
        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca,loca1))

                # create second 'S'
        for b, item2 in enumerate(rack):
            if item2 == -1:
                loca2 = self.loca_calculate(b, size_h, size_v)
                G.add_node('%s_s2' % loca2, loca=loca2, phase=2)
                #G.add_edge('%s_s1' % loca1, '%s_s2' % loca2, weight=self.get_time(loca1, loca2))

        # create 'R1R2'
        for c, item3 in enumerate(rack):
            loca3 = self.loca_calculate(c, size_h, size_v)
            if item3 == outputs[0]:
                G.add_node('%s_r1' % loca3, loca=loca3, phase=3)
                #G.add_edge('%s_s2' % loca2, '%s_r1' % loca3, weight=self.get_time(loca2, loca3))

        for d, item4 in enumerate(rack):
            loca4 = self.loca_calculate(d, size_h, size_v)
            if item4 == outputs[1]:
                G.add_node('%s_r2' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))
                #G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 2:
                    G.add_edge(a,b, weight=self.get_time(data1,data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 2 and data4 == 3:
                    G.add_edge(a,b, weight=self.get_time(data1,data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 3 and data4 == 4:
                    G.add_edge(a,b, weight=self.get_time(data1,data3))

        # remove edges weighted 0

        for n, nbrs in G.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['weight']
                if int(data) == 0:
                    G.remove_edge('%s' % n, '%s' % nbr)

        #print G.node
        #print G.edge

        #print 'end'

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S', 'S', 'R', 'R']
        #nx.draw_networkx(G ,arrows=True,with_labels=True)
        #plt.show()
        return 'SSR1R2', path, length, self.print_dijk(G), io

    def dijk_ssr2r1(self, rs, column, floor, outputs):  # ex :outputs = [10,18]
        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

                # create second 'S'
        for b, item2 in enumerate(rack):
            if item2 == -1:
                loca2 = self.loca_calculate(b, size_h, size_v)
                G.add_node('%s_s2' % loca2, loca=loca2, phase=2)
                # G.add_edge('%s_s1' % loca1, '%s_s2' % loca2, weight=self.get_time(loca1, loca2))

        # create 'R2R1'
        for c, item3 in enumerate(rack):
            loca3 = self.loca_calculate(c, size_h, size_v)
            if item3 == outputs[1]:
                G.add_node('%s_r2' % loca3, loca=loca3, phase=3)
                # G.add_edge('%s_s2' % loca2, '%s_r1' % loca3, weight=self.get_time(loca2, loca3))

        for d, item4 in enumerate(rack):
            loca4 = self.loca_calculate(d, size_h, size_v)
            if item4 == outputs[0]:
                G.add_node('%s_r1' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r1' % loca4, 'end', weight=self.get_time(loca4, end_loca))
                # G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 2:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 2 and data4 == 3:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 3 and data4 == 4:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        # remove edges weighted 0

        for n, nbrs in G.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['weight']
                if data == 0.0:
                    G.remove_edge('%s' % n, '%s' % nbr)

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io= ['S', 'S', 'R', 'R']
        # nx.draw_networkx(G ,arrows=True,with_labels=True)
        # plt.show()
        return 'SSR2R1', path, length, self.print_dijk(G), io

    def dijk_sr1sr2(self, rs, column, floor, outputs): # ex :outputs = ['10','18']
        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # create r1
        for b, item2 in enumerate(rack):
            loca2 = self.loca_calculate(b,size_h, size_v)
            if item2 == outputs[0]:
                G.add_node('%s_r1' % loca2, loca=loca2, phase=2)

                # create s2
                for c, item3 in enumerate(rack):
                    loca3 = self.loca_calculate(c, size_h, size_v)
                    if loca3[0] != loca2[0] and item3 == -1 and loca3[0:2] == loca2[0:2]:
                        G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                        G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                    elif loca3 == loca2:
                        G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                        G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

        """# create s2
        loca3 = self.loca_calculate(b,size_h, size_v)
        for c, item3 in enumerate(rack):
            # check the opposite side is empty
            loca5 = self.loca_calculate(c,size_h, size_v)
            if c != b and loca5[0] == -1 and loca3[1] == loca5[1] and loca3[2] == loca5[2]:
                loca3 = loca5
                G.add_node('%s_s2' % loca3, loca=loca3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
            else:
                G.add_node('%s_s2' % loca3, loca=loca3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))"""

        # create r2
        for d, item4 in enumerate(rack):
            if item4 == outputs[1]:
                loca4 = self.loca_calculate(d, size_h, size_v)
                G.add_node('%s_r2' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 2:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 3 and data4 == 4:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S', 'R', 'S', 'R']
        # nx.draw_networkx(G, arrows=True, with_labels=True)
        # plt.show()
        # print 'SR1SR2', path['start']['end'], length['start']['end']
        return 'SR1SR2', path, length, self.print_dijk(G),io

    def dijk_sr2sr1(self, rs, column, floor, outputs):# ex :outputs = [10,18]
        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # create r2
        for b, item2 in enumerate(rack):
            loca2 = self.loca_calculate(b, size_h, size_v)
            if item2 == outputs[1]:
                G.add_node('%s_r2' % loca2, loca=loca2, phase=2)

                # create s2
                for c, item3 in enumerate(rack):
                    loca3 = self.loca_calculate(c, size_h, size_v)
                    if loca3[0] != loca2[0] and item3 == -1 and loca3[0:2] == loca2[0:2]:
                        G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                        G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                    elif loca3 == loca2:
                        G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                        G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

        """# create s2
        loca3 = self.loca_calculate(b,size_h, size_v)
        for c, item3 in enumerate(rack):
            # check the opposite side is empty
            loca5 = self.loca_calculate(c,size_h, size_v)
            if c != b and loca5[0] == -1 and loca3[1] == loca5[1] and loca3[2] == loca5[2]:
                loca3 = loca5
                G.add_node('%s_s2' % loca3, loca=loca3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
            else:
                G.add_node('%s_s2' % loca3, loca=loca3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))"""

        # create r1
        for d, item4 in enumerate(rack):
            if item4 == outputs[0]:
                loca4 = self.loca_calculate(d, size_h, size_v)
                G.add_node('%s_r1' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r1' % loca4, 'end', weight=self.get_time(loca4, end_loca))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 2:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 3 and data4 == 4:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S','R','S','R']
        # nx.draw_networkx(G, arrows=True, with_labels=True)
        # plt.show()
        # print 'SR2SR1', path['start']['end'], length['start']['end']
        return 'SR2SR1', path, length, self.print_dijk(G), io

    def dijk(self,rs,column,floor,input,output): # concatenate 4 solutions // input/output example : [51,1] = 1 cycle outputs

        a1,b1,c1,d1,e1 = self.dijk_ssr1r2(rs,column,floor,output)
        a2,b2,c2,d2,e2 = self.dijk_ssr2r1(rs,column,floor,output)
        a3,b3,c3,d3,e3 = self.dijk_sr1sr2(rs,column,floor,output)
        a4,b4,c4,d4,e4 = self.dijk_sr2sr1(rs,column,floor,output)
        io = input + output

        if min(c1,c2,c3,c4) == c1:
            io = [io[0],io[1],io[2],io[3]]
            sol = solution.solution(d1,io,e1)
            cycletime = c1
            return sol, cycletime
        elif min(c1,c2,c3,c4) == c2:
            io = [io[0],io[1],io[3],io[2]]
            sol = solution.solution(d2,io,e2)
            cycletime = c2
            return sol, cycletime
        elif min(c1,c2,c3,c4) == c3:
            io = [io[0],io[2],io[1],io[3]]
            sol = solution.solution(d3,io,e3)
            cycletime = c3
            return sol, cycletime
        elif min(c1,c2,c3,c4) == c4:
            io = [io[0],io[3],io[1],io[2]]
            sol = solution.solution(d4,io,e4)
            cycletime = c4
            return sol, cycletime


        #print action.dijk_ssr1r2(rs,size_h, size_v, output)
        #print action.dijk_ssr2r1(rs,size_h, size_v, output)
        #print action.dijk_sr1sr2(rs,size_h, size_v, output)
        #print action.dijk_sr2sr1(rs,size_h, size_v, output)

    def dijk_idx(self, rs, column, floor, input, output, idx):

        io = input + output

        if idx == 0:
            a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs,column,floor,output)
            io = [io[0],io[1],io[2],io[3]]
            sol = solution.solution(d1,io,e1)
            cycletime = c1
            return sol, cycletime

        elif idx == 1:
            a2, b2, c2, d2, e2 = self.dijk_ssr2r1(rs,column,floor,output)
            io = [io[0],io[1],io[3],io[2]]
            sol = solution.solution(d2,io,e2)
            cycletime = c2
            return sol, cycletime

        elif idx == 2:
            a3, b3, c3, d3, e3 = self.dijk_sr1sr2(rs,column,floor,output)
            io = [io[0],io[2],io[1],io[3]]
            sol = solution.solution(d3,io,e3)
            cycletime = c3
            return sol, cycletime

        elif idx == 3:
            a4, b4, c4, d4, e4 = self.dijk_sr2sr1(rs,column,floor,output)
            io = [io[0],io[3],io[1],io[2]]
            sol = solution.solution(d4,io,e4)
            cycletime = c4
            return sol, cycletime

    def dijk_all(self, rs, column, floor, input, output):
            return self.dijk_idx(rs,column,floor,input,output,0), self.dijk_idx(rs,column,floor,input,output,1), \
                   self.dijk_idx(rs,column,floor,input,output,2), self.dijk_idx(rs,column,floor,input,output,3),



if __name__ == '__main__':
    test = problemreader.ProblemReader(10)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor

    ts = action()
    print rs
    a,b = ts.dijk(rs,column,floor,[123,456],[84,753])


    print a.loc,a.oper,a.type
    for i in range(len(rs)):
        for j in range(len(a.type)):
            if rs[i] == a.type[j] and a.oper[j] == 'R':
                print ts.loca_calculate(i,column,floor), a.type[j]


