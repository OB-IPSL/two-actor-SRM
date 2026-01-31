import streamlit as st
import test2
from test2 import generate_P, run_model, plot1, plot2, plot3, plot4, plot5, plot6
import base64

# Function to add background image from a local file
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read())  # Encode image file to base64

    # Inject CSS to set background image using base64 encoded string
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call function to set background image
add_bg_from_local('/Users/krishthe1nonly/Downloads/firewatch-3840x2160-6962.jpg')

# Define page states
PAGES = {
    "Home": "home",
    "Second Page": "second_page",
    "Third Page": "third_page",
    "Fourth Page": "fourth_page",
    "Fifth Page": "fifth_page",
    "Sixth Page": "sixth_page",
    "Next": "next_button",
    "Back": "back_button"
}

# Main function to manage the page states and display content
def main():
    st.title("Welcome to The Climate Model!")

    # Use columns to organize layout
    col1, col2 = st.columns(2)

    global P
    P = {}

    with col1:
        st.header("We are glad to have you here.")
        st.write("""
        This is a place where you will be asked to give some time to aid the environment.
        We hope that is ok with you. Please do enjoy your stay.
        """)

        if st.button("Get Started"):
            st.session_state.page = PAGES["Second Page"]  # Set page state to Second Page upon button click

    with col2:
        st.image("https://www.ipsl.fr/wp-content/themes/ipsltheme/themes/logo/logo_ipsl_1.png")

    # Sidebar with more information
    st.sidebar.title("About Us")
    st.sidebar.write("""
    We are a dedicated team trying to aid the world against the battles of climate change.
    Learn more about our mission and values at: https://www.ipsl.fr/lieu/universite-pierre-et-marie-curie-paris/
    """)

    # Handle page navigation based on state
    if "page" not in st.session_state:
        st.session_state.page = PAGES["Home"]  # Default to Home page

    page_dispatcher(st.session_state.page)

# Function to dispatch the correct page function based on the current state
def page_dispatcher(page):
    if page == PAGES["Second Page"]:
        second_page()
    elif page == PAGES["Third Page"]:
        third_page()
    elif page == PAGES["Fourth Page"]:
        fourth_page()
    elif page == PAGES["Fifth Page"]:
        fifth_page()
    elif page == PAGES["Sixth Page"]:
        sixth_page()

# Function for the second page
def second_page():
    st.title("Selection Task #1")
    st.write("Choose the number of actors participating.")
    
    if "selected_actor" not in st.session_state:
        st.session_state.selected_actor = None

    Actors = ["1 Actor", "2 Actors", "3 Actors"]
    selected_actor = st.radio("How many actors are participating?:", Actors)

    if selected_actor:
        st.session_state.selected_actor = selected_actor
        st.session_state.selected_actor_count = int(selected_actor.split()[0])
        st.session_state.current_actor_index = 1
        st.session_state.results = []
        if st.button("Yes", key="start_button"):  # Unique key for the button
            st.session_state.page = PAGES["Third Page"]

# Function for the third page
def third_page():
    st.title(f"Selection Task #2 for Actor {st.session_state.current_actor_index}")
    st.write("Please select one area to protect.")

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = None

    regions = ["NHST", "SHST", "GMST", "monsoon"]
    selected_region = st.radio("Regions", options=regions, key=f"region_actor_{st.session_state.current_actor_index}")

    st.session_state.selected_region = selected_region

    if st.session_state.selected_region:
        st.write(f"You selected: {st.session_state.selected_region}.")
        handle_navigation_buttons(PAGES["Fourth Page"], PAGES["Second Page"])

# Function for the fourth page
def fourth_page():
    st.title(f"Selection Task #3 for Actor {st.session_state.current_actor_index}")
    st.write("Please select an emission point.")

    if "selected_angle" not in st.session_state:
        st.session_state.selected_angle = None

    emipoints = ["60N", "30N", "15N", "eq", "15S", "30S", "60S"]
    selected_angle = st.multiselect("Choose at least ONE emission point:", emipoints, key=f"angle_{st.session_state.current_actor_index}")

    if selected_angle:
        st.session_state.selected_angle = selected_angle
        st.write(f"You selected: {st.session_state.selected_actor}, {st.session_state.selected_region}, and {st.session_state.selected_angle}.")
    
    handle_navigation_buttons(PAGES["Fifth Page"], PAGES["Third Page"])

# Function for the fifth page
def fifth_page():
    st.title(f"Selection Task #4 for Actor {st.session_state.current_actor_index}")
    st.write("Please select a setpoint.")

    if "setpoint" not in st.session_state:
        st.session_state.selected_setpoint = None

    setpoint = st.number_input("Insert a number from -10.0 -> 10.0", min_value=-10.0, max_value=10.0, step=1.0, placeholder="0.0")

    if setpoint is not None:
        st.session_state.selected_setpoint = setpoint
        st.write(f"You selected: {st.session_state.selected_actor}, {st.session_state.selected_region}, {st.session_state.selected_angle}, and {st.session_state.selected_setpoint}.")

    if st.session_state.selected_setpoint is None:
        st.session_state.selected_setpoint = 0.0
    
    if st.session_state.current_actor_index not in P:
        P[st.session_state.current_actor_index] = {}

    P[st.session_state.current_actor_index]['setpoint'] = st.session_state.selected_setpoint

    if st.button("Next", key=f"next_button_fifth_page_{st.session_state.current_actor_index}"):
        result = {
            "Actor": st.session_state.current_actor_index,
            "type": st.session_state.selected_region,
            "emipoints": st.session_state.selected_angle,
            "setpoint": st.session_state.selected_setpoint
        }
        st.session_state.results.append(result)

        if st.session_state.current_actor_index < st.session_state.selected_actor_count:
            st.session_state.current_actor_index += 1
            st.session_state.page = PAGES["Third Page"]
        else:
            st.session_state.page = PAGES["Sixth Page"]
    elif st.button("Back", key=f"back_button_fifth_page_{st.session_state.current_actor_index}"):
        st.session_state.page = PAGES["Fourth Page"]

# Function for the sixth page
def sixth_page():
    st.title("Your Results")
    st.write("These are your results:")

    if "results" in st.session_state:
        for result in st.session_state.results:
            st.write(f"Actor {result['Actor']}: Region - {result['type']}, Emission Point(s) - {result['emipoints']}, Setpoint - {result['setpoint']}")
        
        P = generate_P(st.session_state.results)
        run_model(P)
        
        display_plots()
    else:
        st.write("No results to display.")
        
    if st.button("Restart"):
        reset_session_state()
        st.session_state.page = PAGES["Home"]

# Function to handle navigation buttons
def handle_navigation_buttons(next_page, back_page):
    next_button_key = f"next_button_{st.session_state.page}_{st.session_state.current_actor_index}"
    back_button_key = f"back_button_{st.session_state.page}_{st.session_state.current_actor_index}"
    if st.button("Next", key=next_button_key):
        st.session_state.page = next_page
    elif st.button("Back", key=back_button_key):
        st.session_state.page = back_page

# Function to display the generated plots
def display_plots():
    fig1 = plot1()
    fig2 = plot2()
    fig3 = plot3(P)
    fig4 = plot4()
    fig5 = plot5()
    fig6 = plot6()
    
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)
    st.pyplot(fig4)
    st.pyplot(fig5)
    st.pyplot(fig6)

# Function to reset the session state
def reset_session_state():
    st.session_state.selected_actor = None
    st.session_state.selected_region = None
    st.session_state.selected_angle = None
    st.session_state.selected_setpoint = None
    st.session_state.results = []

# Run the main function
if __name__ == "__main__":
    main()