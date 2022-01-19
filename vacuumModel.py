import random
from os import remove

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import time
import datetime

start_time = time.time()
erasedElements = 0

#Esta variable es la que se cambia para aumentar o bajar el tiempo
maxTime = 10 #segundos

def getTime(model):

    return time.time()-start_time


class VacuumAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'vacuum'
        self.erasedElements = 0
        self.simulationOver = False

    def step(self):
        self.move()
        self.checkIfClean()

    def move(self):
       if self.simulationOver == False:
            possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True
            )
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)
       else:
           print("Simulation is over")
           print("Vacuums cleaned: ",erasedElements)

           pass


    def checkIfClean(self):
        pass



class trashAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'trash'

    def vacuumTouchedMe(self):
        global erasedElements
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if cellmate.type == 'vacuum':
                self.type = 'erased'








    def step(self):
        self.vacuumTouchedMe()

class vacuumModel(Model):

    def __init__(self, V, T, width, height):
        self.num_vacuum = V
        self.num_trash = T
        self.grid = MultiGrid(width, height, True)

        self.schedule = RandomActivation(self)
        self.running = True

        self.percentageDirty = ((width * height) * T)/100

        for i in range(self.num_vacuum):
            a = VacuumAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1,1))


        for i in range(int(self.percentageDirty)):
            a = trashAgent(i+V, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))


        self.datacollector = DataCollector(
            model_reporters={"Time": getTime},


        )

    def stop(self):
        count = 0
        for agent in self.schedule.agents:
            if agent.type == 'erased':
              count = count + 1
            if count == self.percentageDirty:
                print("Simulation Finished :  100% completed, No more trash to pick up"," Finished in: ", time.time() - start_time)
                self.running = False



    def timeStop(self):
        if ((time.time() - start_time) >= maxTime):
            self.getCleanedPercentage()
            self.running = False
            print("Simulation Finished: Ran out of time")

    def getCleanedPercentage(self):
        global erasedElements
        for agent in self.schedule.agents:
            if agent.type == 'erased':
                erasedElements = erasedElements + 1
                #print(self.num_trash, erasedElements)
        print("Total number of trash cleaned: ", ((erasedElements / self.num_trash) * 100), '%')



    def step(self):
        self.timeStop()
        self.stop()
        self.schedule.step()
        print(time.time() - start_time)

