import gc
import os
import streamlit as st

from .components import github_button

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def app_layout():
    from .layouts import page_0

    st.set_page_config(
        page_title="Streamlit template",
        page_icon="👾",
        layout="wide",
        initial_sidebar_state="auto",
    )

    load_css()

    st.sidebar.markdown(" ## *Streamlit template*\n")

    if 'page' not in st.session_state:
        st.session_state.page = "# First Page"

    st.session_state.page = st.sidebar.radio(
        "Summary",
        [
            "# First Page",
        ],
    )

    col1, col2 = st.columns([3, 4])
    with col1:
        st.markdown('<div class="title">Streamlit</div>', unsafe_allow_html=True)
        st.markdown("#### *A Streamlit App Template* ")
        col_a, col_b= st.columns([1, 6])

        with col_a:
            github_button("https://github.com/mriusero/CICD-Docker-to-HuggingFace-Template")

        with col_b:
            st.text("")
            st.write("")


    with col2:
        st.text("")
        st.text("")
        st.text("")

    line_style = """
        <style>
        .full-width-line {
            height: 2px;
            background-color: #FFFFFF;
            width: 100%;
            margin: 20px 0;
        }
        </style>
    """
    line_html = '<div class="full-width-line"></div>'

    st.markdown(line_style, unsafe_allow_html=True)
    st.markdown(line_html, unsafe_allow_html=True)


    if st.session_state.page == "# First Page":
        page_0()


    st.sidebar.markdown("&nbsp;")

    gc.collect()
