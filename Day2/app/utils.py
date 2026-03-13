import streamlit as st
import networkx as nx
import graphviz

#DEFINING THE GRAPHING FUNCTION
def convert_nx_to_gv_graph(nx_graph: nx.DiGraph):
    #GET NX NODES
    nx_nodes = nx_graph.nodes()
    nx_edges = nx_graph.edges()

    #CREATE EMPTY GV GRAPH
    gv_graph = graphviz.Digraph()

    #CONVERT NX-NODES TO GV NODES
    for node in nx_nodes:
        node_color = nx_graph.nodes[node].get("color", 'lightgray')
        node_id = nx_graph.nodes[node].get("id")
        label = f"{node}\ncolor: {node_color}\nID: {node_id}"
        gv_graph.node(node, label=label, color=node_color, penwidth="2")

    for edge in nx_edges:
        edge_label = nx_graph.edges[edge].get("label")
        gv_graph.edge(edge[0], edge[1], label=edge_label)

    return gv_graph

#DEFINING THE 'LOADING DEMO CAR FUNCTION'
def load_demo_car():
    st.session_state.G.clear()

    st.session_state.G.add_node("LEGO car assembly", color="Red", id="1")
    st.session_state.G.add_node("Base/Chassis/Body Block", color="Blue", id="2")
    st.session_state.G.add_node("Load Block", color="Green", id="3")
    st.session_state.G.add_node("Windshield Block", color="Gray", id="4")
    st.session_state.G.add_node("Body Block", color="Blue", id="5")
    st.session_state.G.add_node("Axle", color="Yellow", id="6")
    st.session_state.G.add_node("Wheel Assembly", color="Green", id="7")
    st.session_state.G.add_node("Tire", color="Black", id="8")
    st.session_state.G.add_node("Rim", color="Red", id="9")


    st.session_state.G.add_edge("LEGO car assembly", "Base/Chassis/Body Block", label="consists of")
    st.session_state.G.add_edge("LEGO car assembly", "Load Block", label="consists of")
    st.session_state.G.add_edge("LEGO car assembly", "Windshield Block", label="consists of")
    st.session_state.G.add_edge("Base/Chassis/Body Block", "Body Block", label="consists of")
    st.session_state.G.add_edge("Base/Chassis/Body Block", "Axle", label="consists of")
    st.session_state.G.add_edge("Base/Chassis/Body Block", "Wheel Assembly", label="consists of")
    st.session_state.G.add_edge("Wheel Assembly", "Rim", label="consists of")
    st.session_state.G.add_edge("Wheel Assembly", "Tire", label="consists of")
