import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

df = pd.read_csv('cleaned_data.csv')
df['Total_Cost'] = df['Conversions'] * df['Acquisition_Cost']

st.title("Campaign Performance Dashboard")

# ---------- filters ----------
f1, f2, f3, f4 = st.columns(4)
platforms = f1.multiselect("Platform", sorted(df['Platform'].unique()), default=sorted(df['Platform'].unique()))
types = f2.multiselect("Campaign type", sorted(df['Campaign_Type'].unique()), default=sorted(df['Campaign_Type'].unique()))
audiences = f3.multiselect("Target audience", sorted(df['Target_Audience'].unique()), default=sorted(df['Target_Audience'].unique()))

d = df[df['Platform'].isin(platforms) & df['Campaign_Type'].isin(types) &
       df['Target_Audience'].isin(audiences)]

if d.empty:
    st.warning("No data for the selected filters.")
    st.stop()

st.divider()
# ---------- KPI cards ----------
st.markdown('#### Key Performance Indicators')
k1, k2, k3, k4 = st.columns(4)
with k1.container():
    st.metric("Campaigns", f"{len(d):,}")
with k2.container():
    st.metric("Total revenue", f"Rs.{d['Revenue'].sum() / 1e9:,.2f} bn")
with k3.container():
    st.metric("Total investment", f"Rs.{d['Total_Cost'].sum() / 1e6:,.1f} m")
with k4.container():
    st.metric("Average ROI", f"{d['ROI'].mean():.2f}")

st.divider()

# ---------- row 1 ----------
c1, c2, c3 = st.columns(3)
with c1.container():
    g = d.groupby('Platform', as_index=False)['Revenue'].sum()
    st.plotly_chart(px.pie(g, names='Platform', values='Revenue', hole=0.5, title="Revenue share by platform", height=300),
                    use_container_width=True)
with c2.container():
    g = d.groupby('Campaign_Type', as_index=False)['Revenue'].sum()
    st.plotly_chart(px.bar(g, x='Campaign_Type', y='Revenue', title="Revenue by campaign type", height=300),
                    use_container_width=True)
with c3.container():
    g = d['Profit/Loss_flag'].map({1: 'Profit', 0: 'Loss'}).value_counts().reset_index()
    g.columns = ['Result', 'Campaigns']
    st.plotly_chart(px.pie(g, names='Result', values='Campaigns', hole=0.5, title="Profit vs loss campaigns", height=300),
                    use_container_width=True)

# ---------- row 2 ----------
c1, c2, c3 = st.columns(3)
with c1.container(border=True):
    g = d.groupby('Campaign_Type', as_index=False)['ROI'].mean()
    st.plotly_chart(px.bar(g, x='Campaign_Type', y='ROI', title="Average ROI by campaign type", height=300),
                    use_container_width=True)
with c2.container(border=True):
    g = d.groupby('Target_Audience', as_index=False)['Revenue'].sum()
    st.plotly_chart(px.bar(g, x='Revenue', y='Target_Audience', orientation='h', title="Revenue by target audience", height=300),
                    use_container_width=True)
with c3.container(border=True):
    ch = d[['Channel_Used', 'Revenue']].copy()
    ch['Channel'] = ch['Channel_Used'].str.split(', ')
    ch = ch.explode('Channel')
    ch = ch[ch['Channel'] != 'Unknown'].groupby('Channel', as_index=False)['Revenue'].mean()
    st.plotly_chart(px.bar(ch, x='Channel', y='Revenue', title="Average revenue per campaign, by channel", height=300),
                    use_container_width=True)

# ---------- row 3 ----------
c1, c2 = st.columns(2)
with c1.container(border=True):
    f = pd.DataFrame({'Stage': ['Impressions', 'Clicks', 'Leads', 'Conversions'],
                      'Total': [d['Impressions'].sum(), d['Clicks'].sum(), d['Leads'].sum(), d['Conversions'].sum()]})
    st.plotly_chart(px.funnel(f, x='Total', y='Stage', title="Campaign funnel (totals)", height=300),
                    use_container_width=True)
with c2.container(border=True):
    g = d.groupby(['Customer_Segment', 'Platform'], as_index=False)['Revenue'].sum()
    st.plotly_chart(px.bar(g, x='Customer_Segment', y='Revenue', color='Platform', barmode='group',
                           title="Revenue by customer segment and platform", height=300),
                    use_container_width=True)

# ---------- detail table ----------
with st.expander("Top 10 campaigns by revenue"):
    st.dataframe(d.nlargest(10, 'Revenue')[['Platform', 'Campaign_Type', 'Target_Audience', 'Conversions',
                                            'Acquisition_Cost', 'Revenue', 'ROI']],
                 use_container_width=True, hide_index=True)