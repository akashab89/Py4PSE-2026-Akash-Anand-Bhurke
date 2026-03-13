import streamlit as st
from streamlit_option_menu import option_menu
from main import day1
from Day2.app.day2_product_graph import day2
from Day3.day3_process_graph_addition import day3
from Day4.day4_aml_int import day4
st.title("AutomationML Analysis")
selected = option_menu(
    "Navigation",
    ["Day 1", "Day 2", "Day 3", "Day 4"],
    orientation="horizontal",
    styles= {"container": {"padding": "0!important", "background-color": "#fafafb"},
             "icon": {"color": "red", "font-size": "20px"},
             "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#efe"},
             "nav-link-selected": {"background-color": "green"}})

if selected == "Day 1":
    st.write("This is Day 1 content")
    day1()

elif selected == "Day 2":
    st.write("This is Day2 content")
    day2()
elif selected == "Day 3":
    st.write("This is Day_3 content")
    day3()
else:
    st.write("This is Day 4 content")
    day4()


