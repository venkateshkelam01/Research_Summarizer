import streamlit as st
import requests
import os
import time

# Base API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")
api_url = f"{API_URL}/api/summarize"

st.set_page_config(
    page_title="Research Summarizer AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- MODERN STYLING -------------------
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeInDown 1s ease-in-out;
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #a8b2d1;
        margin-bottom: 2rem;
        animation: fadeInUp 1.2s ease-in-out;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 1rem 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    /* Styled Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        color: white;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #a8b2d1;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Paper Card */
    .paper-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .paper-card:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: translateX(5px);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(15, 12, 41, 0.8);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(72, 187, 120, 0.1);
        border-left: 4px solid #48bb78;
    }
    
    .stError {
        background: rgba(245, 101, 101, 0.1);
        border-left: 4px solid #f56565;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        font-weight: 600;
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    
    st.markdown("#### 🎨 About")
    st.markdown("""
    This AI-powered tool helps you quickly understand cutting-edge research by:
    - 📚 Fetching papers from ArXiv
    - 🤖 Generating deep summaries
    - 📊 Extracting key insights
    - 🔍 Identifying research gaps
    """)
    
    st.markdown("---")
    st.markdown("#### 📊 Statistics")
    if 'search_count' not in st.session_state:
        st.session_state.search_count = 0
    st.metric("Searches Performed", st.session_state.search_count)
    
    st.markdown("---")
    st.markdown("#### 💡 Tips")
    st.info("""
    **Pro Tips:**
    - Use specific terms for better results
    - Start with 5 papers for quick overview
    - Increase to 10-12 for comprehensive analysis
    """)
    
    st.markdown("---")
    st.markdown("##### 🔗 Links")
    st.markdown("[📖 Documentation](https://github.com) | [⭐ Star on GitHub](https://github.com)")

# ------------------- HEADER -------------------
st.markdown('<div class="hero-title">🔬 Research Summarizer AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Unlock insights from academic research papers using AI-powered analysis</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------- INPUTS -------------------
col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "🔍 Research Topic",
        placeholder="e.g., Federated Learning, Quantum Computing, CRISPR Gene Editing...",
        help="Enter any research topic you want to explore"
    )

with col2:
    n_papers = st.slider(
        "📚 Number of Papers",
        min_value=3,
        max_value=15,
        value=5,
        help="More papers = deeper analysis but slower processing"
    )

# ------------------- SUBMIT -------------------
st.markdown("<br>", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generate_btn = st.button("🚀 Generate AI Summary", use_container_width=True)

if generate_btn and topic:
    st.session_state.search_count += 1
    
    # Progress bar with stages
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Stage 1: Fetching papers
        status_text.markdown("### 📡 Fetching research papers from ArXiv...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        # Stage 2: Processing
        status_text.markdown("### 🤖 AI is analyzing papers...")
        progress_bar.progress(50)
        
            resp = requests.post(
                api_url,
                json={"query": topic, "n_papers": n_papers, "sources": ["arxiv"]},
                timeout=180
            )

            if resp.status_code != 200:
            st.error(f"❌ Server Error: {resp.text}")
                st.stop()

        # Stage 3: Generating summary
        status_text.markdown("### ✨ Generating comprehensive summary...")
        progress_bar.progress(75)
        time.sleep(0.5)

        data = resp.json()
        summary = data.get("summary", {}) or {}
        scores = data.get("eval", {}) or {}
        papers = data.get("papers", []) or []

        # Stage 4: Complete
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        
        st.balloons()
        st.success(f"✅ Successfully analyzed {len(papers)} research papers on **{topic}**!")

        st.markdown("<br>", unsafe_allow_html=True)

            # ------------------- TABS -------------------
        tab_summary, tab_details, tab_papers, tab_insights = st.tabs(
            ["📘 Summary", "🔬 Details & Findings", "📚 Papers", "💡 Insights"]
            )

            # ===== TAB: SUMMARY =====
            with tab_summary:
                st.markdown('<div class="section-header">📊 Quality Metrics</div>', unsafe_allow_html=True)
                
                # Evaluation metrics with improved styling
                col1, col2, col3, col4 = st.columns(4)
                
                metrics = [
                    ("Overall Score", scores.get('overall', 0), "🎯"),
                    ("Coverage", scores.get('coverage', 0), "📊"),
                    ("Depth", scores.get('depth', 0), "🔍"),
                    ("Structure", scores.get('structure', 0), "📐")
                ]
                
                for col, (label, value, icon) in zip([col1, col2, col3, col4], metrics):
                    with col:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div style="font-size: 2rem;">{icon}</div>
                            <div style="font-size: 2rem; font-weight: 700; color: #667eea; margin: 0.5rem 0;">
                                {value:.1f}
                            </div>
                            <div style="color: #a8b2d1; font-size: 0.9rem;">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)

                # Deep paragraphs with glass morphism
                st.markdown('<div class="section-header">📘 Comprehensive Summary</div>', unsafe_allow_html=True)
                
                paragraphs = summary.get("paragraphs", [])
                if paragraphs:
                    for i, p in enumerate(paragraphs, 1):
                        st.markdown(f"""
                        <div class="glass-card">
                            <h4 style="color: #667eea; margin-bottom: 1rem;">Section {i}</h4>
                            <p style="color: #ccd6f6; line-height: 1.8; font-size: 1rem;">{p}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No summary paragraphs available.")

            # ===== TAB: DETAILS =====
            with tab_details:
                mapping = {
                "🔬 Key Findings": ("key_findings", "#667eea"),
                "🧪 Methods & Approaches": ("methods", "#48bb78"),
                "✨ What's New": ("whats_new", "#ed8936"),
                "🧩 Open Problems": ("open_problems", "#f56565"),
                "⚠️ Limitations": ("limitations", "#ecc94b"),
                "🚀 Future Research Directions": ("future_work", "#9f7aea"),
            }

            for title, (key, color) in mapping.items():
                items = summary.get(key, [])
                if items:
                    st.markdown(f'<div class="section-header" style="color: {color};">{title}</div>', unsafe_allow_html=True)
                    
                    for i, item in enumerate(items, 1):
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 4px solid {color};">
                            <p style="color: #ccd6f6; line-height: 1.6;">
                                <strong style="color: {color};">{i}.</strong> {item}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
            
            if not any(summary.get(key, []) for _, (key, _) in mapping.items()):
                st.info("Detailed analysis is not available in mock mode. Use a real LLM provider for comprehensive insights.")

            # ===== TAB: PAPERS =====
            with tab_papers:
            st.markdown('<div class="section-header">⭐ Top Recommended Papers</div>', unsafe_allow_html=True)
            
            top_papers = summary.get("top5_papers", [])
            if top_papers and top_papers[0].get('title') != 'Mock':
                for i, paper in enumerate(top_papers, 1):
                    st.markdown(f"""
                    <div class="paper-card">
                        <div style="color: #667eea; font-weight: 700; margin-bottom: 0.5rem;">
                            #{i} RECOMMENDED
                        </div>
                        <h3 style="color: #ccd6f6; margin-bottom: 0.5rem;">
                            <a href="{paper.get('url')}" target="_blank" style="color: #667eea; text-decoration: none;">
                                {paper.get('title')} 🔗
                            </a>
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📚 All Retrieved Papers ({} total)</div>'.format(len(papers)), unsafe_allow_html=True)
            
            for i, paper in enumerate(papers, 1):
                with st.expander(f"📄 Paper {i}: {paper.get('title', 'Untitled')}", expanded=(i==1)):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="glass-card">
                            <h4 style="color: #667eea; margin-bottom: 1rem;">
                                {paper.get('title', 'Untitled')}
                            </h4>
                            <p style="color: #a8b2d1; margin-bottom: 0.5rem;">
                                <strong>👥 Authors:</strong> {', '.join(paper.get('authors', [])[:5])}
                                {'...' if len(paper.get('authors', [])) > 5 else ''}
                            </p>
                            <p style="color: #a8b2d1; margin-bottom: 1rem;">
                                <strong>📅 Year:</strong> {paper.get('year', 'N/A')} | 
                                <strong>📌 Source:</strong> {paper.get('source', 'ArXiv').upper()}
                            </p>
                            <p style="color: #ccd6f6; line-height: 1.6; margin-bottom: 1rem;">
                                <strong style="color: #667eea;">Abstract:</strong><br>
                                {paper.get('abstract', 'No abstract available.')[:500]}
                                {'...' if len(paper.get('abstract', '')) > 500 else ''}
                            </p>
                            <a href="{paper.get('url', '#')}" target="_blank" 
                               style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                      color: white; padding: 0.5rem 1rem; border-radius: 8px; 
                                      text-decoration: none; display: inline-block; font-weight: 600;">
                                🔗 Read Full Paper
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 1rem;">
                            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📄</div>
                            <div style="color: #667eea; font-weight: 700; font-size: 2rem;">
                                #{i}
                            </div>
                            <div style="color: #a8b2d1; font-size: 0.9rem;">
                                of {len(papers)}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        # ===== TAB: INSIGHTS =====
        with tab_insights:
            st.markdown('<div class="section-header">💡 Quick Insights</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color: #667eea; margin-bottom: 1rem;">📊 Research Landscape</h3>
                    <p style="color: #ccd6f6; line-height: 1.6;">
                        This analysis covers <strong style="color: #667eea;">{}</strong> research papers
                        on the topic of <strong style="color: #667eea;">"{}"</strong>.
                    </p>
                    <br>
                    <p style="color: #a8b2d1;">
                        📅 Publication Years: {} - {}<br>
                        👥 Total Authors: {} (approx)<br>
                        🌐 Source: ArXiv Database
                    </p>
                </div>
                """.format(
                    len(papers),
                    topic,
                    min((p.get('year', 2024) for p in papers if p.get('year')), default=2024),
                    max((p.get('year', 2024) for p in papers if p.get('year')), default=2024),
                    sum(len(p.get('authors', [])) for p in papers)
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color: #48bb78; margin-bottom: 1rem;">🎯 Summary Stats</h3>
                    <p style="color: #ccd6f6; line-height: 1.6;">
                        Generated {} summary sections with comprehensive analysis
                        of current research trends and future directions.
                    </p>
                    <br>
                    <p style="color: #a8b2d1;">
                        ✨ What's New: {} insights<br>
                        🧩 Open Problems: {} identified<br>
                        🚀 Future Directions: {} suggested
                    </p>
                </div>
                """.format(
                    len(summary.get("paragraphs", [])),
                    len(summary.get("whats_new", [])),
                    len(summary.get("open_problems", [])),
                    len(summary.get("future_work", []))
                ), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Word cloud placeholder
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #9f7aea; margin-bottom: 1rem;">🔑 Key Takeaways</h3>
                <ul style="color: #ccd6f6; line-height: 2;">
                    <li>This research area is <strong style="color: #667eea;">actively evolving</strong> with {} recent papers</li>
                    <li>Multiple research groups are working on <strong style="color: #667eea;">innovative solutions</strong></li>
                    <li>Significant <strong style="color: #48bb78;">opportunities exist</strong> for future research</li>
                    <li>The field shows <strong style="color: #ed8936;">high collaboration</strong> among researchers</li>
                </ul>
            </div>
            """.format(len(papers)), unsafe_allow_html=True)

        except requests.exceptions.Timeout:
        progress_bar.empty()
        status_text.empty()
            st.error("❌ Request timed out. Try again or reduce the number of papers.")
        except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"⚠️ Error: {str(e)}")
        st.exception(e)

elif generate_btn and not topic:
    st.warning("⚠️ Please enter a research topic first!")
else:
    # Welcome screen when no search has been made
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔬</div>
            <h2 style="color: #667eea; margin-bottom: 1rem;">Ready to Explore Research?</h2>
            <p style="color: #a8b2d1; font-size: 1.1rem; line-height: 1.8;">
                Enter a research topic above and click <strong>Generate AI Summary</strong>
                to get started with AI-powered research analysis.
            </p>
            <br>
            <p style="color: #8892b0;">
                💡 Try topics like: <em>Machine Learning, Quantum Computing, 
                Blockchain, CRISPR, Neural Networks</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------- FOOTER -------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; 
     border-top: 1px solid rgba(102, 126, 234, 0.2);">
    <p style="color: #8892b0; font-size: 0.9rem; margin-bottom: 0.5rem;">
        Built with ❤️ using <strong style="color: #667eea;">Streamlit</strong> & 
        <strong style="color: #667eea;">FastAPI</strong>
    </p>
    <p style="color: #8892b0; font-size: 0.85rem;">
        🤖 Powered by OpenAI GPT · Ollama · ArXiv API
    </p>
    <p style="color: #495670; font-size: 0.8rem; margin-top: 1rem;">
        © 2025 Research Summarizer AI · All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)
