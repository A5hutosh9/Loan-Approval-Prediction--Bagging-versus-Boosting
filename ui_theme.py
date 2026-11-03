"""Shared visual system for Bharat Loan AI."""
import html
import streamlit as st


def apply_theme():
    """Apply a high-contrast dark glass theme across every page."""
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
            --bg-0: #101820;
            --bg-1: #172923;
            --bg-2: #263a36;
            --glass: rgba(38, 58, 54, .34);
            --glass-strong: rgba(24, 43, 38, .62);
            --glass-soft: rgba(182, 227, 198, .055);
            --line: rgba(182, 227, 198, .18);
            --line-strong: rgba(74, 176, 139, .38);
            --text: #f3f7f2;
            --muted: #c5d7cd;
            --subtle: #9eb8aa;
            --blue: #168c75;
            --cyan: #b6e3c6;
            --gold: #e8c98a;
            --green: #75d6a7;
            --red: #ff9292;
        }

        html, body, [class*="css"] {
            font-family: Inter, "Segoe UI", system-ui, sans-serif;
        }

        .stApp,
        [data-testid="stAppViewContainer"] {
            color: var(--text) !important;
            background:
                radial-gradient(ellipse at 12% 0%, rgba(28, 105, 166, .25), transparent 34%),
                radial-gradient(ellipse at 92% 12%, rgba(73, 77, 160, .20), transparent 32%),
                linear-gradient(145deg, var(--bg-0) 0%, var(--bg-1) 52%, #071421 100%) !important;
        }

        [data-testid="stMain"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 1480px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        #MainMenu, footer { visibility: hidden; }

        [data-testid="stHeader"] {
            background: rgba(5, 17, 31, .70) !important;
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(190, 220, 255, .10);
        }

        /* Main typography: explicit colours prevent low-contrast text. */
        .stApp, .stApp p, .stApp li, .stApp label,
        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stCaptionContainer"] {
            color: var(--text);
        }

        .stApp p, .stApp li {
            line-height: 1.65;
        }

        h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            color: #f5f8ff !important;
            letter-spacing: -.025em;
            font-weight: 750 !important;
        }

        [data-testid="stCaptionContainer"],
        .stCaption, small {
            color: var(--muted) !important;
        }

        a { color: #82c5ff !important; }

        /* Frosted-glass sidebar and navigation. */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(5, 18, 33, .96), rgba(9, 34, 56, .91)) !important;
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] a {
            color: #eaf3ff !important;
        }

        [data-testid="stSidebarNav"] {
            padding: 8px 10px 16px;
        }

        [data-testid="stSidebarNav"] a p {
            text-transform: capitalize !important;
            letter-spacing: .01em;
        }

        [data-testid="stSidebarNav"] a {
            border: 1px solid transparent;
            border-radius: 12px;
            margin: 4px 0;
            padding: 8px 10px;
            transition: background .18s ease, border .18s ease, transform .18s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(113, 181, 245, .12) !important;
            border-color: rgba(139, 198, 255, .18);
            transform: translateX(2px);
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(110deg, rgba(44, 132, 214, .30), rgba(73, 205, 220, .13)) !important;
            border-color: rgba(120, 190, 255, .35);
            box-shadow: inset 3px 0 0 #68baff, 0 8px 22px rgba(0, 0, 0, .15);
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(210, 232, 255, .15) !important;
        }

        .bank-brand {
            background: linear-gradient(135deg, rgba(34, 78, 115, .68), rgba(19, 42, 68, .62));
            border: 1px solid rgba(190, 220, 255, .20);
            border-radius: 18px;
            padding: 17px 16px;
            margin: 8px 0 16px;
            box-shadow: 0 14px 34px rgba(0, 0, 0, .22);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        .bank-brand .logo { font-size: 27px; margin-bottom: 5px; }
        .bank-brand .name {
            color: #ffffff;
            font-size: 19px;
            font-weight: 800;
            letter-spacing: -.02em;
        }
        .bank-brand .tagline {
            color: #c3d8ed;
            font-size: 9px;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        .tricolor {
            height: 4px;
            border-radius: 99px;
            margin-top: 13px;
            background: linear-gradient(90deg, #ff9933 0 33.33%, #ffffff 33.33% 66.66%, #138808 66.66% 100%);
            box-shadow: 0 0 16px rgba(255, 255, 255, .12);
        }

        /* Hero glass panel. */
        .hero {
            position: relative;
            overflow: hidden;
            isolation: isolate;
            background: linear-gradient(112deg, rgba(15, 62, 102, .90), rgba(19, 94, 151, .78) 58%, rgba(30, 116, 152, .68));
            border: 1px solid rgba(184, 222, 255, .27);
            border-radius: 24px;
            padding: 32px 34px;
            margin: 7px 0 24px;
            box-shadow: 0 20px 48px rgba(0, 0, 0, .22);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        .hero:after {
            content: "";
            position: absolute;
            z-index: -1;
            width: 230px;
            height: 230px;
            right: -46px;
            top: -82px;
            border-radius: 50%;
            background: conic-gradient(from 30deg, rgba(255,153,51,.30), rgba(255,255,255,.22), rgba(19,136,8,.24), rgba(255,153,51,.30));
            filter: blur(1px);
            opacity: .82;
        }

        .hero-kicker {
            color: #d8edff;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1.8px;
            font-weight: 750;
            margin-bottom: 9px;
        }

        .hero-title {
            color: #ffffff;
            font-size: clamp(30px, 4vw, 43px);
            line-height: 1.10;
            font-weight: 850;
            letter-spacing: -.04em;
            margin: 0;
            max-width: 850px;
        }

        .hero-title span { color: #ffdb84; }

        .hero-subtitle {
            color: #edf7ff;
            font-size: 15px;
            line-height: 1.6;
            margin-top: 11px;
            max-width: 780px;
        }

        .hero-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 19px;
        }

        .hero-badge {
            color: #f6fbff;
            background: rgba(255, 255, 255, .105);
            border: 1px solid rgba(255, 255, 255, .20);
            border-radius: 99px;
            padding: 7px 11px;
            font-size: 11px;
            font-weight: 650;
            backdrop-filter: blur(12px);
        }

        /* Translucent glass cards and frosted panels. */
        .section-card, .metric-card, .workflow-step, .ai-card,
        [data-testid="stExpander"], [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--glass) !important;
            border: 1px solid var(--line) !important;
            border-radius: 17px !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, .16) !important;
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        .section-card {
            padding: 21px;
            margin-bottom: 16px;
        }

        .section-card, .section-card * {
            color: #eef6ff !important;
        }

        .section-title {
            color: #f4f8ff !important;
            font-size: 20px;
            line-height: 1.3;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .section-subtitle {
            color: #bfd0e3 !important;
            font-size: 12px;
            line-height: 1.6;
            margin-bottom: 13px;
        }

        .metric-card {
            min-height: 118px;
            padding: 17px;
        }

        .metric-label {
            color: #b8cce2 !important;
            font-size: 10px;
            letter-spacing: .9px;
            text-transform: uppercase;
            font-weight: 750;
        }

        .metric-value {
            color: #f4f9ff !important;
            font-size: 27px;
            font-weight: 850;
            margin-top: 7px;
        }

        .metric-note {
            color: #abc1d8 !important;
            font-size: 11px;
            margin-top: 4px;
        }

        .approval-card, .rejection-card {
            border-radius: 18px;
            padding: 21px;
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
        }

        .approval-card {
            background: rgba(16, 117, 80, .24);
            border: 1px solid rgba(85, 214, 160, .48);
            color: #eafff5 !important;
        }
        .approval-card * { color: #eafff5 !important; }
        .approval-title { color: #7bf0ba !important; font-size: 26px; font-weight: 850; }

        .rejection-card {
            background: rgba(157, 45, 72, .22);
            border: 1px solid rgba(255, 130, 149, .48);
            color: #fff0f3 !important;
        }
        .rejection-card * { color: #fff0f3 !important; }
        .rejection-title { color: #ff9bab !important; font-size: 26px; font-weight: 850; }

        .ai-card {
            background: linear-gradient(135deg, rgba(81, 75, 160, .25), rgba(40, 91, 135, .22)) !important;
            border-color: rgba(164, 157, 255, .40) !important;
            padding: 20px;
            color: #f5f3ff !important;
            line-height: 1.75;
        }
        .ai-card, .ai-card * { color: #f5f3ff !important; }
        .ai-label {
            display: inline-block;
            color: #ffffff !important;
            background: rgba(133, 119, 255, .27);
            border: 1px solid rgba(190, 183, 255, .25);
            border-radius: 99px;
            padding: 5px 10px;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .8px;
            margin-bottom: 10px;
        }

        .workflow {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        .workflow-step {
            flex: 1 1 180px;
            padding: 17px;
        }
        .workflow-num {
            display: grid;
            place-items: center;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2475c8, #49bfd3);
            color: #ffffff !important;
            font-weight: 850;
            margin-bottom: 10px;
            box-shadow: 0 5px 16px rgba(44, 143, 211, .25);
        }
        .workflow-title { color: #f2f7ff !important; font-weight: 800; }
        .workflow-text { color: #b9cbe0 !important; font-size: 11px; line-height: 1.55; margin-top: 5px; }

        .footer-card {
            background: rgba(255, 255, 255, .055);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 15px 17px;
            margin-top: 16px;
            color: #bfd0e3 !important;
            font-size: 11px;
        }
        .footer-card * { color: #dceaff !important; }

        /* Labels, inputs, dropdowns and text areas. */
        label, [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label {
            color: #dceaff !important;
            font-weight: 650 !important;
        }

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="textarea"] > div,
        [data-testid="stNumberInputContainer"] {
            background: rgba(5, 20, 36, .78) !important;
            border: 1px solid rgba(131, 184, 232, .38) !important;
            border-radius: 11px !important;
        }

        [data-baseweb="input"] input,
        [data-baseweb="textarea"] textarea,
        [data-testid="stNumberInputField"],
        [data-baseweb="select"] *,
        [data-testid="stNumberInputContainer"] * {
            color: #f4f8ff !important;
            -webkit-text-fill-color: #f4f8ff !important;
        }

        [data-baseweb="input"] input::placeholder,
        [data-baseweb="textarea"] textarea::placeholder {
            color: #9bb2cb !important;
            -webkit-text-fill-color: #9bb2cb !important;
        }

        [data-baseweb="popover"], [role="listbox"] {
            background: #102a43 !important;
            border: 1px solid var(--line-strong) !important;
            color: #f4f8ff !important;
        }
        [role="option"], [role="listbox"] * { color: #f4f8ff !important; }

        /* Buttons with a clear visual hierarchy. */
        .stButton > button, .stDownloadButton > button {
            min-height: 42px;
            border-radius: 11px;
            border: 1px solid rgba(135, 190, 244, .42) !important;
            background: rgba(42, 87, 128, .48) !important;
            color: #f4f8ff !important;
            font-weight: 750 !important;
            transition: transform .16s ease, background .16s ease, border .16s ease;
        }

        .stButton > button:hover, .stDownloadButton > button:hover {
            background: rgba(55, 119, 174, .62) !important;
            border-color: rgba(147, 212, 255, .70) !important;
            transform: translateY(-1px);
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(100deg, #1768bb, #268dd0 58%, #22a8ad) !important;
            border: 1px solid rgba(157, 222, 255, .58) !important;
            color: #ffffff !important;
            box-shadow: 0 8px 22px rgba(18, 112, 181, .28);
        }

        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(100deg, #1c78d1, #2b9bdc 58%, #26b9bd) !important;
        }

        /* Translucent tab bar, alerts, expanders and progress bars. */
        [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, .045);
            border: 1px solid rgba(190, 220, 255, .12);
            border-radius: 13px;
            padding: 4px;
            gap: 4px;
        }
        button[data-baseweb="tab"] {
            color: #c1d3e7 !important;
            border-radius: 9px !important;
            font-weight: 700 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ffffff !important;
            background: rgba(62, 133, 196, .30) !important;
        }

        [data-testid="stAlert"] {
            background: rgba(30, 65, 96, .62) !important;
            border: 1px solid rgba(137, 191, 239, .30) !important;
            border-radius: 13px !important;
            color: #f0f6ff !important;
        }

        [data-testid="stExpander"] summary {
            color: #e8f2ff !important;
            font-weight: 750 !important;
        }

        .stProgress > div > div > div {
            background: linear-gradient(90deg, #2f8ae0, #57c9d0) !important;
            border-radius: 99px;
        }
        .stProgress > div {
            background: rgba(255, 255, 255, .10) !important;
            border-radius: 99px;
        }

        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border: 1px solid var(--line) !important;
            border-radius: 13px !important;
            overflow: hidden;
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p { color: #bfd0e3 !important; }
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] div { color: #f4f8ff !important; }

        @media (max-width: 760px) {
            .block-container { padding: 1.15rem 1rem 2.5rem; }
            .hero { padding: 24px 21px; border-radius: 19px; }
            .hero-title { font-size: 30px; }
            .hero-subtitle { font-size: 13px; }
            .hero:after { width: 150px; height: 150px; right: -65px; top: -35px; }
            .section-card { padding: 17px; }
            .metric-value { font-size: 23px; }
        }

        /* Emerald Glass palette: subtle frosted surfaces, high-contrast content. */
        .stApp, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(ellipse at 10% 0%, rgba(22, 140, 117, .17), transparent 36%),
                radial-gradient(ellipse at 92% 10%, rgba(182, 227, 198, .07), transparent 30%),
                linear-gradient(145deg, #101820 0%, #172923 55%, #101820 100%) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(16, 24, 32, .97), rgba(30, 49, 43, .95)) !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: rgba(22, 140, 117, .18) !important;
            border-color: rgba(116, 205, 169, .30) !important;
            box-shadow: inset 3px 0 0 #168c75 !important;
        }
        [data-testid="stSidebarNav"] a:hover {
            background: rgba(182, 227, 198, .09) !important;
            border-color: rgba(182, 227, 198, .20) !important;
        }

        .hero {
            background: linear-gradient(118deg, rgba(26, 57, 49, .88), rgba(22, 105, 87, .74) 58%, rgba(30, 88, 69, .68)) !important;
            border-color: rgba(182, 227, 198, .23) !important;
            box-shadow: 0 16px 38px rgba(0, 0, 0, .18) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        .hero:after {
            background: radial-gradient(circle, rgba(182, 227, 198, .20), rgba(22, 140, 117, .10) 55%, transparent 72%) !important;
            opacity: .75 !important;
        }
        .hero-title span { color: #b6e3c6 !important; }
        .hero-badge {
            background: rgba(243, 247, 242, .07) !important;
            border-color: rgba(182, 227, 198, .17) !important;
            backdrop-filter: blur(8px);
        }

        .section-card, .metric-card, .workflow-step, .ai-card,
        [data-testid="stExpander"], [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(38, 58, 54, .30) !important;
            border-color: rgba(182, 227, 198, .15) !important;
            box-shadow: 0 8px 22px rgba(0, 0, 0, .12) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        .bank-brand {
            background: rgba(38, 58, 54, .42) !important;
            border-color: rgba(182, 227, 198, .18) !important;
            box-shadow: 0 10px 24px rgba(0, 0, 0, .14) !important;
            backdrop-filter: blur(10px);
        }
        .metric-card { min-width: 0; height: auto; }
        .metric-label, .metric-note, .metric-value {
            max-width: 100%;
            white-space: normal !important;
            overflow: visible !important;
            overflow-wrap: anywhere;
            word-break: normal;
        }
        .metric-value {
            font-size: clamp(19px, 2.2vw, 27px) !important;
            line-height: 1.22 !important;
        }
        [data-testid="stMetric"] { min-width: 0; }
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p {
            white-space: normal !important;
            overflow-wrap: anywhere !important;
            line-height: 1.35 !important;
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] div {
            white-space: normal !important;
            overflow: visible !important;
            overflow-wrap: anywhere !important;
            word-break: normal !important;
            text-overflow: clip !important;
            font-size: clamp(18px, 2.2vw, 30px) !important;
            line-height: 1.2 !important;
        }
        [data-testid="stMetricDelta"] { white-space: normal !important; }

        /* Allow Streamlit columns to wrap instead of squeezing text off-screen. */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            align-items: stretch !important;
            gap: 12px !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            min-width: min(100%, 215px) !important;
            flex: 1 1 215px !important;
            width: auto !important;
        }
        [data-testid="stVerticalBlock"] { min-width: 0; }
        .stMarkdown, [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] * {
            min-width: 0;
            overflow-wrap: anywhere;
        }
        h1, h2, h3, h4, h5, h6 {
            line-height: 1.22 !important;
            overflow-wrap: anywhere;
            hyphens: auto;
        }
        p, li, label, .stCaption {
            overflow-wrap: anywhere;
            word-break: normal;
        }

        /* Keep tables usable on narrow screens without clipping their content. */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            max-width: 100% !important;
            overflow-x: auto !important;
        }
        [data-testid="stDataFrame"] iframe { max-width: 100% !important; }
        [data-testid="stImage"] img, .stPlotlyChart, [data-testid="stPyplot"] {
            max-width: 100% !important;
        }

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="textarea"] > div,
        [data-testid="stNumberInputContainer"] {
            background: rgba(16, 24, 32, .72) !important;
            border-color: rgba(182, 227, 198, .25) !important;
        }
        [data-baseweb="popover"], [role="listbox"] {
            background: #263a36 !important;
            border-color: rgba(182, 227, 198, .28) !important;
        }
        .stButton > button, .stDownloadButton > button {
            background: rgba(38, 58, 54, .52) !important;
            border-color: rgba(182, 227, 198, .26) !important;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            background: rgba(22, 140, 117, .25) !important;
            border-color: rgba(182, 227, 198, .44) !important;
        }
        div.stButton > button[kind="primary"] {
            background: linear-gradient(100deg, #126e5c, #168c75 62%, #399b78) !important;
            border-color: rgba(182, 227, 198, .40) !important;
            box-shadow: 0 7px 18px rgba(13, 92, 73, .20) !important;
        }
        [data-baseweb="tab-list"] {
            background: rgba(38, 58, 54, .24) !important;
            border-color: rgba(182, 227, 198, .14) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background: rgba(22, 140, 117, .20) !important;
        }
        [data-testid="stAlert"] {
            background: rgba(38, 58, 54, .42) !important;
            border-color: rgba(182, 227, 198, .22) !important;
        }
        .workflow-num {
            background: linear-gradient(135deg, #126e5c, #168c75) !important;
            box-shadow: 0 4px 12px rgba(22, 140, 117, .18) !important;
        }
        .approval-card {
            background: rgba(22, 140, 117, .13) !important;
            border-color: rgba(117, 214, 167, .34) !important;
        }
        .approval-title { color: #9be2bd !important; }
        .ai-card {
            background: rgba(38, 58, 54, .28) !important;
            border-color: rgba(182, 227, 198, .20) !important;
        }
        .footer-card {
            background: rgba(38, 58, 54, .25) !important;
            border-color: rgba(182, 227, 198, .14) !important;
        }

        @media (max-width: 760px) {
            .block-container { padding: 1rem .85rem 2.25rem !important; }
            .hero { padding: 21px 18px !important; border-radius: 17px !important; }
            .hero-title { font-size: clamp(25px, 7vw, 32px) !important; line-height: 1.14 !important; }
            .hero-subtitle { font-size: 13px !important; }
            .hero-badges { gap: 6px !important; }
            .hero-badge { font-size: 10px !important; padding: 6px 9px !important; }
            .section-card { padding: 15px !important; }
            .metric-card { min-height: 0 !important; padding: 14px !important; }
            .metric-value { font-size: clamp(18px, 5vw, 23px) !important; }
            [data-testid="stHorizontalBlock"] > [data-testid="column"] {
                flex-basis: 100% !important;
                min-width: 100% !important;
                width: 100% !important;
            }
            [data-testid="stDataFrame"] { font-size: 12px !important; }
            .workflow-step { flex: 1 1 100% !important; }
            .approval-title, .rejection-title { font-size: clamp(20px, 5.5vw, 26px) !important; }
        }
        @media (min-width: 761px) and (max-width: 1100px) {
            [data-testid="stHorizontalBlock"] > [data-testid="column"] {
                flex-basis: calc(50% - 12px) !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    """Render the consistent project brand in the sidebar."""
    st.sidebar.markdown(
        """
        <div class="bank-brand">
            <div class="logo">🏛️</div>
            <div class="name">BHARAT LOAN AI</div>
            <div class="tagline">ACADEMIC MACHINE-LEARNING PROJECT</div>
            <div class="tricolor"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title="Loan Approval Prediction", subtitle="A data-driven academic ML demonstration"):
    """Render a consistent title banner."""
    safe_title = html.escape(str(title))
    if "Prediction" in safe_title:
        safe_title = safe_title.replace("Prediction", "<span>Prediction</span>", 1)

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">🇮🇳 BHARAT LOAN AI · GROUP 10</div>
            <div class="hero-title">{safe_title}</div>
            <div class="hero-subtitle">{html.escape(str(subtitle))}</div>
            <div class="hero-badges">
                <span class="hero-badge">⚡ MODEL INSIGHTS</span>
                <span class="hero-badge">🛡️ RESPONSIBLE ML</span>
                <span class="hero-badge">📊 ENSEMBLE LEARNING</span>
                <span class="hero-badge">🤖 GEMINI EXPLANATION</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
