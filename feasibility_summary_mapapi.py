import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Feasibility Study Summary", layout="centered")

st.title("📍 Feasibility Study Report")

# Input fields
address = st.text_input("📌 Site Address")
lot_size = st.text_input("📐 Lot Size (sqm)")
gmap_link = st.text_input("🗺️ Google Maps Link")
competitor = st.text_area("🏢 Nearby Competitor(s)")
asking_price = st.text_input("💰 Asking Price (₱)")
api_key = st.text_input("🔑 Google Maps Static API Key", type="password")

# Upload images
st.markdown("---")
st.subheader("📸 Upload Optional Site Photos")
site_image = st.file_uploader("Upload Site Photo", type=["jpg", "png", "jpeg"])
related_image = st.file_uploader("Upload Related Photo", type=["jpg", "png", "jpeg"])

if st.button("Generate Summary"):
    st.markdown("## 📝 Feasibility Study Summary")
    st.write(f"**📍 Address:** {address}")
    st.write(f"**📐 Lot Size:** {lot_size} sqm")
    st.write(f"**🗺️ Google Maps Link:** [Open Map]({gmap_link})")
    st.write(f"**🏢 Nearby Competitor(s):** {competitor}")
    st.write(f"**💰 Asking Price:** ₱{asking_price}")

    # Static Map Image from Google Maps
    if address and api_key:
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
            img = Image.open(BytesIO(res.content))
            st.image(img, caption="🗺️ Map Preview", use_column_width=True)
        else:
            st.warning("Map preview failed. Check address or API key.")

    if site_image:
        st.image(site_image, caption="📸 Site Photo", use_column_width=True)
    if related_image:
        st.image(related_image, caption="📸 Related Photo", use_column_width=True)