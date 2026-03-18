import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

st.set_page_config(
    page_title="Credit Risk Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0a0f1e; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0d1526;
        border-right: 1px solid #1e3a5f;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #0d1f3c;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        padding: 20px;
    }
    [data-testid="stMetricLabel"] { color: #7a9cc4 !important; font-size: 13px !important; }
    [data-testid="stMetricValue"] { color: #e8f4fd !important; font-size: 28px !important; font-weight: 700 !important; }
    
    /* Headers */
    h1 { color: #e8f4fd !important; font-size: 2rem !important; font-weight: 700 !important; }
    h2 { color: #e8f4fd !important; font-size: 1.3rem !important; }
    h3 { color: #7a9cc4 !important; font-size: 1rem !important; }
    
    /* Sidebar text */
    .css-1d391kg, [data-testid="stSidebar"] * { color: #a8c5e0 !important; }
    
    /* Divider */
    hr { border-color: #1e3a5f !important; }

    /* Caption */
    .stCaption { color: #4a7a9b !important; }

    /* Radio buttons */
    .stRadio label { color: #a8c5e0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Chart style ───────────────────────────────────────────
def set_chart_style():
    mpl.rcParams.update({
        'figure.facecolor': '#0d1f3c',
        'axes.facecolor': '#0d1f3c',
        'axes.edgecolor': '#1e3a5f',
        'axes.labelcolor': '#7a9cc4',
        'text.color': '#a8c5e0',
        'xtick.color': '#7a9cc4',
        'ytick.color': '#7a9cc4',
        'grid.color': '#1e3a5f',
        'grid.alpha': 0.5,
        'font.family': 'sans-serif',
        'font.size': 11,
    })

set_chart_style()

# ── Load data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    ecl = pd.read_csv(r"output/ecl_by_grade.csv")
    vintage = pd.read_csv(r"output/vintage_analysis.csv")
    stress = pd.read_csv(r"output/stress_scenarios.csv")
    summary = pd.read_csv(r"output/portfolio_summary.csv")
    return ecl, vintage, stress, summary

ecl_df, vintage_df, stress_df, summary_df = load_data()

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Credit Risk Analytics")
    st.markdown("*Lending Club Portfolio 2007–2018*")
    st.markdown("---")
    page = st.radio("Navigation", [
        "Portfolio Overview",
        "Vintage Analysis",
        "Stress Testing",
        "Data Tables"
    ])
    st.markdown("---")
    st.markdown("**Dataset**")
    st.markdown("2.26M loans · $29.7B EAD")
    st.markdown("**Framework**")
    st.markdown("IFRS 9 · Basel III")

# ── PAGE 1 ────────────────────────────────────────────────
if page == "Portfolio Overview":
    st.markdown("# Portfolio Overview")
    st.caption("Expected Credit Loss analysis across 2.26 million Lending Club loans")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Loans", f"{int(summary_df['Total Loans'][0]):,}")
    col2.metric("Total EAD", f"${summary_df['Total EAD ($B)'][0]}B")
    col3.metric("Total ECL", f"${summary_df['Total ECL ($B)'][0]}B")
    col4.metric("Portfolio ECL %", f"{summary_df['Portfolio ECL %'][0]}%")

    st.markdown("---")
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("### ECL by Loan Grade")
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.barh(ecl_df['grade'], ecl_df['total_ECL'] / 1e9,
                       color='#1a6ab5', edgecolor='#2a8fd4', linewidth=0.5)
        ax.bar_label(bars, fmt='$%.2fB', padding=4, color='#a8c5e0', fontsize=10)
        ax.set_xlabel("ECL ($ Billions)")
        ax.set_ylabel("Loan Grade")
        ax.grid(axis='x', alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig)

    with col6:
        st.markdown("### Probability of Default by Grade")
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        colors = ['#1a6ab5','#2080cc','#f0a500','#e07b00','#d94f3d','#b83228','#8b1a1a']
        bars2 = ax2.bar(ecl_df['grade'], ecl_df['PD'], color=colors,
                        edgecolor='#0a0f1e', linewidth=0.5)
        ax2.bar_label(bars2, fmt='%.1f%%', padding=3, color='#a8c5e0', fontsize=10)
        ax2.set_xlabel("Loan Grade")
        ax2.set_ylabel("PD (%)")
        ax2.grid(axis='y', alpha=0.3)
        fig2.tight_layout()
        st.pyplot(fig2)

# ── PAGE 2 ────────────────────────────────────────────────
elif page == "Vintage Analysis":
    st.markdown("# Vintage Analysis")
    st.caption("Performance of loan cohorts by origination year")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Default Rate by Issue Year")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(vintage_df['issue_year'], vintage_df['default_rate'],
                marker='o', color='#e05c5c', linewidth=2.5, markersize=6)
        ax.axvline(x=2008, color='#f0a500', linestyle='--',
                   alpha=0.8, linewidth=1.5, label='2008 Financial Crisis')
        ax.fill_between(vintage_df['issue_year'], vintage_df['default_rate'],
                        alpha=0.1, color='#e05c5c')
        ax.set_xlabel("Issue Year")
        ax.set_ylabel("Default Rate (%)")
        ax.legend(facecolor='#0d1f3c', edgecolor='#1e3a5f')
        ax.grid(alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown("### Loan Volume by Issue Year")
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        ax2.bar(vintage_df['issue_year'], vintage_df['total_loans'],
                color='#1a6ab5', edgecolor='#2a8fd4', linewidth=0.5)
        ax2.set_xlabel("Issue Year")
        ax2.set_ylabel("Number of Loans")
        ax2.grid(axis='y', alpha=0.3)
        fig2.tight_layout()
        st.pyplot(fig2)

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Total ECL by Issue Year ($B)")
        fig3, ax3 = plt.subplots(figsize=(7, 4))
        ax3.bar(vintage_df['issue_year'], vintage_df['total_ECL'] / 1e9,
                color='#e05c5c', edgecolor='#b83228', linewidth=0.5)
        ax3.set_xlabel("Issue Year")
        ax3.set_ylabel("ECL ($ Billions)")
        ax3.grid(axis='y', alpha=0.3)
        fig3.tight_layout()
        st.pyplot(fig3)

    with col4:
        st.markdown("### ECL % by Issue Year")
        fig4, ax4 = plt.subplots(figsize=(7, 4))
        ax4.plot(vintage_df['issue_year'], vintage_df['ECL_pct'],
                 marker='s', color='#f0a500', linewidth=2.5, markersize=6)
        ax4.axvline(x=2008, color='#e05c5c', linestyle='--',
                    alpha=0.8, linewidth=1.5, label='2008 Financial Crisis')
        ax4.fill_between(vintage_df['issue_year'], vintage_df['ECL_pct'],
                         alpha=0.1, color='#f0a500')
        ax4.set_xlabel("Issue Year")
        ax4.set_ylabel("ECL %")
        ax4.legend(facecolor='#0d1f3c', edgecolor='#1e3a5f')
        ax4.grid(alpha=0.3)
        fig4.tight_layout()
        st.pyplot(fig4)

# ── PAGE 3 ────────────────────────────────────────────────
elif page == "Stress Testing":
    st.markdown("# Stress Testing")
    st.caption("Simulate the impact of increased default rates on portfolio ECL")
    st.markdown("---")

    base_ecl = 3.745
    total_ead = 29.699

    multiplier = st.slider(
        "PD Multiplier — drag to simulate stress scenarios",
        1.0, 4.0, 1.0, 0.25
    )

    stressed_ecl = base_ecl * multiplier
    stressed_pct = (stressed_ecl / total_ead) * 100
    increase = stressed_ecl - base_ecl

    col1, col2, col3 = st.columns(3)
    col1.metric("Stressed ECL", f"${stressed_ecl:.2f}B",
                f"+${increase:.2f}B vs base" if multiplier > 1 else "Base case")
    col2.metric("ECL % of Portfolio", f"{stressed_pct:.2f}%")
    col3.metric("PD Multiplier", f"{multiplier}x")

    st.markdown("---")

    scenarios = ['Base\nCase', 'Mild\n1.25x', 'Moderate\n1.5x', 'Severe\n2x', 'Extreme\n3x']
    ecl_vals = [base_ecl * m for m in [1, 1.25, 1.5, 2, 3]]
    colors = ['#1a6ab5', '#f0a500', '#e07b00', '#d94f3d', '#8b1a1a']

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].bar(scenarios, ecl_vals, color=colors, edgecolor='#0a0f1e', linewidth=0.5, width=0.5)
    axes[0].set_title("ECL by Scenario ($B)", color='#e8f4fd', fontsize=13, pad=12)
    axes[0].set_ylabel("ECL ($ Billions)")
    axes[0].axhline(y=stressed_ecl, color='#00d4ff', linestyle='--',
                    linewidth=1.5, label=f'Current: ${stressed_ecl:.2f}B')
    axes[0].legend(facecolor='#0d1f3c', edgecolor='#1e3a5f')
    axes[0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(ecl_vals):
        axes[0].text(i, v + 0.1, f'${v:.2f}B', ha='center',
                     color='#a8c5e0', fontsize=10)

    axes[1].bar(scenarios, [v / total_ead * 100 for v in ecl_vals],
                color=colors, edgecolor='#0a0f1e', linewidth=0.5, width=0.5)
    axes[1].set_title("ECL as % of Portfolio", color='#e8f4fd', fontsize=13, pad=12)
    axes[1].set_ylabel("ECL %")
    axes[1].grid(axis='y', alpha=0.3)
    for i, v in enumerate([v / total_ead * 100 for v in ecl_vals]):
        axes[1].text(i, v + 0.3, f'{v:.1f}%', ha='center',
                     color='#a8c5e0', fontsize=10)

    fig.tight_layout()
    st.pyplot(fig)

# ── PAGE 4 ────────────────────────────────────────────────
elif page == "Data Tables":
    st.markdown("# Data Tables")
    st.markdown("---")

    st.markdown("### ECL by Grade")
    st.dataframe(ecl_df, use_container_width=True, hide_index=True)

    st.markdown("### Vintage Analysis")
    st.dataframe(vintage_df, use_container_width=True, hide_index=True)

    st.markdown("### Stress Scenarios")
    st.dataframe(stress_df, use_container_width=True, hide_index=True)
