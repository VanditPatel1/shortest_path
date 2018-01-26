import math
from get_curr_new import *

def create_distance_table(curr):

    distances = {}
    for currency in curr:
        distances[currency] = float('inf')                  # set all starting vertices to be infinite distance away
    # for x in distances:
    #     print (x, distances[x])
    return distances

def create_predecessor_table(curr):

    predecessor = {}
    for currency in curr:
        predecessor[currency] = None                        #set all starting vertices to have no predecessor
    # for x in predecessor:
    #     print (x, predecessor[x])
    return predecessor

def show_negative_weight_cycle(predecessors, node):

    arbitrage = [node]                                      # temp list used to display currencies with arbitrage opportunities
    next_node = predecessors[node]

    while next_node not in arbitrage:
        arbitrage.append(next_node)
        next_node = predecessors[next_node]

    arbitrage.append(next_node)
    arbitrage = arbitrage[arbitrage.index(next_node):]
    return arbitrage


############################################        WEIGHTED GRAPH      ############################################

class weighted_graph:

    def __init__(self, currs):

        self.currencies = currs                                         # list of currencies
        self.curr_df, self.curr_matrix = get_data(currs)                # currency data frame (with listings of all edges)
        print (self.curr_df)
        print ('------------')
        print (self.curr_matrix)

    def get_weight(self, edge):

        edge_rate = self.curr_df.get_value(edge, 'edge_weight')         # edge weights based on NEGATIVE LOG-EXCHANGE RATE
        return edge_rate

    def bellmanford(self, start):

        updated = True                                                  # keeps track of whether an update was made or not
        iteration = 1                                                   # keeps track of the iteration number
        num_currencies = len(self.currencies)                           # number of currencies
        currency_list = self.currencies                                 # temp list to store currencies

        dist_table = create_distance_table(currency_list)               # shortest path table
        dist_table[start] = 0                                           # set up start node
        pre_table = create_predecessor_table(currency_list)             # predecessor table

        # FIRST |V-1| ITERATIONS
        while iteration < num_currencies and updated == True:
            updated = False                                             # reset updated for checking if an update occurs later
            for from_curr in currency_list:                             # First Loop for each currency
                for to_curr in currency_list:                           # Second Loop for each currency that

                        if dist_table[from_curr] + self.get_weight(from_curr + to_curr) < dist_table[to_curr]:              # if a shorter path is found to THIS node
                            dist_table[to_curr] = dist_table[from_curr] + self.get_weight(from_curr + to_curr)              # update distance table with shorter path distance
                            pre_table[to_curr] = from_curr                                                                  # update predecessor table with shorter path node
                            updated = True                                                                                  # an update occurred so updated = True

            iteration = iteration + 1

        # FINAL ITERATION to detect NEGATIVE WEIGHT CYCLES
        if updated == True:
            for from_curr in currency_list:                           # First Loop for each currency
                for to_curr in currency_list:                         # Second Loop for each currency that

                        if dist_table[from_curr] + self.get_weight(from_curr + to_curr) < dist_table[to_curr]:    # negative cycle detected
                            # Display the arbitrage opportunity using the predecessors table
                            return show_negative_weight_cycle(pre_table, to_curr)

        # No negative cycles detected
        return None

    def show_arbitrage_opportunities(self):

        arbitrage_opportunities = []
        for curr in self.currencies:
            arbitrage = self.bellmanford(curr)
            if arbitrage is not None and arbitrage not in arbitrage_opportunities:
                arbitrage_opportunities.append(arbitrage)

        print ("ARBITRAGE: " + str(arbitrage_opportunities))
        return arbitrage_opportunities






test = weighted_graph(['USD', 'CAD', 'GBP', 'JPY', 'AUD'])
arb = test.show_arbitrage_opportunities()
