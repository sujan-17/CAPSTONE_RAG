import streamlit as st
import requests

# =========================
# CONFIG
# =========================

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Jewellery Multimodal Search",
    page_icon="💎",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================

if "results" not in st.session_state:
    st.session_state.results = None

if "view" not in st.session_state:
    st.session_state.view = "search"   # search | results

# =========================
# STYLES
# =========================

st.markdown(
    """
    <style>
    .card {
        border-radius: 14px;
        padding: 14px;
        background-color: white;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        margin-bottom: 22px;
    }
    .score {
        font-size: 14px;
        color: #555;
        margin-top: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================

st.title("💎 Jewellery Multimodal Search")
st.caption("Text • Image • Handwritten Search")

st.divider()

# =========================
# BACKEND CALLS
# =========================

def search_text(query: str):
    res = requests.post(
        f"{API_BASE}/search/text",
        params={"query": query}
    )
    return res.json()

def search_image(image_file):
    files = {"file": image_file}
    res = requests.post(
        f"{API_BASE}/search/image",
        files=files
    )
    return res.json()

# =========================
# SEARCH VIEW
# =========================

if st.session_state.view == "search":

    mode = st.radio(
        "Search mode",
        ["Text Query", "Image Query"],
        horizontal=True
    )

    if mode == "Text Query":
        query = st.text_input(
            "Enter jewellery description",
            placeholder="e.g. heart shaped diamond ring in white gold"
        )

        if st.button("🔍 Search", use_container_width=True):
            if query.strip():
                with st.spinner("Searching..."):
                    st.session_state.results = search_text(query)
                    st.session_state.view = "results"
                    st.rerun()

    else:
        uploaded = st.file_uploader(
            "Upload an image (jewel / sketch / handwritten)",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded and st.button("🔍 Search", use_container_width=True):
            with st.spinner("Processing image..."):
                st.session_state.results = search_image(uploaded)
                st.session_state.view = "results"
                st.rerun()

# =========================
# RESULTS VIEW
# =========================

if st.session_state.view == "results":

    if st.button("⬅ Back to Search"):
        st.session_state.view = "search"
        st.session_state.results = None
        st.rerun()

    results = st.session_state.results

    if results and "results" in results:
        st.divider()
        st.subheader("Results")

        cols = st.columns(4)

        for idx, item in enumerate(results["results"]):
            col = cols[idx % 4]

            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                metadata = item["metadata"]

                image_url = (
                    f"{API_BASE}/static/"
                    f"{metadata['category']}/"
                    f"{metadata['image_name']}"
                )

                st.image(
                    image_url,
                    use_container_width=True
                )

                score = item.get("rerank_score", item.get("score", 0.0))

                st.markdown(
                    f"<div class='score'><b>Score:</b> {score:.3f}</div>",
                    unsafe_allow_html=True
                )

                st.write(metadata["short_description"])

                st.markdown("</div>", unsafe_allow_html=True)
