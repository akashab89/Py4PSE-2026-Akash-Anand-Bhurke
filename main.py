import streamlit as st

def day1():
    st.set_page_config(page_title="Production Planner", page_icon="🏭", layout="wide")

    st.title("""🏭 Production Planner""")
    st.info("App for building Production Planning")

    ##SIDEBAR
    st.sidebar.header("Production Settings")
    product_name = st.sidebar.text_input("Product Name")
    quantity = st.sidebar.number_input("Production Quantity", value=1, min_value=0, max_value=100, step=1)

    ##LIST GENERATION IN BACKEND SESSION STATE
    if "box_with_cars_list" not in st.session_state:
        st.session_state.box_with_cars_list = [] #Creation of 'Box with cars - list'

    #MAIN DATA ENTRY
    product_name = st.text_input("Customer Name")
    #st.info(type(product_name))

    #quantity = st.number_input("Production Quantity", min_value=1, max_value=100, step=1)
    #st.info(type(quantity))
    #st.write(quantity)

    in_house = st.checkbox("Produced In-house")
    #st.info(type(in_house))
    #st.write(in_house)

    employee_list = ["Akash", "Abdul", "Aryan", "Kishor"]
    #st.info(type(employee_list))
    st.write(employee_list)

    st.selectbox("Select an employee", employee_list)

    st.divider()

    #COST CALCULATION
    st.header("Cost Calculation")

    col1, col2, col3 = st.columns(3)

    with col1:
        material_cost = st.number_input("Material Cost per unit (€)", value=10, icon="🏭")
    # st.write(material_cost)
    with col2:
        labor_cost = st.number_input("Labor Cost per unit (€)", value=15, disabled= True, icon="👷")
    # st.write(labor_cost)
    with col3:
        machine_cost = st.number_input("Machine Cost per unit (€)", value=5, icon="🎰")
    # st.write(machine_cost)

    cost_list = [material_cost, labor_cost, machine_cost]
    st.write(cost_list)

    unit_cost = material_cost + labor_cost + machine_cost #unit cost
    total_cost = unit_cost * quantity #Total cost
    # st.write("Unit Cost:" + str(unit_cost))
    # st.write("Total Cost:" + str(total_cost))
    st.metric("Unit Cost", unit_cost)
    st.metric("Total Cost", total_cost)

    st.divider()

    #PANDAS VISUALISATION
    st.header("Pandas visualization")

    cost_dict = {
        "Cost Type": ["Material", "Labor", "Machine"],
        "Cost per unit": [material_cost, labor_cost, machine_cost]
    }

    st.info(type(cost_dict))
    st.write(cost_dict)
    # st.json(cost_dict) #similar to st.write but of type json VV IMP


    #DATAFRAME
    import pandas as pd
    cost_table = pd.DataFrame.from_dict(cost_dict)

    st.dataframe(cost_table)

    #PLOTTING
    st.bar_chart(cost_table.set_index("Cost Type"))

    st.divider()

    #BUTTON
    if st.button("Press me", width="stretch"):
        st.session_state.box_with_cars_list.append(product_name)

    st.write(st.session_state.box_with_cars_list)

    #name and cost of the cars in the append - Refer HW-Day1.py
    #mapping of list/dict can look like

