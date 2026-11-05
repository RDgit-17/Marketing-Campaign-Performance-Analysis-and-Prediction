# Multi-Brand Marketing Campaign Performance Analysis & Prediction

An end-to-end machine learning project that cleans and analyses marketing campaign data from three beauty brands (**Nykaa**, **Purplle**, **Tira**), predicts campaign Revenue (regression) and whether a campaign will end in Profit or Loss (classification), and serves everything through an interactive Streamlit app.

## Features

* **Data Cleaning & Preprocessing:** Merging brand-level CSVs, handling missing values and duplicates, type conversion, and ROI validation/correction.
* **Feature Engineering:** Multi-label encoding of `Channel_Used` (multiple channels in one cell), `Profit/Loss_flag` derived from ROI, and `Total_Cost = Conversions × Acquisition_Cost`.
* **Exploratory Data Analysis (EDA):** Brand-, campaign-type-, and channel-wise performance analysis, alongside relationships between spend, clicks, revenue, and ROI.
* **Machine Learning Models:**
  * **Revenue Regression:** `CatBoostRegressor`
  * **Profit/Loss Classification:** `LightGBM` Classifier
  * Both models are wrapped in robust `scikit-learn` Pipelines (scaling + ordinal encoding + channel multi-label encoding). *Note: ROI is excluded from classification features to prevent data leakage.*
* **Interactive Streamlit App:** Multi-page layout featuring a Home overview, an analytical Dashboard, and a live Prediction interface.



## Results

| Task | Model | Metric | Score |
| :--- | :--- | :--- | :--- |
| **Revenue Prediction** | CatBoost Regressor | R2 | 0.987 |
| **Profit/Loss Prediction** | LightGBM Classifier | Accuracy | 0.998 |


## Project Structure

```text
├── app.py                      # Streamlit entry point (navigation)
├── pages/
│   ├── 1_home.py
│   ├── 2_dashboard.py
│   └── 3_prediction.py
├── data/
│   ├── raw/                    # nykaa_raw.csv, purplle_raw.csv, tira_raw.csv
│   └── processed/              # cleaned_data.csv
├── notebooks/
│   ├── Cleaning_and_preprocessing.ipynb
│   ├── EDA.ipynb
│   ├── Model_building.ipynb    # Source for final metrics
│   └── Final_pipeline.ipynb    # Trains and exports the pipelines
├── models/
│   ├── revenue_pipeline_app.pkl
│   └── profit_loss_pipeline_app.pkl
├── requirements.txt
└── README.md
```
## Dataset Schema Description

 - *Campaign_ID :* Unique campaign identifier
 - *Campaign_Type :* Type of Campaign
 - *Target_Audience :* Group of customers targeted by the campaign
 - *Duration :* Campaign length in days
 - *Channel_Used :* Marketing channels used for the campaign (may contain multiple channels)
 - *Impressions :* Number of times the campaign was displayed to users
 - *Clicks :* Number of users who clicked on the campaign
 - *Leads :* Number of potential customers generated
 - *Conversions :* Number of successful actions (e.g., purchases or sign-ups)
 - *Acquisition_Cost :* Cost incurred to run the campaign
 - *Revenue :* Total revenue generated from the campaign
 - *ROI :* Return on Investment; indicating campaign profitability
 - *Language :* Language used in the campaign content
 - *Engagement_Score :* Measure of user interaction and engagement level
 - *Customer_Segment :* Category of customers targeted
 - *Date :* Date on which the campaign was executed

 ## Tech Stack

Python, Pandas, NumPy, scikit-learn, CatBoost, LightGBM, Matplotlib, Seaborn, Plotly, Streamlit

## Notes & Limitations
- Pickled models depend on the library versions in `requirements.txt`; use the same versions to load them.
- The classification target is derived from ROI, which itself depends on revenue and cost, so high accuracy partly reflects that relationship.
