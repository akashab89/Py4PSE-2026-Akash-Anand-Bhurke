import streamlit as st
import pandas as pd
import graphviz
import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path_length

from Day3.process_utils_addition import convert_nx_to_gv_graph, create_graph_from_list

def day3():
    #PAGE SETUP
    st.set_page_config(page_title="Day_3 Product", page_icon="📃", layout="wide", initial_sidebar_state="expanded")
    st.title("📃 Process Graph App")
    st.markdown("""
    Analyze manufacturing processes and compute **weighted shortest paths** between operations.
    """)
    st.write("Version 1: Reading data, visualising")

    #UPLOADING THE FILE
    #uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type=["csv", "xlsx"])
    with st.sidebar:
        st.header("Input Settings")

        uploaded_file = st.file_uploader("Upload Process File", type=["xlsx","csv"])
    if uploaded_file:
        st.success("Successfully uploaded the file.")
        st.subheader("List visualisation")
        with st.expander("Raw Data"):
            st.write(pd.read_excel(uploaded_file))
        process_df = pd.read_excel(
            uploaded_file,
            header=3)
        with st.expander("Modified Data"):
            st.write(process_df)

        with st.expander("Cleaned Data"):
            st.dataframe(process_df)

        st.divider()

        #GENERATING GRAPHS
        st.subheader("Process Graph Visualisation")
        process_graph = nx.DiGraph()

        #GENERATING NODES
        for _, row in process_df.iterrows():
            process_id = row["Process"]
            if process_id == "_":
                continue
            label = f"{process_id}\nType: \[{row['ManufacturingTime']}\]"
            process_graph.add_node(process_id, label=label)
            # st.write(process_id)

        #GENERATING EDGES
        for _, row in process_df.iterrows():
            source_node = row["Process"]
            target_node = row["Successor"]
            weight = row["ManufacturingTime"]

            if target_node != "_":
                process_graph.add_edge(source_node, target_node, weight=weight)
            # process_graph.edge(source_node, target_node)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Process Graph")
            st.graphviz_chart(convert_nx_to_gv_graph(process_graph))

        st.divider()

        #SHORTEST PATH CALCULATION - WITH EDGE WEIGHTS

        process_list = process_df["Process"].to_list()
        with st.sidebar:
            st.subheader("Shortest Path Calculation without edge weights")
            start_node = st.selectbox("Select Start Node", process_list)
            end_node = st.selectbox("Select End Node", process_list)

            if st.button("Compute Shortest Path", width="stretch"):
                shortest_path_list = nx.shortest_path(
                    process_graph,
                    source=start_node,
                    target=end_node,
                    weight="weight"
                )
                path_length = nx.shortest_path_length(
                    process_graph,
                    source=start_node,
                    target=end_node,
                    weight="weight"
                )


                graph = create_graph_from_list(shortest_path_list, process_graph)

                with col2:
                    st.subheader("Shortest Path Result")
                    st.write("Shortest Path:", shortest_path_list)
                    st.write("Shortest Time:", path_length)
                    st.graphviz_chart(convert_nx_to_gv_graph(graph), width="content")

                    st.success("Shortest path calculated successfully")

                    st.info(f"Start: {start_node} → End: {end_node}")

                    st.metric("Total Manufacturing Time", path_length)

    if st.sidebar.button("Reset"):
        st.session_state.clear()
        st.rerun()
