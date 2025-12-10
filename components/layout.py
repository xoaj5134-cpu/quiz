# components/layout.py

import streamlit as st


def render_page_header(title: str, subtitle: str | None = None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")
