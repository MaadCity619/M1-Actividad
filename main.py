from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from vacuumModel import vacuumModel

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 1
    }

    if agent.type == 'vacuum':
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 3

    elif agent.type == 'trash':
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2


    elif agent.type == 'erased':
        portrayal["Color"] = "white"
        portrayal["Layer"] = 1

    return portrayal

grid = CanvasGrid(
    agent_portrayal,
    5,#grid x
    5,#grid y
    500,#pixeles x
    500,#pixeles y
)

chart = ChartModule([{
    'Label': 'Time',
    'Color':'Black'
}],
data_collector_name='datacollector')

server = ModularServer(
    vacuumModel,
    [grid, chart],
    "Vacuum Model",
    {"V":1,"T":20,"width":5, "height":5} # El tamaño tiene que se igual a los valores arriba
    #numero de aspiradoras, porcentaje de cuadros con basura, ancho y altura
)
server.port = 8521
server.launch()