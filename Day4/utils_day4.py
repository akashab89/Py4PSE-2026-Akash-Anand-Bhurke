import streamlit as st
import networkx as nx
import graphviz

#DEFINING THE GRAPHING FUNCTION
def convert_nx_to_gv_graph(nx_graph: nx.DiGraph):

    # if str(type(nx_graph)) == "<class 'networkx.classes.graph.Graph'>":
    #     gv_graph = graphviz.Graph()
    # else:
    #     gv_graph = graphviz.DiGraph()

    #GET NX NODES
    nx_nodes = nx_graph.nodes()
    nx_edges = nx_graph.edges()

    #CREATE EMPTY GV GRAPH
    gv_graph = graphviz.Digraph()

    #CONVERT NX-NODES TO GV NODES
    for node, attrs in nx_nodes(data=True):
        gv_graph.node(
            str(node),
            label= attrs.get("name", str(node)),
            penwidth="2")

    for source, target in nx_edges:
        gv_graph.edge(str(source), str(target))

    return gv_graph