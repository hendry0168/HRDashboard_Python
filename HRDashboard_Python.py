import streamlit as st
import pandas as pd
import plotly.express as px
import pyodbc
#import db_utils
#from db_utils import get_ssms_connection

# streamlit run HRDashboard_Python.py

st.set_page_config(page_title="HR Dashboard"
                   , page_icon="👨‍💼"
                   , layout="wide")

def get_ssms_connection():
    server = 'LAPTOP-U55QS3H6\LIVE'  # e.g., 'localhost\\SQLEXPRESS'
    database = 'DBHR'
    #username = 'YOUR_USERNAME'  # or Windows auth
    #password = 'YOUR_PASSWORD'  # omit if using Windows auth
    
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;'
    )
    return conn

# --- Custom Card Component ---
def metric_card(title, value, delta=None):
    st.markdown(f"""
    <div class="metric-card">
        <p style="font-weight:600;margin:0;font-size:14px">{title}</p>
        <p style="font-size:24px;margin:5px 0;font-weight:700">{value}</p>
        {f'<p style="font-size:12px;margin:0;color:#2ecc71">{delta}</p>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def main(): 
    st.title("HR Dashboard (Python & SQL)")
    
    st.header("Statistics")

    conn = get_ssms_connection()

    try:   
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DBHR.dbo.GetHeadCountActive()")
        HeadCount = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetMaleHeadCountActive()")
        MaleHeadCount = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetFemaleHeadCountActive()")
        FemaleHeadCount = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetAverageAge()")
        AverageAge = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetAverageTenure()")
        AverageTenure = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetAverageTurnover()")
        AverageTurnover = cursor.fetchone()[0]
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")
        
    cols = st.columns(3)
    with cols[0]: metric_card("👥 Head Count", HeadCount)
    with cols[1]: metric_card("♂️ Male", MaleHeadCount)
    with cols[2]: metric_card("♀️ Female", FemaleHeadCount)
        

# --------------------------------------------------------------------------

    cols = st.columns(3)
    with cols[0]: metric_card("⌛ Avg. Age", AverageAge)
    with cols[1]: metric_card("📆 Avg. Tenure", AverageTenure)
    with cols[2]: metric_card("🔄 Avg. Turnover", AverageTurnover)

# --------------------------------------------------------------------------

    st.header("📈 Distribution Analysis")
    cols = st.columns(3)

    try:   
        query = """SELECT * FROM DBHR.dbo.GetEmploymentTypeCount()""" 
        EmploymentType = pd.read_sql(query, conn)
        #conn.close()
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")

    with cols[0]:
        fig = px.pie(EmploymentType, names="Employment Type", 
                    values="Employment Type Count",
                    title="📝 Employment Type", hole=0.3,
                    template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    try:   
        query = """SELECT * FROM DBHR.dbo.GetPersonnelLevelCount()""" 
        Level = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")

    with cols[1]:
        fig = px.pie(Level, names="Personnel Level", 
                    values="Personnel Level Count",
                    title="📶 Level", hole=0.3,
                    template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    try:   
        query = """SELECT * FROM DBHR.dbo.GetReligionCount()""" 
        Religion = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")

    with cols[2]:
        fig = px.pie(Religion, names="Religion", 
                    values="Personnel Religion Count",
                    title="🛐 Religion", hole=0.3,
                    template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------------------
    cols = st.columns(2)

    try:   
        query = """SELECT * FROM DBHR.dbo.GetAgeDistributionCount() ORDER BY seq""" 
        age_distribution = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")
    
    with cols[0]:
        fig1 = px.bar(age_distribution, x="Age Count", 
                    y="Age", 
                    title="📊 Age Distribution", 
                    color="Age Count",
                    orientation='h')  # Changed to vertical columns
        fig1.update_traces(marker_line_width=1, marker_line_color='white')
        st.plotly_chart(fig1, use_container_width=True)

    try:   
        query = """SELECT * FROM DBHR.dbo.GetEducationCount() ORDER BY seq""" 
        education_degree = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")
    
    with cols[1]:
        fig2 = px.bar(education_degree, x="Education Level Count", 
                    y="Education Level", 
                    title="🎓 Education Degree", 
                    color="Education Level Count",
                    orientation='h')  # Changed to vertical columns
        fig2.update_traces(marker_line_width=1, marker_line_color='white')
        st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------------------------------

    st.header("Hiring & Turnover")

    try:   
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DBHR.dbo.GetLastMonthHiringCount()")
        LastMonthHiringCount = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetLastMonthSeparationCount()")
        LastMonthSeparationCount = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetCurrentMonthHiringCount()")
        CurrentMonthHiringCount = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetCurrentMonthSeparationCount()")
        CurrentMonthSeparationCount = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetYTDHiringCount()")
        YTDHiringCount = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM DBHR.dbo.GetYTDSeparationCount()")
        YTDSeparationCount = cursor.fetchone()[0]
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")

    cols = st.columns(2)
    with cols[0]: metric_card("⏪👥 Previous Month Hiring", LastMonthHiringCount)
    with cols[1]: metric_card("⏪🔄 Previous Month Turnover", LastMonthSeparationCount)
    
    cols = st.columns(2)
    with cols[0]: metric_card("📌👥 Current Month Hiring", CurrentMonthHiringCount, CurrentMonthHiringCount - LastMonthHiringCount)
    with cols[1]: metric_card("📌🔄 Current Month Turnover", CurrentMonthSeparationCount, CurrentMonthSeparationCount - LastMonthSeparationCount)
    
    cols = st.columns(2)
    with cols[0]: metric_card("📈👥 Year To Date Hiring", YTDHiringCount)
    with cols[1]: metric_card("📈🔄 Year To Date Turnover", YTDSeparationCount)

# --------------------------------------------------------------------------

    try:   
        # -- Fetch data from SQL functions --
        onboarding_df = pd.read_sql("SELECT MonthYear, EmployeeCount FROM DBHR.dbo.GetMonthlyHiringCount() ORDER BY MonthDate", conn)
        onboarding_df.rename(columns={"EmployeeCount": "Onboarding"}, inplace=True)
        
        offboarding_df = pd.read_sql("SELECT MonthYear, EmployeeCount FROM DBHR.dbo.GetMonthlySeparationCount() ORDER BY MonthDate", conn)
        offboarding_df.rename(columns={"EmployeeCount": "Offboarding"}, inplace=True)

        # -- Merge both datasets on Department --
        merged_df = pd.merge(onboarding_df, offboarding_df, on="MonthYear").fillna(0)

    except Exception as e:
        st.error(f"🚨 Database Error: {e}")

    # --- Create Vertical Grouped Bar Chart ---
    fig = px.bar(merged_df,
                x="MonthYear",
                y=["Onboarding", "Offboarding"],
                title="<b>Monthly Onboarding & Offboarding Statistic</b>",
                color_discrete_map={"Onboarding": "#4CAF50"
                                    , "Offboarding": "#F44336"},
                barmode='group',  
                template="plotly_white",
                labels={"value": "Number of Employees"
                        , "variable": "Movement"})

    # --- Customize Layout ---
    fig.update_layout(
        height=500,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Add value labels on bars
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------------------

    cols = st.columns(2)

    try:   
        query = """SELECT * FROM DBHR.dbo.GetTenureCount() ORDER BY seq""" 
        Tenure = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")

    with cols[0]:
        fig3 = px.bar(Tenure, x="Tenure", y="Tenure Count",
                    title="🕰️ Tenure", color="Tenure")
        st.plotly_chart(fig3, use_container_width=True)

    try:   
        query = """SELECT * FROM DBHR.dbo.GetTenureByTurnoverCount() ORDER BY seq""" 
        TenureByTurnover = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")

    with cols[1]:
        fig4 = px.bar(TenureByTurnover, x="Tenure By Turnover", 
                    y="Tenure By Turnover Count",
                    title="🔁 Turnover", color="Tenure By Turnover")
        st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------------------------------
 
main()