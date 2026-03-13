import streamlit as st
import networkx as nx

def day2():
    #FUNCTION FOR VISUALISATION
    from Day2.app.utils import convert_nx_to_gv_graph
    from Day2.app.utils import load_demo_car

    #PAGE SETUP
    st.set_page_config(page_title="Day 1 Product", page_icon="🚗", layout="wide", initial_sidebar_state="expanded")
    st.title("🚗 LEGO car BOM builder")
    st.write("Version 1: create parts, connect them as a BOM, and view the graph.")

    #SIDEBAR
    st.sidebar.header("Visualisation Settings")
    if st.sidebar.button("Load Demo Car", width="stretch"):
        load_demo_car()
        st.sidebar.write("Demo car loaded")
    with st.sidebar:
        st.divider()
    if st.sidebar.button("Clear all inputs", width="stretch"):
        st.session_state.G.clear()
        st.sidebar.write("Cleared all inputs")

    #SESSION STATE
    if "G" not in st.session_state:
        st.session_state.G = nx.DiGraph()

    #CHECKING
    #st.write(st.session_state.G)
    #st.info(type(st.session_state.G))

    #TAB CREATION
    tab1, tab2, tab3 = st.tabs(["Create Nodes", "Create Edges", "Create Graph"])

    #CREATING NODES
    with tab1:
        st.write("Tab for creating nodes")

        #ADDING NODE FORM
        with st.form("Add Product Form"):
            st.write("Add a new part to graph")
            node_name = st.text_input("Specify node name")
            part_id = st.number_input("Specify node ID", min_value=1, max_value=100, step=1)
            #slider_val = st.slider("Form slider")
            #checkbox_val = st.checkbox("Form checkbox")

            color = st.selectbox("Select color", ["Red", "Green", "Blue", "Yellow", "Black", "White", "Brown", "Purple", "Gray"])

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit", width="stretch")
            if submitted:
                st.session_state.G.add_node(node_name, color=color, id=part_id)
                #st.success("Node " + node_name + " added to graph")
                st.success(f"Node \"{node_name}\" with color \"{color}\" added to the graph.")

        st.write(st.session_state.G.nodes(data=True))
        ##GOING INTO THE DICTIONARY TO ACCESS DATA
        for node in st.session_state.G.nodes(data=True):
            st.write(f"Name: {node[0]}, Color: {node[1]['color']}, ID: {node[1]['id']}")

    #CREATING EDGES
    with tab2:
        st.write("Tab for creating edges")

        #ADDING EDGE FORM
        with st.form("Add Edge Form"):
            edge_label = st.text_input("Specify edge label")
            source_edge = st.selectbox("Select source node", st.session_state.G.nodes())
            destination_edge = st.selectbox("Select destination node", st.session_state.G.nodes())

            submitted = st.form_submit_button("Submit", width="stretch")
            if submitted:
                st.session_state.G.add_edge(source_edge, destination_edge, label=edge_label)
                # st.success("Node " + node_name + " added to graph")
                st.success(f"Edge \"{edge_label}\" from {source_edge} to {destination_edge}.")
        st.write(st.session_state.G.edges(data=True))
        for edge in st.session_state.G.edges():
            st.write(edge)
            source = edge[0]
            target = edge[1]

            st.write(f"source is {source}")
            st.write(f"target is {target}")


    #CREATING GRAPHICAL VISUALISATION
    with tab3:
        st.write("Tab for viewing graph")
        st.write(st.session_state.G)
        # st.info(type(st.session_state.G))

        #CALLING THE FUNCTION
        gv_graph = convert_nx_to_gv_graph(st.session_state.G)

        #VISUALISE GV NODES
        st.graphviz_chart(gv_graph)


    ##HW - COLORS REPRESENTED IN NODES - ✅
    ##HW - ADD SIDEBAR ✅, LOAD DEMO CAR ENTIRELY - DUMP IN SINGLE FUNCTION ✅, RESET THE GRAPH(DELETE ALL INPUTS) - RESETTING TO TOP ✅