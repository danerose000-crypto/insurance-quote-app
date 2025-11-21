import streamlit as st

st.set_page_config(page_title="Insurance Quote Request", layout="centered")

import streamlit as st

st.set_page_config(page_title="Insurance Quote Request", layout="centered")

# ---------- BASIC STYLING (colors: red, black, gray) ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f4f4; /* light gray background */
    }

    /* Make all inputs white so they pop against the gray */
    input, textarea, select {
        background-color: #ffffff !important;
    }

    /* Top header card */
    .rose-header {
        background: linear-gradient(90deg, #111111, #2b2b2b);
        padding: 1.25rem 1.75rem;
        border-radius: 0.75rem;
        margin-bottom: 1.5rem;
        border: 1px solid #333333;
    }
    .rose-header h1 {
        color: #ffffff;
        margin: 0 0 0.3rem 0;
        font-size: 1.75rem;
    }
    .rose-header p {
        color: #cccccc;
        margin: 0.1rem 0;
        font-size: 0.95rem;
    }
    .rose-header a {
        color: #ff4b4b; /* red accent */
        text-decoration: none;
        font-weight: 600;
    }
    .rose-header a:hover {
        text-decoration: underline;
    }

    /* Section wrapper - now transparent, no white box or red bar */
    .section-card {
        background-color: transparent;  /* no white box */
        padding: 0;                     /* let Streamlit handle spacing */
        border-radius: 0;
        border-left: none;              /* remove red left border */
        margin-bottom: 1rem;
        box-shadow: none;
    }

    /* Make subheaders a bit darker */
    .stMarkdown h3, .stMarkdown h4 {
        color: #222222;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER WITH YOUR CONTACT INFO ----------
st.markdown(
    """
    <div class="rose-header">
        <h1>Rose Insurance – Online Quote Request</h1>
        <p>Questions or prefer to talk it through?</p>
        <p>
            Email:
            <a href="mailto:Roseinserv@gmail.com">Roseinserv@gmail.com</a>
            &nbsp;|&nbsp;
            Call / Text:
            <a href="tel:17023032170">(702) 303-2170</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("Fill this out and I'll shop your insurance options and follow up with you.")

# ---------- QUOTE TYPE SELECTION ----------
with st.container():
    st.m
