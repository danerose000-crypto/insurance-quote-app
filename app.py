import streamlit as st

st.set_page_config(page_title="Insurance Quote Request", layout="centered")

import streamlit as st

st.set_page_config(page_title="Insurance Quote Request", layout="centered")

st.title("Rose Insurance – Quote Request")
st.write("Fill this out and I'll shop your insurance options and follow up with you.")

# --- Quote type selection ---
quote_type = st.selectbox(
    "What do you want a quote for?",
    ["Auto", "Home", "Landlord", "Renters", "Commercial", "Other"],
)

# --- Contact info ---
st.subheader("Contact information")
name = st.text_input("Full name*")
email = st.text_input("Email*")
phone = st.text_input("Phone*")
preferred_contact = st.selectbox(
    "Preferred contact method",
    ["Phone", "Email", "Text"],
)

# --- Prepare vars so they exist even if not used ---
auto_drivers = []
auto_vehicles = []
garaging_location = ""
current_insurer = ""

home_fields = {}
landlord_fields = {}
renters_fields = {}
commercial_fields = {}
other_needs = ""

# --- Dynamic questions based on quote type ---

if quote_type == "Auto":
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

elif quote_type == "Home":
    st.subheader("Home details")
    home_fields["property_address"] = st.text_input(
        "Property address (street, city, state, ZIP)"
    )
    home_fields["replacement_cost"] = st.text_input(
        "Desired dwelling coverage / replacement cost ($)"
    )

elif quote_type == "Landlord":
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

elif quote_type == "Renters":
    st.subheader("Renters details")
    renters_fields["rental_address"] = st.text_input(
        "Rental address (street, city, state, ZIP)"
    )
    renters_fields["contents_value"] = st.text_input(
        "Estimated personal property value ($)"
    )

elif quote_type == "Commercial":
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

else:
    st.subheader("Describe what you need")
    other_needs = st.text_area(
        "Tell me what type of coverage you're looking for."
    )

# --- Extra notes ---
notes = st.text_area("Anything else I should know?")

# --- Submit button ---
if st.button("Submit quote request"):
    if not name or not email or not phone:
        st.error("Please fill in your name, email, and phone.")
    else:
        st.success("Thanks! Your quote request has been submitted. I'll follow up soon.")

        # For now, just show back the info (later we'll save it to a sheet)
        st.write("### Summary of what you entered:")
        st.write(f"**Type of quote:** {quote_type}")
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone:** {phone}")
        st.write(f"**Preferred contact:** {preferred_contact}")

        if quote_type == "Auto":
            st.write("#### Drivers")
            for idx, d in enumerate(auto_drivers, start=1):
                st.write(
                    f"- **Driver {idx}:** {d.get('name','')} | DOB: {d.get('dob','')} | DL: {d.get('license_number','')}"
                )

            st.write("#### Vehicles")
            for idx, v in enumerate(auto_vehicles, start=1):
                st.write(
                    f"- **Vehicle {idx}:** {v.get('year','')} {v.get('make','')} {v.get('model','')} "
                    f"(VIN: {v.get('vin','')}) – Coverages: {v.get('coverages_desired','')}"
                )

            st.write(f"**Garaging address:** {garaging_location}")
            st.write(f"**Current insurer:** {current_insurer}")

        elif quote_type == "Home":
            st.write("#### Home details")
            for label, value in home_fields.items():
                st.write(f"- **{label.replace('_', ' ').title()}:** {value}")

        elif quote_type == "Landlord":
            st.write("#### Landlord details")
            for label, value in landlord_fields.items():
                st.write(f"- **{label.replace('_', ' ').title()}:** {value}")

        elif quote_type == "Renters":
            st.write("#### Renters details")
            for label, value in renters_fields.items():
                st.write(f"- **{label.replace('_', ' ').title()}:** {value}")

        elif quote_type == "Commercial":
            st.write("#### Commercial details")
            for label, value in commercial_fields.items():
                st.write(f"- **{label.replace('_', ' ').title()}:** {value}")

        else:
            st.write("#### Other coverage needs")
            st.write(other_needs)

        st.write("**Notes:**")
        st.write(notes)
