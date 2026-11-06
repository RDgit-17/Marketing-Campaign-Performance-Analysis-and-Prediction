import streamlit as st
import pandas as pd

st.set_page_config(page_title="Marketing Campaign Analysis", page_icon="📊", layout="wide")

df = pd.read_csv('cleaned_data.csv')

# ---------- title ----------
st.title("Marketing Campaign Performance Analysis",text_alignment="center")
st.markdown('''Understand how campaigns perform across Nykaa, Purplle and Tira, and predict the revenue
        and outcome of your next campaign before you launch it.''',text_alignment="center")

st.write("")
b1, b2, b3, b4 = st.columns([1, 1.2, 1.2, 1])
with b2:
    st.page_link("pages/2_dashboard.py", label="Explore the dashboard", icon="📈", use_container_width=True,)
with b3:
    st.page_link("pages/3_prediction.py", label="Predict a campaign", icon="🔮", use_container_width=True)

st.divider()

# ---------- what you can do ----------
st.header("What you can do here")
c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.subheader("📈 Explore performance")
        st.write("See revenue, ROI and profitability by platform, campaign type and target audience. "
                 "Filter the data and find which campaigns work best.")
with c2:
    with st.container(border=True):
        st.subheader("🔮 Predict a new campaign")
        st.write("Enter a campaign's details, such as audience, channels, impressions and cost per conversion. "
                 "Get the predicted revenue, ROI and whether it is likely to make a profit or a loss.")

st.divider()

# ---------- how it works ----------
st.header("How it works")
s1, s2, s3, s4 = st.columns(4)
with s1:
    with st.container(border=True):
        st.markdown("#### 1. Collect")
        st.write("Campaign data from three beauty platforms is combined into one dataset.")
with s2:
    with st.container(border=True):
        st.markdown("#### 2. Clean")
        st.write("Missing values are handled, ROI is checked against its formula, and outliers are treated.")
with s3:
    with st.container(border=True):
        st.markdown("#### 3. Model")
        st.write("Many regression and classification models are compared, and the best ones are saved.")
with s4:
    with st.container(border=True):
        st.markdown("#### 4. Predict")
        st.write("This app loads the saved models and predicts for any campaign you describe.")

st.divider()

# ---------- about the data ----------
st.header("About the data")
d1, d2 = st.columns([1.2, 1])
with d1:
    st.write("Each row is one marketing campaign. The data describes how the campaign was set up, "
             "how many people it reached, and what it earned.")
    st.markdown("""
- **Setup:** platform, campaign type, target audience, customer segment, language, channels, duration
- **Reach and response:** impressions, clicks, leads, conversions, engagement score
- **Money:** acquisition cost per conversion, total cost, revenue, ROI
""")
with d2:
    with st.container(border=True):
        st.markdown("**At a glance**")
        st.write(f"Campaign types: {df['Campaign_Type'].nunique() - 1}")
        st.write(f"Target audiences: {df['Target_Audience'].nunique() - 1}")
        st.write(f"Languages: {df['Language'].nunique() - 1}")
        st.write("Channels: 6 (Email, Facebook, Google, Instagram, WhatsApp, YouTube)")

st.divider()

# ---------- how to read a prediction ----------
st.header("Reading a prediction")
r1, r2, r3 = st.columns(3)
r1.info("**Total investment**\n\nConversions × acquisition cost per conversion. Calculated for you.")
r2.info("**Predicted ROI**\n\n(Predicted revenue − total investment) ÷ total investment.")
r3.info("**Profit or loss**\n\nA second model estimates whether the campaign is likely to earn more than it costs.")

st.caption("Predictions are estimates based on patterns in historical campaign data, not guarantees. "
           "Values outside the range of the training data may be unreliable.")

