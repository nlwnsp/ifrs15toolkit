import streamlit as st
from datetime import date, timedelta
import pandas as pd
import re
import copy

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG & GLOBAL STYLES — PROFESSIONAL WHITE THEME
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IFRS 15 Revenue Recognition Tool",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

/* ── Global base — WHITE THEME ── */
html, body {
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: #2C2C2C !important;
}

.stApp {
    background-color: #FFFFFF !important;
}

/* Force ALL main-area text to be dark */
.main p, .main span, .main label, .main div,
.main li, .main caption, .main small,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
.stRadio label, .stCheckbox label,
.stTextInput label, .stSelectbox label,
.stNumberInput label, .stDateInput label,
.stRadio div[data-testid="stMarkdownContainer"] p,
.row-widget label {
    color: #2C2C2C !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}

/* Input fields */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    color: #2C2C2C !important;
    background-color: #FFFFFF !important;
    border: 1.5px solid #D0D0D0 !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #C0392B !important;
    box-shadow: 0 0 0 2px rgba(192,57,43,0.15) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    color: #2C2C2C !important;
    background-color: #FFFFFF !important;
    border: 1.5px solid #D0D0D0 !important;
    border-radius: 3px !important;
}
.stSelectbox svg { color: #2C2C2C !important; }

/* Radio buttons */
.stRadio > div { gap: 6px; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #2C2C2C !important; }

/* Checkboxes */
.stCheckbox [data-testid="stMarkdownContainer"] p { color: #2C2C2C !important; }

/* ── Sidebar — LIGHT GRAY ── */
section[data-testid="stSidebar"] {
    background-color: #F8F8F8 !important;
    border-right: 3px solid #C0392B;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] caption {
    color: #2C2C2C !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #C0392B !important;
    border-bottom: 1px solid #C0392B !important;
}

/* ── Headings (main area) ── */
h1 {
    font-family: 'IBM Plex Mono', monospace !important;
    color: #1A1A2E !important;
    font-size: 1.8rem !important;
    border-bottom: 3px solid #C0392B !important;
    padding-bottom: 10px !important;
    letter-spacing: -1px;
}
h2, h3, h4 {
    font-family: 'IBM Plex Mono', monospace !important;
    color: #2C2C2C !important;
    border-bottom: none !important;
}

/* ── Custom boxes ── */
.step-badge {
    display: inline-block;
    background: #C0392B;
    color: #FFFFFF !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 2px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.step-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: #1A1A2E !important;
    margin-bottom: 4px;
}
.ifrs-ref {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #555555 !important;
    background: #F5F5F5;
    border-left: 3px solid #C0392B;
    padding: 4px 10px;
    margin-bottom: 16px;
    border-radius: 0 2px 2px 0;
}
.guidance-box {
    background: #EAF0FB;
    border-left: 4px solid #2980B9;
    padding: 10px 14px;
    border-radius: 0 4px 4px 0;
    font-size: 0.85rem;
    color: #2C2C2C !important;
    margin-bottom: 12px;
}
.guidance-box * { color: #2C2C2C !important; }

.warning-box {
    background: #FFF3CD;
    border-left: 4px solid #F39C12;
    padding: 10px 14px;
    border-radius: 0 4px 4px 0;
    font-size: 0.85rem;
    color: #2C2C2C !important;
    margin-bottom: 12px;
}
.warning-box * { color: #2C2C2C !important; }

.result-box {
    background: #E8F5E9;
    border-left: 4px solid #27AE60;
    padding: 10px 14px;
    border-radius: 0 4px 4px 0;
    font-size: 0.85rem;
    color: #2C2C2C !important;
    margin: 10px 0;
}
.result-box * { color: #2C2C2C !important; }

.divider {
    border: none;
    border-top: 2px dashed #E8E8E8;
    margin: 24px 0;
}

/* ═══════════════════════════════════════════════════════════════════════
   BUTTONS — Professional white theme with red accent
═══════════════════════════════════════════════════════════════════════ */
.stButton > button,
.stButton > button:link,
.stButton > button:visited {
    background-color: #FFFFFF !important;
    color: #C0392B !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    border-radius: 3px !important;
    border: 2px solid #C0392B !important;
    letter-spacing: 0.5px;
    transition: background-color 0.18s ease, border-color 0.18s ease, color 0.18s ease;
}
.stButton > button *,
.stButton > button p,
.stButton > button span,
.stButton > button div,
.stButton > button label,
.stButton > button em {
    color: #C0392B !important;
    font-family: 'IBM Plex Mono', monospace !important;
    background: transparent !important;
}

.stButton > button:hover,
.stButton > button:hover:focus {
    background-color: #C0392B !important;
    border-color: #C0392B !important;
    color: #FFFFFF !important;
}
.stButton > button:hover *,
.stButton > button:hover p,
.stButton > button:hover span,
.stButton > button:hover div,
.stButton > button:hover em {
    color: #FFFFFF !important;
    background: transparent !important;
}

.stButton > button:active {
    background-color: #A93226 !important;
    border-color: #A93226 !important;
    color: #FFFFFF !important;
}
.stButton > button:active * { color: #FFFFFF !important; background: transparent !important; }

.stButton > button:focus:not(:active) {
    outline: 2px solid #C0392B !important;
    outline-offset: 2px !important;
    color: #C0392B !important;
}
.stButton > button:focus:not(:active) * { color: #C0392B !important; }

.stDownloadButton > button,
.stDownloadButton > button:link,
.stDownloadButton > button:visited {
    background-color: #FFFFFF !important;
    color: #C0392B !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    border-radius: 3px !important;
    border: 2px solid #C0392B !important;
    transition: background-color 0.18s ease, border-color 0.18s ease;
}
.stDownloadButton > button *,
.stDownloadButton > button p,
.stDownloadButton > button span,
.stDownloadButton > button div {
    color: #C0392B !important;
    font-family: 'IBM Plex Mono', monospace !important;
    background: transparent !important;
}
.stDownloadButton > button:hover {
    background-color: #C0392B !important;
    border-color: #C0392B !important;
    color: #FFFFFF !important;
}
.stDownloadButton > button:hover * { color: #FFFFFF !important; background: transparent !important; }
.stDownloadButton > button:active {
    background-color: #A93226 !important;
    border-color: #A93226 !important;
    color: #FFFFFF !important;
}
.stDownloadButton > button:active * { color: #FFFFFF !important; }
.stButton > button p { color: #C0392B !important; }

/* ── Progress bar ── */
.progress-container {
    display: flex;
    gap: 6px;
    margin-bottom: 28px;
    align-items: center;
}
.progress-step {
    height: 6px;
    flex: 1;
    border-radius: 3px;
    background: #E8E8E8;
}
.progress-step.done  { background: #27AE60; }
.progress-step.active { background: #C0392B; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #F8F8F8 !important;
    padding: 14px 18px;
    border-radius: 4px;
    border-bottom: 3px solid #C0392B;
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] p,
[data-testid="metric-container"] div {
    color: #2C2C2C !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border: 1.5px solid #E8E8E8;
    border-radius: 4px;
}

/* ── Info / warning / success Streamlit native boxes ── */
[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #2C2C2C !important;
}

/* Caption text */
.stCaption, .stCaption p { color: #666666 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def fmt_number(n: int, currency: str) -> str:
    return f"{currency} {n:,}"


def fmt_metric(n, currency: str) -> str:
    """Abbreviate large numbers for st.metric cards (K/M/B/T)."""
    try:
        n = int(n)
    except (TypeError, ValueError):
        return str(n)
    abs_n = abs(n)
    if abs_n >= 1_000_000_000_000:
        return f"{currency} {n/1_000_000_000_000:.2f}T"
    if abs_n >= 1_000_000_000:
        return f"{currency} {n/1_000_000_000:.2f}B"
    if abs_n >= 1_000_000:
        return f"{currency} {n/1_000_000:.2f}M"
    if abs_n >= 1_000:
        return f"{currency} {n/1_000:.1f}K"
    return fmt_number(n, currency)


def _kpi(col, label: str, abbr: str, full: str = ""):
    """Compact dark KPI card — replaces st.metric for large numbers."""
    col.markdown(
        f'<div style="background:#1A1A2E;border-bottom:2px solid #C0392B;border-radius:3px;'
        f'padding:8px 12px;margin:2px 0;">'
        f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.60rem;color:#9A9888;'
        f'text-transform:uppercase;letter-spacing:0.4px;margin-bottom:3px;">{label}</div>'
        f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.82rem;font-weight:600;'
        f'color:#E8E6E0;">{abbr}</div>'
        + (f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.60rem;'
           f'color:#6A6860;margin-top:1px;">{full}</div>' if full else '')
        + '</div>',
        unsafe_allow_html=True,
    )


def parse_number(s: str) -> int:
    cleaned = re.sub(r"[^\d]", "", s)
    return int(cleaned) if cleaned else 0


def render_progress(current_step: int, total: int = 5):
    bars = ""
    for i in range(1, total + 1):
        if i < current_step:
            cls = "done"
        elif i == current_step:
            cls = "active"
        else:
            cls = ""
        bars += f'<div class="progress-step {cls}"></div>'
    st.markdown(
        f'<div class="progress-container">{bars}</div>'
        f'<p style="font-family:IBM Plex Mono,monospace;font-size:0.78rem;color:#888;margin-top:-18px;">'
        f'Step {current_step} of {total}</p>',
        unsafe_allow_html=True,
    )


def step_header(step_num: int, label: str, ifrs_ref: str):
    st.markdown(f'<div class="step-badge">Step {step_num}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">{label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ifrs-ref">📖 {ifrs_ref}</div>', unsafe_allow_html=True)


def guidance(text: str):
    st.markdown(f'<div class="guidance-box">ℹ️ {text}</div>', unsafe_allow_html=True)


def warning(text: str):
    st.markdown(f'<div class="warning-box">⚠️ {text}</div>', unsafe_allow_html=True)


def result(text: str):
    st.markdown(f'<div class="result-box">✅ {text}</div>', unsafe_allow_html=True)


def build_sfc_schedule(nominal_tp: int, direction: str, annual_rate_pct: float, period_months: int):
    """
    Compute SFC adjustment and build month-by-month interest accretion schedule.
    """
    r_annual  = annual_rate_pct / 100
    r_monthly = (1 + r_annual) ** (1 / 12) - 1
    n         = int(period_months)
    is_adv    = (direction == "advance")

    if is_adv:
        start_bal = nominal_tp
        end_bal   = round(nominal_tp * (1 + r_annual) ** (n / 12))
    else:
        start_bal = round(nominal_tp / (1 + r_annual) ** (n / 12))
        end_bal   = nominal_tp

    adj_revenue = end_bal   if is_adv else start_bal
    finance_amt = end_bal - nominal_tp if is_adv else nominal_tp - start_bal

    col_open  = "Liability (Opening)"  if is_adv else "Receivable (Opening)"
    col_int   = "Finance Cost Accreted" if is_adv else "Finance Income Accreted"
    col_close = "Liability (Closing)"  if is_adv else "Receivable (Closing)"
    jnl_mid   = ("Dr Finance Cost / Cr Contract Liability"
                 if is_adv else "Dr Receivable / Cr Finance Income")
    jnl_last  = ("→ Dr Contract Liability / Cr Revenue"
                 if is_adv else "→ Dr Cash / Cr Receivable [full collection]")

    rows    = []
    balance = start_bal
    for m in range(1, n + 1):
        opening  = balance
        interest = round(balance * r_monthly)
        closing  = opening + interest
        balance  = closing
        rows.append({
            "Month":   m,
            col_open:  opening,
            col_int:   interest,
            col_close: closing,
            "Journal": jnl_last if m == n else jnl_mid,
        })

    if rows:
        diff = end_bal - rows[-1][col_close]
        rows[-1][col_close] += diff
        rows[-1][col_int]   += diff

    df = pd.DataFrame(rows)
    for col in [col_open, col_int, col_close]:
        df[col] = df[col].apply(lambda x: f"{int(x):,}")

    return adj_revenue, finance_amt, df


# ─────────────────────────────────────────────────────────────────────────────
# SFC MATH HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def calc_implicit_rate_single(cash_price: float, nominal: float, period_months: int) -> float:
    if cash_price <= 0 or nominal <= 0 or period_months <= 0:
        return 0.0
    ratio = nominal / cash_price
    if ratio <= 0:
        return 0.0
    r_annual = ratio ** (12.0 / period_months) - 1
    return round(r_annual * 100, 4)


def calc_implicit_rate_annuity(cash_price: float, pmt: float, n_months: int) -> float:
    if cash_price <= 0 or pmt <= 0 or n_months <= 0:
        return 0.0
    if cash_price >= pmt * n_months:
        return 0.0

    def annuity_pv(r_m):
        if r_m < 1e-10:
            return pmt * n_months
        return pmt * (1 - (1 + r_m) ** (-n_months)) / r_m

    lo, hi = 1e-8, 2.0
    for _ in range(100):
        mid = (lo + hi) / 2
        pv_mid = annuity_pv(mid)
        if abs(pv_mid - cash_price) < 0.01:
            break
        if pv_mid > cash_price:
            lo = mid
        else:
            hi = mid
    r_annual = (1 + mid) ** 12 - 1
    return round(r_annual * 100, 4)


def build_sfc_annuity_schedule(hw_nominal_alloc: int, monthly_hw_pmt: float,
                                n_months: int, annual_rate_pct: float) -> tuple:
    r_annual  = annual_rate_pct / 100
    r_monthly = (1 + r_annual) ** (1 / 12) - 1

    if r_monthly < 1e-10:
        adj_revenue = round(monthly_hw_pmt * n_months)
    else:
        adj_revenue = round(monthly_hw_pmt * (1 - (1 + r_monthly) ** (-n_months)) / r_monthly)

    finance_income = hw_nominal_alloc - adj_revenue

    balance = adj_revenue
    rows = []
    for m in range(1, n_months + 1):
        opening  = balance
        interest = round(balance * r_monthly)
        billing  = round(monthly_hw_pmt)
        closing  = opening + interest - billing
        balance  = closing
        journal  = (
            "Dr AR / Cr Contract Asset (billing) + Dr Contract Asset / Cr Finance Income (interest)"
        )
        rows.append({
            "Month":                    m,
            "Contract Asset (Opening)": opening,
            "Finance Income Accreted":  interest,
            "Hardware Billing Raised":  billing,
            "Contract Asset (Closing)": closing,
            "Journal Summary":          journal,
        })

    if rows:
        diff = rows[-1]["Contract Asset (Closing)"]
        rows[-1]["Contract Asset (Closing)"] = 0
        rows[-1]["Finance Income Accreted"] -= diff

    df = pd.DataFrame(rows)
    for col in ["Contract Asset (Opening)", "Finance Income Accreted",
                "Hardware Billing Raised", "Contract Asset (Closing)"]:
        df[col] = df[col].apply(lambda x: f"{int(x):,}" if not pd.isna(x) else "")
    return adj_revenue, finance_income, df


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
TOTAL_STEPS = 5
defaults = {
    "record_db": [],
    "step": 1,
    "s1_done": False, "s1_data": {},
    "s2_done": False, "s2_data": {},
    "s3_done": False, "s3_data": {},
    "s4_done": False, "s4_data": {},
    "sfc_data": {},
    "po_list": [],
    "loyalty_data": {},
    "po_edit_idx": None,
    "edit_idx": None,
    "editing_idx": None,
    "view_mode": "workflow",
    "view_rec_idx": None,
    "flash_message": "",
    "form_epoch": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_workflow():
    for k in ["s1_done", "s2_done", "s3_done", "s4_done"]:
        st.session_state[k] = False
    for k in ["s1_data", "s2_data", "s3_data", "s4_data"]:
        st.session_state[k] = {}
    st.session_state.step = 1

    st.session_state.po_list = []
    st.session_state.loyalty_data = {}
    st.session_state.po_edit_idx = None

    widget_keys = [
        "i_company", "i_proj", "i_cust", "i_doc",
        "i_cur", "i_fee", "i_start", "i_end",
        "i_cancellable", "i_sig_comp", "i_enf_months",
        "m_is_mod", "m_has_add", "m_blend",
        "po_distinct_q1", "po_distinct_b1", "po_distinct_b2", "po_distinct_b3",
        "po_mat_right", "po_implied", "po_shipping",
        "new_po_name", "new_po_cat", "new_po_timing",
        "new_po_transfer_date", "new_po_svc_start", "new_po_svc_end", "new_po_method",
        "new_po_ssp",
        "loy_enabled", "loy_type", "loy_rate", "loy_market_eq",
        "loy_prob_below", "loy_avg_below", "loy_redemption_rate", "loy_ssp_override",
        "v_has", "v_dir", "v_val", "v_method", "v_prob",
        "sfc_enabled", "sfc_direction", "sfc_b50_a", "sfc_b50_b", "sfc_b50_c",
        "sfc_significant", "sfc_rate",
        "sfc_mode", "sfc_po_idx", "sfc_use_implicit",
        # Updated specific PMT and SFC keys for safe duplicate handling:
        "sfc_cash_price_ann", "sfc_cash_price_single",
        "sfc_months_impl_ann", "sfc_months_impl_single",
        "sfc_months_main_single", "sfc_months_main_ann",
        "sfc_impl_monthly_pmt", "sfc_monthly_pmt_override",
    ]
    for k in widget_keys:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state.sfc_data = {}
    st.session_state.edit_idx  = None
    st.session_state.editing_idx = None
    st.session_state.view_mode = "workflow"
    st.session_state.view_rec_idx = None
    st.session_state.form_epoch += 1


# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR  (simplified — nav + downloads only)
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 IFRS 15 Tool")
    st.markdown("**Revenue Recognition**  \nWorkflow Assistant")
    st.markdown("---")

    n_buf = len(st.session_state.record_db)
    st.markdown(f"### 📁 Buffer: {n_buf} contract(s)")

    # ── Navigation buttons ──
    if st.button("➕ New Assessment", use_container_width=True,
                 help="Start assessing a new contract"):
        reset_workflow()
        st.rerun()

    if n_buf > 0:
        if st.button("📂 View Saved Contracts", use_container_width=True,
                     help="Open the contract buffer dashboard"):
            st.session_state.view_mode = "buffer"
            st.rerun()

    st.markdown("---")

    # ── Downloads (only when buffer has records) ──
    if n_buf > 0:
        cur = st.session_state.record_db

        # Contract summary CSV
        csv_recs = [{k: v for k, v in r.items() if not k.startswith("_")} for r in cur]
        full_df   = pd.DataFrame(csv_recs)
        csv_data  = full_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 Contract Summary (CSV)",
            data=csv_data,
            file_name=f"IFRS15_Contracts_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # Multi-sheet export — bundled as ZIP of CSVs (zero external dependencies)
        import io, zipfile

        s1_rows = [{
            "Date_Recorded":      r.get("Date_Recorded",""),
            "Company":            r.get("Company",""),
            "Project_ID":         r.get("Project_ID",""),
            "Customer":           r.get("Customer",""),
            "Doc_Number":         r.get("Doc_Number",""),
            "Currency":           r.get("Currency",""),
            "Basic_Fee":          r.get("Basic_Fee",""),
            "Delivery_Start":     r.get("Delivery_Start",""),
            "Delivery_End":       r.get("Delivery_End",""),
            "Cancellable":        r.get("Cancellable",""),
            "Significant_Comp":   r.get("Significant_Comp",""),
            "Enforceable_Period": r.get("Enforceable_Period",""),
        } for r in csv_recs]

        s2_rows = [{
            "Project_ID":      r.get("Project_ID",""),
            "Customer":        r.get("Customer",""),
            "Contract_Type":   r.get("Contract_Type",""),
            "Mod_Treatment":   r.get("Mod_Treatment",""),
            "Mod_Description": r.get("Mod_Description",""),
        } for r in csv_recs]

        s3_rows = []
        for r in csv_recs:
            for i in range(1, int(r.get("PO_Count", 0)) + 1):
                p = f"PO{i}"
                s3_rows.append({
                    "Project_ID":      r.get("Project_ID",""),
                    "Customer":        r.get("Customer",""),
                    "PO_Number":       i,
                    "PO_Name":         r.get(f"{p}_Name",""),
                    "PO_Catalogue":    r.get(f"{p}_Catalogue",""),
                    "PO_Timing":       r.get(f"{p}_Timing",""),
                    "PO_SSP":          r.get(f"{p}_SSP",""),
                    "PO_Allocated_TP": r.get(f"{p}_Allocated_TP",""),
                    "Is_Loyalty":      r.get(f"{p}_Is_Loyalty",""),
                    "Transfer_Date":   r.get(f"{p}_Transfer_Date",""),
                    "Svc_Start":       r.get(f"{p}_Svc_Start",""),
                    "Svc_End":         r.get(f"{p}_Svc_End",""),
                    "Measure_Method":  r.get(f"{p}_Measure_Method",""),
                })

        s4_rows = [{
            "Project_ID":           r.get("Project_ID",""),
            "Customer":             r.get("Customer",""),
            "Has_Variable":         r.get("Has_Variable_Consid",""),
            "Variable_Type":        r.get("Variable_Type",""),
            "Variable_Amount":      r.get("Variable_Amount",""),
            "Est_Method":           r.get("Estimation_Method",""),
            "Constrained":          r.get("Variable_Constrained",""),
            "Final_TP":             r.get("Final_TP",""),
            "SFC_Enabled":          r.get("SFC_Enabled",""),
            "SFC_B50_Exception":    r.get("SFC_B50_Exception",""),
            "SFC_Significant":      r.get("SFC_Significant",""),
            "SFC_Direction":        r.get("SFC_Direction",""),
            "SFC_Rate_Pct":         r.get("SFC_Rate_Pct",""),
            "SFC_Period_Months":    r.get("SFC_Period_Months",""),
            "SFC_Nominal_TP":       r.get("SFC_Nominal_TP",""),
            "SFC_Adjusted_Revenue": r.get("SFC_Adjusted_Revenue",""),
            "SFC_Finance_Amount":   r.get("SFC_Finance_Amount",""),
        } for r in csv_recs]

        s5_rows = [{
            "Project_ID":           r.get("Project_ID",""),
            "Customer":             r.get("Customer",""),
            "Currency":             r.get("Currency",""),
            "OneTime_Revenue":      r.get("OneTime_Revenue",""),
            "Recurring_Revenue":    r.get("Recurring_Revenue",""),
            "Deferred_Rev_Loyalty": r.get("Deferred_Revenue_Loyalty",""),
            "Final_TP":             r.get("Final_TP",""),
            "Loyalty_Enabled":      r.get("Loyalty_Enabled",""),
            "Loyalty_SSP":          r.get("Loyalty_SSP",""),
            "Loyalty_Redemption_%": r.get("Loyalty_Redemption_Pct",""),
            "Loyalty_Redeemed_Rev": r.get("Loyalty_Redeemed_Rev",""),
            "Loyalty_Breakage_Rev": r.get("Loyalty_Breakage_Rev",""),
            "IAS37_Provision":      r.get("Loyalty_IAS37_Provision",""),
        } for r in csv_recs]

        zip_sheets = [
            ("00_All_Contracts.csv",            csv_recs),
            ("01_Step1_Contract_ID.csv",         s1_rows),
            ("02_Step2_Modification.csv",        s2_rows),
            ("03_Step3_Perf_Obligations.csv",    s3_rows),
            ("04_Step4_TP_and_SFC.csv",          s4_rows),
            ("05_Step5_Revenue_Summary.csv",     s5_rows),
        ]

        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for fname, rows in zip_sheets:
                csv_bytes = pd.DataFrame(rows).to_csv(index=False).encode("utf-8-sig")
                zf.writestr(fname, csv_bytes)
        zip_buf.seek(0)

        st.download_button(
            label="📊 Full Assessment (ZIP — 6 CSV sheets)",
            data=zip_buf.read(),
            file_name=f"IFRS15_Assessment_{date.today()}.zip",
            mime="application/zip",
            use_container_width=True,
        )

        # PO detail CSV
        po_rows = []
        for rec in cur:
            po_count = rec.get("PO_Count", 0)
            cf = {k: rec.get(k) for k in [
                "Date_Recorded","Company","Project_ID","Customer","Doc_Number",
                "Currency","Basic_Fee","Delivery_Start","Delivery_End",
                "Cancellable","Significant_Comp","Enforceable_Period",
                "Contract_Type","Mod_Treatment","Has_Variable_Consid",
                "Variable_Type","Variable_Amount","Estimation_Method",
                "Variable_Constrained","Final_TP","OneTime_Revenue","Recurring_Revenue"]}
            for i in range(1, int(po_count)+1):
                p = f"PO{i}"
                row = dict(cf)
                row.update({
                    "PO_Number":    i,
                    "PO_Name":      rec.get(f"{p}_Name",""),
                    "PO_Catalogue": rec.get(f"{p}_Catalogue",""),
                    "PO_Timing":    rec.get(f"{p}_Timing",""),
                    "PO_Is_Loyalty":rec.get(f"{p}_Is_Loyalty","No"),
                    "PO_SSP":       rec.get(f"{p}_SSP",""),
                    "PO_Allocated_TP": rec.get(f"{p}_Allocated_TP",""),
                    "Transfer_Date":   rec.get(f"{p}_Transfer_Date",""),
                    "Svc_Start":       rec.get(f"{p}_Svc_Start",""),
                    "Svc_End":         rec.get(f"{p}_Svc_End",""),
                    "Measure_Method":  rec.get(f"{p}_Measure_Method",""),
                })
                po_rows.append(row)
        if po_rows:
            po_csv = pd.DataFrame(po_rows).to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📥 PO Detail (CSV)",
                data=po_csv,
                file_name=f"IFRS15_PO_Detail_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("---")
        if st.button("🗑️ Clear All Records", use_container_width=True):
            st.session_state.record_db = []
            st.rerun()
    else:
        st.caption("No contracts saved yet. Complete all 5 steps to save.")

    st.markdown("---")
    st.markdown("""
**5-Step IFRS 15 Framework**
1. Contract Identification
2. Modification Assessment
3. Performance Obligations
4. Transaction Price
5. Review & Save

*Complete each step sequentially.*
""")



# ─────────────────────────────────────────────────────────────────────────────
def all_months_between(start: date, end: date):
    months = []
    y, m = start.year, start.month
    ey, em = end.year, end.month
    while (y, m) <= (ey, em):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months


def month_start(y, m): return date(y, m, 1)
def month_end(y, m):
    if m == 12: return date(y + 1, 1, 1) - timedelta(days=1)
    return date(y, m + 1, 1) - timedelta(days=1)


def po_schedule_dict(po: dict) -> dict:
    alloc = po["allocated_tp"]
    if po["timing"] == "Point in Time":
        d = po["transfer_date"]
        return {(d.year, d.month): alloc}

    s, e = po["svc_start"], po["svc_end"]
    if e <= s:
        return {(s.year, s.month): alloc}

    method = po.get("method", "Time-Elapsed (straight-line)")
    months = all_months_between(s, e)
    result_d = {}

    if method.startswith("Time-Elapsed"):
        n = len(months)
        if n == 0:
            return {(s.year, s.month): alloc}

        first_is_full = (s == month_start(s.year, s.month))
        last_is_full  = (e == month_end(e.year, e.month))

        if n == 1:
            result_d[(s.year, s.month)] = alloc
        elif first_is_full and last_is_full:
            base   = alloc // n
            rem    = alloc - base * n
            for i, (y, m) in enumerate(months):
                result_d[(y, m)] = base + (1 if i < rem else 0)
        else:
            total_days = (e - s).days + 1

            partial_alloc = 0
            partial_keys  = set()

            if not first_is_full:
                fy, fm = months[0]
                days_first = (month_end(fy, fm) - s).days + 1
                amt = round(alloc * days_first / total_days)
                result_d[(fy, fm)] = amt
                partial_alloc += amt
                partial_keys.add((fy, fm))

            if not last_is_full:
                ly, lm = months[-1]
                days_last = (e - month_start(ly, lm)).days + 1
                amt = round(alloc * days_last / total_days)
                result_d[(ly, lm)] = result_d.get((ly, lm), 0) + amt
                partial_alloc += amt
                partial_keys.add((ly, lm))

            full_months = [(y, m) for (y, m) in months if (y, m) not in partial_keys]
            remaining   = alloc - partial_alloc
            nf = len(full_months)
            if nf > 0:
                base = remaining // nf
                rem  = remaining - base * nf
                for i, (y, m) in enumerate(full_months):
                    result_d[(y, m)] = base + (1 if i < rem else 0)
            else:
                result_d[(months[0][0], months[0][1])] = alloc

    else:
        total_days = (e - s).days or 1
        for (y, m) in months:
            ps   = max(month_start(y, m), s)
            pe   = min(month_end(y, m), e)
            if ps > pe:
                continue
            days = (pe - ps).days + 1
            result_d[(y, m)] = round(alloc * days / total_days)

    if result_d:
        diff = alloc - sum(result_d.values())
        last_key = sorted(result_d.keys())[-1]
        result_d[last_key] += diff

    return result_d


def build_blended_schedule(po_list: list, currency: str) -> pd.DataFrame:
    if not po_list:
        return pd.DataFrame()

    all_keys = set()
    po_dicts = []
    for po in po_list:
        d = po_schedule_dict(po)
        po_dicts.append(d)
        all_keys.update(d.keys())

    sorted_keys = sorted(all_keys)

    rows = []
    for (y, m) in sorted_keys:
        row = {"Period": date(y, m, 1).strftime("%b %Y")}
        total = 0
        for i, po in enumerate(po_list):
            amt = po_dicts[i].get((y, m), 0)
            row[f"PO{i+1}: {po['name'][:18]}"] = amt
            total += amt
        row[f"Total ({currency})"] = total
        rows.append(row)

    df = pd.DataFrame(rows)

    totals = {"Period": "GRAND TOTAL"}
    for col in df.columns[1:]:
        totals[col] = df[col].sum()
    df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

    for col in df.columns[1:]:
        def _fmt(x, col=col):
            if pd.isna(x) or x == "":
                return ""
            v = int(x)
            if v == 0 and not col.startswith("Total"):
                return "-"
            return f"{v:,}"
        df[col] = df[col].apply(_fmt)

    return df



# ─────────────────────────────────────────────────────────────────────────────
# MAIN TITLE
# ─────────────────────────────────────────────────────────────────────────────
# Flash message (shows once after save, then clears)
if st.session_state.get("flash_message"):
    st.success(st.session_state.flash_message)
    st.session_state.flash_message = ""

st.title("IFRS 15 — Revenue Recognition Procedures")
st.markdown(
    '<div style="margin-top:6px;margin-bottom:20px;padding:6px 12px;'
    'background:#F0EFEB;border-radius:3px;border-left:3px solid #C0392B;">'
    '<span style="font-family:IBM Plex Mono,monospace;font-size:0.73rem;color:#555555;">'
    'Experimental tool based on <strong style="color:#1A1A2E;">Claude AI Sonnet 4.6</strong>, likely to contain bugs — for research only. '
    '&nbsp;·&nbsp; by <strong style="color:#1A1A2E;">Nelwan Satria Putra</strong>'
    '</span></div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# BUFFER DASHBOARD  (view_mode == "buffer")
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.view_mode == "buffer":
    st.markdown("### 📁 Saved Contracts")
    _buf = st.session_state.record_db
    if not _buf:
        st.info("No contracts in the buffer yet. Click **➕ New Assessment** in the sidebar to start.")
        st.stop()

    # Top action bar
    bc1, bc2 = st.columns([1, 4])
    with bc1:
        if st.button("➕ New Assessment", use_container_width=True):
            reset_workflow()
            st.rerun()

    st.markdown("---")

    for _bi, _brec in enumerate(_buf):
        _pid   = _brec.get("Project_ID", f"#{_bi+1}")
        _cust  = _brec.get("Customer", "—")
        _curr  = _brec.get("Currency", "")
        _fee   = _brec.get("Final_TP", 0)
        _po_n  = _brec.get("PO_Count", 0)
        _start = _brec.get("Delivery_Start", "")
        _end   = _brec.get("Delivery_End", "")
        _sfc   = "✅ SFC" if _brec.get("SFC_Enabled") == "Yes" and _brec.get("SFC_Significant") == "Yes" else ""
        _loy   = "🎁 Loyalty" if _brec.get("Loyalty_Enabled") == "Yes" else ""
        _tags  = "  ".join(t for t in [_sfc, _loy] if t)

        with st.container():
            card_col, btn_col = st.columns([7, 3])
            with card_col:
                st.markdown(
                    f"**{_pid}** &nbsp;|&nbsp; {_cust}  \n"
                    f"<span style='font-size:0.82rem;color:#555;font-family:IBM Plex Mono,monospace;'>"
                    f"{_curr} {_fee:,} &nbsp;·&nbsp; {_po_n} PO(s) &nbsp;·&nbsp; "
                    f"{_start} → {_end}"
                    + (f" &nbsp;·&nbsp; {_tags}" if _tags else "") +
                    "</span>",
                    unsafe_allow_html=True
                )
            with btn_col:
                _v_col, _e_col, _d_col = st.columns(3)
                if _v_col.button("👁", key=f"buf_view_{_bi}", help="View full assessment"):
                    st.session_state.view_mode    = "view_rec"
                    st.session_state.view_rec_idx = _bi
                    st.rerun()
                if _e_col.button("✏️", key=f"buf_edit_{_bi}", help="Edit this contract"):
                    _rec = st.session_state.record_db[_bi]  # keep in buffer
                    _s1 = _rec.get("_s1", {})
                    _s3_snap = _rec.get("_s3", {})
                    if _s1:
                        st.session_state.editing_idx = _bi   # mark which slot we are editing
                        st.session_state.s1_data = _s1
                        st.session_state.s2_data = _rec.get("_s2", {})
                        st.session_state.s3_data = _s3_snap
                        st.session_state.s4_data = _rec.get("_s4", {})
                        st.session_state.po_list = copy.deepcopy(_s3_snap.get("po_list", []))
                        for _k in ["s1_done","s2_done","s3_done","s4_done"]:
                            st.session_state[_k] = True
                        st.session_state.step      = 5
                        st.session_state.view_mode = "workflow"
                        st.session_state.form_epoch += 1
                        _ep = st.session_state.form_epoch
                        st.session_state[f"i_company_{_ep}"] = _s1.get("company", "")
                        st.session_state[f"i_proj_{_ep}"]    = _s1.get("project_id", "")
                        st.session_state[f"i_cust_{_ep}"]    = _s1.get("customer", "")
                        st.session_state[f"i_doc_{_ep}"]     = _s1.get("doc_num", "")
                        st.session_state[f"i_cur_{_ep}"]     = _s1.get("currency", "IDR")
                        st.session_state[f"i_fee_{_ep}"]     = str(_s1.get("raw_fee", 0))
                        st.session_state[f"i_start_{_ep}"]   = _s1.get("start_date")
                        st.session_state[f"i_end_{_ep}"]     = _s1.get("end_date")
                        st.session_state[f"i_cancellable_{_ep}"] = (
                            "Yes — cancellable without consent"
                            if _s1.get("cancellable") else
                            "No — not cancellable (full duration enforceable)"
                        )
                        # restore dependent controls if contract was cancellable
                        if _s1.get("cancellable"):
                            st.session_state[f"i_sig_comp_{_ep}"] = _s1.get("sig_comp", "No")
                            if _s1.get("sig_comp") == "Yes":
                                enf = _s1.get("enf_period")
                                if isinstance(enf, int):
                                    st.session_state[f"i_enf_months_{_ep}"] = enf
                            else:
                                # remove any old months key so it doesn't stick if toggled later
                                keym = f"i_enf_months_{_ep}"
                                if keym in st.session_state:
                                    del st.session_state[keym]
                    else:
                        st.warning("No snapshot data — please re-enter manually.")
                    st.rerun()
                if _d_col.button("🗑️", key=f"buf_del_{_bi}", help="Delete this record"):
                    st.session_state.record_db.pop(_bi)
                    st.rerun()
            st.markdown('<hr style="margin:6px 0;border-top:1px dashed #D0CEC8;">', unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# CONTRACT VIEW  (view_mode == "view_rec")  — read-only full assessment recap
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.view_mode == "view_rec":
    _vi  = st.session_state.view_rec_idx
    _buf = st.session_state.record_db
    if _vi is None or _vi >= len(_buf):
        st.session_state.view_mode = "buffer"
        st.rerun()

    _vr = _buf[_vi]
    _vd1 = _vr.get("_s1", {})
    _vd2 = _vr.get("_s2", {})
    _vd3 = _vr.get("_s3", {})
    _vd4 = _vr.get("_s4", {})

    # Nav bar
    nav1, nav2, nav3 = st.columns([2, 2, 6])
    if nav1.button("← Back to Buffer"):
        st.session_state.view_mode = "buffer"
        st.rerun()
    if nav2.button("✏️ Edit this Contract"):
        _rec = st.session_state.record_db[_vi]  # keep in buffer
        _s1  = _rec.get("_s1", {})
        _s3_snap = _rec.get("_s3", {})
        if _s1:
            st.session_state.editing_idx = _vi   # mark slot
            st.session_state.s1_data = _s1
            st.session_state.s2_data = _rec.get("_s2", {})
            st.session_state.s3_data = _s3_snap
            st.session_state.s4_data = _rec.get("_s4", {})
            st.session_state.po_list = copy.deepcopy(_s3_snap.get("po_list", []))
            for _k in ["s1_done","s2_done","s3_done","s4_done"]:
                st.session_state[_k] = True
            st.session_state.step      = 5
            st.session_state.view_mode = "workflow"
            st.session_state.view_rec_idx = None
            st.session_state.form_epoch += 1
            _ep = st.session_state.form_epoch
            st.session_state[f"i_company_{_ep}"] = _s1.get("company", "")
            st.session_state[f"i_proj_{_ep}"]    = _s1.get("project_id", "")
            st.session_state[f"i_cust_{_ep}"]    = _s1.get("customer", "")
            st.session_state[f"i_doc_{_ep}"]     = _s1.get("doc_num", "")
            st.session_state[f"i_cur_{_ep}"]     = _s1.get("currency", "IDR")
            st.session_state[f"i_fee_{_ep}"]     = str(_s1.get("raw_fee", 0))
            st.session_state[f"i_start_{_ep}"]   = _s1.get("start_date")
            st.session_state[f"i_end_{_ep}"]     = _s1.get("end_date")
            # restore cancellability and its dependent controls
            st.session_state[f"i_cancellable_{_ep}"] = (
                "Yes — cancellable without consent"
                if _s1.get("cancellable") else
                "No — not cancellable (full duration enforceable)"
            )
            if _s1.get("cancellable"):
                st.session_state[f"i_sig_comp_{_ep}"] = _s1.get("sig_comp", "No")
                if _s1.get("sig_comp") == "Yes":
                    enf = _s1.get("enf_period")
                    if isinstance(enf, int):
                        st.session_state[f"i_enf_months_{_ep}"] = enf
                else:
                    keym = f"i_enf_months_{_ep}"
                    if keym in st.session_state:
                        del st.session_state[keym]
        else:
            st.warning("No snapshot — please re-enter manually.")
        st.rerun()

    st.markdown(f"## 📄 {_vr.get('Project_ID','—')}  |  {_vr.get('Customer','—')}")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if not _vd1:
        st.warning("This record was saved before full-snapshot support. Only flat summary is available.")
        _flat_rows = [(k, str(v)) for k, v in _vr.items() if not k.startswith("_")]
        st.dataframe(pd.DataFrame(_flat_rows, columns=["Field", "Value"]),
                     use_container_width=True, hide_index=True)
        st.stop()

    # ── Summary table (mirrors Step 5) ──
    _vcur = _vd1.get("currency", _vr.get("Currency", ""))
    _summary_rows = [
        ("Company",           _vd1.get("company", "")),
        ("Customer",          _vd1.get("customer", "")),
        ("Project ID",        _vd1.get("project_id", "")),
        ("Document Number",   _vd1.get("doc_num") or "—"),
        ("Currency",          _vcur),
        ("Basic Contract Fee", fmt_number(_vd1.get("raw_fee", 0), _vcur)),
        ("Delivery Period",   f"{_vd1.get('start_date','')} → {_vd1.get('end_date','')}"),
        ("── Enforceability ──", ""),
        ("Cancellable?",      "Yes" if _vd1.get("cancellable") else "No"),
        ("Significant Comp.", str(_vd1.get("sig_comp", ""))),
        ("Enforceable Period", str(_vd1.get("enf_period", ""))),
        ("── Modification ──", ""),
        ("Contract Type",     _vd2.get("is_mod", "")),
        ("Mod Treatment",     _vd2.get("mod_treatment", "")),
        ("── Perf. Obligations ──", ""),
        ("PO Status",         _vd3.get("po_status", "")),
        ("Timing Mix",        _vd3.get("timing_summary", "")),
        ("── Transaction Price ──", ""),
        ("Variable Consid.",  _vd4.get("has_var", "")),
        ("Var. Amount",       fmt_number(_vd4.get("var_impact", 0), _vcur) if _vd4.get("var_impact") else "—"),
        ("Constrained?",      "Yes" if _vd4.get("constrained") else "No"),
        ("Final TP",          fmt_number(_vd4.get("final_tp", 0), _vcur)),
    ]
    _vsfc = _vd4.get("sfc_data", {})
    if _vsfc.get("enabled"):
        if _vsfc.get("b50_exception"):
            _summary_rows += [("── Financing Component ──", ""), ("SFC", "B50 Exception — No Adjustment")]
        elif not _vsfc.get("sfc_significant"):
            _summary_rows += [("── Financing Component ──", ""), ("SFC", "Not Significant — No Adjustment")]
        else:
            _summary_rows += [
                ("── Financing Component ──", ""),
                ("SFC Direction", "Advance" if _vsfc.get("is_advance") else "Deferred"),
                ("Rate", f"{_vsfc.get('rate_pct',0):.2f}% p.a."),
                ("Period", f"{_vsfc.get('period_months',0)} months"),
                ("SFC-Adjusted Revenue", fmt_number(_vsfc.get("adj_revenue",0), _vcur)),
                ("Finance Amount", fmt_number(_vsfc.get("finance_amt",0), _vcur)),
            ]
    st.dataframe(pd.DataFrame(_summary_rows, columns=["Field", "Value"]),
                 use_container_width=True, hide_index=True)

    # ── PO Allocation table ──
    if _vd4.get("po_list_alloc"):
        st.markdown("---")
        st.markdown("**Performance Obligations & Allocation**")
        _vpo_rows = []
        for _vpo in _vd4["po_list_alloc"]:
            _pi = (f"Transfer: {_vpo['transfer_date']}" if _vpo["timing"] == "Point in Time"
                   else f"{_vpo['svc_start']} → {_vpo['svc_end']}")
            _vpo_rows.append({
                "PO Name":   _vpo["name"],
                "Type":      _vpo["catalogue"],
                "Timing":    _vpo["timing"],
                "Loyalty":   "Yes" if _vpo.get("is_loyalty") else "No",
                "Period":    _pi,
                f"SSP ({_vcur})":          f"{_vpo['ssp']:,}",
                f"Allocated TP ({_vcur})": f"{_vpo['allocated_tp']:,}",
            })
        st.dataframe(pd.DataFrame(_vpo_rows), use_container_width=True, hide_index=True)

    # ── Blended schedule ──
    if _vd4.get("po_list_alloc"):
        st.markdown("---")
        st.markdown("**📅 Blended Revenue Recognition Schedule**")
        _vbl = build_blended_schedule(_vd4["po_list_alloc"], _vcur)
        if not _vbl.empty:
            st.dataframe(_vbl, use_container_width=True, hide_index=True)
            _vpit = sum(p["allocated_tp"] for p in _vd4["po_list_alloc"]
                        if p["timing"] == "Point in Time" and not p.get("is_loyalty"))
            _vot  = sum(p["allocated_tp"] for p in _vd4["po_list_alloc"] if p["timing"] == "Over Time")
            _vloy = sum(p["allocated_tp"] for p in _vd4["po_list_alloc"] if p.get("is_loyalty"))
            _c1, _c2, _c3 = st.columns(3)
            _c1.metric("One-Time Revenue",  fmt_metric(_vpit, _vcur))
            _c2.metric("Recurring Revenue", fmt_metric(_vot,  _vcur))
            _c3.metric("Total Contract TP", fmt_metric(_vd4.get("final_tp",0), _vcur))
            if _vloy > 0:
                st.caption(f"Deferred Revenue (Loyalty): {fmt_number(_vloy, _vcur)}")

    st.stop()




# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: CONTRACT IDENTIFICATION & ENFORCEABILITY
# ─────────────────────────────────────────────────────────────────────────────
# ── Workflow progress bar ──
render_progress(st.session_state.step, TOTAL_STEPS)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

step_header(1, "Contract Identification & Enforceability", "IFRS 15.9–15.16")
guidance(
    "A contract exists when it has commercial substance, both parties have approved it, "
    "rights and payment terms are identifiable, and collection is probable. "
    "The 'enforceable period' determines how long the entity must account for the contract."
)

col1, col2 = st.columns(2)
with col1:
    company   = st.text_input("Company Name *", placeholder="e.g., PT ABC Indonesia", key=f"i_company_{st.session_state.form_epoch}")
    project_id = st.text_input("Project ID (YY/NNN) *", placeholder="e.g., 26/001", key=f"i_proj_{st.session_state.form_epoch}")
    customer  = st.text_input("Customer Name *", placeholder="e.g., Client XYZ Ltd", key=f"i_cust_{st.session_state.form_epoch}")
    doc_num   = st.text_input("Contract Document Number", placeholder="e.g., SPK-2026-001", key=f"i_doc_{st.session_state.form_epoch}")

with col2:
    currency = st.selectbox("Currency *", ["IDR", "USD", "KRW", "JPY", "SGD", "EUR"], key=f"i_cur_{st.session_state.form_epoch}")
    # use existing session value if present to avoid Streamlit warnings about default vs session state
    fee_key = f"i_fee_{st.session_state.form_epoch}"
    fee_default = st.session_state.get(fee_key, "0")
    fee_raw  = st.text_input("Basic Contract Fee *", value=fee_default, placeholder="e.g., 1,500,000,000", key=fee_key)
    raw_fee  = parse_number(fee_raw)
    if raw_fee > 0:
        st.caption(f"Parsed: {fmt_number(raw_fee, currency)}")
    start_date = st.date_input("Delivery Start Date *", key=f"i_start_{st.session_state.form_epoch}")
    end_key = f"i_end_{st.session_state.form_epoch}"
    end_default = st.session_state.get(end_key, date.today() + timedelta(days=365))
    end_date   = st.date_input("Delivery End Date *", key=end_key,
                                value=end_default)

st.markdown("**Cancellability Assessment**")
c1 = st.radio(
    "Can either party cancel this contract without the other's consent?",
    ["No — not cancellable (full duration enforceable)",
     "Yes — cancellable without consent"],
    key=f"i_cancellable_{st.session_state.form_epoch}",
)
is_cancellable = c1.startswith("Yes")
sig_comp   = "N/A"
enf_period = "Full Duration"

if is_cancellable:
    guidance(
        "If cancellable without consent, the enforceable period may be shorter than the full contract. "
        "Significant compensation (e.g., a break fee) creates an economic incentive to continue, "
        "which may extend the enforceable period. (IFRS 15.B34–B38)"
    )
    sc = st.radio(
        "Is significant compensation payable upon cancellation?",
        ["No", "Yes"],
        key=f"i_sig_comp_{st.session_state.form_epoch}",
    )
    sig_comp = sc
    if sc == "Yes":
        enf_period = st.selectbox(
            "Shorter enforceable period (months from start):",
            list(range(1, 61)),
            key=f"i_enf_months_{st.session_state.form_epoch}",
        )
        result(
            f"Enforceable period set to {enf_period} month(s) due to significant compensation clause."
        )
    else:
        warning(
            "Without significant compensation, the contract may be enforceable only for the "
            "current period or notice period. Consider reassessing contract term."
        )

if not is_cancellable:
    result("Contract is not cancellable — enforceable for full duration.")

s1_errors = []
if not company.strip():     s1_errors.append("Company Name is required.")
if not customer.strip():    s1_errors.append("Customer Name is required.")
if not project_id.strip():  s1_errors.append("Project ID is required.")
if not re.match(r"^\d{2}/\d{1,4}$", project_id.strip()) and project_id.strip():
    s1_errors.append("Project ID should follow YY/NNN format (e.g., 26/001).")
if raw_fee <= 0:            s1_errors.append("Basic Fee must be greater than 0.")
# allow same-day delivery; only complain if end is before start
if end_date < start_date:
    s1_errors.append("End Date must be on or after Start Date.")

if st.button("✔ Complete Step 1 — Contract Identification"):
    if s1_errors:
        for e in s1_errors:
            st.error(e)
    else:
        st.session_state.s1_data = {
            "company": company, "project_id": project_id, "customer": customer,
            "doc_num": doc_num, "currency": currency, "raw_fee": raw_fee,
            "start_date": start_date, "end_date": end_date,
            "cancellable": is_cancellable, "sig_comp": sig_comp, "enf_period": enf_period,
        }
        st.session_state.s1_done = True
        st.session_state.step = 2
        st.rerun()

if not st.session_state.s1_done:
    st.stop()

st.markdown('<hr class="divider">', unsafe_allow_html=True)
d1 = st.session_state.s1_data   # shorthand


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: CONTRACT MODIFICATION
# ─────────────────────────────────────────────────────────────────────────────
step_header(2, "Contract Modification Assessment", "IFRS 15.18–15.21")
guidance(
    "A contract modification is a change in the scope or price (or both) approved by both parties. "
    "The accounting treatment depends on whether additional goods/services are distinct and priced at "
    "their standalone selling price."
)

is_mod = st.radio(
    "Is this a modification of an existing contract, or a new contract?",
    ["New Contract", "Modification of Existing Contract"],
    key="m_is_mod",
)
mod_treatment   = "N/A - New Contract"
mod_description = ""

if is_mod == "Modification of Existing Contract":
    has_add = st.radio(
        "Does the modification add distinct goods/services at their standalone selling price?",
        ["Yes", "No"],
        key="m_has_add",
    )
    if has_add == "Yes":
        mod_treatment   = "Separate Contract (IFRS 15.20)"
        mod_description = (
            "Treat as a separate contract. Existing contract is unchanged. "
            "New contract is accounted for independently."
        )
        result(mod_description)
    else:
        blend = st.radio(
            "Are remaining goods/services distinct from those already transferred?",
            ["Yes — remaining goods/services are distinct",
             "No — not distinct from already transferred"],
            key="m_blend",
        )
        if blend.startswith("Yes"):
            mod_treatment   = "Prospective Modification (IFRS 15.21a)"
            mod_description = (
                "Treat as termination of old contract and creation of a new one. "
                "Allocate remaining consideration prospectively."
            )
        else:
            mod_treatment   = "Catch-Up Adjustment (IFRS 15.21b)"
            mod_description = (
                "Treat as part of the original contract. Record a cumulative catch-up "
                "adjustment to revenue in the current period."
            )
        result(f"{mod_treatment}: {mod_description}")

if st.button("✔ Complete Step 2 — Modification Assessment"):
    st.session_state.s2_data = {
        "is_mod": is_mod, "mod_treatment": mod_treatment, "mod_description": mod_description,
    }
    st.session_state.s2_done = True
    st.session_state.step = 3
    st.rerun()

if not st.session_state.s2_done:
    st.stop()

st.markdown('<hr class="divider">', unsafe_allow_html=True)
d2 = st.session_state.s2_data


# ─────────────────────────────────────────────────────────────────────────────
# PO CATALOGUE — Default timing and guidance per item type
# ─────────────────────────────────────────────────────────────────────────────
PO_CATALOGUE = {
    "Hardware Supply":                      {"timing": "Point in Time", "note": "Control transfers on physical delivery to customer."},
    "Software Licence - Perpetual":         {"timing": "Point in Time", "note": "Right-to-use licence; recognised at point of delivery."},
    "Software Licence - Subscription/SaaS": {"timing": "Over Time",    "note": "Access-based licence; recognised over the subscription period."},
    "Hardware + Software Bundle":           {"timing": "Point in Time", "note": "Combined transfer treated as single deliverable at point of control transfer."},
    "Managed / Professional Services":      {"timing": "Over Time",    "note": "Customer consumes benefits as the entity performs (IFRS 15.35a)."},
    "Implementation / Installation":        {"timing": "Point in Time", "note": "Usually on completion; override to Over Time if criteria 15.35a-c apply."},
    "Training":                             {"timing": "Point in Time", "note": "Recognised on completion of the training event."},
    "Support & Maintenance":                {"timing": "Over Time",    "note": "Stand-ready obligation; recognised ratably over the support period."},
    "Extended Warranty":                    {"timing": "Over Time",    "note": "Insurance-type PO; recognised over the coverage period."},
    "Material Right / Option":              {"timing": "Point in Time", "note": "Recognised at point of customer exercise of the option."},
    "Custom / Other":                       {"timing": "Point in Time", "note": "User-defined PO - override timing as appropriate."},
}
CAT_NAMES = list(PO_CATALOGUE.keys())


# ─────────────────────────────────────────────────────────────────────────────
# BLENDED SCHEDULE GENERATOR


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: PO BUILDER
# ─────────────────────────────────────────────────────────────────────────────
step_header(3, "Performance Obligation (PO) Builder", "IFRS 15.22–15.30 | 15.73–15.86")
# ── Fee reference banner for SSP entry ──
_s3_total_ssp = sum(p["ssp"] for p in st.session_state.po_list)
_s3_remaining = d1["raw_fee"] - _s3_total_ssp
_s3_rem_color = "#27AE60" if _s3_remaining >= 0 else "#C0392B"
st.markdown(
    f'<div style="background:#1A1A2E;color:#E8E6E0;padding:10px 16px;border-radius:4px;'
    f'font-family:IBM Plex Mono,monospace;font-size:0.82rem;margin-bottom:12px;">'
    f'📌 <b>Basic Contract Fee:</b> {fmt_number(d1["raw_fee"], d1["currency"])} &nbsp;·&nbsp; '
    f'<b>SSP Entered So Far:</b> {fmt_number(_s3_total_ssp, d1["currency"])} &nbsp;·&nbsp; '
    f'<span style="color:{_s3_rem_color};font-weight:600;">Remaining: '
    f'{fmt_number(_s3_remaining, d1["currency"])}</span></div>',
    unsafe_allow_html=True,
)

guidance(
    "Identify each distinct promised good or service as a separate performance obligation. "
    "Use the catalogue to select the PO type — timing defaults are pre-filled based on IFRS 15 "
    "but can be overridden. Enter the Standalone Selling Price (SSP) for each PO; the tool will "
    "allocate the final transaction price proportionally in Step 4."
)

with st.expander("📋 Distinctness Assessment Guide (IFRS 15.27–15.29)", expanded=False):
    st.markdown(
        "Before building POs, confirm whether items in the contract are **distinct**. "
        "A good/service is distinct when *both* conditions are met:"
    )
    st.markdown(
        "- **Capable of being distinct:** Customer can benefit from it on its own or with other readily available resources.\n"
        "- **Distinct in context of contract:** The entity's promise to transfer the item is separately identifiable from other promises."
    )
    st.markdown("**Bundling indicators (if any apply, combine into one PO):**")
    cb1 = st.checkbox("Significant integration service — entity combines goods/services into a bundle", key="po_distinct_b1")
    cb2 = st.checkbox("Significant customisation — one item significantly modifies or customises another", key="po_distinct_b2")
    cb3 = st.checkbox("Highly interrelated / interdependent — neither can be fulfilled without the other", key="po_distinct_b3")
    if cb1 or cb2 or cb3:
        st.markdown('<div class="warning-box">⚠️ Bundling indicator(s) detected. Consider combining affected items into a single PO entry below.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box">✅ No bundling indicators — each item may be a separate PO. Build the PO list below.</div>', unsafe_allow_html=True)
    st.markdown("**Additional obligations to check:**")
    ac1 = st.checkbox("Material Right (future discount / reward option)", key="po_mat_right")
    ac2 = st.checkbox("Implied Promise (business practice / customer expectation)", key="po_implied")
    ac3 = st.checkbox("Post-Transfer Shipping (shipping after control transfer)", key="po_shipping")
    if ac1 or ac2 or ac3:
        extras = [x for x, y in [("Material Right", ac1), ("Implied Promise", ac2), ("Post-Transfer Shipping", ac3)] if y]
        st.markdown(f'<div class="warning-box">⚠️ Add separate PO row(s) for: {", ".join(extras)}</div>', unsafe_allow_html=True)

st.markdown("---")

po_list = st.session_state.po_list
po_edit_idx = st.session_state.get("po_edit_idx", None)

if po_list:
    st.markdown(f"**{len(po_list)} PO(s) added to this contract:**")
    for idx, po in enumerate(po_list):
        if po.get("is_loyalty"):
            tag_color, tag_label = "#D9945A", "🎁 Loyalty (Deferred Revenue)"
        elif po["timing"] == "Over Time":
            tag_color, tag_label = "#27AE60", "🔄 Over Time"
        else:
            tag_color, tag_label = "#2E7D9C", "⚡ Point in Time"
        with st.container():
            col_info, col_actions = st.columns([9, 2])
            with col_info:
                st.markdown(
                    f"**{idx+1}. {po['name']}** &nbsp;&nbsp;"
                    f'<span style="background:{tag_color};color:white;padding:2px 8px;border-radius:3px;font-size:0.75rem;font-family:IBM Plex Mono,monospace;">{tag_label}</span>',
                    unsafe_allow_html=True,
                )
                timing_detail = (
                    f"Transfer date: {po['transfer_date']}"
                    if po["timing"] == "Point in Time"
                    else f"Service period: {po['svc_start']} → {po['svc_end']} | Method: {po['method']}"
                )
                st.caption(f"Catalogue: {po['catalogue']} | SSP: {po['currency']} {po['ssp']:,} | {timing_detail}")
            with col_actions:
                edit_col, del_col = st.columns(2)
                with edit_col:
                    if st.button("✏️", key=f"edit_po_{idx}", help="Edit this PO"):
                        st.session_state.po_edit_idx = idx
                        # Pre-fill form with PO data
                        st.session_state["new_po_name"] = po["name"]
                        st.session_state["new_po_cat"] = po["catalogue"]
                        st.session_state["new_po_timing"] = po["timing"]
                        st.session_state["new_po_ssp"] = str(po["ssp"])
                        st.session_state["new_po_transfer_date"] = po["transfer_date"]
                        st.session_state["new_po_svc_start"] = po["svc_start"]
                        st.session_state["new_po_svc_end"] = po["svc_end"]
                        st.session_state["new_po_method"] = po["method"]
                        st.rerun()
                with del_col:
                    if st.button("✕", key=f"del_po_{idx}", help="Remove this PO"):
                        st.session_state.po_list.pop(idx)
                        st.rerun()
    st.markdown("---")
else:
    st.info("No POs added yet. Use the form below to add at least one PO.")

if po_edit_idx is not None:
    st.markdown("#### ✏️ Edit Performance Obligation")
    st.markdown(f'<div style="background:#FFF3CD;border-left:4px solid #F39C12;padding:8px 12px;border-radius:0 4px 4px 0;font-size:0.85rem;color:#1A1A2E;margin-bottom:12px;">Editing PO #{po_edit_idx + 1}: <strong>{po_list[po_edit_idx]["name"]}</strong></div>', unsafe_allow_html=True)
else:
    st.markdown("#### ➕ Add Performance Obligation")

def _sync_timing_from_catalogue():
    selected_cat = st.session_state.get("new_po_cat", CAT_NAMES[0])
    st.session_state["new_po_timing"] = PO_CATALOGUE[selected_cat]["timing"]

np_col1, np_col2 = st.columns(2)
with np_col1:
    new_name = st.text_input(
        "PO Name *",
        key="new_po_name",
        placeholder="e.g., Hardware & Software Bundle",
        help="Give this PO a clear descriptive name"
    )
    new_cat = st.selectbox(
        "PO Catalogue Type *", CAT_NAMES, key="new_po_cat",
        on_change=_sync_timing_from_catalogue,
    )
    cat_info = PO_CATALOGUE[new_cat]
    st.markdown(
        f'<div class="ifrs-ref">📖 Default: <b>{cat_info["timing"]}</b> - {cat_info["note"]}</div>',
        unsafe_allow_html=True,
    )
    new_ssp_raw = st.text_input(
        f"Standalone Selling Price (SSP) in {d1['currency']} *",
        value="0", key="new_po_ssp",
        placeholder="e.g., 500,000,000",
        help="SSP is used to allocate the contract transaction price proportionally. Commas are ignored."
    )
    new_ssp = parse_number(new_ssp_raw)
    if new_ssp > 0:
        st.caption(f"Parsed: {fmt_number(new_ssp, d1['currency'])}")

with np_col2:
    if "new_po_timing" not in st.session_state:
        st.session_state["new_po_timing"] = cat_info["timing"]
    new_timing = st.radio(
        "Recognition Timing *",
        ["Point in Time", "Over Time"],
        key="new_po_timing",
        help="Pre-filled from catalogue. Override if your assessment differs."
    )
    if new_timing == "Point in Time":
        # default the transfer date to the contract delivery start
        default_transfer = d1.get("start_date") or d1.get("end_date")
        new_transfer = st.date_input(
            "Control Transfer Date *",
            key="new_po_transfer_date",
            value=default_transfer,
            help="Date when control of the good/service transfers to the customer."
        )
        new_svc_start = new_svc_end = new_transfer
        new_method = "N/A - Point in Time"
    else:
        new_svc_start = st.date_input("Service Period Start *", key="new_po_svc_start", value=d1["start_date"])
        new_svc_end   = st.date_input("Service Period End *",   key="new_po_svc_end",   value=d1["end_date"])
        new_method = st.selectbox(
            "Progress Measurement Method",
            ["Time-Elapsed (straight-line)", "Output Method (milestones/units)", "Input Method (costs/hours)"],
            key="new_po_method",
        )
        new_transfer = new_svc_start

add_errors = []
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    button_label = "💾 Save Changes" if po_edit_idx is not None else "➕ Add PO to Contract"
    if st.button(button_label):
        if not new_name.strip():
            add_errors.append("PO Name is required.")
        if new_ssp <= 0:
            add_errors.append("SSP must be greater than 0.")
        if new_timing == "Over Time" and new_svc_end <= new_svc_start:
            add_errors.append("Service Period End must be after Start.")
        if add_errors:
            for e in add_errors:
                st.error(e)
        else:
            po_data = {
                "name":          new_name.strip(),
                "catalogue":     new_cat,
                "timing":        new_timing,
                "ssp":           new_ssp,
                "transfer_date": new_transfer,
                "svc_start":     new_svc_start,
                "svc_end":       new_svc_end,
                "method":        new_method,
                "currency":      d1["currency"],
                "allocated_tp":  0,   
            }
            
            if po_edit_idx is not None:
                # Update existing PO
                st.session_state.po_list[po_edit_idx] = po_data
                st.session_state.po_edit_idx = None
                success_msg = f"✅ PO updated: {new_name.strip()}"
            else:
                # Add new PO
                st.session_state.po_list.append(po_data)
                success_msg = f"✅ PO added: {new_name.strip()}"
            
            # Clear form
            for k in ["new_po_name", "new_po_cat", "new_po_timing",
                      "new_po_transfer_date", "new_po_svc_start",
                      "new_po_svc_end", "new_po_method", "new_po_ssp"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.success(success_msg)
            st.rerun()

with btn_col2:
    if po_edit_idx is not None:
        if st.button("❌ Cancel Edit"):
            st.session_state.po_edit_idx = None
            for k in ["new_po_name", "new_po_cat", "new_po_timing",
                      "new_po_transfer_date", "new_po_svc_start",
                      "new_po_svc_end", "new_po_method", "new_po_ssp"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

st.markdown("---")
st.markdown("#### 🎁 Loyalty & Marketing Incentive Programme")
guidance(
    "If this contract includes a loyalty or marketing incentive programme, the customer reward "
    "is a Material Right under IFRS 15.B39 — a separate performance obligation. A portion of the "
    "transaction price must be deferred as a liability (Deferred Revenue) until the customer redeems "
    "the reward or it expires (breakage). This is NOT an OPEX item — unless an IAS 37 onerous "
    "obligation arises when the fulfilment cost exceeds the allocated TP."
)

loy_enabled = st.checkbox(
    "This contract includes a loyalty or marketing incentive programme",
    key="loy_enabled",
)

loyalty_data = {"enabled": False}

if loy_enabled:
    loy_col1, loy_col2 = st.columns(2)

    with loy_col1:
        loy_type = st.selectbox(
            "Q1 — Programme type *",
            ["Loyalty Points (redeemable for own products/services)",
             "Marketing Incentive (sponsorship / holiday / gifts)",
             "Volume Rebate (cash or credit)",
             "Other Incentive Programme"],
            key="loy_type",
            help="Determines Material Right vs. cost provision treatment."
        )
        loy_rate = st.number_input(
            "Q2 — Reward rate (% of contract fee) *",
            min_value=0.0, max_value=100.0, value=0.1, step=0.01, format="%.4f",
            key="loy_rate",
            help="e.g. 0.1 means 0.1% of the basic contract fee."
        )
        loy_ssp_calc = round(d1["raw_fee"] * loy_rate / 100)
        st.caption(f"Calculated Loyalty SSP: {fmt_number(loy_ssp_calc, d1['currency'])}")
        _loy_override_raw = st.text_input(
            "Override SSP (leave 0 to use calculated amount)",
            value="0", key="loy_ssp_override",
            placeholder="e.g., 50,000,000",
            help="Override if the fair value of the reward is independently observable. Commas ignored."
        )
        loy_ssp_override = parse_number(_loy_override_raw)
        loy_ssp = loy_ssp_override if loy_ssp_override > 0 else loy_ssp_calc
        loy_redemption_rate = st.slider(
            "Q6 — Expected redemption rate (%)",
            min_value=0, max_value=100, value=100, step=5,
            key="loy_redemption_rate",
            help="IFRS 15.B42: % of rewards expected to be redeemed. Default 100% = assume full redemption."
        )

    with loy_col2:
        loy_market_eq = st.radio(
            "Q3 — Is the redemption item priced at normal market value?",
            ["Yes — redemption value equals normal market price",
             "Sometimes below — entity may fulfil at below market price"],
            key="loy_market_eq",
        )
        loy_prob_below  = 0.0
        loy_avg_below   = 0
        ias37_provision = 0

        if loy_market_eq.startswith("Sometimes"):
            guidance(
                "When there is a probability the entity fulfils at below market price, "
                "the EXCESS cost above the allocated TP is an IAS 37.66 onerous obligation. "
                "Use the Most Likely Amount method (IFRS 15.53b) to estimate it."
            )
            loy_prob_below = st.slider(
                "Q4 — Probability of below-market redemption (%)",
                min_value=0, max_value=100, value=25, step=5,
                key="loy_prob_below",
            )
            _avg_below_raw = st.text_input(
                f"Q5 — Average shortfall ({d1['currency']}) when item is below market",
                value="0", key="loy_avg_below",
                placeholder="e.g., 5,000,000",
                help="Amount by which fulfilment cost exceeds the loyalty SSP in below-market scenarios. Commas ignored."
            )
            loy_avg_below = parse_number(_avg_below_raw)
            ias37_provision = round(loy_prob_below / 100 * loy_avg_below)

        loy_redeemed_rev = round(loy_ssp * loy_redemption_rate / 100)
        loy_breakage_rev = loy_ssp - loy_redeemed_rev

        st.markdown("**Computed Summary**")
        comp_rows = [
            ("Loyalty SSP = Deferred Revenue",     fmt_number(loy_ssp, d1["currency"])),
            ("Expected Redeemed Revenue",           fmt_number(loy_redeemed_rev, d1["currency"])),
            ("Breakage Revenue (IFRS 15.B44)",      fmt_number(loy_breakage_rev, d1["currency"])),
        ]
        if ias37_provision > 0:
            comp_rows.append(("IAS 37 OPEX Provision (onerous)", fmt_number(ias37_provision, d1["currency"])))
        st.dataframe(pd.DataFrame(comp_rows, columns=["Item", "Amount"]),
                     use_container_width=True, hide_index=True)

    if loy_market_eq.startswith("Yes"):
        result(
            f"IFRS 15 Material Right: At contract inception — "
            f"Cr Revenue {fmt_number(d1['raw_fee'] - loy_ssp, d1['currency'])} "
            f"+ Cr Deferred Revenue {fmt_number(loy_ssp, d1['currency'])}. "
            f"Deferred Revenue released on redemption or breakage. No OPEX entry required."
        )
    else:
        result(
            f"IFRS 15 Material Right + IAS 37 Onerous Risk: "
            f"Deferred Revenue {fmt_number(loy_ssp, d1['currency'])} (IFRS 15). "
            f"Separate OPEX provision {fmt_number(ias37_provision, d1['currency'])} "
            f"for excess fulfilment cost (IAS 37). Do NOT combine these into one OPEX line."
        )

    loyalty_data = {
        "enabled":            True,
        "programme_type":     loy_type,
        "reward_rate_pct":    loy_rate,
        "loyalty_ssp":        loy_ssp,
        "ssp_overridden":     loy_ssp_override > 0,
        "redemption_rate_pct":loy_redemption_rate,
        "market_eq":          loy_market_eq.split(" — ")[0] if " — " in loy_market_eq else loy_market_eq,
        "prob_below_pct":     loy_prob_below,
        "avg_below_amount":   loy_avg_below,
        "ias37_provision":    ias37_provision,
        "redeemed_revenue":   loy_redeemed_rev,
        "breakage_revenue":   loy_breakage_rev,
    }

    existing_loyalty = [p for p in st.session_state.po_list if p.get("is_loyalty")]
    if existing_loyalty:
        warning(
            "Loyalty PO already in the PO list above "
            f"(SSP: {fmt_number(existing_loyalty[0]['ssp'], d1['currency'])}). "
            "Remove it from the list and re-add if you changed the SSP."
        )
    else:
        if st.button("➕ Add Loyalty PO to Contract List", key="btn_add_loyalty"):
            if loy_ssp <= 0:
                st.error("Loyalty SSP must be greater than 0 before adding.")
            else:
                po_name = f"Loyalty - {loy_type.split('(')[0].strip() if '(' in loy_type else loy_type}"
                st.session_state.po_list.append({
                    "name":          po_name,
                    "catalogue":     "Material Right / Option",
                    "timing":        "Point in Time",
                    "ssp":           loy_ssp,
                    "transfer_date": d1["end_date"],
                    "svc_start":     d1["start_date"],
                    "svc_end":       d1["end_date"],
                    "method":        "N/A - Point in Time",
                    "currency":      d1["currency"],
                    "allocated_tp":  0,
                    "is_loyalty":    True,
                })
                st.rerun()

else:
    orphaned = [p for p in st.session_state.po_list if p.get("is_loyalty")]
    if orphaned:
        warning(
            "Loyalty programme has been toggled off, but a Loyalty PO is still in the PO list. "
            "Remove it from the list above if it is no longer applicable."
        )

st.markdown("---")
if st.button("✔ Complete Step 3 — PO Builder"):
    if not st.session_state.po_list:
        st.error("Add at least one Performance Obligation before proceeding.")
    else:
        total_ssp = sum(p["ssp"] for p in st.session_state.po_list)
        po_status = "Single PO" if len(st.session_state.po_list) == 1 else f"Multiple POs ({len(st.session_state.po_list)})"
        timings   = list({p["timing"] for p in st.session_state.po_list})
        timing_summary = "Mixed (Point in Time + Over Time)" if len(timings) > 1 else timings[0]
        st.session_state.s3_data = {
            "po_list":        copy.deepcopy(st.session_state.po_list),
            "po_status":      po_status,
            "total_ssp":      total_ssp,
            "timing_summary": timing_summary,
            "loyalty_data":   loyalty_data,
        }
        st.session_state.s3_done = True
        st.session_state.step = 4
        st.rerun()

if not st.session_state.s3_done:
    st.stop()

st.markdown('<hr class="divider">', unsafe_allow_html=True)
d3 = st.session_state.s3_data


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: TRANSACTION PRICE, VARIABLE CONSIDERATION & PO ALLOCATION
# ─────────────────────────────────────────────────────────────────────────────
step_header(4, "Transaction Price & PO Allocation", "IFRS 15.47–15.72 | 15.73–15.86")

st.markdown("**Variable Consideration (IFRS 15.50–15.56)**")
guidance(
    "Assessed at contract level. Variable consideration is included in the transaction price only "
    "to the extent it is highly probable that a significant revenue reversal will not occur. "
    "Once the final TP is determined, it is allocated to each PO based on relative SSP."
)

vc_col1, vc_col2 = st.columns(2)
with vc_col1:
    has_var = st.radio("Is there any variable consideration?", ["No", "Yes"], key="v_has")
    var_impact  = 0
    var_type    = "None"
    est_method  = "N/A"
    constrained = False

    if has_var == "Yes":
        var_dir = st.radio(
            "Direction of variable consideration",
            ["Reduction (penalty / refund / discount)", "Addition (bonus / incentive)"],
            key="v_dir",
        )
        var_impact = st.number_input(
            "Estimated variable amount", min_value=0, value=0, step=1000, key="v_val"
        )
        est_method = st.selectbox(
            "Estimation method",
            ["Expected Value (probability-weighted)", "Most Likely Amount"],
            key="v_method",
        )
        prob = st.radio(
            "Constraint test — highly probable no significant reversal? (IFRS 15.56)",
            ["Yes — include in TP", "No — constrain / exclude"],
            key="v_prob",
        )
        constrained = prob.startswith("No")
        var_type = "Reduction" if var_dir.startswith("Reduction") else "Addition"

with vc_col2:
    base_fee = d1["raw_fee"]
    if has_var == "Yes" and not constrained:
        final_tp = base_fee - var_impact if var_type == "Reduction" else base_fee + var_impact
    else:
        final_tp = base_fee

    if constrained and has_var == "Yes":
        warning("Variable consideration constrained — excluded from TP. Re-assess at each reporting date.")

    mc1, mc2 = st.columns(2)
    _kpi(mc1, "Basic Contract Fee",
         fmt_metric(base_fee, d1["currency"]),
         fmt_number(base_fee, d1["currency"]))
    _kpi(mc2, "Final Transaction Price",
         fmt_metric(final_tp, d1["currency"]),
         fmt_number(final_tp, d1["currency"]) if base_fee != final_tp else "")

_loy_d4 = d3.get("loyalty_data", {})
_has_loyalty_po = any(p.get("is_loyalty") for p in d3.get("po_list", []))
if _has_loyalty_po and has_var == "Yes" and var_type == "Reduction":
    warning(
        "Double-count risk detected: You have a Loyalty Material Right PO in the PO list "
        "AND a Variable Consideration Reduction entered above. "
        "The loyalty reward is already deducted from primary-PO revenue through TP allocation — "
        "do NOT also enter it as a VC Reduction, or the transaction price will be reduced twice. "
        "Remove the VC Reduction if it relates to the loyalty programme."
    )

# ════════════════════════════════════════════════════════════════════════════
# SIGNIFICANT FINANCING COMPONENT (IFRS 15.60–15.65)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("**💰 Significant Financing Component (IFRS 15.60–15.65)**")
guidance(
    "IFRS 15.60 requires the transaction price to be adjusted for the time value of money "
    "when the payment timing gives either party a significant financing benefit. "
    "This arises when there is a material gap between (a) when the customer pays and "
    "(b) when control of goods/services transfers. "
    "Practical expedient (IFRS 15.62): if the gap is ≤12 months, skip this entire section."
)

sfc_enabled = st.checkbox(
    "The timing of payment and transfer of goods/services is separated by more than 12 months",
    key="sfc_enabled",
)
sfc_data = {"enabled": False}

if sfc_enabled:
    st.markdown("##### Step 1 — Direction of Financing (IFRS 15.60)")
    guidance(
        "Identify WHO provides finance to WHOM. "
        "**Advance:** customer pays before delivery → entity holds customer's money → records Finance COST, "
        "Revenue > cash received. "
        "**Deferred:** customer pays after delivery → entity extends credit → records Finance INCOME, "
        "Revenue < nominal receivable."
    )
    sfc_direction = st.radio(
        "Payment arrangement:",
        [
            "Advance — customer pays BEFORE transfer of goods/services "
            "(entity uses customer's cash → Finance Cost, Revenue > Cash received)",
            "Deferred — customer pays AFTER transfer of goods/services "
            "(entity extends credit → Finance Income, Revenue < Nominal receivable)",
        ],
        key="sfc_direction",
    )
    is_advance = sfc_direction.startswith("Advance")

    st.markdown("##### Step 2 — IFRS 15.B50 Exception Check")
    guidance(
        "Even when the gap exceeds 12 months, IFRS 15.B50 exempts the SFC adjustment "
        "in three situations. Tick any that apply."
    )
    b50_c1, b50_c2, b50_c3 = st.columns(3)
    with b50_c1:
        sfc_b50_a = st.checkbox(
            "**Exception (a)** — Customer paid in advance AND the timing of transfer "
            "is at the **customer's discretion** (e.g., activate licence whenever they choose)",
            key="sfc_b50_a",
        )
    with b50_c2:
        sfc_b50_b = st.checkbox(
            "**Exception (b)** — A substantial portion of consideration is **variable** "
            "and its amount/timing depends on a future event outside both parties' control",
            key="sfc_b50_b",
        )
    with b50_c3:
        sfc_b50_c = st.checkbox(
            "**Exception (c)** — The **difference** between the promised consideration "
            "and the cash selling price is NOT material to the contract",
            key="sfc_b50_c",
        )

    sfc_b50_triggered = sfc_b50_a or sfc_b50_b or sfc_b50_c
    if sfc_b50_triggered:
        exceptions_hit = [
            lbl for lbl, hit in [
                ("(a) Customer-Discretion Timing", sfc_b50_a),
                ("(b) Variable Consideration Dominant", sfc_b50_b),
                ("(c) Immaterial Difference", sfc_b50_c),
            ] if hit
        ]
        result(
            f"IFRS 15.B50 Exception applies — {', '.join(exceptions_hit)}. "
            "No SFC adjustment required. Nominal transaction price stands."
        )
        sfc_data = {
            "enabled": True, "mode": "none", "direction": "advance" if is_advance else "deferred",
            "b50_exception": True, "b50_flags": exceptions_hit,
            "adj_revenue": final_tp, "finance_amt": 0, "rate_pct": 0,
            "period_months": 0, "sfc_significant": False,
        }

    else:
        st.markdown("##### Step 3 — Significance Assessment (IFRS 15.B49)")
        guidance(
            "A gap > 12 months does NOT automatically create an SFC — you must judge whether "
            "the financing component is significant in the context of this contract. "
            "Key factors: (1) the difference between adjusted and nominal amounts is material, "
            "(2) financing was a primary commercial reason for the payment structure, "
            "(3) market interest rates produce a material adjustment."
        )
        sfc_sig_radio = st.radio(
            "Is the financing component significant to this contract?",
            ["Yes — financing is significant, adjustment required",
             "No — financing is not significant, nominal TP stands"],
            key="sfc_significant",
        )
        is_sig = sfc_sig_radio.startswith("Yes")

        if not is_sig:
            result(
                "Financing component assessed as NOT significant (IFRS 15.B49). "
                "No SFC adjustment required. Nominal transaction price stands."
            )
            sfc_data = {
                "enabled": True, "mode": "none", "direction": "advance" if is_advance else "deferred",
                "b50_exception": False, "b50_flags": [],
                "adj_revenue": final_tp, "finance_amt": 0, "rate_pct": 0,
                "period_months": 0, "sfc_significant": False,
            }
        else:
            st.markdown("##### Step 4 — Payment Structure Mode")
            guidance(
                "Choose the payment model that matches your contract. "
                "**Single Payment** = one lump-sum paid before or after delivery (simplest). "
                "**Annuity** = equal monthly installments billed over time; hardware/goods delivered "
                "upfront while payments are collected over the contract term — this is the correct "
                "model for blended hardware + services contracts with monthly invoicing."
            )
            sfc_mode = st.radio(
                "Payment structure:",
                [
                    "Single Payment — one lump-sum payment before or after delivery",
                    "Annuity — equal monthly installments billed over multiple periods",
                ],
                key="sfc_mode",
            )
            is_annuity = sfc_mode.startswith("Annuity")

            sfc_po_idx = 0
            _po_names  = [p["name"] for p in d3["po_list"]]
            if is_annuity and _po_names:
                st.markdown("##### Step 4a — Which PO Carries the Financing Component?")
                guidance(
                    "In a blended contract (e.g. hardware + managed services), only the hardware PO "
                    "carries the SFC because hardware control transfers at delivery (Month 1) while "
                    "payments are collected over 36 months. The services PO is delivered and billed in the "
                    "same month — its financing gap is typically immaterial (IFRS 15.B50(c) exception). "
                    "Select the PO that is delivered upfront but paid over time."
                )
                sfc_po_name = st.selectbox(
                    "Select the PO that carries the financing component *",
                    options=_po_names,
                    key="sfc_po_idx",
                    help="This PO's allocated TP will be replaced with the SFC-adjusted (PV) revenue amount."
                )
                sfc_po_idx = _po_names.index(sfc_po_name) if sfc_po_name in _po_names else 0
                _sfc_po    = d3["po_list"][sfc_po_idx]
                _hw_ssp    = _sfc_po["ssp"]
                _total_ssp = d3["total_ssp"] or 1
                _hw_ssp_pct = _hw_ssp / _total_ssp
                st.caption(
                    f"Selected: **{_sfc_po['name']}** | SSP: {fmt_number(_hw_ssp, d1['currency'])} "
                    f"({_hw_ssp_pct*100:.1f}% of total SSP)"
                )
            else:
                _hw_ssp_pct = 1.0

            st.markdown("##### Step 5 — Discount Rate (IFRS 15.63)")
            guidance(
                "Use the rate that a separate financing transaction between entity and customer would reflect "
                "at contract inception. Two options: "
                "(A) **Incremental Borrowing Rate (IBR)** — rate at which your entity could borrow a similar "
                "amount for a similar term (most common in practice). "
                "(B) **Implicit Rate** — derived mathematically from the cash selling price vs. deferred total "
                "(use the calculator below if both amounts are observable)."
            )

            with st.expander("🧮 Implicit Rate Calculator (optional — use if cash selling price is known)", expanded=False):
                if is_annuity:
                    st.markdown(
                        "**Annuity mode:** Enter the cash price the customer would pay today for the hardware "
                        "PO if it were sold standalone for immediate cash, plus the monthly hardware-attributed "
                        "installment and number of months. The tool solves for the rate."
                    )
                    impl_col1, impl_col2 = st.columns(2)
                    with impl_col1:
                        _impl_cash_raw = st.text_input(
                            f"Cash selling price of hardware PO ({d1['currency']})",
                            value="0", key="sfc_cash_price_ann",
                            placeholder="e.g., 800,000,000",
                            help="What the hardware would cost if the customer paid 100% upfront today."
                        )
                        _impl_cash = parse_number(_impl_cash_raw)
                        if _impl_cash > 0:
                            st.caption(f"Parsed: {fmt_number(_impl_cash, d1['currency'])}")
                        _impl_n = st.number_input(
                            "Number of monthly installments",
                            min_value=1, max_value=360, value=36, step=1,
                            key="sfc_months_impl_ann",
                        )
                    with impl_col2:
                        _impl_n_safe = _impl_n if isinstance(_impl_n, (int, float)) and _impl_n > 0 else 36
                        _monthly_inv_default = int(final_tp / _impl_n_safe)
                        _monthly_inv_raw = st.text_input(
                            f"Monthly blended invoice ({d1['currency']})",
                            value=str(_monthly_inv_default), key="sfc_impl_monthly_pmt",
                            placeholder="e.g., 41,666,667",
                            help="Total monthly invoice amount (hardware + services combined)."
                        )
                        _monthly_inv = parse_number(_monthly_inv_raw)
                        if _monthly_inv > 0 and _impl_n > 0:
                            _monthly_hw = _monthly_inv * _hw_ssp_pct
                            st.caption(f"Hardware portion of each invoice: {fmt_number(int(_monthly_hw), d1['currency'])} ({_hw_ssp_pct*100:.1f}%)")
                        else:
                            _monthly_hw = 0

                        if _impl_cash > 0 and _monthly_hw > 0 and _impl_n > 0:
                            _derived_rate = calc_implicit_rate_annuity(_impl_cash, _monthly_hw, int(_impl_n))
                            if _derived_rate > 0:
                                st.success(f"**Derived implicit rate: {_derived_rate:.4f}% p.a.** \nCopy this to the rate field below.")
                            else:
                                st.warning("Could not derive rate — check that cash price < total nominal installments.")
                else:
                    st.markdown(
                        "**Single payment mode:** Enter the cash selling price (PV) and the nominal deferred "
                        "amount the customer actually pays. The tool solves for the annual implicit rate."
                    )
                    impl_col1, impl_col2 = st.columns(2)
                    with impl_col1:
                        _impl_cash_raw = st.text_input(
                            f"Cash selling price today ({d1['currency']})",
                            value="0", key="sfc_cash_price_single",
                            placeholder="e.g., 900,000,000",
                        )
                        _impl_cash = parse_number(_impl_cash_raw)
                        if _impl_cash > 0:
                            st.caption(f"Parsed: {fmt_number(_impl_cash, d1['currency'])}")
                    with impl_col2:
                        _impl_n_single = st.number_input(
                            "Months between payment and delivery",
                            min_value=1, max_value=360, value=18, step=1,
                            key="sfc_months_impl_single",
                        )
                        if _impl_cash > 0 and _impl_n_single > 0 and final_tp > 0:
                            _derived_rate = calc_implicit_rate_single(_impl_cash, final_tp, int(_impl_n_single))
                            if _derived_rate > 0:
                                st.success(f"**Derived implicit rate: {_derived_rate:.4f}% p.a.** \nCopy this to the rate field below.")

            sfc_rate = st.number_input(
                "Discount rate — annual % (IBR or implicit rate) *",
                min_value=0.01, max_value=50.0, value=7.5, step=0.25, format="%.2f",
                key="sfc_rate",
                help="e.g. 7.50 = 7.50% p.a. Paste the derived implicit rate here if you used the calculator above.",
            )

            if not is_annuity:
                st.markdown("##### Step 6 — Single Payment Period")
                sfc_months_single = st.number_input(
                    "Months between payment and control transfer *",
                    min_value=1, max_value=360, value=18, step=1,
                    key="sfc_months_main_single",
                    help="Advance: months from payment to delivery. Deferred: months from delivery to collection.",
                )
                _dir = "advance" if is_advance else "deferred"
                adj_rev, fin_amt, _sfc_df = build_sfc_schedule(
                    final_tp, _dir, sfc_rate, int(sfc_months_single)
                )
                fin_pct = fin_amt / final_tp * 100 if final_tp else 0

                memo_col1, memo_col2 = st.columns(2)
                with memo_col1:
                    st.markdown("**SFC Adjustment (Memo Line)**")
                    st.dataframe(pd.DataFrame([
                        ("Nominal Contract Fee",             fmt_number(final_tp, d1["currency"])),
                        ("SFC-Adjusted Revenue",             fmt_number(adj_rev,  d1["currency"])),
                        ("Finance " + ("Cost" if is_advance else "Income"),
                                                             fmt_number(fin_amt,  d1["currency"])),
                        ("Adjustment %",                     f"{fin_pct:.2f}%"),
                        ("Rate",                             f"{sfc_rate:.2f}% p.a."),
                        ("Period",                           f"{int(sfc_months_single)} months"),
                    ], columns=["Item", "Value"]), use_container_width=True, hide_index=True)
                    if fin_pct < 1:
                        warning(f"Adjustment is only {fin_pct:.2f}% of contract value — reconsider materiality (IFRS 15.B49).")

                with st.expander("📒 Journal Entry Templates — Single Payment (IFRS 15.65)", expanded=False):
                    if is_advance:
                        st.markdown(f"""
**At contract signing (cash received):**
Dr  Cash / Bank                        {fmt_number(final_tp, d1['currency'])}
Cr  Contract Liability                {fmt_number(final_tp, d1['currency'])}

**Each month during advance period (accretion):**
Dr  Finance Cost (P&L — separate line)  [monthly amount — see schedule below]
Cr  Contract Liability                 [monthly amount]

**At delivery / control transfer:**
Dr  Contract Liability                 {fmt_number(adj_rev, d1['currency'])}
Cr  Revenue                            {fmt_number(adj_rev, d1['currency'])}

⚠️ **IFRS 15.65:** Finance Cost **must appear as a separate line on the P&L face** — never net against Revenue or include in Cost of Sales.

Revenue at delivery: **{fmt_number(adj_rev, d1['currency'])}** (> cash received {fmt_number(final_tp, d1['currency'])})  
Total Finance Cost: **{fmt_number(fin_amt, d1['currency'])}**
""")
                    else:
                        st.markdown(f"""
**At delivery / control transfer:**
Dr  Receivable (PV-adjusted)           {fmt_number(adj_rev, d1['currency'])}
Cr  Revenue                            {fmt_number(adj_rev, d1['currency'])}

**Each month during credit period (accretion):**
Dr  Receivable                         [monthly amount — see schedule below]
Cr  Finance Income (P&L — separate line)  [monthly amount]

**At collection:**
Dr  Cash / Bank                        {fmt_number(final_tp, d1['currency'])}
Cr  Receivable                        {fmt_number(final_tp, d1['currency'])}

⚠️ **IFRS 15.65:** Finance Income **must appear as a separate line on the P&L face** — never gross up Revenue or bury in Other Income.

Revenue at delivery: **{fmt_number(adj_rev, d1['currency'])}** (< nominal {fmt_number(final_tp, d1['currency'])})  
Total Finance Income: **{fmt_number(fin_amt, d1['currency'])}**
""")

                st.markdown("**📅 Monthly Interest Accretion Schedule**")
                st.dataframe(_sfc_df, use_container_width=True, hide_index=True)

                sfc_data = {
                    "enabled": True, "mode": "single", "is_advance": is_advance,
                    "direction": _dir, "b50_exception": False, "b50_flags": [],
                    "sfc_significant": True, "rate_pct": sfc_rate,
                    "period_months": int(sfc_months_single),
                    "nominal_tp": final_tp, "adj_revenue": adj_rev, "finance_amt": fin_amt,
                    "sfc_po_idx": None,
                }

            else:
                st.markdown("##### Step 6 — Annuity Structure Inputs")
                guidance(
                    "For a blended contract (hardware + services, monthly invoice), the hardware PO "
                    "is delivered at Month 1 but paid through 36 equal monthly installments. "
                    "Its revenue = PV of its share of all future installments. "
                    "The difference accretes monthly as Finance Income on the Contract Asset (Unbilled AR)."
                )
                ann_col1, ann_col2 = st.columns(2)
                with ann_col1:
                    _ann_months = st.number_input(
                        "Number of monthly installments (e.g., 36 for 3-year contract) *",
                        min_value=1, max_value=360, value=36, step=1,
                        key="sfc_months_main_ann",
                        help="Total number of equal monthly invoices over the contract term.",
                    )
                    _ann_inv_default = str(int(final_tp / max(_ann_months, 1)))
                    _ann_inv_raw = st.text_input(
                        f"Monthly blended invoice amount ({d1['currency']}) *",
                        value=_ann_inv_default,
                        placeholder="e.g., 41,666,667",
                        help="Total monthly invoice = hardware portion + services portion combined.",
                        key="sfc_monthly_pmt_override",
                    )
                    _ann_inv = parse_number(_ann_inv_raw)
                    if _ann_inv > 0:
                        st.caption(f"Parsed: {fmt_number(_ann_inv, d1['currency'])}")

                with ann_col2:
                    if _ann_inv > 0 and _ann_months > 0:
                        _monthly_hw_pmt  = _ann_inv * _hw_ssp_pct
                        _hw_nominal      = round(_monthly_hw_pmt * _ann_months)
                        adj_rev_ann, fin_inc_ann, _ca_df = build_sfc_annuity_schedule(
                            _hw_nominal, _monthly_hw_pmt, int(_ann_months), sfc_rate
                        )
                        fin_pct_ann = fin_inc_ann / _hw_nominal * 100 if _hw_nominal else 0

                        st.markdown("**SFC Adjustment — Hardware PO (Memo)**")
                        _sfc_po_name = _po_names[sfc_po_idx] if _po_names else "Selected PO"
                        st.dataframe(pd.DataFrame([
                            ("PO bearing SFC",               _sfc_po_name),
                            ("Hardware SSP share",           f"{_hw_ssp_pct*100:.1f}%"),
                            ("Monthly HW instalment",        fmt_number(int(_monthly_hw_pmt), d1["currency"])),
                            ("HW nominal total (36 × pmt)",  fmt_number(_hw_nominal, d1["currency"])),
                            ("IFRS 15 HW Revenue (PV)",      fmt_number(adj_rev_ann, d1["currency"])),
                            ("Finance Income (total)",        fmt_number(fin_inc_ann, d1["currency"])),
                            ("Adjustment %",                  f"{fin_pct_ann:.2f}%"),
                            ("Rate",                          f"{sfc_rate:.2f}% p.a."),
                            ("Installments",                  f"{int(_ann_months)} months"),
                        ], columns=["Item", "Value"]), use_container_width=True, hide_index=True)

                        if fin_pct_ann < 1:
                            warning(f"Adjustment is only {fin_pct_ann:.2f}% — reconsider materiality (IFRS 15.B49).")

                if _ann_inv > 0 and _ann_months > 0:
                    _monthly_hw_pmt  = _ann_inv * _hw_ssp_pct
                    _hw_nominal      = round(_monthly_hw_pmt * _ann_months)
                    adj_rev_ann, fin_inc_ann, _ca_df = build_sfc_annuity_schedule(
                        _hw_nominal, _monthly_hw_pmt, int(_ann_months), sfc_rate
                    )

                    with st.expander("📒 Journal Entry Templates — Annuity / Contract Asset (IFRS 15.65)", expanded=False):
                        _svc_monthly = int(_ann_inv * (1 - _hw_ssp_pct))
                        st.markdown(f"""
**Month 1 — Hardware delivered, Contract Asset (Unbilled AR) recognised:**
Dr  Contract Asset (Unbilled AR)       {fmt_number(adj_rev_ann, d1['currency'])}
Cr  Revenue — Hardware                {fmt_number(adj_rev_ann, d1['currency'])}

*Revenue = PV of {int(_ann_months)} monthly HW instalments at {sfc_rate:.2f}% p.a. — NOT the nominal sum.*

**Each subsequent month (Months 2 → {int(_ann_months)+1}) — three simultaneous events:**

*Event 1 — Finance Income accreted on Contract Asset:*
Dr  Contract Asset                     [monthly interest — see schedule]
Cr  Finance Income (P&L)              [monthly interest]

*Event 2 — Monthly invoice raised (billing right crystallises):*
Dr  Accounts Receivable (Trade AR)     {fmt_number(_ann_inv, d1['currency'])}
Cr  Contract Asset                    {fmt_number(int(_monthly_hw_pmt), d1['currency'])}  [HW portion]
Cr  Revenue — Services                {fmt_number(_svc_monthly, d1['currency'])}  [Services portion]

*Event 3 — Customer pays invoice:*
Dr  Cash / Bank                        {fmt_number(_ann_inv, d1['currency'])}
Cr  Accounts Receivable               {fmt_number(_ann_inv, d1['currency'])}


⚠️ **IFRS 15.65 — Presentation:** Finance Income **must be a separate line on the P&L face**.  
Do NOT gross up Revenue or include it in Other Income.

Hardware Revenue at Month 1: **{fmt_number(adj_rev_ann, d1['currency'])}** (PV — less than nominal {fmt_number(_hw_nominal, d1['currency'])})  
Total Finance Income over {int(_ann_months)} months: **{fmt_number(fin_inc_ann, d1['currency'])}** Contract Asset reaches **zero** at end of Month {int(_ann_months)} ✓
""")

                    st.markdown("**📅 Contract Asset (Unbilled AR) — Monthly Waterfall Schedule**")
                    st.dataframe(_ca_df, use_container_width=True, hide_index=True)

                    sfc_data = {
                        "enabled": True, "mode": "annuity", "is_advance": False,
                        "direction": "deferred", "b50_exception": False, "b50_flags": [],
                        "sfc_significant": True, "rate_pct": sfc_rate,
                        "period_months": int(_ann_months),
                        "nominal_tp": _hw_nominal, "adj_revenue": adj_rev_ann,
                        "finance_amt": fin_inc_ann, "sfc_po_idx": sfc_po_idx,
                        "monthly_invoice": _ann_inv, "monthly_hw_pmt": _monthly_hw_pmt,
                        "hw_ssp_pct": _hw_ssp_pct,
                    }
                else:
                    sfc_data = {
                        "enabled": True, "mode": "annuity", "direction": "deferred",
                        "b50_exception": False, "b50_flags": [], "sfc_significant": True,
                        "rate_pct": sfc_rate, "period_months": 0,
                        "nominal_tp": 0, "adj_revenue": final_tp, "finance_amt": 0,
                        "sfc_po_idx": sfc_po_idx, "monthly_invoice": 0,
                        "monthly_hw_pmt": 0, "hw_ssp_pct": _hw_ssp_pct,
                    }

st.markdown("---")
st.markdown("**TP Allocation by Performance Obligation (IFRS 15.73–15.80)**")
guidance(
    "The transaction price is allocated to each PO based on its relative SSP. "
    "If the sum of SSPs differs from contract TP, the residual or adjusted SSP method may apply. "
    "If a PO carries a Significant Financing Component (annuity mode), its allocated TP is replaced "
    "with the SFC-adjusted PV revenue amount — the correct IFRS 15 revenue for that PO."
)

po_list_work = copy.deepcopy(d3["po_list"])
total_ssp    = d3["total_ssp"] or 1

_sfc_annuity_active = (
    sfc_data.get("enabled") and
    sfc_data.get("sfc_significant") and
    sfc_data.get("mode") == "annuity" and
    sfc_data.get("adj_revenue", 0) > 0
)
_sfc_po_idx_alloc = sfc_data.get("sfc_po_idx")

alloc_rows = []
for i, po in enumerate(po_list_work):
    alloc = round(final_tp * po["ssp"] / total_ssp)
    sfc_override = (
        _sfc_annuity_active and
        _sfc_po_idx_alloc is not None and
        i == _sfc_po_idx_alloc
    )
    if sfc_override:
        alloc = sfc_data["adj_revenue"]
    po["allocated_tp"] = alloc
    alloc_rows.append({
        "PO Name":          po["name"],
        "Catalogue Type":   po["catalogue"],
        "Timing":           po["timing"],
        f"SSP ({d1['currency']})":          f"{po['ssp']:,}",
        "SSP %":            f"{po['ssp']/total_ssp*100:.1f}%",
        f"Allocated TP ({d1['currency']})": f"{alloc:,}",
        "SFC Adjusted":     "✅ PV-adjusted" if sfc_override else "—",
    })

# Rounding correction: for non-SFC POs, ensure sum equals final_tp
if not _sfc_annuity_active:
    _total_non_sfc = sum(p["allocated_tp"] for p in po_list_work)
    _rounding_diff = final_tp - _total_non_sfc
    if po_list_work and _rounding_diff != 0:
        po_list_work[-1]["allocated_tp"] += _rounding_diff
        alloc_rows[-1][f"Allocated TP ({d1['currency']})"] = f"{po_list_work[-1]['allocated_tp']:,}"
else:
    # SFC annuity: fix rounding on non-SFC POs so they still sum correctly
    _non_sfc_total = sum(
        p["allocated_tp"] for i, p in enumerate(po_list_work)
        if i != _sfc_po_idx_alloc
    )
    _non_sfc_target = final_tp - (sfc_data.get("adj_revenue", 0) if _sfc_po_idx_alloc is not None else 0)
    _rounding_diff2 = _non_sfc_target - _non_sfc_total
    if _rounding_diff2 != 0 and po_list_work:
        # Apply to last non-SFC PO
        for _rci in range(len(po_list_work)-1, -1, -1):
            if _rci != _sfc_po_idx_alloc:
                po_list_work[_rci]["allocated_tp"] += _rounding_diff2
                alloc_rows[_rci][f"Allocated TP ({d1['currency']})"] = f"{po_list_work[_rci]['allocated_tp']:,}"
                break

total_alloc_shown = sum(p["allocated_tp"] for p in po_list_work)
alloc_rows.append({
    "PO Name":          "TOTAL",
    "Catalogue Type":   "",
    "Timing":           "",
    f"SSP ({d1['currency']})":          f"{total_ssp:,}",
    "SSP %":            "100.0%",
    f"Allocated TP ({d1['currency']})": f"{total_alloc_shown:,}",
    "SFC Adjusted":     "",
})

alloc_df = pd.DataFrame(alloc_rows)
st.dataframe(alloc_df, use_container_width=True, hide_index=True)

if _sfc_annuity_active and _sfc_po_idx_alloc is not None:
    _sfc_po_name = po_list_work[_sfc_po_idx_alloc]["name"] if _sfc_po_idx_alloc < len(po_list_work) else "SFC PO"
    result(
        f"SFC Annuity: {_sfc_po_name} allocated TP replaced with PV-adjusted revenue "
        f"{fmt_number(sfc_data['adj_revenue'], d1['currency'])} (nominal was "
        f"{fmt_number(sfc_data['nominal_tp'], d1['currency'])}). "
        f"Finance Income of {fmt_number(sfc_data['finance_amt'], d1['currency'])} will be "
        f"recognised monthly as the Contract Asset unwinds."
    )
elif total_ssp != final_tp:
    warning(
        f"Note: Sum of SSPs ({d1['currency']} {total_ssp:,}) differs from Final TP "
        f"({d1['currency']} {final_tp:,}). The allocation uses relative SSP proportions. "
        "Consider whether residual method (IFRS 15.78c) or SSP adjustment is appropriate."
    )

if st.button("✔ Complete Step 4 — TP & Allocation"):
    st.session_state.s4_data = {
        "has_var":      has_var,
        "var_type":     var_type,
        "var_impact":   var_impact,
        "est_method":   est_method,
        "constrained":  constrained,
        "final_tp":     final_tp,
        "po_list_alloc": po_list_work,
        "sfc_data":     sfc_data,
    }
    st.session_state.s4_done = True
    st.session_state.step = 5
    st.rerun()

if not st.session_state.s4_done:
    st.stop()

st.markdown('<hr class="divider">', unsafe_allow_html=True)
d4 = st.session_state.s4_data


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5: SUMMARY, BLENDED SCHEDULE & SAVE
# ─────────────────────────────────────────────────────────────────────────────
step_header(5, "Procedure Review, Blended Schedule & Save", "Complete IFRS 15 Assessment")
_editing_slot = st.session_state.get("editing_idx")
if _editing_slot is not None:
    _editing_pid = st.session_state.record_db[_editing_slot].get("Project_ID", f"#{_editing_slot+1}") \
        if _editing_slot < len(st.session_state.record_db) else ""
    st.markdown(
        f'<div style="background:#FFF3CD;border-left:4px solid #F39C12;padding:8px 14px;'
        f'border-radius:0 4px 4px 0;font-family:IBM Plex Mono,monospace;font-size:0.82rem;'
        f'color:#1A1A2E;margin-bottom:12px;">✏️ <strong>Editing:</strong> Contract '
        f'{_editing_pid} — saving will update this record in the buffer. '
        f'Discard to cancel without changes.</div>',
        unsafe_allow_html=True,
    )

st.markdown("**Contract Summary**")
summary_rows = [
    ("Company",               d1["company"]),
    ("Customer",              d1["customer"]),
    ("Project ID",            d1["project_id"]),
    ("Document Number",       d1["doc_num"] or "-"),
    ("Currency",              d1["currency"]),
    ("Basic Contract Fee",    fmt_number(d1["raw_fee"], d1["currency"])),
    ("Delivery Period",       f"{d1['start_date']} → {d1['end_date']}"),
    ("── Enforceability ──",  ""),
    ("Cancellable?",          "Yes" if d1["cancellable"] else "No"),
    ("Significant Comp.",     d1["sig_comp"]),
    ("Enforceable Period",    str(d1["enf_period"])),
    ("── Modification ──",    ""),
    ("Contract Type",         d2["is_mod"]),
    ("Mod Treatment",         d2["mod_treatment"]),
    ("── Performance Oblig.", ""),
    ("PO Status",             d3["po_status"]),
    ("Timing Mix",            d3["timing_summary"]),
    ("── Transaction Price ──",""),
    ("Variable Consid.",      d4["has_var"]),
    ("Var. Amount",           fmt_number(d4["var_impact"], d1["currency"]) if d4["var_impact"] else "-"),
    ("Constrained?",          "Yes" if d4["constrained"] else "No"),
    ("Final TP",              fmt_number(d4["final_tp"], d1["currency"])),
]
_sfc = d4.get("sfc_data", {})
if _sfc.get("enabled"):
    if _sfc.get("b50_exception"):
        summary_rows += [
            ("── Financing Component ──",  ""),
            ("SFC Assessment",             "IFRS 15.B50 Exception — No Adjustment"),
            ("Exception(s) Applied",       ", ".join(_sfc.get("b50_flags", []))),
        ]
    elif not _sfc.get("sfc_significant"):
        summary_rows += [
            ("── Financing Component ──",  ""),
            ("SFC Assessment",             "Not Significant (IFRS 15.B49) — No Adjustment"),
        ]
    else:
        _dir_label = "Advance (Customer → Entity)" if _sfc.get("is_advance") else "Deferred (Entity → Customer)"
        _fin_label = "Finance Cost (entity's expense)" if _sfc.get("is_advance") else "Finance Income (entity's income)"
        summary_rows += [
            ("── Financing Component ──",        ""),
            ("SFC Direction",                    _dir_label),
            ("Rate Used",                        f"{_sfc.get('rate_pct', 0):.2f}% p.a."),
            ("Period",                           f"{_sfc.get('period_months', 0)} months"),
            ("Nominal Contract Fee",             fmt_number(_sfc.get("nominal_tp", 0), d1["currency"])),
            ("SFC-Adjusted Revenue (Memo)",      fmt_number(_sfc.get("adj_revenue", 0), d1["currency"])),
            (_fin_label + " (Memo)",             fmt_number(_sfc.get("finance_amt", 0), d1["currency"])),
            ("IFRS 15.65 — P&L Presentation",   "Finance line SEPARATE from Revenue"),
        ]
_ld = d3.get("loyalty_data", {})
if _ld.get("enabled"):
    summary_rows += [
        ("── Loyalty Programme ──", ""),
        ("Programme Type",       _ld["programme_type"].split("(")[0].strip() if "(" in _ld["programme_type"] else _ld["programme_type"]),
        ("Reward Rate",          f"{_ld['reward_rate_pct']:.4f}%"),
        ("Loyalty SSP / Deferred Revenue", fmt_number(_ld["loyalty_ssp"], d1["currency"])),
        ("Expected Redemption",  f"{_ld['redemption_rate_pct']}%"),
        ("Redeemed Revenue",     fmt_number(_ld["redeemed_revenue"], d1["currency"])),
        ("Breakage Revenue",     fmt_number(_ld["breakage_revenue"], d1["currency"])),
        ("Below-Market Risk",    _ld["market_eq"]),
        ("IAS 37 OPEX Provision",fmt_number(_ld["ias37_provision"], d1["currency"])),
    ]
summary_df = pd.DataFrame(summary_rows, columns=["Field", "Value"])
st.dataframe(summary_df, use_container_width=True, hide_index=True)

st.markdown("---")

st.markdown("**Performance Obligation Details & Allocation**")
po_detail_rows = []
for i, po in enumerate(d4["po_list_alloc"]):
    if po["timing"] == "Point in Time":
        period_info = f"Transfer: {po['transfer_date']}"
    else:
        period_info = f"{po['svc_start']} → {po['svc_end']} | {po['method']}"
    po_detail_rows.append({
        "#":                                i + 1,
        "PO Name":                          po["name"],
        "Type":                             po["catalogue"],
        "Timing":                           po["timing"],
        "Loyalty / Deferred":               "Yes - Deferred Revenue" if po.get("is_loyalty") else "No",
        "Period / Date":                    period_info,
        f"SSP ({d1['currency']})":             f"{po['ssp']:,}",
        f"Allocated TP ({d1['currency']})":     f"{po['allocated_tp']:,}",
    })
po_detail_df = pd.DataFrame(po_detail_rows)
st.dataframe(po_detail_df, use_container_width=True, hide_index=True)

st.markdown("---")

st.markdown("**📅 Blended Revenue Recognition Schedule**")
guidance(
    "One-time POs (Point in Time) show their full allocated TP in the month of control transfer. "
    "Recurring POs (Over Time) are spread using straight-line time-elapsed allocation across the "
    "service period. Adjust for your chosen measurement method in practice."
)

blended_df = build_blended_schedule(d4["po_list_alloc"], d1["currency"])

if not blended_df.empty:
    st.dataframe(blended_df, use_container_width=True, hide_index=True)

    loyalty_pos = [p for p in d4["po_list_alloc"] if p.get("is_loyalty")]
    pit_pos     = [p for p in d4["po_list_alloc"] if p["timing"] == "Point in Time" and not p.get("is_loyalty")]
    ot_pos      = [p for p in d4["po_list_alloc"] if p["timing"] == "Over Time"]
    pit_total    = sum(p["allocated_tp"] for p in pit_pos)
    ot_total     = sum(p["allocated_tp"] for p in ot_pos)
    loy_total    = sum(p["allocated_tp"] for p in loyalty_pos)

    if loyalty_pos:
        mc1, mc2, mc3, mc4 = st.columns(4)
        _kpi(mc1, "One-Time Revenue",
             fmt_metric(pit_total, d1["currency"]), fmt_number(pit_total, d1["currency"]))
        _kpi(mc2, "Recurring Revenue",
             fmt_metric(ot_total, d1["currency"]), fmt_number(ot_total, d1["currency"]))
        _kpi(mc3, "Deferred Rev. (Loyalty)",
             fmt_metric(loy_total, d1["currency"]), fmt_number(loy_total, d1["currency"]))
        _kpi(mc4, "Total Contract TP",
             fmt_metric(d4["final_tp"], d1["currency"]), fmt_number(d4["final_tp"], d1["currency"]))
    else:
        mc1, mc2, mc3 = st.columns(3)
        _kpi(mc1, "One-Time Revenue",
             fmt_metric(pit_total, d1["currency"]), fmt_number(pit_total, d1["currency"]))
        _kpi(mc2, "Recurring Revenue",
             fmt_metric(ot_total, d1["currency"]), fmt_number(ot_total, d1["currency"]))
        _kpi(mc3, "Total Contract TP",
             fmt_metric(d4["final_tp"], d1["currency"]), fmt_number(d4["final_tp"], d1["currency"]))

    if pit_pos:
        result(
            f"One-Time POs ({len(pit_pos)}): " +
            ", ".join(f"{p['name']} [{d1['currency']} {p['allocated_tp']:,}]" for p in pit_pos)
        )
    if ot_pos:
        result(
            f"Recurring POs ({len(ot_pos)}): " +
            ", ".join(f"{p['name']} [{d1['currency']} {p['allocated_tp']:,}]" for p in ot_pos)
        )
    if loyalty_pos:
        _ld5 = d3.get("loyalty_data", {})
        warning(
            f"Loyalty / Deferred Revenue: {fmt_number(loy_total, d1['currency'])} "
            f"allocated to loyalty PO(s). This amount is NOT recognised as revenue at contract "
            f"inception — it is posted to Deferred Revenue (liability) until the customer redeems "
            f"the reward or it expires as breakage. "
            + (f"IAS 37 OPEX provision for onerous risk: {fmt_number(_ld5.get('ias37_provision', 0), d1['currency'])}."
               if _ld5.get('ias37_provision', 0) > 0 else "")
        )

    # Bug B8: warn when SFC has reduced the schedule total vs nominal contract fee
_bl_sfc = d4.get("sfc_data", {})
if (_bl_sfc.get("sfc_significant") and
        _bl_sfc.get("mode") == "annuity" and
        _bl_sfc.get("adj_revenue", 0) > 0 and
        _bl_sfc.get("nominal_tp", 0) != _bl_sfc.get("adj_revenue", 0)):
    _bl_diff = _bl_sfc["nominal_tp"] - _bl_sfc["adj_revenue"]
    warning(
        f"Note: The blended schedule total reflects IFRS 15 revenue — "
        f"the hardware PO uses its PV-adjusted amount ({fmt_number(_bl_sfc['adj_revenue'], d1['currency'])}) "
        f"rather than its nominal value ({fmt_number(_bl_sfc['nominal_tp'], d1['currency'])}). "
        f"The {fmt_number(_bl_diff, d1['currency'])} difference is Finance Income "
        f"recognised separately as the Contract Asset unwinds each month."
    )

    sched_csv = blended_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 Download Blended Schedule (CSV)",
        data=sched_csv,
        file_name=f"RevSchedule_{d1['project_id'].replace('/', '_')}_{date.today()}.csv",
        mime="text/csv",
    )

st.markdown("---")

_sfc5 = d4.get("sfc_data", {})
if _sfc5.get("enabled") and _sfc5.get("sfc_significant") and not _sfc5.get("b50_exception"):
    if _sfc5.get("rate_pct", 0) > 0 and _sfc5.get("period_months", 0) > 0:
        _mode5    = _sfc5.get("mode", "single")
        _is_adv5  = _sfc5.get("is_advance", _sfc5.get("direction") == "advance")
        _fin_lbl5 = "Finance Cost" if _is_adv5 else "Finance Income"

        if _mode5 == "annuity":
            st.markdown("**💰 Significant Financing Component — Contract Asset (Unbilled AR) Waterfall**")
            _monthly_hw5 = _sfc5.get("monthly_hw_pmt", 0)
            _nom5        = _sfc5.get("nominal_tp", 0)
            _n5          = _sfc5.get("period_months", 0)
            adj5, fin5, sched5_df = build_sfc_annuity_schedule(
                _nom5, _monthly_hw5, _n5, _sfc5["rate_pct"]
            )
            _sfc_po5_name = "Hardware PO"
            if _sfc5.get("sfc_po_idx") is not None:
                _idx5 = _sfc5["sfc_po_idx"]
                if _idx5 < len(d4["po_list_alloc"]):
                    _sfc_po5_name = d4["po_list_alloc"][_idx5]["name"]

            sfc_k1, sfc_k2, sfc_k3, sfc_k4 = st.columns(4)
            sfc_k1.metric("PO bearing SFC",               _sfc_po5_name)
            sfc_k2.metric("HW Nominal (sum of instalments)", fmt_number(_nom5, d1["currency"]))
            sfc_k3.metric("IFRS 15 Revenue (PV)",          fmt_number(adj5, d1["currency"]))
            sfc_k4.metric("Finance Income (total)",         fmt_number(fin5, d1["currency"]))

            result(
                f"Hardware delivered at Month 1: Revenue = {fmt_number(adj5, d1['currency'])} (PV). "
                f"Contract Asset (Unbilled AR) opens at {fmt_number(adj5, d1['currency'])}, "
                f"accretes {fmt_number(fin5, d1['currency'])} Finance Income over {_n5} months at "
                f"{_sfc5['rate_pct']:.2f}% p.a., reduces by HW billing each month, closes at zero."
            )
            warning(
                f"IFRS 15.65 — Presentation: Finance Income of {fmt_number(fin5, d1['currency'])} "
                "must appear as a SEPARATE line on the P&L face — not netted into Revenue or "
                "included in Other Income/Expense."
            )
            st.markdown("**Monthly Contract Asset Waterfall**")
            st.dataframe(sched5_df, use_container_width=True, hide_index=True)

        else:
            st.markdown("**💰 Significant Financing Component — Interest Accretion Schedule**")
            _dir5 = _sfc5["direction"]
            adj5, fin5, sched5_df = build_sfc_schedule(
                _sfc5["nominal_tp"], _dir5, _sfc5["rate_pct"], _sfc5["period_months"]
            )
            sfc_kpi1, sfc_kpi2, sfc_kpi3 = st.columns(3)
            sfc_kpi1.metric("Nominal Contract Fee",       fmt_number(_sfc5["nominal_tp"], d1["currency"]))
            sfc_kpi2.metric("IFRS 15 Revenue (Adjusted)", fmt_number(adj5, d1["currency"]))
            sfc_kpi3.metric(_fin_lbl5 + " (Total)",       fmt_number(fin5, d1["currency"]))

            if _is_adv5:
                result(
                    f"Advance: Revenue {fmt_number(adj5, d1['currency'])} > Cash received "
                    f"{fmt_number(_sfc5['nominal_tp'], d1['currency'])}. "
                    f"Finance Cost {fmt_number(fin5, d1['currency'])} accreted over "
                    f"{_sfc5['period_months']} months at {_sfc5['rate_pct']:.2f}% p.a."
                )
            else:
                result(
                    f"Deferred: Revenue {fmt_number(adj5, d1['currency'])} < Nominal "
                    f"{fmt_number(_sfc5['nominal_tp'], d1['currency'])}. "
                    f"Finance Income {fmt_number(fin5, d1['currency'])} unwound over "
                    f"{_sfc5['period_months']} months at {_sfc5['rate_pct']:.2f}% p.a."
                )
            warning(
                f"IFRS 15.65: {_fin_lbl5} of {fmt_number(fin5, d1['currency'])} must be a "
                "SEPARATE line on the P&L face."
            )
            st.dataframe(sched5_df, use_container_width=True, hide_index=True)

        sfc_csv = sched5_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 Download SFC Schedule (CSV)",
            data=sfc_csv,
            file_name=f"SFC_{d1['project_id'].replace('/', '_')}_{date.today()}.csv",
            mime="text/csv",
        )
        st.markdown("---")

col_save, col_discard = st.columns(2)

if col_save.button("✅ Save to Buffer & Add Another Contract"):
    record = {
        "Date_Recorded":          date.today(),
        "Company":                d1["company"],
        "Project_ID":             d1["project_id"],
        "Customer":               d1["customer"],
        "Doc_Number":             d1["doc_num"] or "",
        "Currency":               d1["currency"],
        "Basic_Fee":              d1["raw_fee"],
        "Delivery_Start":         d1["start_date"],
        "Delivery_End":           d1["end_date"],
        "Cancellable":            "Yes" if d1["cancellable"] else "No",
        "Significant_Comp":       d1["sig_comp"],
        "Enforceable_Period":     d1["enf_period"],
        "Contract_Type":          d2["is_mod"],
        "Mod_Treatment":          d2["mod_treatment"],
        "Mod_Description":        d2["mod_description"],
        "PO_Count":               len(d4["po_list_alloc"]),
        "PO_Status":              d3["po_status"],
        "Timing_Mix":             d3["timing_summary"],
        "Total_SSP":              d3["total_ssp"],
        "Has_Variable_Consid":    d4["has_var"],
        "Variable_Type":          d4["var_type"],
        "Variable_Amount":        d4["var_impact"],
        "Estimation_Method":      d4["est_method"],
        "Variable_Constrained":   "Yes" if d4["constrained"] else "No",
        "Final_TP":               d4["final_tp"],
        "SFC_Enabled":            "Yes" if d4.get("sfc_data", {}).get("enabled") else "No",
        "SFC_B50_Exception":      "Yes" if d4.get("sfc_data", {}).get("b50_exception") else "No",
        "SFC_B50_Flags":          ", ".join(d4.get("sfc_data", {}).get("b50_flags", [])),
        "SFC_Significant":        "Yes" if d4.get("sfc_data", {}).get("sfc_significant") else "No",
        "SFC_Direction":          d4.get("sfc_data", {}).get("direction", ""),
        "SFC_Rate_Pct":           d4.get("sfc_data", {}).get("rate_pct", ""),
        "SFC_Period_Months":      d4.get("sfc_data", {}).get("period_months", ""),
        "SFC_Nominal_TP":         d4.get("sfc_data", {}).get("nominal_tp", ""),
        "SFC_Adjusted_Revenue":   d4.get("sfc_data", {}).get("adj_revenue", ""),
        "SFC_Finance_Amount":     d4.get("sfc_data", {}).get("finance_amt", ""),
        "OneTime_Revenue":        sum(p["allocated_tp"] for p in d4["po_list_alloc"]
                                   if p["timing"] == "Point in Time" and not p.get("is_loyalty")),
        "Recurring_Revenue":      sum(p["allocated_tp"] for p in d4["po_list_alloc"]
                                   if p["timing"] == "Over Time"),
        "Deferred_Revenue_Loyalty": sum(p["allocated_tp"] for p in d4["po_list_alloc"]
                                        if p.get("is_loyalty")),
        "Loyalty_Enabled":        "Yes" if d3.get("loyalty_data", {}).get("enabled") else "No",
        "Loyalty_Programme_Type": d3.get("loyalty_data", {}).get("programme_type", ""),
        "Loyalty_Reward_Rate_Pct":d3.get("loyalty_data", {}).get("reward_rate_pct", ""),
        "Loyalty_SSP":            d3.get("loyalty_data", {}).get("loyalty_ssp", ""),
        "Loyalty_Redemption_Pct": d3.get("loyalty_data", {}).get("redemption_rate_pct", ""),
        "Loyalty_Redeemed_Rev":   d3.get("loyalty_data", {}).get("redeemed_revenue", ""),
        "Loyalty_Breakage_Rev":   d3.get("loyalty_data", {}).get("breakage_revenue", ""),
        "Loyalty_Below_Mkt_Risk": d3.get("loyalty_data", {}).get("market_eq", ""),
        "Loyalty_Prob_Below_Pct": d3.get("loyalty_data", {}).get("prob_below_pct", ""),
        "Loyalty_Avg_Below_Amt":  d3.get("loyalty_data", {}).get("avg_below_amount", ""),
        "Loyalty_IAS37_Provision":d3.get("loyalty_data", {}).get("ias37_provision", ""),
    }

    for i, po in enumerate(d4["po_list_alloc"], start=1):
        prefix = f"PO{i}"
        record[f"{prefix}_Name"]          = po["name"]
        record[f"{prefix}_Catalogue"]     = po["catalogue"]
        record[f"{prefix}_Timing"]        = po["timing"]
        record[f"{prefix}_SSP"]           = po["ssp"]
        record[f"{prefix}_Allocated_TP"]  = po["allocated_tp"]
        record[f"{prefix}_Is_Loyalty"]    = "Yes" if po.get("is_loyalty") else "No"
        if po["timing"] == "Point in Time":
            record[f"{prefix}_Transfer_Date"] = po["transfer_date"]
            record[f"{prefix}_Svc_Start"]     = ""
            record[f"{prefix}_Svc_End"]       = ""
            record[f"{prefix}_Measure_Method"]= ""
        else:
            record[f"{prefix}_Transfer_Date"] = ""
            record[f"{prefix}_Svc_Start"]     = po["svc_start"]
            record[f"{prefix}_Svc_End"]       = po["svc_end"]
            record[f"{prefix}_Measure_Method"]= po["method"]

    record["_s1"] = copy.deepcopy(d1)
    record["_s2"] = copy.deepcopy(d2)
    record["_s3"] = copy.deepcopy(d3)
    record["_s4"] = copy.deepcopy(d4)
    _edit_slot = st.session_state.get("editing_idx")
    if _edit_slot is not None and _edit_slot < len(st.session_state.record_db):
        st.session_state.record_db[_edit_slot] = record  # replace existing
        _action = "updated"
    else:
        st.session_state.record_db.append(record)         # new contract
        _action = "saved"
    _saved_pid = d1["project_id"]
    _saved_n   = len(st.session_state.record_db)
    reset_workflow()  # bumps form_epoch, clears editing_idx
    st.session_state.flash_message = (
        f"✅ Contract '{_saved_pid}' {_action}! "
        f"Buffer now has {_saved_n} contract(s). "
        f"Starting fresh assessment — or open 📂 Saved Contracts to review."
    )
    st.rerun()

if col_discard.button("❌ Discard & Reset"):
    reset_workflow()  # clears editing_idx — original record stays untouched in buffer
    st.session_state.view_mode = "buffer" if st.session_state.record_db else "workflow"
    st.rerun()