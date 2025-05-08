import streamlit as st

if "interest" not in st.session_state:
    st.session_state.interest = None

INTERESTS = {
    None: {},  # unauthenticated
    "What": {
        "Title": "I'm just interested in the data and the visualization",
        "Description": "I just want to see what you have done, the final dataframe, it's visualization and predictions",
    },
    "How": {
        "Title": "I'm interested in how you've collected, processed and exibited tha data",
        "Description": "I want to see from where you've collected the data, how you've processed it, and with witch tools you've exibited a dashboard",
    },
    "Why": {
        "Title": "I'm interested in why you've chosen this dataset and built this dashboard",
        "Description": "I want to know what made you choose this dataset, what was your motivation to build this dashboard and what do you want to achieve with it",
    },
    "Who": {
        "Title": "I want to know who you are",
        "Description": "I want to know who you are, what is your background and what do you want to achieve with this project",
    },
}


interest = st.session_state.interest

def login():
    st.write("# Welcome to my Streamlit app! 👋")

    st.markdown(
        """
        I've built this app using [Streamlit](https://streamlit.io), a powerful
        open-source app framework for Machine Learning and Data Science projects.
        ### **Select one of the interests below:**
        """
    )

    for interest_key, interest in INTERESTS.items():
        if interest_key is not None:  # Skip None key
            if st.button(
                f"### {interest['Title']}"
                + (
                    f"\n\n{interest['Description']}"
                    if "Description" in interest
                    else ""
                ),
                use_container_width=True,
            ):
                st.session_state.interest = interest_key
                st.rerun()

# == User Experience Pages ==

options = st.Page("user_experience/options.py", title="Options", icon=":material/menu:")
settings = st.Page(
    "user_experience/settings.py", title="Settings", icon=":material/settings:"
)

# == visualization Pages ==

exploratory_analysis = st.Page(
    "visualization/exploratory_analysis.py",
    title="Exploratory Analysis",
    icon=":material/search:",
    default=(interest == "What"),
)

predictive_analysis = st.Page(
    "visualization/predictive_analysis.py",
    title="Predictive Analysis",
    icon=":material/monitoring:",
    default=(interest == "What"),
)

# == Development Pages ==

## For later

# == Project Pages ==

initiative = st.Page(
    "project/initiative.py",
    title="Initiative",
    icon=":material/rocket_launch:",
    default=(interest == "Why"),
)

dataframe = st.Page(
    "project/dataframe.py",
    title="Dataframe",
    icon=":material/database:",
    default=(interest == "Why"),
)

# == Author Pages ==

about = st.Page(
    "author/about.py",
    title="About",
    icon=":material/person:",
    default=(interest == "Who"),
)

user_experience_pages = [options, settings]
visualization_pages = [exploratory_analysis, predictive_analysis]
development_pages = []
project_pages = [initiative, dataframe]
author_pages = [about]

pages_dict = {}

if st.session_state.interest in ["What", "How", "Why", "Who"]:
    pages_dict["User Experience"] = user_experience_pages
if st.session_state.interest in ["What", "How"]:
    pages_dict["Visualization"] = visualization_pages
if st.session_state.interest == "How":
    pages_dict["Development"] = development_pages
if st.session_state.interest == "Why":
    pages_dict["Project"] = project_pages
if st.session_state.interest == "Who":
    pages_dict["Author"] = author_pages

if len(pages_dict) > 0:
    pg = st.navigation({"User Experience": user_experience_pages} | pages_dict)
else:
    pg = st.Page(
    login,
    title="Login",
    icon=":material/login:",
    default=(interest is None),
)

pg.run()