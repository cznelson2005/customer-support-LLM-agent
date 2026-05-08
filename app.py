import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Support Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Mono', monospace;
    }

    .stApp {
        background-color: #0a0a0f;
        color: #e8e8f0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f0f1a;
        border-right: 1px solid #1e1e3a;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #12122a 0%, #1a1a35 100%);
        border: 1px solid #2a2a50;
        border-radius: 12px;
        padding: 16px;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Syne', sans-serif;
        font-size: 2rem !important;
        font-weight: 800;
        color: #a78bfa;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: #6b6b9a;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Headers */
    h1 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        color: #f0f0ff !important;
        letter-spacing: -0.03em !important;
    }

    h2, h3 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        color: #c8c8f0 !important;
    }

    /* Severity badges */
    .badge-high {
        background: #3d1515; color: #ff6b6b;
        border: 1px solid #ff6b6b40;
        padding: 2px 10px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .badge-medium {
        background: #3d2e10; color: #ffa94d;
        border: 1px solid #ffa94d40;
        padding: 2px 10px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .badge-low {
        background: #0f2d1f; color: #69db7c;
        border: 1px solid #69db7c40;
        padding: 2px 10px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.05em;
    }

    /* Cards */
    .card {
        background: linear-gradient(135deg, #12122a 0%, #1a1a35 100%);
        border: 1px solid #2a2a50;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .complaint-pill {
        background: #1a1a2e;
        border-left: 3px solid #a78bfa;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin: 6px 0;
        font-size: 0.82rem;
        color: #b0b0d0;
        line-height: 1.5;
    }

    .rec-card {
        background: #0f1a2e;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .effort-low  { color: #69db7c; }
    .effort-med  { color: #ffa94d; }
    .effort-high { color: #ff6b6b; }

    /* Divider */
    hr { border-color: #1e1e3a; }

    /* Expander */
    [data-testid="stExpander"] {
        background: #12122a;
        border: 1px solid #2a2a50;
        border-radius: 10px;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        background: #12122a;
        border-color: #2a2a50;
        color: #e8e8f0;
    }

    /* Tab */
    .stTabs [data-baseweb="tab-list"] {
        background: #0f0f1a;
        border-bottom: 1px solid #1e1e3a;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #6b6b9a;
        font-family: 'DM Mono', monospace;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background: #1a1a35 !important;
        color: #a78bfa !important;
        border-bottom: 2px solid #a78bfa;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0f; }
    ::-webkit-scrollbar-thumb { background: #2a2a50; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data(data_dir: str):
    cluster_df  = pd.read_csv(os.path.join(data_dir, "cluster_analysis.csv"))
    sample_df   = pd.read_csv(os.path.join(data_dir, "df_sample.csv"))
    with open(os.path.join(data_dir, "final_report.json")) as f:
        report = json.load(f)
    return cluster_df, sample_df, report


def severity_badge(sev: str) -> str:
    cls = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}.get(sev, "badge-low")
    return f'<span class="{cls}">{sev}</span>'


def effort_class(effort: str) -> str:
    return {"Low": "effort-low", "Medium": "effort-med", "High": "effort-high"}.get(effort, "")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 Support Intelligence")
    st.markdown("<p style='color:#6b6b9a; font-size:0.75rem;'>AI-powered complaint analysis</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 📁 Data Source")
    data_dir = st.text_input(
        "Path to data folder",
        value="data",
        help="Folder containing cluster_analysis.csv, df_sample.csv, final_report.json"
    )

    st.markdown("---")
    st.markdown("### 🏢 Company")
    st.markdown("<div style='background:#1a1a35; border:1px solid #2a2a50; border-radius:8px; padding:10px 14px; font-size:0.85rem; color:#a78bfa; font-family:Syne,sans-serif; font-weight:700;'>AirbnbHelp</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color:#3a3a60; font-size:0.7rem;'>Built with Gemini 2.5 Flash<br/>Async Map-Reduce Pipeline</p>", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
try:
    cluster_df, sample_df, report = load_data(data_dir)
except Exception as e:
    st.error(f"❌ Could not load data from `{data_dir}`: {e}")
    st.info("Make sure the folder contains: `cluster_analysis.csv`, `df_sample.csv`, `final_report.json`")
    st.stop()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='margin-bottom:0'>Customer Complaint Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b6b9a; font-size:0.85rem; margin-top:4px;'>AirbnbHelp · Twitter Support Analysis · Powered by Gemini + Map-Reduce Agents</p>", unsafe_allow_html=True)
st.markdown("---")

# ── KPI metrics ───────────────────────────────────────────────────────────────
total_complaints = len(sample_df)
total_clusters   = len(cluster_df)
high_sev         = len(cluster_df[cluster_df.business_severity == "High"])
top_issues_count = len(report.get("top_issues", []))

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Complaints", total_complaints)
c2.metric("Clusters Found",   total_clusters)
c3.metric("High Severity",    high_sev)
c4.metric("Top Issues",       top_issues_count)

st.markdown("<br>", unsafe_allow_html=True)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Cluster Explorer", "💡 Recommendations", "📋 Executive Summary"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Overview
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### Top Complaint Clusters by Volume")
        chart_df = cluster_df.sort_values("cluster_size", ascending=True).tail(15)
        color_map = {"High": "#ff6b6b", "Medium": "#ffa94d", "Low": "#69db7c", "Unknown": "#6b6b9a"}
        chart_df["color"] = chart_df["business_severity"].map(color_map).fillna("#6b6b9a")

        fig = go.Figure(go.Bar(
            x=chart_df["cluster_size"],
            y=chart_df["issue_label"],
            orientation="h",
            marker=dict(color=chart_df["color"], line=dict(width=0)),
            text=chart_df["cluster_size"],
            textposition="outside",
            textfont=dict(color="#e8e8f0", size=11, family="DM Mono"),
            hovertemplate="<b>%{y}</b><br>Complaints: %{x}<extra></extra>"
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Mono", color="#e8e8f0"),
            xaxis=dict(showgrid=True, gridcolor="#1e1e3a", color="#6b6b9a"),
            yaxis=dict(showgrid=False, color="#e8e8f0"),
            margin=dict(l=0, r=40, t=10, b=10),
            height=420,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("### Severity Distribution")
        sev_counts = cluster_df["business_severity"].value_counts()
        colors     = [color_map.get(s, "#6b6b9a") for s in sev_counts.index]

        fig2 = go.Figure(go.Pie(
            labels=sev_counts.index,
            values=sev_counts.values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(color="#0a0a0f", width=3)),
            textinfo="label+percent",
            textfont=dict(family="DM Mono", size=11, color="#e8e8f0"),
            hovertemplate="<b>%{label}</b><br>%{value} clusters<extra></extra>"
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Mono", color="#e8e8f0"),
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=10),
            height=260
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Top Issues")
        for issue in report.get("top_issues", [])[:5]:
            sev  = issue.get("severity", "Low")
            badge = severity_badge(sev)
            st.markdown(
                f"<div class='card' style='padding:12px 16px; margin-bottom:8px;'>"
                f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
                f"<span style='font-size:0.82rem; color:#c8c8f0;'>#{issue['rank']} {issue['issue']}</span>"
                f"{badge}</div></div>",
                unsafe_allow_html=True
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Cluster Explorer
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Cluster Explorer")

    # Selector
    cluster_options = {
        f"[{row.business_severity}] {row.issue_label} ({row.cluster_size} complaints)": row.cluster_id
        for _, row in cluster_df.sort_values("cluster_size", ascending=False).iterrows()
    }
    selected_label = st.selectbox("Select a cluster to inspect", list(cluster_options.keys()))
    selected_id    = cluster_options[selected_label]
    row            = cluster_df[cluster_df.cluster_id == selected_id].iloc[0]

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Issue Summary")
        sev_badge = severity_badge(row.business_severity)
        st.markdown(
            f"<div class='card'>"
            f"<div style='margin-bottom:8px'>{sev_badge}</div>"
            f"<h3 style='margin:0 0 12px 0; font-size:1.1rem;'>{row.issue_label}</h3>"
            f"<p style='color:#9090c0; font-size:0.83rem; margin:0 0 12px 0;'>{row.issue_description}</p>"
            f"<hr style='border-color:#2a2a50; margin:12px 0;'>"
            f"<p style='color:#6b6b9a; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 4px 0;'>Root Cause</p>"
            f"<p style='color:#c8c8f0; font-size:0.83rem; margin:0 0 12px 0;'>{row.likely_root_cause}</p>"
            f"<p style='color:#6b6b9a; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 4px 0;'>Customer Pain Point</p>"
            f"<p style='color:#c8c8f0; font-size:0.83rem; margin:0 0 12px 0;'>{row.customer_pain_point}</p>"
            f"<p style='color:#6b6b9a; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 4px 0;'>Recommended Action</p>"
            f"<p style='color:#a78bfa; font-size:0.83rem; margin:0;'>{row.recommended_action}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("#### Sample Complaints")
        complaints = (
            sample_df[sample_df.cluster_id == selected_id]["clean_text"]
            .astype(str)
            .tolist()
        )
        if complaints:
            for c in complaints[:8]:
                st.markdown(f"<div class='complaint-pill'>&#8220;{c}&#8221;</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#6b6b9a;'>No complaints found for this cluster.</p>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Recommendations
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### LLM Recommendations")
    st.markdown("<p style='color:#6b6b9a; font-size:0.82rem;'>Generated by Gemini Reduce Agent — ranked by priority</p>", unsafe_allow_html=True)

    recs = report.get("recommendations", [])

    # Effort filter
    effort_filter = st.multiselect(
        "Filter by effort",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"]
    )

    filtered_recs = [r for r in recs if r.get("effort", "Medium") in effort_filter]

    if filtered_recs:
        for rec in filtered_recs:
            effort     = rec.get("effort", "Medium")
            eff_cls    = effort_class(effort)
            priority   = rec.get("priority", "—")
            action     = rec.get("action", "")
            impact     = rec.get("expected_impact", "")

            st.markdown(
                f"<div class='rec-card'>"
                f"<div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;'>"
                f"<span style='font-family:Syne,sans-serif; font-weight:700; font-size:0.75rem; color:#6b6b9a;'>PRIORITY {priority}</span>"
                f"<span class='{eff_cls}' style='font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em;'>● {effort} effort</span>"
                f"</div>"
                f"<p style='color:#e8e8f0; font-size:0.88rem; margin:0 0 8px 0; line-height:1.5;'>{action}</p>"
                f"<p style='color:#6b6b9a; font-size:0.78rem; margin:0;'>Impact: {impact}</p>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No recommendations match the selected filters.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Root Causes")
    for cause in report.get("root_causes", []):
        with st.expander(f"#{cause['rank']} — {cause['cause']}"):
            related = cause.get("related_issues", [])
            if related:
                st.markdown("**Related issues:**")
                for issue in related:
                    st.markdown(f"- {issue}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Executive Summary
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Executive Summary")

    summary = report.get("executive_summary", "No summary available.")
    st.markdown(
        f"<div class='card' style='border-left:3px solid #a78bfa; padding:24px;'>"
        f"<p style='font-size:1rem; color:#c8c8f0; line-height:1.8; margin:0;'>{summary}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### All Cluster Results")

    display_df = cluster_df[[
        "cluster_id", "issue_label", "business_severity",
        "issue_description", "likely_root_cause", "cluster_size"
    ]].sort_values("cluster_size", ascending=False)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "cluster_id"       : st.column_config.NumberColumn("ID", width="small"),
            "issue_label"      : st.column_config.TextColumn("Issue Label", width="medium"),
            "business_severity": st.column_config.TextColumn("Severity", width="small"),
            "issue_description": st.column_config.TextColumn("Description", width="large"),
            "likely_root_cause": st.column_config.TextColumn("Root Cause", width="large"),
            "cluster_size"     : st.column_config.NumberColumn("# Complaints", width="small"),
        }
    )
