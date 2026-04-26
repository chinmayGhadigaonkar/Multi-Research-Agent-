import streamlit as st
from pipeline import run_research_pipeline

# Page config
st.set_page_config(page_title="Research Agent", page_icon="🔍", layout="centered")

# Title & description
st.title("🔍 Multi Research Agent")
st.markdown("Get AI-powered research reports in seconds.")

# Card-like container
with st.container():
    st.subheader("Enter your topic")
    
    topic = st.text_input(
    label="Research Topic",
    placeholder="e.g. Future of AI in healthcare...",
    label_visibility="collapsed"
    )

    run_btn = st.button("🚀 Run Research")

# Run only when button clicked
if run_btn and topic:
    with st.spinner("Running research... please wait ⏳"):
        result = run_research_pipeline(topic=topic)

    st.success("Research completed ✅")

    # Tabs for better UI
    tab1, tab2 = st.tabs(["📄 Report", "💡 Feedback"])

    with tab1:
        st.markdown("### Research Report")
        st.write(result["report"])

    with tab2:
        st.markdown("### Feedback")
        st.write(result["feedback"])

elif run_btn and not topic:
    st.warning("Please enter a topic first ⚠️")