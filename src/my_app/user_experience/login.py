import streamlit as st

from streamlit_app import INTERESTS

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