import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- 1. إعدادات الهوية البصرية (Petrel Dark Mode Style) ---
st.set_page_config(
    page_title="Eng. Sulaiman Kudaimi | Reservoir Digital Twin",
    page_icon="🚀",
    layout="wide"
)

# تصميم واجهة المستخدم CSS المحسن لوضوح القائمة الجانبية
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stSidebar { background-color: #1a1c24; border-right: 1px solid #3b82f6; }
    
    /* تحسين وضوح نصوص القائمة الجانبية */
    .css-17l6nlh, .css-12ttj6m { color: #f8fafc !important; font-weight: 500; }
    
    .developer-section {
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #1e293b, #3b82f6);
        border: 2px solid #60a5fa;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .main-header {
        border-left: 6px solid #3b82f6;
        padding-left: 20px;
        margin-bottom: 30px;
    }
    
    /* جعل نصوص السلايدر والملفات واضحة جداً */
    div[data-testid="stMarkdownContainer"] p { color: #e2e8f0; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الشريط الجانبي (Professional Sidebar) ---
with st.sidebar:
    st.markdown(f"""
        <div class='developer-section'>
            <p style='margin:0; color:#cbd5e1; font-size: 0.8em; text-transform: uppercase; letter-spacing: 2px;'>System Architect & Developer</p>
            <h2 style='margin:10px 0; color:white; font-family:sans-serif; font-size: 1.3em;'>Eng. SULAIMAN KUDAIMI</h2>
            <p style='margin:0; color:#e2e8f0; font-size: 0.9em; font-weight: bold;'>Reservoir Digital Solutions Lead</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ميزة رفع الملفات العالمية (Universal Data Ingest)
    st.markdown("<h3 style='color: #60a5fa; font-size: 1.1em;'>🌐 Universal Data Ingest</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Reservoir CSV/LAS", type=['csv', 'las'], help="Upload your field data to update the twin")
    
    if uploaded_file is not None:
        st.success(f"✅ Data Detected: {uploaded_file.name}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # التحكم في المحاكاة
    st.markdown("<h3 style='color: #60a5fa; font-size: 1.1em;'>🎛️ Simulation Controls</h3>", unsafe_allow_html=True)
    forecast_horizon = st.slider("Select Forecast Year", 2026, 2035, 2026)
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8em;'>© 2026 | Proprietary Reservoir Engine</p>", unsafe_allow_html=True)

# --- 3. العنوان الرئيسي للواجهة ---
st.markdown(f"""
    <div class='main-header'>
        <h1>Deep-Earth Digital Twin Platform</h1>
        <p style='color: #94a3b8;'>Designed & Developed by <b>Eng. Sulaiman Kudaimi</b> | Future Energy Solutions</p>
    </div>
""", unsafe_allow_html=True)

# --- 4. وظائف تحميل البيانات ---
@st.cache_data
def load_data():
    try:
        # محاولة تحميل الملف المرفوع إذا وجد
        if uploaded_file is not None:
            return pd.read_csv(uploaded_file)
        # تحميل الملف الافتراضي
        return pd.read_csv("Data/Norway-NA-15_47_9-F-9 A depth.csv")
    except:
        return pd.DataFrame({'Depth': np.linspace(2000, 3500, 100), 'Value': np.random.normal(50, 10, 100)})

df_well = load_data()

# --- 5. اللوحة الرئيسية (Tabs) ---
tab1, tab2, tab3 = st.tabs(["🌐 3D Digital Twin", "📊 Well Interpretation", "🔮 AI Prediction Engine"])

with tab1:
    st.subheader("Interactive Reservoir Model (Spatial Dynamics)")
    col_a, col_b = st.columns([4, 1])
    
    with col_a:
        # بناء الشبكة الجيولوجية
        grid_x, grid_y = np.mgrid[0:1000:50j, 0:1000:50j]
        grid_z = -3000 + (np.sin(grid_x/100) * 40)
        
        # حساب الضغط بناءً على التنبؤ
        pressure_drop = (forecast_horizon - 2026) * 15
        grid_pressure = 3200 - pressure_drop + (np.cos(grid_y/100) * 30)

        # إعداد الرسم الثلاثي الأبعاد
        fig = go.Figure(data=[go.Surface(
            x=grid_x, y=grid_y, z=grid_z,
            surfacecolor=grid_pressure,
            colorscale='RdYlBu',
            colorbar=dict(title="Pressure (psi)", thickness=20)
        )])
        
        fig.update_layout(
            template='plotly_dark',
            scene=dict(
                xaxis_title='East (m)', yaxis_title='North (m)', zaxis_title='Depth (m)',
                aspectratio=dict(x=1, y=1, z=0.5),
                bgcolor="#0e1117"
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=650
        )
        st.plotly_chart(fig, use_container_width=True, theme=None)
    
    with col_b:
        st.metric("Field Pressure", f"{3200 - pressure_drop} psi", f"-{pressure_drop} psi")
        st.metric("Recovery Factor", "34.2%", "+0.45%")
        st.write("---")
        st.info(f"Target Year: {forecast_horizon}")
        st.caption("Algorithm: AI-Proxy Simulation")

with tab2:
    st.subheader("Well Log Data Analysis")
    st.dataframe(df_well.head(15), use_container_width=True)
    fig_log = go.Figure()
    fig_log.add_trace(go.Scatter(x=df_well.iloc[:, 1], y=df_well.iloc[:, 0], line=dict(color="#3b82f6", width=2)))
    fig_log.update_layout(template='plotly_dark', title="Lithology Depth Profile", yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_log, use_container_width=True, theme=None)

with tab3:
    st.subheader("AI Prediction: Decline Curve Analysis")
    timeline = np.arange(2020, 2036)
    prod = 1000 * np.exp(-0.06 * (timeline - 2020))
    fig_prod = go.Figure()
    fig_prod.add_trace(go.Scatter(x=timeline, y=prod, mode='lines+markers', name="Oil Forecast", line=dict(color="#f87171")))
    fig_prod.add_vline(x=forecast_horizon, line_dash="dash", line_color="yellow", annotation_text="Forecast Horizon")
    fig_prod.update_layout(template='plotly_dark', title="Long-term Estimated Ultimate Recovery (EUR)")
    st.plotly_chart(fig_prod, use_container_width=True, theme=None)

# --- 6. التذييل (Footer) ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #94a3b8;'>Proprietary Digital Twin Engine | Developed by <b>Eng. Sulaiman Kudaimi</b></p>", unsafe_allow_html=True)
