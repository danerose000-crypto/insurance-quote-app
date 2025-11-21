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
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    quote_type = st.selectbox(
        "What do you want a quote for?",
        ["Auto", "Home", "Landlord", "Renters", "Commercial", "Other"],
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- CONTACT INFO ----------
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Contact information")
    name = st.text_input("Full name*")
    email = st.text_input("Email*")
    phone = st.text_input("Phone*")
    preferred_contact = st.selectbox(
        "Preferred contact method",
        ["Phone", "Email", "Text"],
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Prepare vars so they exist
auto_drivers = []
auto_vehicles = []
garaging_location = ""
current_insurer = ""

home_fields = {}
landlord_fields = {}
renters_fields = {}
commercial_fields = {}
other_needs = ""

# ---------- DYNAMIC SECTIONS BY QUOTE TYPE ----------

if quote_type == "Auto":
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Auto details")

        # Number of drivers
        num_drivers = st.number_input(
            "How many drivers will be on this policy?",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
        )

        st.markdown("#### Driver information")
        auto_drivers = []
        for i in range(int(num_drivers)):
            st.markdown(f"**Driver {i+1}**")
            d_name = st.text_input(
                f"Full name (Driver {i+1})",
                key=f"driver_{i+1}_name",
            )
            d_dob = st.text_input(
                f"Date of birth (Driver {i+1})",
                key=f"driver_{i+1}_dob",
                placeholder="MM/DD/YYYY",
            )
            d_dl = st.text_input(
                f"Driver's license number (Driver {i+1})",
                key=f"driver_{i+1}_dl",
            )
            auto_drivers.append(
                {
                    "name": d_name,
                    "dob": d_dob,
                    "license_number": d_dl,
                }
            )

        # Number of vehicles
        st.markdown("#### Vehicle information")
        num_vehicles = st.number_input(
            "How many vehicles will be on this policy?",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
        )

        auto_vehicles = []
        for i in range(int(num_vehicles)):
            st.markdown(f"**Vehicle {i+1}**")
            v_year = st.text_input(
                f"Year (Vehicle {i+1})",
                key=f"vehicle_{i+1}_year",
            )
            v_make = st.text_input(
                f"Make (Vehicle {i+1})",
                key=f"vehicle_{i+1}_make",
            )
            v_model = st.text_input(
                f"Model (Vehicle {i+1})",
                key=f"vehicle_{i+1}_model",
            )
            v_vin = st.text_input(
                f"VIN (Vehicle {i+1})",
                key=f"vehicle_{i+1}_vin",
            )
            v_cov = st.text_area(
                f"Coverages desired for Vehicle {i+1}",
                key=f"vehicle_{i+1}_cov",
            )
            auto_vehicles.append(
                {
                    "year": v_year,
                    "make": v_make,
                    "model": v_model,
                    "vin": v_vin,
                    "coverages_desired": v_cov,
                }
            )

        garaging_location = st.text_input(
            "Garaging address (street, city, state, ZIP)"
        )
        current_insurer = st.text_input("Current insurance company (if any)")
        st.markdown("</div>", unsafe_allow_html=True)

elif quote_type == "Home":
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Home details")
        home_fields["property_address"] = st.text_input(
            "Property address (street, city, state, ZIP)"
        )
        home_fields["replacement_cost"] = st.text_input(
            "Desired dwelling coverage / replacement cost ($)"
        )
        st.markdown("</div>", unsafe_allow_html=True)

elif quote_type == "Landlord":
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Landlord (rental property) details")
        landlord_fields["property_address"] = st.text_input(
            "Rental property address (street, city, state, ZIP)"
        )
        landlord_fields["replacement_cost"] = st.text_input(
            "Desired dwelling coverage / replacement cost ($)"
        )
        landlord_fields["occupancy"] = st.selectbox(
            "Type of rental",
            ["Single-family home", "Duplex", "Fourplex", "Apartment / other"],
        )
        landlord_fields["number_of_units"] = st.number_input(
            "Number of units",
            min_value=1,
            max_value=50,
            value=1,
            step=1,
        )
        st.markdown("</div>", unsafe_allow_html=True)

elif quote_type == "Renters":
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Renters details")
        renters_fields["rental_address"] = st.text_input(
            "Rental address (street, city, state, ZIP)"
        )
        renters_fields["contents_value"] = st.text_input(
            "Estimated personal property value ($)"
        )
        st.markdown("</div>", unsafe_allow_html=True)

elif quote_type == "Commercial":
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Commercial insurance details")
        commercial_fields["business_name"] = st.text_input("Business name")
        commercial_fields["business_type"] = st.text_input(
            "Type of business (what you do)"
        )
        commercial_fields["years_in_business"] = st.text_input("Years in business")
        commercial_fields["annual_revenue"] = st.text_inpu]()_

