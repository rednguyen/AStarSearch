from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush
import math

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "ucs":
            self.frontier = [(0, self.grid.start)]
            heapify(self.frontier)
            self.temp = []
            self.checked = []
            self.explored = []
        elif self.type == "astar":
            self.frontier = [(0, 0, self.grid.start)]
            #heapify(self.frontier)
            self.temp = []
            self.checked = []
            self.explored = []
        


    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    #DFS: BUGGY, fix it first
    def dfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        
        current = self.frontier.pop()

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        self.explored.append(current)

        for n in children:
            if n in self.explored or n in self.frontier:
                continue
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    self.previous[n] = current
                    if n == self.grid.goal:
                        self.finished = True
                    else:
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True
                        
                            
    
    #Implement BFS here (Don't forget implement initialization at line 23)
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        current = self.frontier.pop(0)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n in self.explored or n in self.frontier:
                continue
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    self.previous[n] = current
                    if n == self.grid.goal:
                        self.finished = True
                    else:
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True
                    
        #Implement UCS here (Don't forget implement initialization at line 23)
    
    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        current = heappop(self.frontier)
        self.grid.nodes[current[1]].color_checked = True
        self.grid.nodes[current[1]].color_frontier = False
        
        self.checked.append(current)
        self.explored.append(current[1])
        value = self.checked.pop()[0]
        if current[1] == self.grid.goal:
            self.finished = True
            return

        children = [(current[1][0]+a[0], current[1][1]+a[1]) for a in ACTIONS]

        for n in children:

            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if n in self.explored or n in self.temp:
                    continue
                if not self.grid.nodes[n].puddle:
                    self.previous[n] = current[1]
                    heappush(self.frontier, (self.grid.nodes[n].cost()+value,n))
                    self.temp.append(n)
                    self.grid.nodes[n].color_frontier = True

                        

    #Implement Astar here (Don't forget implement initialization at line 23)
    def astar_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        #current = heappop(self.frontier)
        f,g,current = heappop(self.frontier)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        
        #self.checked.append(current)
        #self.explored.append(current[1])
        self.explored.append(current)

#current h-cost and F-cost
        #parent_H = abs(current[1][0] - self.grid.goal[0]) + abs(current[1][1] - self.grid.goal[1])
        #parent_F = current[0]
        #parent_G = parent_F - parent_H
            
        #value = self.checked.pop()[0]
        if current == self.grid.goal:
            self.finished = True
            return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                new_h = math.sqrt((n[0]-self.grid.goal[0])**2 + (n[1]-self.grid.goal[1])**2)
                new_g =  self.grid.nodes[n].cost() + g
                new_f = new_h + new_g
                new_child = (new_f, new_g, n)
                for k in self.frontier:
                    if k[2] == n and k[1] > new_g:
                        self.previous[n] = current
                        heappush(self.frontier, new_child)
                        return


                if n in self.explored or n in self.temp:
                    continue
               
                #h = abs(n[0] - self.grid.goal[0]) + abs(n[1] - self.grid.goal[1])
                #new_cost = parent_G + self.grid.nodes[n].cost() + h # new F cost

                if not self.grid.nodes[n].puddle:
                    self.previous[n] = current
                    heappush(self.frontier, new_child)
                    self.temp.append(n)
                    self.grid.nodes[n].color_frontier = True

        
                





        


