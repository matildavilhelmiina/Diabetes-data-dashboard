import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Page config

st.set_page_config(page_title="Diabetes Dashboard", layout="wide")


# Load data

df = pd.read_csv("../data/diabetes_cleaned.csv")


# Title

st.title("Diabetes Risk Analysis Dashboard")
st.write("This dashboard explores key health indicators associated with diabetes.")


# Sidebar filter

st.sidebar.header("Filters")

age_range = st.sidebar.slider(
    "Age range",
    int(df["age"].min()),
    int(df["age"].max()),
    (20, 60)
)

gender = st.sidebar.selectbox(
    "Select gender",
    options=["All", "Male", "Female"]
)

filtered_df = df[
    (df["age"] >= age_range[0]) & 
    (df["age"] <= age_range[1])
]

if gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == gender]


# Metrics

st.markdown("## Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Patients", len(filtered_df))
col2.metric("Diabetes %", f"{filtered_df['diabetes'].mean()*100:.1f}%")
col3.metric("Avg BMI", f"{filtered_df['bmi'].mean():.1f}")


# Diabetes distribution

st.markdown("## Diabetes Distribution")

col1, col2 = st.columns([2, 3])

with col1:
    fig, ax = plt.subplots(figsize=(6,5))
    filtered_df["diabetes"].value_counts().plot(kind="bar", ax=ax)

    ax.set_xticks([0,1])
    ax.set_xticklabels(["No Diabetes", "Diabetes"], rotation=0)
    ax.set_ylabel("Count")
    ax.set_title("Diabetes Distribution")

    sns.despine()

    st.pyplot(fig)


# Biomarkers

st.markdown("## Biomarkers")

col1, col2 = st.columns(2)

with col1:
    st.subheader("HbA1c Levels")
    fig, ax = plt.subplots()
    sns.boxplot(x="diabetes", y="HbA1c_level", data=filtered_df, ax=ax)
    ax.set_xticklabels(["No Diabetes", "Diabetes"])
    sns.despine()
    st.pyplot(fig)

with col2:
    st.subheader("Blood Glucose (mmol/L)")
    fig, ax = plt.subplots()
    sns.boxplot(x="diabetes", y="blood_glucose_mmol", data=filtered_df, ax=ax)
    ax.set_xticklabels(["No Diabetes", "Diabetes"])
    sns.despine()
    st.pyplot(fig)


# Risk factors

st.markdown("## Risk Factors")

col1, col2 = st.columns(2)

with col1:
    st.subheader("BMI")
    fig, ax = plt.subplots()
    sns.boxplot(x="diabetes", y="bmi", data=filtered_df, ax=ax)
    ax.set_xticklabels(["No Diabetes", "Diabetes"])
    sns.despine()
    st.pyplot(fig)

with col2:
    st.subheader("Hypertension")

    hypertension_percent = filtered_df.groupby("hypertension")["diabetes"].mean() * 100

    fig, ax = plt.subplots()
    hypertension_percent.plot(kind="bar", ax=ax)

    ax.set_xticks([0,1])
    ax.set_xticklabels(["No Hypertension", "Hypertension"], rotation=0)
    ax.set_ylabel("Diabetes (%)")

    for i, v in enumerate(hypertension_percent):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha='center')

    sns.despine()

    st.pyplot(fig)


# Insights

st.markdown("## Key Insights")

st.write("""
- Individuals with diabetes show higher HbA1c and blood glucose levels  
- Higher BMI is associated with increased diabetes prevalence  
- Diabetes is significantly more common among individuals with hypertension  
""")