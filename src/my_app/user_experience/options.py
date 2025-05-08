import streamlit as st

from streamlit_app import INTERESTS

st.write("# Looking for something else ? 🔎")

st.markdown(
    """
    This project have other pages, you can check them out by clicking the buttons below:
    """
)
for interest_key, interest in INTERESTS.items():
    if (
        interest_key is not None and interest_key != st.session_state.interest
    ):  # Skip None key and current interest
        if st.button(
            f"### {interest['Title']}"
            + (f"\n\n{interest['Description']}" if "Description" in interest else ""),
            use_container_width=True,
        ):
            st.session_state.interest = interest_key
            st.rerun()
