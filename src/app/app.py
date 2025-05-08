import streamlit as st


user_experience_pages = [
    st.Page("user_experience/settings.py", title="Settings", icon=":material/settings:")
]

getting_started_pages = [
    st.Page(
        "getting_started/home.py",
        title="Home",
        icon=":material/home:",
        default=True,
    )
]

visualization_pages = [
    st.Page(
        "visualization/exploratory_analysis.py",
        title="Exploratory Analysis",
        icon=":material/search:",
    ),
    st.Page(
        "visualization/predictive_analysis.py",
        title="Predictive Analysis",
        icon=":material/monitoring:",
    ),
]

project_pages = [
    st.Page("project/dataframe.py", title="Dataframe", icon=":material/database:"),
    st.Page(
        "project/initiative.py",
        title="Initiative",
        icon=":material/rocket_launch:",
    ),
]

sections = [
    ("Getting Started", getting_started_pages),
    ("User Experience", user_experience_pages),
    ("Visualization", visualization_pages),
    ("Project", project_pages),
]

nav_dict = {section[0]: section[1] for section in sections}

st.navigation(nav_dict).run()
