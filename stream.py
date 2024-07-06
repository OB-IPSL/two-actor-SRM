import streamlit as st  # Import Streamlit library
import base64  # Import base64 module for encoding/decoding binary data
import engine
import myclim

# Function to add background from a local image file
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())  # Encode image file to base64

    # Inject CSS to set background image using base64 encoded string
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Call function to set background image
#add_bg_from_local('/Users/omar/Documents/island.jpg')

# Dictionary defining page names and corresponding identifiers
PAGES = {
    "Home": "home",
    "Select actors": "select_actors",
    "Select target": "select_target",
    "Select setpoint": "select_setpoint",
    "Select injection points": "select_injection",
    "Your results": "your_result",
    "Next": "next_button"
}

# CSS style for custom buttons
button_css = """
<style>
/* Target Streamlit buttons */
div.stButton > button {
    background-color: #81dbcf; /* Blue background */
    border: none; /* Remove borders */
    color: white; /* White text */
    padding: 15px 32px; /* Add some padding */
    text-align: center; /* Center the text */
    text-decoration: none; /* Remove underline */
    display: inline-block; /* Make the container block-level */
    font-size: 16px; /* Increase font size */
    margin: 4px 2px; /* Add some margin */
    cursor: pointer; /* Add a pointer cursor on hover */
    border-radius: 8px; /* Rounded corners */
}

div.stButton > button:hover {
    background-color: #5a9991; /* Darker Blue on hover */
    color: #aaabad; /* Darker white text on hover */
}
</style>
"""

# Add the CSS style to the Streamlit app
st.markdown(button_css, unsafe_allow_html=True)

# Main function
def main():
    # Use columns to organize layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Simulation of two actor deployment of Solar Radiation Management")
        st.write("""
        Click 'Get started' to begin your simulation
        """)
        st.markdown(button_css, unsafe_allow_html=True)
        if st.button("Get Started"):
            st.session_state.page = PAGES["Select actors"]  # Set page state to "Select actors" page upon button click

    with col2:
        st.image("inputs/Sciences_SU.png")  # Display an image in the second column

    # Sidebar with more information

    # Handle page navigation based on state
    if "page" not in st.session_state:
        st.session_state.page = PAGES["Home"]  # Default to Home page

    if st.session_state.page == PAGES["Select actors"]: select_actors()

    if st.session_state.page == PAGES["Select target"]: select_target()

    if st.session_state.page == PAGES["Select setpoint"]: select_setpoint()

    if st.session_state.page == PAGES["Select injection points"]: select_injection()

    if st.session_state.page == PAGES["Your results"]: your_result()

# Function for the actors selection
def select_actors():
    st.title("Selection of actors")
    st.write("Please choose your preferred number of actors.")

    actors = ["1 Actor", "2 Actors", "3 Actors"]
    selected_actor = st.radio("Possible number of actors", actors)

    if selected_actor:
        st.session_state.selected_actor_count = int(selected_actor.split()[0])
        st.session_state.current_actor_index = 'A'
        st.session_state.results = []
        st.write(f"You selected: {selected_actor}.")
        if st.button("Next", key="start_target"):  # Unique key for the button
            st.session_state.page = PAGES["Select target"]

# Function for the target selection
def select_target():
    st.title(f"Selection of target for Actor {st.session_state.current_actor_index}")
    st.write("Please select a target.")

    if "selected_target" not in st.session_state: st.session_state.selected_target = None

    targets = ["NHST", "SHST", "GMST", "monsoon"]
    selected_target = st.radio("Possible targets:", options=targets, key=f"target_actor_{st.session_state.current_actor_index}")

    if selected_target:
        st.session_state.selected_target = selected_target
        st.write(f"You selected: {st.session_state.selected_target}.")
        if st.button("Next", key="start_setpoint"):  # Unique key for the button
            st.session_state.page = PAGES["Select setpoint"]

# Function for the setpoint selection
def select_setpoint():
    st.title(f"Selection of setpoint for Actor {st.session_state.current_actor_index}")
    if "set_num" not in st.session_state: st.session_state.set_num = None

    set_num = st.text_input(
        "Please enter a setpoint (Default 0.0, Press enter to apply)", "0.0",
        key=f"set_actor_{st.session_state.current_actor_index}",
    )
    st.session_state.set_num = float(set_num)

    if st.button("Next", key="start_injection"):  # Unique key for the button
         st.session_state.page = PAGES["Select injection points"]

# Function for the injection selection
def select_injection():
    st.title(f"Selection of injection points for Actor {st.session_state.current_actor_index}")
    st.write("Please select one or more injection points.")

    #if "tinjections" not in st.session_state: st.session_state.tinjections = []
    st.session_state.tinjections = []

    test_locations = ["60S", "30S", "15S", "eq", "15N", "30N", "60N"]

    for location in test_locations:
        if st.checkbox(location, key=location+f"_actor_{st.session_state.current_actor_index}"):
            if location not in st.session_state.tinjections:
                st.session_state.tinjections.append(location)

    if st.button("Next", key=f"next_button_your_result_{st.session_state.current_actor_index}"):
        result = {
            "actor": st.session_state.current_actor_index,
            "target": st.session_state.selected_target,
            "setpoint": st.session_state.set_num,
            "emipoints": st.session_state.tinjections
        }
        st.session_state.results.append(result)

        if ord(st.session_state.current_actor_index)-ord('A')+1 < st.session_state.selected_actor_count:
            st.session_state.current_actor_index =  chr(ord(st.session_state.current_actor_index)+1)
            st.session_state.page = PAGES["Select target"]
        else:
            st.session_state.page = PAGES["Your results"]

# Function for the results
def your_result():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Your Results:")

    # Convert results into a dictionary to run the model
    P={}
    default_T={'Kp':0.8, 'Ki':0.6, 'Kd':0.0,'emimin':0.0,'emimax':10.0,'t1':50,'t2':70,'stops':[]}
    default_m={'Kp':0.08,'Ki':0.06,'Kd':0.0,'emimin':0.0,'emimax':10.0,'t1':50,'t2':70,'stops':[]}

    print(st.session_state.results)
    for res in st.session_state.results:
      
      P[res['actor']] = {k:v for k,v in res.items() if k != 'actor'}
      if res['target']=='monsoon': 
         P[res['actor']] = P[res['actor']] | default_m
      else: 
         P[res['actor']] = P[res['actor']] | default_T
    print(P)

    #--some more fixed inputs (duplicated from main)
    #--volcano
    volcano=True
    #--period of integration
    t5=200
    #--max GHG forcing
    fmax=4.0
    #--noise type: white, red, mixed
    noise_type='white'
    #--noise level
    noise_T=0.15       #--in K
    noise_monsoon=5.   #--in % change
    #--interhemispheric timescales (in years)
    tau_nh_sh_upper=20.
    tau_nh_sh_lower=20.

    #--create a list of all emission points
    emipoints = engine.set_emipoints(P)
    #
    #--initialise impulse response functions
    aod_strat_sh, aod_strat_nh, nbyr_irf = myclim.initialise_aod_responses()
    #
    #--initialise GHG forcing scenario, increases linearly for 100 yrs then constant then decrease slowly
    f = engine.initialise_forcing(t5,fmax,volcano)
    #
    #--time profiles of climate noise
    Tsh_noise, Tnh_noise, monsoon_noise = engine.set_noise(t5,noise_T,noise_monsoon,noise_type)
    #
    #--call controller
    emi_SRM, emissmin, g_SRM_nh,g_SRM_sh,T_noSRM_nh,T_noSRM_sh,T_SRM_nh,T_SRM_sh,monsoon_noSRM,monsoon_SRM = \
           engine.run_controller(t5,nbyr_irf,f,P,tau_nh_sh_upper,tau_nh_sh_lower, \
                                 aod_strat_sh,aod_strat_nh,Tsh_noise,Tnh_noise,monsoon_noise)

    # Display various graphs using functions from module engine
    fig = engine.plot1(t5,f)
    st.pyplot(fig)

    fig = engine.plot2(t5,Tsh_noise,Tnh_noise,monsoon_noise)
    st.pyplot(fig)

    fig = engine.plot3(t5,P,emi_SRM,emissmin)
    st.pyplot(fig)

    fig = engine.plot4(t5,g_SRM_sh,g_SRM_nh)
    st.pyplot(fig)

    fig = engine.plot5(t5,T_noSRM_sh,T_noSRM_nh,T_SRM_sh,T_SRM_nh)
    st.pyplot(fig)

    fig = engine.plot6(t5,monsoon_noSRM,monsoon_SRM)
    st.pyplot(fig)
        
    # Back home
    if st.button("Home", key="start_button"):  # Unique key for the button
       st.session_state.page = PAGES["Home"]

# Entry point of the script
if __name__ == "__main__":
    main()
