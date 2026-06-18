import streamlit as st
import re
import nltk
import fitz
from nltk.corpus import stopwords
from collections import Counter

# Import modules
from modules.summarizer import generate_summary
from modules.reviewer import generate_review
from modules.score_parser import extract_score, extract_all_scores
from modules.report_generator import generate_pdf_report, generate_text_report
from modules.recommendation_parser import extract_recommendation_simple
from modules.domain_classifier import classify_domain_simple
from modules.problem_extractor import extract_problem_statement
from modules.contribution_extractor import extract_contributions
from modules.entity_extractor import extract_entities
from modules.arxiv_retriever import search_arxiv
from modules.rag_ranker import rank_papers
from modules.analytics import (
    create_radar_chart,
    create_keyword_frequency_chart,
    create_domain_distribution_chart,
    create_recommendation_summary_chart,
    create_metrics_summary
)

# ============================================
# CONFIGURATION & SETUP
# ============================================

st.set_page_config(
    page_title="AI Conference Paper Reviewer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# NLTK Setup
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

# ============================================
# HELPER FUNCTIONS
# ============================================

def preprocess_text(text):
    """Preprocess text: lowercase, remove punctuation, remove stopwords"""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    stop_words = set(stopwords.words("english"))
    tokens = [w for w in tokens if w not in stop_words and len(w) > 2]
    return " ".join(tokens)

def extract_keywords(clean_text):
    """Extract meaningful keywords from preprocessed text"""
    blacklist = {
        "group", "training", "models", "paper", "approach", "research", 
        "results", "model", "using", "method", "methods", "study", 
        "learning", "arxiv", "figure", "table", "data", "section",
        "proposed", "introduction", "methodology", "conclusion", "framework"
    }
    
    words = [w for w in clean_text.split() if len(w) > 3 and w not in blacklist]
    common_words = Counter(words)
    return [word for word, count in common_words.most_common(10)]

@st.cache_data
def extract_pdf_text(uploaded_file):
    """Extract text and page count from PDF"""
    text = ""
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(pdf)
    for page in pdf:
        text += page.get_text("text")
    return text, total_pages

@st.cache_data
def extract_sections(text):
    """Extract paper sections using regex patterns"""
    sections = {
        "Abstract": "",
        "Introduction": "",
        "Methodology": "",
        "Results": "",
        "Conclusion": ""
    }

    try:
        # ABSTRACT
        abstract_patterns = [r"abstract(.*?)(keywords|index terms|1\.|i\.|introduction)"]
        for pattern in abstract_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections["Abstract"] = match.group(1)[:3000]
                break

        # INTRODUCTION
        intro_patterns = [r"(introduction)(.*?)(related work|background|preliminaries|methodology|approach|method)"]
        for pattern in intro_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections["Introduction"] = match.group(2)[:3000]
                break

        # METHODOLOGY
        method_patterns = [
            r"(4\.\s*Methodology Used)(.*?)(5\.\s*Main Results)",
            r"(Methodology Used)(.*?)(Main Results)",
            r"(Methodology)(.*?)(Results)"
        ]
        for pattern in method_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections["Methodology"] = match.group(2)[:3000]
                break

        # RESULTS
        result_patterns = [
            r"(5\.\s*Main Results)(.*?)(6\.\s*Conclusion)",
            r"(results and discussion)(.*?)(conclusion)",
            r"(results)(.*?)(conclusion)",
            r"(evaluation)(.*?)(conclusion)",
            r"(experiments)(.*?)(conclusion)"
        ]
        for pattern in result_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections["Results"] = match.group(2)[:3000]
                break

        # CONCLUSION
        conclusion_patterns = [r"(conclusion|future work)(.*)"]
        for pattern in conclusion_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections["Conclusion"] = match.group(2)[:3000]
                break

    except Exception as e:
        st.error(f"Error extracting sections: {e}")

    return sections

@st.cache_data
def get_related_papers(query):
    """Retrieve related papers from arXiv"""
    return search_arxiv(query, max_results=5)

# ============================================
# HEADER SECTION
# ============================================

st.markdown("""
<div style="text-align:center; margin-bottom:-10px;">
""", unsafe_allow_html=True)

st.image("assets/logo.png", width=150)

st.markdown("""
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-title">
📄 AI Conference Paper Reviewer
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-subtitle">
Intelligent Analysis • Automated Reviews • Research Insights • AI-Powered Evaluation
</div>
""", unsafe_allow_html=True)

# ============================================
# FILE UPLOAD SECTION
# ============================================

st.markdown("""
<div class="glass-card center-card">
<h2>Upload Your Research Paper</h2>
<p>Supported formats: IEEE • Springer • arXiv</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

# ============================================
# MAIN PROCESSING
# ============================================

if uploaded_file is not None:
    current_file = uploaded_file.name

    # Session state management
    if "last_file" not in st.session_state:
        st.session_state.last_file = current_file
    elif st.session_state.last_file != current_file:
        st.session_state.problem_statement = ""
        st.session_state.contributions = ""
        st.session_state.summary = ""
        st.session_state.review = ""
        st.session_state.last_file = current_file

    # Extract PDF content
    text, total_pages = extract_pdf_text(uploaded_file)

    st.success("✅ Paper uploaded successfully!")

    st.markdown("""
    <div class="glass-card center-card">
    <h3>Processing Complete</h3>
    <p>Your paper is ready for summary, review, and analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # ANALYTICS & STATISTICS
    # ============================================

    original_words = len(text.split())
    clean_text = preprocess_text(text)
    research_domain = classify_domain_simple(text)
    keywords = extract_keywords(clean_text)
    processed_words = len(clean_text.split())
    
    search_query = " ".join(keywords[:5]) if keywords else research_domain
    retrieved_papers = get_related_papers(search_query)
    top_papers = rank_papers(text, retrieved_papers)
    entities = extract_entities(text)
    sections = extract_sections(text)

    reduction_percentage = round(((original_words - processed_words) / original_words) * 100, 2) if original_words > 0 else 0

    st.markdown("""
    <div class="section-title">
    📊 Paper Overview
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h2>{total_pages}</h2>
        <p>Pages</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h2>{original_words:,}</h2>
        <p>Words</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <h2>{processed_words:,}</h2>
        <p>Processed</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{research_domain}</h3>
        <p>Domain</p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # TABS: SUMMARY, REVIEW, ANALYTICS
    # ============================================

    st.markdown("""
    <div class="section-title">
    🚀 Analysis & Insights
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 Summary", "📝 Review", "📊 Analytics"])

    # ---- TAB 1: SUMMARY ----
    with tab1:
        if "problem_statement" not in st.session_state:
            st.session_state.problem_statement = ""
        if "contributions" not in st.session_state:
            st.session_state.contributions = ""
        if "summary" not in st.session_state:
            st.session_state.summary = ""

        if st.session_state.problem_statement:
            st.markdown(f"""
            <div class="glass-card">
            <h3>🎯 Problem Statement</h3>
            <p>{st.session_state.problem_statement}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.contributions:
            st.markdown(f"""
            <div class="glass-card">
            <h3>🚀 Research Contributions</h3>
            <p>{st.session_state.contributions}</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("📋 Generate Summary")
        if st.button("🔍 Generate AI Summary", key="summary_btn"):
            with st.spinner("Analyzing paper and generating summary..."):
                st.session_state.problem_statement = extract_problem_statement(text)
                st.session_state.contributions = extract_contributions(text)
                st.session_state.summary = generate_summary(sections)

        if st.session_state.summary:
            st.markdown("""
            <div class="glass-card">
            <h3>📝 Summary</h3>
            </div>
            """, unsafe_allow_html=True)
            st.write(st.session_state.summary)

    # ---- TAB 2: REVIEW ----
    with tab2:
        st.subheader("📝 Conference Review")
        if "review" not in st.session_state:
            st.session_state.review = ""

        if st.button("⚖️ Generate Review", key="review_btn"):
            with st.spinner("Generating conference review..."):
                retrieved_context = "\n\n".join([f"{paper['title']}\n{paper['summary']}" for paper in top_papers])
                st.session_state.review = generate_review(sections, retrieved_context)

        if st.session_state.review:
            review = st.session_state.review
            clean_review = re.sub(r"Novelty Score:.*?Detailed Review:", "Detailed Review:", review, flags=re.DOTALL)

            st.subheader("📋 Reviewer Report")
            st.write(clean_review)

            # Scoring metrics
            c1, c2, c3, c4 = st.columns(4)
            novelty = extract_score(review, "Novelty Score")
            technical = extract_score(review, "Technical Quality Score")
            clarity = extract_score(review, "Clarity Score")
            significance = extract_score(review, "Significance Score")

            with c1:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{novelty}/10</h2>
                <p>Novelty</p>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{technical}/10</h2>
                <p>Technical Quality</p>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{clarity}/10</h2>
                <p>Clarity</p>
                </div>
                """, unsafe_allow_html=True)

            with c4:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{significance}/10</h2>
                <p>Significance</p>
                </div>
                """, unsafe_allow_html=True)

            # Overall score
            overall_score = (novelty + technical + clarity + significance) / 4
            st.subheader("🏆 Overall Score")

            if overall_score >= 8:
                st.success(f"⭐ Overall Score: {overall_score:.1f}/10")
            elif overall_score >= 6:
                st.warning(f"✓ Overall Score: {overall_score:.1f}/10")
            else:
                st.error(f"✗ Overall Score: {overall_score:.1f}/10")

            st.progress(overall_score / 10)

            # Recommendation
            recommendation = extract_recommendation_simple(review)
            st.subheader("📌 Decision")

            if recommendation == "Accept":
                st.success("✅ ACCEPT")
            elif recommendation == "Minor Revision":
                st.warning("🟡 MINOR REVISION REQUIRED")
            elif recommendation == "Major Revision":
                st.warning("🟠 MAJOR REVISION REQUIRED")
            elif recommendation == "Reject":
                st.error("❌ REJECT")
            else:
                st.info("Unable to determine recommendation")

            # Export reports
            st.markdown("""
            <div class="glass-card center-card">
            <h3>📥 Export Reports</h3>
            <p>Download your review in multiple formats</p>
            </div>
            """, unsafe_allow_html=True)

            # Prepare metadata
            metadata = {
                "Pages": total_pages,
                "Words": f"{original_words:,}",
                "Domain": research_domain,
                "Generated": "AI Conference Paper Reviewer"
            }
            
            # Prepare scores dict
            scores_dict = {
                "novelty": novelty,
                "technical": technical,
                "clarity": clarity,
                "significance": significance
            }
            
            # Generate text report
            text_report = generate_text_report(
                review,
                recommendation,
                scores=scores_dict,
                metadata=metadata
            )
            
            st.download_button(
                label="📥 Download Text Report",
                data=text_report,
                file_name="review_report.txt",
                mime="text/plain"
            )

            # Generate PDF report
            try:
                pdf_filename = "review_report.pdf"
                generate_pdf_report(
                    pdf_filename,
                    clean_review,
                    recommendation,
                    scores=scores_dict
                )
                with open(pdf_filename, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_file,
                        file_name="review_report.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.warning(f"⚠️ PDF generation note: {str(e)}")


    # ---- TAB 3: ANALYTICS ----
    with tab3:
        # Create two columns for layout
        analytics_col1, analytics_col2 = st.columns([2, 1])
        
        with analytics_col1:
            st.subheader("📊 Paper Analysis Dashboard")
            
            # Display metrics if review exists
            if st.session_state.get("review"):
                st.markdown("""
                <div class="glass-card">
                <h4>📈 Analysis Metrics</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Create metrics columns
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric("Pages", total_pages)
                
                with metric_col2:
                    st.metric("Domain", research_domain)
                
                with metric_col3:
                    st.metric("Entities", len(entities) if entities else 0)
                
                with metric_col4:
                    try:
                        overall_score = (novelty + technical + clarity + significance) / 4
                        st.metric("Overall Score", f"{overall_score:.1f}/10")
                    except:
                        st.metric("Overall Score", "—")
                
                # Scores Radar Chart
                st.markdown("""
                <div class="glass-card">
                <h4>🎯 Score Analysis</h4>
                </div>
                """, unsafe_allow_html=True)
                
                scores_for_radar = {
                    "Novelty": novelty,
                    "Technical Quality": technical,
                    "Clarity": clarity,
                    "Significance": significance
                }
                
                try:
                    radar_fig = create_radar_chart(scores_for_radar, "Comprehensive Score Analysis")
                    st.plotly_chart(radar_fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not generate radar chart: {e}")
                
                # Keyword Analysis
                if text:
                    st.markdown("""
                    <div class="glass-card">
                    <h4>🔑 Keyword Frequency</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        keyword_fig = create_keyword_frequency_chart(text, top_n=12)
                        st.plotly_chart(keyword_fig, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not generate keyword chart: {e}")
            
            else:
                st.info("👆 Upload a paper and generate a review to see analytics")
        
        with analytics_col2:
            st.markdown("""
            <div class="glass-card">
            <h4>📋 Quick Info</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.get("review"):
                st.markdown(f"**Domain:** {research_domain}")
                st.markdown(f"**Pages:** {total_pages}")
                st.markdown(f"**Words (Original):** {original_words:,}")
                st.markdown(f"**Entities Found:** {len(entities) if entities else 0}")
                st.markdown(f"**Related Papers:** {len(top_papers)}")
                
                # Recommendation badge
                rec_color_map = {
                    "Accept": "✅ green",
                    "Minor Revision": "🟡 orange",
                    "Major Revision": "🟠 red",
                    "Reject": "❌ darkred"
                }
                
                try:
                    recommendation = extract_recommendation_simple(st.session_state.review)
                    st.markdown(f"**Recommendation:** {recommendation}")
                except:
                    pass
        
        # Related Research Section
        st.divider()
        st.subheader("📚 Related Research")
        
        if top_papers:
            st.markdown("""
            <div class="glass-card">
            <p>Found <strong>{}</strong> related papers on arXiv</p>
            </div>
            """.format(len(top_papers)), unsafe_allow_html=True)
            
            for idx, paper in enumerate(top_papers, 1):
                st.markdown(f"**{idx}. {paper['title']}**")
                with st.expander("View Summary"):
                    st.write(paper['summary'][:500] + "...")
                    if paper.get('authors'):
                        st.markdown(f"**Authors:** {paper['authors']}")
                    st.markdown(f"[📖 Read Full Paper]({paper['url']})")
                st.divider()
        else:
            st.info("📖 No related papers found yet. Upload a paper and generate a review to see related research.")
        
        # Text Statistics Section
        st.divider()
        st.subheader("📊 Text Statistics")
        
        if text:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Pages", total_pages)
            
            with col2:
                st.metric("Original Words", f"{original_words:,}")
            
            with col3:
                st.metric("Processed Words", f"{processed_words:,}")
            
            with col4:
                st.metric("Reduction", f"{reduction_percentage}%")
            
            # Entities
            if entities:
                st.markdown("""
                <div class="glass-card">
                <h4>🏷️ Detected Entities (Top 10)</h4>
                </div>
                """, unsafe_allow_html=True)
                
                entity_cols = st.columns(5)
                for i, entity in enumerate(entities[:10]):
                    with entity_cols[i % 5]:
                        st.markdown(f"""
                        <div class="metric-card">
                        <p style="font-size: 12px; word-break: break-word;">{entity}</p>
                        </div>
                        """, unsafe_allow_html=True)

        # Keywords
        st.subheader("🔑 Top Keywords")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Vocabulary Size", len(set(clean_text.split())))

        with col2:
            st.metric("Total Processed Words", processed_words)

        word_freq = Counter(clean_text.split())
        top_keywords = word_freq.most_common(10)

        st.write("#### Top Terms")
        for word, count in top_keywords:
            st.write(f"• **{word}** ({count})")

        # Sections breakdown
        st.subheader("📑 Paper Sections")
        for section_name, section_content in sections.items():
            if section_content:
                with st.expander(section_name):
                    st.write(section_content[:2000])

        st.subheader("📈 Section Statistics")
        available_sections = {
            name: len(content.split())
            for name, content in sections.items()
            if content
        }

        if available_sections:
            cols = st.columns(len(available_sections))
            for i, (name, count) in enumerate(available_sections.items()):
                cols[i].metric(name, f"{count} words")

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:40px 20px; color:#64748b;'>
<p><strong>AI Conference Paper Reviewer</strong></p>
<p>Powered by: SpaCy • NLP • RAG • OpenRouter • Streamlit</p>
<p style="font-size:0.9rem; margin-top:20px;">© 2026 • Making Research Review Intelligent</p>
</div>
""", unsafe_allow_html=True)
