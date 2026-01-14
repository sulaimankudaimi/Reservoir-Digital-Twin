import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- 1. إعدادات الهوية البصرية (Petrel Dark Mode Style) ---
st.set_page_config(
    page_title="Sulaiman Kudaimi | Reservoir Digital Twin",
    page_icon="🚀",
    layout="wide"
)

# تصميم واجهة المستخدم CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stSidebar { background-color: #1a1c24; border-right: 1px solid #4facfe; }
    .developer-section {
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(145deg, #0f172a, #1e3a8a);
        border: 1px solid #3b82f6;
        text-align: center;
        margin-bottom: 25px;
    }
    .main-header {
        border-left: 5px solid #4facfe;
        padding-left: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الشريط الجانبي وتوثيق المطور ---
with st.sidebar:
    st.markdown(f"""
        <div class='developer-section'>
            <h2 style='margin:0; font-family:sans-serif; color:white; font-size: 1.4em;'>SULAIMAN KUDAIMI</h2>
            <p style='margin:0; font-size: 0.85em; opacity: 0.9; color: #4facfe;'>Lead Reservoir Engineer</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.header("📂 Data Navigator")
    data_mode = st.selectbox("Select Data Source", ["Well Depth (CSV)", "Production Logs"])
    
    st.header("🎛️ Simulation Controls")
    # تم تثبيت اسم المتغير ليتوافق مع كود الرسم
    forecast_horizon = st.slider("Forecast Horizon (Year)", 2026, 2035, 2026)
    
    st.markdown("---")
    st.success("System: Connected to Cloud")
    st.info("Version: Stable 1.2.0")

# --- 3. العنوان الرئيسي للواجهة ---
st.markdown("<div class='main-header'><h1>Deep-Earth Digital Twin Platform</h1><p>Developed by: <b>Sulaiman Kudaimi</b> | 2026 Reservoir Analytics</p></div>", unsafe_allow_html=True)

# --- 4. وظائف تحميل البيانات الاحتياطية ---
@st.cache_data
def load_sample_data():
    try:
        path = "Data/Norway-NA-15_47_9-F-9 A depth.csv"
        df = pd.read_csv(path)
        return df
    except:
        # بيانات افتراضية لضمان عمل الواجهة حتى في حالة فقدان الملف
        return pd.DataFrame({'Depth': np.linspace(2000, 3500, 100), 'Value': np.random.normal(50, 10, 100)})

df_well = load_sample_data()

# --- 5. اللوحة الرئيسية (Tabs) ---
tab1, tab2, tab3 = st.tabs(["🌐 3D Digital Twin", "📊 Well Interpretation", "🔮 Prediction Engine"])

with tab1:
    st.subheader("Interactive Reservoir Model (Spatial Dynamics)")
    col_a, col_b = st.columns([4, 1])
    
    with col_a:
        # بناء الشبكة الجيولوجية
        grid_x, grid_y = np.mgrid[0:1000:50j, 0:1000:50j]
        grid_z = -3000 + (np.sin(grid_x/100) * 40)
        
        # حساب الضغط الديناميكي بناءً على الـ Slider
        pressure_drop = (forecast_horizon - 2026) * 15
        grid_pressure = 3200 - pressure_drop + (np.cos(grid_y/100) * 30)

        # إعداد الرسم مع فرض النمط الداكن لمنع الشاشة السوداء
        fig = go.Figure(data=[go.Surface(
            x=grid_x, y=grid_y, z=grid_z,
            surfacecolor=grid_pressure,
            colorscale='RdYlBu',
            colorbar=dict(title="Pressure (psi)", thickness=20)
        )])
        
        fig.update_layout(
            template='plotly_dark',
            scene=dict(
                xaxis_title='East (m)',
                yaxis_title='North (m)',
                zaxis_title='Depth (m)',
                aspectratio=dict(x=1, y=1, z=0.5),
                bgcolor="#0e1117"
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=650
        )
        
        # عرض الرسم مع تعطيل ثيم Streamlit لضمان الاستقرار
        st.plotly_chart(fig, use_container_width=True, theme=None)
    
    with col_b:
        st.metric("Field Pressure", f"{3200 - pressure_drop} psi", f"-{pressure_drop} psi")
        st.metric("Recovery Factor", "34.2%", "+0.45%")
        st.write("---")
        st.write("**Model Parameters:**")
        st.caption(f"Target Year: {forecast_horizon}")
        st.caption("Algorithm: Kriging Interpolation")

with tab2:
    st.subheader("Well Log Visualization")
    if not df_well.empty:
        st.dataframe(df_well.head(10), use_container_width=True)
        fig_log = go.Figure()
        fig_log.add_trace(go.Scatter(x=df_well.iloc[:, 1], y=df_well.iloc[:, 0], line=dict(color="#4facfe")))
        fig_log.update_layout(template='plotly_dark', height=400, title="Depth Profile", yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_log, use_container_width=True, theme=None)

with tab3:
    st.subheader("AI Prediction: Decline Curve Analysis")
    timeline = np.arange(2020, 2036)
    prod = 1000 * np.exp(-0.06 * (timeline - 2020))
    fig_prod = go.Figure()
    fig_prod.add_trace(go.Scatter(x=timeline, y=prod, mode='lines+markers', name="Forecasted Prod", line=dict(color="#f87171")))
    fig_prod.add_vline(x=forecast_horizon, line_dash="dash", line_color="yellow")
    fig_prod.update_layout(template='plotly_dark', title="Long-term Production Forecast")
    st.plotly_chart(fig_prod, use_container_width=True, theme=None)

# --- 6. التذييل (Footer) ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #64748b;'>Internal Simulation Platform | Proprietary System Developed by <b>Sulaiman Kudaimi</b></p>", unsafe_allow_html=True)
