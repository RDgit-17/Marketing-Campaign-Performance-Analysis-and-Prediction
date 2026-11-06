import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

st.set_page_config(page_title="Prediction", layout="wide")
st.title("Marketing Campaign Revenue Prediction System")
st.divider()

# ---------- load models and data ----------
revenue_pipeline = pickle.load(open('revenue_pipeline_app.pkl', 'rb'))
profit_loss_pipeline = pickle.load(open('profit_loss_pipeline_app.pkl', 'rb'))
df = pd.read_csv('cleaned_data.csv')

def options(column):
    return sorted([v for v in df[column].unique() if v != 'Unknown'])

app_cols = ['Platform','Campaign_Type','Target_Audience','Channel_Used','Language','Customer_Segment',
            'Duration','Impressions','Clicks','Leads','Conversions','Acquisition_Cost','Engagement_Score','Total_Cost']

# ---------- layout: inputs on the left (3 columns), result on the right ----------
inputs_area, result_area = st.columns([0.8, 1.2], gap="large")

with inputs_area:
    col1, col2, = st.columns([0.4,0.4])

    with col1:
        platform = st.selectbox("Platform", options('Platform'), index=None, placeholder="Select platform")
        campaign_type = st.selectbox("Campaign type", options('Campaign_Type'), index=None, placeholder="Select campaign type")
        target_audience = st.selectbox("Target audience", options('Target_Audience'), index=None, placeholder="Select audience")
        customer_segment = st.selectbox("Customer segment", options('Customer_Segment'), index=None, placeholder="Select segment")
        language = st.selectbox("Language", options('Language'), index=None, placeholder="Select language")
        channels = st.multiselect("Channels", ['Email','Facebook','Google','Instagram','WhatsApp','YouTube'], placeholder="Select channels")
        duration = st.number_input("Duration (days)", min_value=5, max_value=30, value=None, placeholder="Enter No.of days")
    
    with col2:
        impressions = st.number_input("Impressions", min_value=10001, max_value = 100000,value=None, placeholder="Enter impressions")
        clicks = st.number_input("Clicks", min_value=0, value=None, placeholder="Enter clicks")
        leads = st.number_input("Leads", min_value=0 ,value=None, placeholder="Enter leads")
        conversions = st.number_input("Conversions", min_value=0, value=None, placeholder="Enter conversions")
        acquisition_cost = st.number_input("Acquisition cost (per conversion)", min_value=8.18, value=None, placeholder="Enter cost")
        engagement_score = st.number_input("Engagement score", min_value=0, value=None, placeholder="Enter score")

    predict = st.button("Predict", type="primary", use_container_width=True)
    
prediction_done = False
with result_area: 
    st.subheader("Result")
    if not predict:
        st.info("Fill in all fields and press Predict.")
    else:
        required = {
            "Platform": platform, "Campaign type": campaign_type, "Target audience": target_audience,
            "Customer segment": customer_segment, "Language": language, "Duration": duration,
            "Channels": channels, "Impressions": impressions, "Clicks": clicks, "Leads": leads,
            "Conversions": conversions, "Acquisition cost": acquisition_cost, "Engagement score": engagement_score}
        missing = [name for name, value in required.items() if value is None or value == []]

        if missing:
            st.error("Please fill in all the fields. Missing: " + ", ".join(missing))
        else:
            row = pd.DataFrame([{
                'Platform': platform, 'Campaign_Type': campaign_type, 'Target_Audience': target_audience,
                'Channel_Used': ', '.join(channels),
                'Language': language, 'Customer_Segment': customer_segment, 'Duration': duration,
                'Impressions': impressions, 'Clicks': clicks, 'Leads': leads, 'Conversions': conversions,
                'Acquisition_Cost': acquisition_cost, 'Engagement_Score': engagement_score}])
            row['Total_Cost'] = row['Conversions'] * row['Acquisition_Cost']       # calculated by the app

            revenue = revenue_pipeline.predict(row[app_cols])[0]
            flag = profit_loss_pipeline.predict(row[app_cols])[0]
            total_cost = row['Total_Cost'][0]
            roi = (revenue - total_cost) / total_cost

            col1,col2,col3 = st.columns(3)
            result1 = col1.metric("Total Investment (calculated)", f"Rs.{total_cost:,.0f}")
            result2 = col2.metric("Predicted revenue", f"Rs.{revenue:,.0f}")
            result3 = col3.metric("Predicted ROI", f"{roi:.2f}")
            if flag == 1:
                st.success("Expected result: PROFIT")
            else:
                st.error("Expected result: LOSS")
            prediction_done = True

# ---------- visuals based on the prediction ----------
    if prediction_done:
        st.subheader("How this campaign compares")

        v1, v2, v3 = st.columns(3)

        # 1. cost vs predicted revenue
        with v1:
            d = pd.DataFrame({'Item': ['Total cost', 'Predicted revenue'], 'Amount': [total_cost, revenue]})
            fig = px.bar(d, x='Item', y='Amount', color='Item', text_auto='.3s',
                     color_discrete_map={'Total cost': '#9E9E9E', 'Predicted revenue': '#2E7D32' if flag == 1 else '#C62828'})
            fig.update_layout(title="Cost vs predicted revenue", showlegend=False, height=330, margin=dict(t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)

        # 2. campaign funnel from the inputs
        with v2:
            d = pd.DataFrame({'Stage': ['Impressions', 'Clicks', 'Leads', 'Conversions'],
                                'Count': [impressions, clicks, leads, conversions]})
            fig = px.funnel(d, x='Count', y='Stage')
            fig.update_layout(title="Campaign funnel", height=330, margin=dict(t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)


    # 3. step-by-step rates from the inputs
        with v3:
            d = pd.DataFrame({'Rate': ['Click rate', 'Lead rate', 'Conversion rate'],
                            'Percent': [clicks / impressions * 100, leads / clicks * 100, conversions / leads * 100]})
            fig = px.bar(d, x='Rate', y='Percent', color='Rate', text_auto='.1f')
            fig.update_layout(title="Funnel rates (%)", showlegend=False, height=330, margin=dict(t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)


