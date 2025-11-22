import streamlit as st
from style import apply_greptile_style

st.set_page_config(
    page_title="AgriGuard - AI Plant Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(apply_greptile_style(), unsafe_allow_html=True)

st.sidebar.title("🌿 AgriGuard")
st.sidebar.markdown("AI-Powered Plant Disease Detection")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Detection", "About", "Help"]
)

if page == "Detection":
    st.title("Plant Disease Detection")
    st.markdown("Upload a leaf image to analyze its health status and receive agricultural recommendations.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a leaf image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo of a plant leaf"
        )

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

            if st.button("Analyze Image", use_container_width=True):
                with st.spinner("Analyzing..."):
                    st.success("Analysis complete!")

    with col2:
        st.subheader("Results")

        if uploaded_file is not None:
            st.info("Upload an image and click 'Analyze Image' to see results here.")
        else:
            st.info("Please upload an image to begin analysis.")

        st.markdown("---")
        st.subheader("Sample Predictions")

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Confidence", "0%")
        with col_b:
            st.metric("Status", "Pending")

elif page == "About":
    st.title("About AgriGuard")
    st.markdown("""
    AgriGuard is an AI-powered plant disease detection system designed to help farmers
    and agricultural professionals identify plant diseases early and take preventive action.

    ### Features
    - **Image Classification**: Analyze leaf photos to detect diseases
    - **Health Status**: Determine if crops are Healthy or Diseased
    - **Recommendations**: Receive actionable agricultural advice
    - **Mobile Ready**: Optimized for deployment on edge devices

    ### Technology
    Built with deep learning and computer vision to provide accurate,
    real-time disease detection suitable for field use.
    """)

elif page == "Help":
    st.title("How to Use AgriGuard")

    with st.expander("📸 Taking Photos", expanded=True):
        st.markdown("""
        - Take clear, well-lit photos of leaves
        - Ensure the leaf fills most of the frame
        - Avoid blurry or dark images
        - Capture both sides if possible
        """)

    with st.expander("🔍 Getting Results"):
        st.markdown("""
        - Upload your image using the file uploader
        - Click the 'Analyze Image' button
        - View the disease classification and confidence score
        - Read the agricultural recommendations
        """)

    with st.expander("💡 Best Practices"):
        st.markdown("""
        - Use images taken in natural lighting
        - Ensure leaves are dry and clearly visible
        - Include any visible symptoms in the frame
        - Regular monitoring provides best results
        """)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
st.sidebar.metric("Analyses Today", "0")
st.sidebar.metric("Accuracy Rate", "0%")
