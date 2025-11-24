import streamlit as st
import datetime as dt
import pandas as pd
import json

st.set_page_config(page_title="Insurance Quote Request", layout="centered")

# Google Sheet ID from your sheet URL
SHEET_ID = "1og5tSQ2xSAt1iXADHrIIOm1ON48gwOjrxEnlF-k_XdI"


@st.cache_resource
def get_gsheet_client():
    """Create a Google Sheets client using service-account credentials in Streamlit secrets."""
    try:
        creds_json_str = st.secrets["gcp_service_account"]
    except KeyError:
        st.warning(
            "Google Sheets is not configured yet (missing gcp_service_account in secrets). "
            "Submissions will not be saved until this is set up."
        )
        return None

    import gspread
    from google.oauth2.service_account import Credentials

    # Read the JSON from secrets (we stored the whole JSON string there)
    creds_dict = json.loads(creds_json_str, strict=False)

    # Only use the Sheets scope – no Drive storage
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(credentials)
    return client


def append_submission_to_sheet(submission: dict):
    """Append one submission as a row in the existing Google Sheet."""
    client = get_gsheet_client()
    if client is None:
        return

    try:
        # Open the sheet directly by its ID
        sheet = client.open_by_key(SHEET_ID).sheet1
    except Exception as e:
        # show full repr so we can debug
        st.error(f"Error opening Google Sheet: {repr(e)}")
        return

    # Ensure header row exists, and extend it with any new keys
    existing_headers = sheet.row_values(1)
    if not existing_headers:
        headers = list(submission.keys())
        sheet.append_row(headers)
        existing_headers = headers
    else:
        headers = existing_headers[:]
        for key in submission.keys():
            if key not in headers:
                headers.append(key)
        # If we added new headers, update the first row
        if headers != existing_headers:
            sheet.update("1:1", [headers])

    # Order row according to final headers list
    row = [submission.get(col, "") for col in headers]
    sheet.append_row(row)


def load_all_submissions() -> pd.DataFrame:
    """Load all submissions from Google Sheets into a DataFrame."""
    client = get_gsheet_client()
    if client is None:
        return pd.DataFrame()

    try:
        sheet = client.open_by_key(SHEET_ID).sheet1
        data = sheet.get_all_records()
    except Exception as e:
        st.error(f"Error loading submissions from Google Sheets: {repr(e)}")
        return pd.DataFrame()

    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


# ---------- BASIC STYLING (colors: red, black, gray) ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #303030;  /* darker gray */
        color: #f5f5f5;             /* light text on dark bg */
    }
    input, textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
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
        color: #ff4b4b;
        text-decoration: none;
        font-weight: 600;
    }
    .rose-header a:hover {
        text-decoration: underline;
    }
    .section-card {
        background-color: transparent;
        padding: 0;
        border-radius: 0;
        border-left: none;
        margin-bottom: 1rem;
        box-shadow: none;
    }
    .stMarkdown h3, .stMarkdown h4 {
        color: #f5f5f5;
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
    dob = st.text_input("Date of birth*", placeholder="MM/DD/YYYY")
    email = st.text_input("Email*")
    phone = st.text_input("Phone*")
    effective_date = st.text_input(
        "When do you need coverage to start?*",
        placeholder="MM/DD/YYYY",
    )
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
        commercial_fields["annual_revenue"] = st.text_input(
            "Approx. annual revenue ($)"
        )
        commercial_fields["location"] = st.text_input(
            "Main business address (street, city, state, ZIP)"
        )
        commercial_fields["operations_desc"] = st.text_area(
            "Brief description of your operations & what you need coverage for"
        )
        st.markdown("</div>", unsafe_allow_html=True)

else:
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Describe what you need")
        other_needs = st.text_area(
            "Tell me what type of coverage you're looking for."
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- EXTRA NOTES ----------
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    notes = st.text_area("Anything else I should know?")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SUBMIT BUTTON & SAVE ----------
if st.button("Submit quote request"):
    if not name or not email or not phone or not dob or not effective_date:
        st.error("Please fill in your name, date of birth, effective date, email, and phone.")
    else:
        lines = [
            f"Type of quote: {quote_type}",
            f"Name: {name}",
            f"Date of birth: {dob}",
            f"Email: {email}",
            f"Phone: {phone}",
            f"Effective date: {effective_date}",
            f"Preferred contact: {preferred_contact}",
        ]

        if quote_type == "Auto":
            lines.append("DRIVERS:")
            for idx, d in enumerate(auto_drivers, start=1):
                lines.append(
                    f"  Driver {idx}: {d.get('name','')} | DOB: {d.get('dob','')} | DL: {d.get('license_number','')}"
                )

            lines.append("VEHICLES:")
            for idx, v in enumerate(auto_vehicles, start=1):
                lines.append(
                    f"  Vehicle {idx}: {v.get('year','')} {v.get('make','')} {v.get('model','')} "
                    f"(VIN: {v.get('vin','')}) – Coverages: {v.get('coverages_desired','')}"
                )

            lines.append(f"Garaging address: {garaging_location}")
            lines.append(f"Current insurer: {current_insurer}")

        elif quote_type == "Home":
            lines.append("HOME DETAILS:")
            for label, value in home_fields.items():
                lines.append(f"  {label.replace('_', ' ').title()}: {value}")

        elif quote_type == "Landlord":
            lines.append("LANDLORD DETAILS:")
            for label, value in landlord_fields.items():
                lines.append(f"  {label.replace('_', ' ').title()}: {value}")

        elif quote_type == "Renters":
            lines.append("RENTERS DETAILS:")
            for label, value in renters_fields.items():
                lines.append(f"  {label.replace('_', ' ').title()}: {value}")

        elif quote_type == "Commercial":
            lines.append("COMMERCIAL DETAILS:")
            for label, value in commercial_fields.items():
                lines.append(f"  {label.replace('_', ' ').title()}: {value}")

        else:
            lines.append("OTHER COVERAGE NEEDS:")
            lines.append(other_needs)

        if notes:
            lines.append("Notes:")
            lines.append(notes)

        details_text = "\n".join(lines)

        st.success("Thanks! Your quote request has been submitted. I'll follow up soon.")
        st.write("### Summary of what you entered:")
        st.text(details_text)

        submission = {
            "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
            "quote_type": quote_type,
            "name": name,
            "date_of_birth": dob,
            "email": email,
            "phone": phone,
            "effective_date": effective_date,
            "preferred_contact": preferred_contact,
            "details": details_text,
        }

        try:
            append_submission_to_sheet(submission)
        except Exception as e:
            st.error(
                f"There was an issue saving your request to Google Sheets: {repr(e)}"
            )

# ---------- ADMIN VIEW ----------
# ---------- ADMIN VIEW (HIDDEN BY DEFAULT) ----------
# Only show admin controls if the URL has ?admin=1
params = st.experimental_get_query_params()
admin_mode = params.get("admin", ["0"])[0] == "1"

if admin_mode:
    st.sidebar.markdown("---")
    show_admin = st.sidebar.checkbox("Admin view")

    if show_admin:
        st.header("Admin – Quote Requests")

        admin_pw = st.text_input("Admin password", type="password")
        if st.button("Log in as admin"):
            real_pw = st.secrets.get("ADMIN_PASSWORD", "roseadmin123")
            if admin_pw != real_pw:
                st.error("Incorrect password.")
            else:
                st.session_state["admin_logged_in"] = True

    if st.session_state.get("admin_logged_in"):
        st.success("Admin access granted.")

        df = load_all_submissions()
        if df.empty:
            st.info("No submissions found yet.")
        else:
            df_sorted = df.sort_values("timestamp", ascending=False)
            st.dataframe(df_sorted, use_container_width=True)
