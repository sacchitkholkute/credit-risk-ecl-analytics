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
    .stApp { background-color: #0a0f1e; }
    [data-testid="stSidebar"] {
        background-color: #0d1526;
        border-right: 1px solid #1e3a5f;
    }
    [data-testid="stMetric"] {
        background-color: #0d1f3c;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        padding: 20px;
    }
    [data-testid="stMetricLabel"] { color: #7a9cc4 !important; font-size: 13px !important; }
    [data-testid="stMetricValue"] { color: #e8f4fd !important; font-size: 28px !important; font-weight: 700 !important; }
    h1 { color: #e8f4fd !important; font-size: 2rem !important; font-weight: 700 !important; }
    h2 { color: #e8f4fd !important; font-size: 1.3rem !important; }
    h3 { color: #7a9cc4 !important; font-size: 1rem !important; }
    hr { border-color: #1e3a5f !important; }
    .stCaption { color: #4a7a9b !important; }
    .stRadio label { color: #a8c5e0 !important; }
    .insight-box {
        background-color: #0d1f3c;
        border-left: 3px solid #1a6ab5;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #a8c5e0;
        font-size: 14px;
    }
    .info-box {
        background-color: #0d1f3c;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        color: #a8c5e0;
    }
    .calc-box {
        background-color: #0d1f3c;
        border: 1px solid #1a6ab5;
        border-radius: 10px;
        padding: 24px;
        margin: 10px 0;
    }
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
        "ECL Calculator",
        "Data Tables",
        "About"
    ])
    st.markdown("---")
    st.markdown("**Dataset**")
    st.markdown("2.26M loans · $29.7B EAD")
    st.markdown("**Framework**")
    st.markdown("IFRS 9 · Basel III")

# ── PAGE 1 — Portfolio Overview ───────────────────────────
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

    # Grade filter
    st.markdown("### Filter by Loan Grade")
    all_grades = ecl_df['grade'].tolist()
    selected_grades = st.multiselect(
        "Select grades to display",
        options=all_grades,
        default=all_grades
    )
    filtered_ecl = ecl_df[ecl_df['grade'].isin(selected_grades)]

    col5, col6 = st.columns(2)

    with col5:
        st.markdown("### ECL by Loan Grade")
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.barh(filtered_ecl['grade'], filtered_ecl['total_ECL'] / 1e9,
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
        grade_colors = [colors[all_grades.index(g)] for g in filtered_ecl['grade']]
        bars2 = ax2.bar(filtered_ecl['grade'], filtered_ecl['PD'],
                        color=grade_colors, edgecolor='#0a0f1e', linewidth=0.5)
        ax2.bar_label(bars2, fmt='%.1f%%', padding=3, color='#a8c5e0', fontsize=10)
        ax2.set_xlabel("Loan Grade")
        ax2.set_ylabel("PD (%)")
        ax2.grid(axis='y', alpha=0.3)
        fig2.tight_layout()
        st.pyplot(fig2)

    # Key insights
    st.markdown("---")
    st.markdown("## Key Insights")

    highest_ecl_grade = ecl_df.loc[ecl_df['total_ECL'].idxmax(), 'grade']
    highest_ecl_val = ecl_df['total_ECL'].max() / 1e9
    riskiest_grade = ecl_df.loc[ecl_df['PD'].idxmax(), 'grade']
    riskiest_pd = ecl_df['PD'].max()
    safest_grade = ecl_df.loc[ecl_df['PD'].idxmin(), 'grade']
    safest_pd = ecl_df['PD'].min()
    highest_vintage = vintage_df.loc[vintage_df['default_rate'].idxmax(), 'issue_year']
    highest_vintage_rate = vintage_df['default_rate'].max()

    insights = [
        f"📌 Grade {highest_ecl_grade} carries the highest total ECL at ${highest_ecl_val:.2f}B — not because it's the riskiest grade, but because it has the most loan volume.",
        f"⚠️ Grade {riskiest_grade} has the highest default rate at {riskiest_pd:.1f}% — nearly 11x riskier than Grade {safest_grade} ({safest_pd:.1f}%).",
        f"📉 The {int(highest_vintage)} vintage had the highest default rate at {highest_vintage_rate:.1f}% — loans issued during the financial crisis were hit hardest.",
        "📊 LGD is above 96% across all grades — Lending Club's unsecured loans mean almost nothing is recovered after a default.",
        "🔎 2017–2018 vintages show low default rates, but this is misleading — these loans haven't had enough time to mature and default yet."
    ]

    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

# ── PAGE 2 — Vintage Analysis ─────────────────────────────
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

# ── PAGE 3 — Stress Testing ───────────────────────────────
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

    axes[0].bar(scenarios, ecl_vals, color=colors,
                edgecolor='#0a0f1e', linewidth=0.5, width=0.5)
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

# ── PAGE 4 — ECL Calculator ───────────────────────────────
elif page == "ECL Calculator":
    st.markdown("# ECL Calculator")
    st.caption("Estimate the Expected Credit Loss for an individual loan")
    st.markdown("---")

    pd_map = {'A': 3.59, 'B': 8.66, 'C': 14.36, 'D': 20.35,
              'E': 28.28, 'F': 36.42, 'G': 40.01}
    lgd_map = {'A': 99.80, 'B': 99.48, 'C': 99.04, 'D': 98.53,
               'E': 97.70, 'F': 96.75, 'G': 96.32}

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Loan Details")
        loan_amount = st.number_input("Loan Amount ($)", min_value=500,
                                      max_value=40000, value=15000, step=500)
        grade = st.selectbox("Loan Grade", options=['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        term = st.radio("Loan Term", options=["36 months", "60 months"])
        annual_income = st.number_input("Borrower Annual Income ($)",
                                        min_value=10000, max_value=500000,
                                        value=60000, step=5000)
        dti = st.slider("Debt-to-Income Ratio (%)", 0.0, 50.0, 15.0, 0.5)

    with col2:
        st.markdown("### ECL Breakdown")

        pd_val = pd_map[grade] / 100
        lgd_val = lgd_map[grade] / 100
        ead_val = loan_amount
        ecl_val = pd_val * lgd_val * ead_val

        term_multiplier = 1.15 if term == "60 months" else 1.0
        dti_multiplier = 1.0 + (max(0, dti - 20) * 0.01)
        adjusted_ecl = ecl_val * term_multiplier * dti_multiplier

        st.markdown(f'<div class="calc-box">', unsafe_allow_html=True)
        st.metric("Probability of Default (PD)", f"{pd_map[grade]}%")
        st.metric("Loss Given Default (LGD)", f"{lgd_map[grade]}%")
        st.metric("Exposure at Default (EAD)", f"${ead_val:,.0f}")
        st.markdown("---")
        st.metric("Base ECL (PD × LGD × EAD)", f"${ecl_val:,.2f}")
        st.metric("Adjusted ECL (term + DTI factors)", f"${adjusted_ecl:,.2f}",
                  f"{((adjusted_ecl/ecl_val)-1)*100:.1f}% adjustment" if adjusted_ecl != ecl_val else "No adjustment")
        st.metric("ECL as % of Loan", f"{(adjusted_ecl/loan_amount)*100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Risk Assessment")

    ecl_pct = (adjusted_ecl / loan_amount) * 100
    if ecl_pct < 5:
        risk_level = "🟢 Low Risk"
        risk_color = "#2ecc71"
        risk_note = "This loan falls within acceptable risk parameters."
    elif ecl_pct < 15:
        risk_level = "🟡 Moderate Risk"
        risk_color = "#f0a500"
        risk_note = "This loan carries moderate risk. Standard monitoring recommended."
    elif ecl_pct < 25:
        risk_level = "🟠 High Risk"
        risk_color = "#e07b00"
        risk_note = "This loan carries high risk. Enhanced due diligence recommended."
    else:
        risk_level = "🔴 Very High Risk"
        risk_color = "#e05c5c"
        risk_note = "This loan carries very high risk. Consider declining or requiring collateral."

    st.markdown(f'<div class="insight-box" style="border-left-color: {risk_color}">'
                f'<strong>{risk_level}</strong> — {risk_note}</div>',
                unsafe_allow_html=True)

# ── PAGE 5 — Data Tables ──────────────────────────────────
elif page == "Data Tables":
    st.markdown("# Data Tables")
    st.markdown("---")

    st.markdown("### ECL by Grade")
    st.dataframe(ecl_df, use_container_width=True, hide_index=True)

    st.markdown("### Vintage Analysis")
    st.dataframe(vintage_df, use_container_width=True, hide_index=True)

    st.markdown("### Stress Scenarios")
    st.dataframe(stress_df, use_container_width=True, hide_index=True)

# ── PAGE 6 — About ────────────────────────────────────────
elif page == "About":
    st.markdown("# About This Project")
    st.markdown("---")

    st.markdown("""
    <div class="info-box">
    <h3 style="color:#a8c5e0">What is this?</h3>
    <p>This is a credit risk analytics system built on the Lending Club loan dataset (2007–2018).
    It analyzes 2.26 million real loans to estimate how much money a lender can expect to lose —
    and which segments of the portfolio are the most dangerous.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-box">
        <h3 style="color:#a8c5e0">PD — Probability of Default</h3>
        <p>The likelihood that a borrower will stop repaying their loan.
        Calculated from historical default rates grouped by loan grade.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box">
        <h3 style="color:#a8c5e0">LGD — Loss Given Default</h3>
        <p>The fraction of the outstanding amount that is unrecoverable after a default.
        Since Lending Club loans are unsecured, LGD is above 96% across all grades.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-box">
        <h3 style="color:#a8c5e0">EAD — Exposure at Default</h3>
        <p>The outstanding loan balance at the time of default.
        This is the amount the lender stands to lose before recoveries.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="margin-top:16px">
    <h3 style="color:#a8c5e0">ECL = PD × LGD × EAD</h3>
    <p>Expected Credit Loss is the core formula used by banks under <strong>IFRS 9</strong>
    (International Financial Reporting Standard 9, in effect since January 2018).
    It replaced the older IAS 39 standard and requires banks to provision for
    expected losses proactively rather than waiting for losses to occur.</p>
    <p style="margin-top:8px">This project also aligns with <strong>Basel III</strong> thinking around
    capital adequacy, risk segmentation, and stress testing — the same framework
    used by banks and NBFCs regulated by the RBI in India.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Tools Used")
    col4, col5, col6 = st.columns(3)
    col4.markdown('<div class="info-box">🐍 Python<br>pandas, numpy, matplotlib</div>',
                  unsafe_allow_html=True)
    col5.markdown('<div class="info-box">🗄️ SQL<br>SQLite — 7 queries</div>',
                  unsafe_allow_html=True)
    col6.markdown('<div class="info-box">📊 Streamlit<br>This web app</div>',
                  unsafe_allow_html=True)
