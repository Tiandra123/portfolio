# crypto currency arbitrage

# import libraries

import networkx as nx
from networkx import Graph
import json
import requests as req
import matplotlib.pyplot as plt #might not need this

# functions
def API_call(url):
  request = req.get(url)
  data = json.loads(request.text)
  return data

def add_to_graph(id_list, vs_currencies_list, data): # add data from other function
  for currency in id_list:
    if currency == 'ripple':
      node1 = 'xrp'
    elif currency == 'cardano':
      node1 = 'ada'
    elif currency == 'bitcoin-cash':
      node1 = 'bch'
    elif currency == 'eos':
      node1 = 'eos'
    elif currency == 'litecoin':
      node1 = 'ltc'
    elif currency == 'ethereum':
      node1 = 'eth'
    elif currency == 'bitcoin':
      node1 = 'btc'
    for node2 in vs_currencies_list:
      try:
        g.add_weighted_edges_from([(node1, node2, data[currency][node2])])
        # print(node1, node2, data[currency][node2])
      except: 
        KeyError
        # print("KeyError")
  return
  
def calc_edge_weights(path, g): # all nodes in the path and the graph to get edge weights from it
  edgewght = 1
  for i in range(len(path)-1): # need to iterate through the index length of path to pull pairs
    ndto = path[i]
    ndfrom = path[i+1]
    edgewght *= g[ndto][ndfrom]['weight']
    # print(edgewght)
  return edgewght


# variables
id = ['ripple', 'cardano', 'bitcoin-cash' , 'eos', 'litecoin', 'ethereum', 'bitcoin']
vs_currencies =['eth', 'btc', 'ltc', 'xrp', 'eos', 'ada', 'bch' ] #tickers
g = nx.DiGraph()

API_url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin,litecoin,ripple,cardano,bitcoin-cash,eos&vs_currencies=eth,btc,ltc,xrp,ada,bch,eos'

nodes = g.nodes()

greatest_path = []
greatest_path_weight = 0

smallest_path = []
smallest_path_weight = 0

# Logic
data = API_call(API_url)
add_to_graph(id, vs_currencies, data)

# Check to see if it worked
# print("Number of nodes:", g.number_of_nodes())
# print("Number of edges:", g.number_of_edges())
# print("Nodes:", list(g.nodes()))

nodes = g.nodes()

# Traverse Graph

for nd1 in nodes:
  for nd2 in nodes:
    if nd1 !=nd2: # check to make sure you aren't looking at same node for nd1 and 2

      # output p1 
      print("\n", "Paths from", nd1, "to", nd2, "-------------------------", "\n")  

      # forward path
      to_from = list(nx.all_simple_paths(g, nd1, nd2)) # convert to list or calc func won't work
      for i in to_from:
        forward = calc_edge_weights(i, g)
        print(i, forward)

        # reverse the string and calc again NOTE: add try and except bc reverse might not be legit 
        try:
          reverse = calc_edge_weights(i[::-1], g) # reverse path
          print(i[::-1], reverse)

 
        # disequilibrium? add inside reverse try logic bc only want to do if reverse path be legit 
          x = forward * reverse
          print("\n", x)

            # output p2
          if x > 1:
            if x > greatest_path_weight:
              greatest_path_weight = x
              greatest_path = i, i[::-1] # pulling single path list from list of lists 
              # print("Arbitrage!! GAIN", forward * reverse)
          if x < 1:
            if smallest_path_weight == 0: # first smallest path check // add to 0 or it stays zero forever
              smallest_path_weight = x
              smallest_path = i[::-1], i
            if x < smallest_path_weight:
              smallest_path_weight = x
              smallest_path = i[::-1], i
              # print("Arbitrage!! LOSS", forward * reverse)


        except:
          print("skipping - reverse path is not legit", "\n")
          continue # skip if not legit
      

print("\n", "Smallest Paths Weight Factor: ", smallest_path_weight)
print("Paths: ", smallest_path)

print("\n", "Greatest Paths Weight Factor: ", greatest_path_weight)
print("Paths: ", greatest_path)

      
