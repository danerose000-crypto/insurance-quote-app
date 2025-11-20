import streamlit as st

st.set_page_config(page_title="Insurance Quote – Test", layout="centered")

import streamlit as st

st.set_page_config(page_title="Insurance Quote Request", layout="centered")

st.title("Rose Insurance – Quote Request")
st.write("Fill this out and I'll shop your insurance options and follow up with you.")

# --- Quote type selection ---
quote_type = st.selectbox(
    "What do you want a quote for?",
    ["Auto", "Home", "Renters", "Other"],
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

# --- Dynamic questions based on quote type ---
auto_fields = {}
home_fields = {}
renters_fields = {}
other_needs = ""

if quote_type == "Auto":
    st.subheader("Auto details")
    auto_fields["drivers"] = st.text_input(
        "List all drivers (names & dates of birth)"
    )
    auto_fields["vehicles"] = st.text_input(
        "List all vehicles (year, make, model)"
    )
    auto_fields["garaging_location"] = st.text_input(
        "Garaging ZIP / city, state"
    )
    auto_fields["current_insurer"] = st.text_input(
        "Current insurance company (if any)"
    )
    auto_fields["tickets_claims"] = st.text_area(
        "Tickets/accidents/claims in last 5 years"
    )

elif quote_type == "Home":
    st.subheader("Home details")
    home_fields["property_address"] = st.text_input("Property address")
    home_fields["year_built"] = st.text_input("Year built")
    home_fields["square_feet"] = st.text_input("Approximate square footage")
    home_fields["roof_year"] = st.text_input("Roof year (approx.)")
    home_fields["prior_claims"] = st.text_area(
        "Any prior claims in last 5 years?"
    )

elif quote_type == "Renters":
    st.subheader("Renters details")
    renters_fields["rental_address"] = st.text_input("Rental address")
    renters_fields["contents_value"] = st.text_input(
        "Estimated personal property value ($)"
    )
    renters_fields["prior_claims"] = st.text_area(
        "Any prior claims in last 5 years?"
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
            st.write("**Auto details:**")
            for label, value in auto_fields.items():
                st.write(f"- **{label.replace('_', ' ').title()}:** {value}")

        elif quote_type == "Home":
            st.write("**Home details:**")
            for label, value in home_fields.items():
                st.write(f"- **{label.replace('_', ' ').title()}:** {value}")

        elif quote_type == "Renters":
            st.write("**Renters details:**")
            for label, value in renters_fields.items():
                st.write(f"- **{label.replace('_', ' ').title()}:** {value}")

        else:
            st.write("**Other coverage needs:**")
            st.write(other_needs)

        st.write("**Notes:**")
        st.write(notes)
