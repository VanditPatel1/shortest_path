import math
from get_curr import *

#Look-Up Table for Edge Weights
edges = get_data()

def create_shortest_path_table():

    global CURRENCIES
    distances = {}
    for curr in list(edges.index.values):
        distances[curr] = float("inf") #set all starting vertices to be infinite distance away
    return distances

def get_weight(currency):

    global edges
    return edges.get_value(currency, 'ask') #returns edge weights based on 'ask' price



#BELLMAN-FORD ALGORITHM
create_shortest_path_table()