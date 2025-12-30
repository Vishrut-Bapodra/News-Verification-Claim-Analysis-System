import streamlit as st
from main import verify_article

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(
    page_title="Agentic News Verification System",
    layout="wide"
)

st.title("📰 Agentic News Verification System")
st.write(
    "Analyze a news article using multi-step reasoning, "
    "claim verification, bias analysis, and evidence grounding."
)

# -----------------------
# Input Section
# -----------------------
article_url = st.text_input(
    "Enter a news article URL",
    placeholder="https://example.com/news/article"
)

verify_btn = st.button("Verify Article")

# -----------------------
# Run Verification
# -----------------------
if verify_btn:
    if not article_url.strip():
        st.warning("Please enter a valid article URL.")
    else:
        with st.spinner("Analyzing article... this may take a moment"):
            result = verify_article(article_url)

        if "error" in result:
            st.error(result.get("error"))
            if "details" in result:
                st.write(result["details"])
        else:
            # -----------------------
            # Results Display
            # -----------------------

            st.success("Analysis completed")

            # Article Info
            st.subheader("🔗 Article")
            st.write(result.get("article_url"))

            # -----------------------
            # Claim Verification
            # -----------------------
            st.subheader("📌 Claim-by-Claim Verification")

            claims = result.get("claims", [])
            if not claims:
                st.info("No clear factual claims were extracted.")
            else:
                for idx, item in enumerate(claims, start=1):
                    with st.expander(f"Claim {idx}"):
                        st.write("**Claim:**")
                        st.write(item.get("claim"))

                        st.write("**Analysis:**")
                        st.write(item.get("analysis"))

                        sources = item.get("sources", [])
                        if sources:
                            st.write("**Sources:**")
                            for src in sources:
                                st.markdown(
                                    f"- [{src.get('title')}]({src.get('url')})"
                                )
                        else:
                            st.write("No external sources found.")

            # -----------------------
            # Bias Analysis
            # -----------------------
            st.subheader("⚠️ Bias & Sensationalism Analysis")
            bias = result.get("bias_analysis", {})
            st.write(bias.get("analysis", "No bias analysis available."))

            # -----------------------
            # Final Assessment
            # -----------------------
            st.subheader("📊 Final Confidence & Explanation")
            st.write(result.get("final_assessment"))
