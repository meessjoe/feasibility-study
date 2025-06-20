import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Feasibility Study Summary", layout="centered")

st.title("📊 Feasibility Study Summary Report")

# Inputs for business presentation
with st.form("feasibility_form"):
    col1, col2 = st.columns(2)
    with col1:
        address = st.text_input("📍 Site Address")
        lot_size = st.text_input("📐 Lot Size (sqm)")
        asking_price = st.text_input("💰 Asking Price (₱)")
    with col2:
        gmap_link = st.text_input("🗺️ Google Maps Link")
        competitor = st.text_area("🏢 Nearby Competitor(s)")
    
    st.markdown("### 📸 Upload Photos")
    site_image = st.file_uploader("Site Photo (from Google Maps or field visit)", type=["jpg", "jpeg", "png"])
    related_image = st.file_uploader("Competitor or Area Photo", type=["jpg", "jpeg", "png"])
    
    st.markdown("### 🗺️ Optional: Show Static Map")
    api_key = st.text_input("Google Maps Static API Key (optional)", type="password")

    submitted = st.form_submit_button("Generate Summary")

# Display the summary
if submitted:
    st.markdown("## 📝 Executive Summary")

    st.markdown(f"""
    <div style='font-size:16px; line-height:1.8'>
    ✅ <strong>Site Address:</strong> {address} <br>
    ✅ <strong>Lot Size:</strong> {lot_size} sqm <br>
    ✅ <strong>Asking Price:</strong> ₱{asking_price} <br>
    ✅ <strong>Google Maps Link:</strong> <a href="{gmap_link}" target="_blank">{gmap_link}</a> <br>
    ✅ <strong>Nearby Competitors:</strong> {competitor.replace("\\n", "<br>")}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Show static map
    if api_key and address:
        map_url = "https://maps.googleapis.com/maps/api/staticmap"
        params = {
            "center": address,
            "zoom": 17,
            "size": "600x300",
            "maptype": "roadmap",
            "markers": f"color:red|{address}",
            "key": api_key
        }
        res = requests.get(map_url, params=params)
        if res.status_code == 200:
            st.image(Image.open(BytesIO(res.content)), caption="📍 Location Map", use_column_width=True)
        else:
            st.warning("Map preview failed. Double-check API key or address.")

    # Uploaded images
    if site_image:
        st.image(site_image, caption="📸 Site Photo", use_column_width=True)
    if related_image:
        st.image(related_image, caption="📸 Related Area or Competitor", use_column_width=True)

    st.success("Presentation-ready summary generated.")
