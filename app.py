import requests
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="DD Recovery OS | FMC Compliance Auditor",
    page_icon="⚖️",
    layout="centered",
)

# App Header
st.title("⚖️ DD Recovery OS")
st.subheader("Automated Demurrage & Detention Compliance Auditor")
st.markdown(
    "Upload your carrier invoice PDF to check compliance against **46 CFR §541.6** regulations and instantly calculate legally voidable charges."
)

st.divider()

# File uploader widget
uploaded_file = st.file_uploader(
    "Upload Carrier Invoice (PDF)", type=["pdf"]
)

if uploaded_file is not None:
  # Display file details
  st.write(f"**Filename:** `{uploaded_file.name}`")

  if st.button("Run Legal Audit", type="primary"):
    with st.spinner("Analyzing statutory requirements..."):
      try:
        # Prepare file payload for your live FastAPI backend
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        }
        api_url = "https://dd-recovery-os-api.onrender.com/api/v1/audit-invoice"

        # Send request to your live cloud server
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
          data = response.json()
          audit = data.get("audit_result", {})
          extracted = data.get("extracted_data", {})

          st.success("Audit Complete!")

          # Metrics Section
          col1, col2, col3 = st.columns(3)
          col1.metric("Completeness Score", f"{audit.get('completeness_score')}%")
          col2.metric(
              "Legally Enforceable?",
              "Yes" if audit.get("is_legally_enforceable") else "No ❌",
          )
          col3.metric(
              "Disputable Amount",
              f"${audit.get('potential_disputable_amount', 0)}",
          )

          st.divider()

          # Extracted Data & Defects tabs
          tab1, tab2 = st.tabs(["Extracted Invoice Data", "Legal Defects Found"])

          with tab1:
            st.json(extracted)

          with tab2:
            defects = audit.get("defects_found", [])
            if defects:
              for defect in defects:
                st.error(f"⚠️ {defect}")
            else:
              st.info(
                  "✨ No statutory defects found! This invoice meets all FMC"
                  " billing requirements."
              )

        else:
          st.error(
              f"Server error ({response.status_code}): {response.text}"
          )

      except Exception as e:
        st.error(
            f"Failed to connect to backend server. Make sure it's active. Error:"
            f" {e}"
        )
