import streamlit as st
import networkx as nx
import graphviz
from fontTools.varLib.avar.plan import WEIGHTS


#DEFINING THE GRAPHING FUNCTION
def convert_nx_to_gv_graph(nx_graph: nx.DiGraph):
    # CREATE EMPTY GV GRAPH
    gv_graph = graphviz.Digraph(
        graph_attr={"rankdir": "LR"},
        node_attr={"shape": "box", "style": "rounded,filled", "fillcolor": "lightblue"},
        edge_attr={"fontsize": "10"}
    )

    #GET NX NODES AND EDGES
    nx_nodes = nx_graph.nodes()
    nx_edges = nx_graph.edges(data=True)

    #CONVERT NX-NODES TO GV NODES
    for node in nx_nodes:
        gv_graph.node(node, label=str(node), penwidth="2")

    for u, v, data in nx_edges:
        weight = data.get("weight", "")
        gv_graph.edge(str(u), str(v), label=str(weight))

    return gv_graph

def create_graph_from_list(path_list, original_graph):
    path_graph = nx.DiGraph()
    for i in range(len(path_list)-1):
        source_node = path_list[i]
        target_node = path_list[i + 1]

        weight = original_graph[source_node][target_node]["weight"]
        path_graph.add_edge(source_node, target_node, weight=weight)
    return path_graph
# def create_graph_from_list(path_list):
#     path_graph = nx.DiGraph()
#     for i in range(len(path_list)):
#         path_graph.add_node(path_list[i])
#
#     for i in range(len(path_list) - 1):
#         source_node = path_list[i]
#         end_node = path_list[i + 1]
#         weight = path_list["ManufacturingTime"]
#         path_graph.add_edge(source_node, end_node)
#     return path_graph