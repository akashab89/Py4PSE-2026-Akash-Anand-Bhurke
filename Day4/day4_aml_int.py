import streamlit as st
import pandas as pd
import graphviz
import networkx as nx
import xml.etree.ElementTree as ET

from Day4.utils_day4 import convert_nx_to_gv_graph

def day4():
    #PAGE SETUP
    st.set_page_config(page_title="Day 4 AML Integration", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
    st.title("🤖 AML Integration in Python")
    st.subheader("AML Integration in Python using Streamlit")
    st.markdown("""
    Do the integration 
    """)
    st.write("Version 1: Reading data, visualising")

    #UPLOADING THE FILE
    #uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type=["csv", "xlsx"])
    with st.sidebar:
        st.header("Input Settings")

        uploaded_file = st.file_uploader("Upload Process File", type=["aml", "xml"], accept_multiple_files=False)

    if uploaded_file:
        st.success("Successfully uploaded the file.")
        # st.write(uploaded_file)
        # st.write(uploaded_file.getvalue())
        st.subheader("AML Integration")

        #PARSING THE FILE
        try:
            tree = ET.parse(uploaded_file)
            root = tree.getroot()

            st.success("File uploaded successfully.")
            # st.write("Root tag:", root.tag)

        except Exception as e:
            st.error(f"Error while parsing AML: {e}")
            with st.expander("Full error"):
                st.write(f"Error while parsing AML: {e}")

        #CLEARING THE NAMESPACE
        if "{" in root.tag:
            ns = root.tag.split("}")[0].strip("{")
            actual_tag = root.tag.split("}")[1]
            # st.write(ns)
            st.write("Root tag:", actual_tag)

            ns_dict = {"aml" : ns}
            ih = root.find(".//aml:InstanceHierarchy", ns_dict)
            st.write("Instance hierarchy:", ih)

            if ih is None:
                st.error("No InstanceHierarchy found in the AML file.")
                st.stop()

            #GETTING ELEMENTS
            element_list = []
            for ie in ih.findall("aml:InternalElement", ns_dict):
                st.write(ie)
                ie_name = ie.get("Name")
                ie_id = ie.get("ID")
                ie_class = ie.get("RefBaseSystemUnitPath")

                # for attr in ie.findall("aml:Attribute", ns_dict):
                #     attr_name = attr.get("Name")
                #     value_elem = attr.find("aml:Value", ns_dict)
                #     if value_elem is not None:
                #         attr_value = value_elem.text
                #         attribute_text = f"{attr_name}: {attr_value}"
                #     st.write("Attribute:", attribute_text)
                # full_label = f"{ie_name}\n{attribute_text}"
                st.write("Internal element name:", ie_name)
                element_list.append({"Name":ie_name,"ID":ie_id,"Class":ie_class})

            with st.expander("InternalElements"):
                st.write(element_list)

            #GETTING LINKS
            link_list = []
            for ie in ih.findall("aml:InternalElement", ns_dict):
                for il in ie.findall("aml:InternalLink", ns_dict):
                    il_name = il.get("Name")
                    il_source = il.get("RefPartnerSideA")
                    il_target = il.get("RefPartnerSideB")
                    st.write("InternalLink name:", il_name)
                    link_list.append({"Name": il_name, "Source": il_source, "Target": il_target})

            with st.expander("InternalLinks"):
                st.write(link_list)

            # MAPPING EXTERNAL INTERFACE ID TO ELEMENT
            ei_mapping_dict = {}
            for ie in ih.findall("aml:InternalElement", ns_dict):
                ie_id = ie.get("ID")
                for external_interface in ie.findall("aml:ExternalInterface", ns_dict):
                    ei_id = external_interface.get("ID")
                    ei_mapping_dict[ei_id] = ie_id

            with st.expander("ExternalInterface Owner mapping"):
                st.write(ei_mapping_dict)


            #CREATE GRAPH
            G = nx.DiGraph()

            #CREATE NX NODES
            for ie in element_list:
                G.add_node(ie["ID"], name=ie["Name"], suc=ie["Class"])

            # CREATE NX EDGES
            for il in link_list:
                actual_source = ei_mapping_dict[il["Source"]]
                actual_target = ei_mapping_dict[il["Target"]]
                G.add_edge(actual_source, actual_target, label=il["Name"])
            with st.expander("Graph Visualisation"):
                st.graphviz_chart(convert_nx_to_gv_graph(G))

    ##HW - ADD ATTRIBUTES AND COLORS TO THE NODES, ADD ATTRIBUTES TO THE EDGES

            st.divider()

            #GRAPH ANALYSIS
            st.subheader("Graph Analysis")
            with st.expander("Analysis of node and edge amount"):
                st.write(f"Analysis of node and edge amount")
                st.write(f"Number of nodes: {G.number_of_nodes()}")
                st.write(f"Number of edges: {G.number_of_edges()}")

            st.divider()
            with st.expander("Analysis of node and edge data"):
                st.write(f"Analysis of node and edge data")
                st.json(dict(G.nodes(data=True)))
                st.write(G.edges(data=True))

            st.divider()

            #NEIGHBOURHOOD ANALYSIS
            st.subheader("Neighbourhood Analysis")
            with st.expander("Undirected Graph"):
                G_undirected = G.to_undirected()
                for node in G_undirected.nodes():
                    st.write(f"Node: {node}")
                    st.write(list(G_undirected.neighbors(node)))
                st.graphviz_chart(convert_nx_to_gv_graph(G_undirected))


            with st.expander("Directed graph"):
                for node in G.nodes():
                    st.write(f"Node: {node}")
                    st.write(list(G.neighbors(node)))
                st.graphviz_chart(convert_nx_to_gv_graph(G))

            st.divider()

            #ISOLATED NODE
            isolated_nodes = nx.isolates(G)
            st.write(list(isolated_nodes))

            if list(isolated_nodes) != []:
                st.success("Everything is connected")
            else:
                isolated_nodes = nx.isolates(G) #DON'T KNOW WHY NEEDS TO BE REWRITED
                st.warning(f"There are isolated nodes: {list(isolated_nodes)}")
