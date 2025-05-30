import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_card import card

# Load data
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")


st.sidebar.info("Use the filters above to explore employee attrition patterns by department, role, and more.")


# Sidebar filters
st.sidebar.header("Filters")
department = st.sidebar.multiselect("Department", options=df['Department'].unique(), default=df['Department'].unique())
gender = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

# Filter data
filtered_df = df[df['Department'].isin(department) & df['Gender'].isin(gender)]

# Key Metrics
total_employees = len(filtered_df)
attrition_count = filtered_df[filtered_df['Attrition'] == 'Yes'].shape[0]
average_age = round(filtered_df['Age'].mean(), 1)
average_salary = round(filtered_df['MonthlyIncome'].mean(), 1)

st.title("HR Attrition Dashboard")
st.markdown("Interactive dashboard for employee attrition analysis.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Employees", total_employees)
col2.metric("Attrition Count", attrition_count)
col3.metric("Avg. Age", average_age)
col4.metric("Avg. Salary", average_salary)

# Department-wise attrition (Seaborn/Matplotlib)
fig1, ax1 = plt.subplots(figsize=(10,6))
sns.countplot(data=filtered_df, x="Department", hue="Attrition", palette="viridis", ax=ax1)
st.pyplot(fig1)

# Attrition based on gender (Seaborn/Matplotlib)
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.countplot(data=filtered_df, x="Gender", hue="Attrition", palette="Purples", ax=ax2)
st.pyplot(fig2)

# Distribution of business travel (Matplotlib Pie Chart)
fig3, ax3 = plt.subplots(figsize=(6,6))
filtered_df['BusinessTravel'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='coolwarm', ax=ax3)
ax3.set_ylabel('')
ax3.set_title('Distribution of Business Travel')
st.pyplot(fig3)

# Business travel vs attrition (Seaborn/Matplotlib)
fig4 = sns.displot(data=filtered_df, x="BusinessTravel", hue="Attrition", height=6, aspect=1.5, palette="viridis")
plt.title("Attrition based on Business Travel")
st.pyplot(fig4.fig)

# Attrition by marital status and gender (Seaborn Heatmap)
df_attrition = filtered_df[filtered_df["Attrition"] == "Yes"]
df_heatmap = df_attrition.pivot_table(index="MaritalStatus", columns="Gender", values="EmployeeNumber", aggfunc="count")
fig5, ax5 = plt.subplots(figsize=(8,6))
sns.heatmap(df_heatmap, annot=True, cmap="coolwarm", fmt="d", ax=ax5)
ax5.set_title("Attrition by Marital Status & Gender (Heatmap)")
st.pyplot(fig5)

# Department wise attrition based on performance rating (Seaborn FacetGrid)
filtered_df = df.copy()  # You can filter as needed
fig6 = sns.displot(
    data=filtered_df,
    x="PerformanceRating",
    hue="Attrition",
    col="Department",
    palette="viridis",
    multiple="stack",
    height=5,
    aspect=1
)
plt.subplots_adjust(top=0.85)
plt.suptitle("Distribution of Performance Rating Based on Attrition Across Departments", y=1.05)
st.pyplot(fig6.fig)

# Monthly income distribution (Seaborn/Matplotlib)
fig7 = sns.displot(data=filtered_df, x="MonthlyIncome", palette="viridis", hue="Attrition", height=6, aspect=1.5)
plt.title("Distribution of Monthly Income")
st.pyplot(fig7.fig)

# Distance from home vs attrition (Seaborn/Matplotlib)
fig8, ax8 = plt.subplots(figsize=(10,6))
sns.boxplot(x='Attrition', y='DistanceFromHome', data=filtered_df, palette='viridis', ax=ax8)
ax8.set_title('Distance from Home vs Attrition')
st.pyplot(fig8)

# Age distribution (Seaborn/Matplotlib)
fig9 = sns.displot(data=filtered_df, x="Age", color="Purple", height=6, aspect=1.5)
plt.title("Distribution of Age")
st.pyplot(fig9.fig)

# Monthly Income and Work Life Balance (Seaborn/Matplotlib)
fig10, ax10 = plt.subplots(figsize=(10,6))
sns.boxplot(data=filtered_df, x="WorkLifeBalance", y="MonthlyIncome", palette="viridis", ax=ax10)
ax10.set_title("Distribution of Monthly Income and Work Life Balance")
ax10.set_xlabel("Work Life Balance")
ax10.set_ylabel("Monthly Income")
st.pyplot(fig10)

# Employee attrition funnel (Plotly)
funnel_data = {
    "stage": ["Total Employees", "Joined Last Year", "Employees Leaving < 1 Year", "Retained Employees"],
    "count": [
        df.shape[0],
        df[df['YearsAtCompany'] <= 1].shape[0],
        df[(df['YearsAtCompany'] <= 1) & (df['Attrition'] == 'Yes')].shape[0],
        df.shape[0] - df[(df['YearsAtCompany'] <= 1) & (df['Attrition'] == 'Yes')].shape[0]
    ]
}

fig_funnel = px.funnel(funnel_data, x='count', y='stage', title="Employee Funnel")
st.plotly_chart(fig_funnel)


# distribution of employees working with current manager
plt.figure(figsize = (10,6))
fig11 = sns.displot(data =df, x = "YearsWithCurrManager", hue = "Attrition", height = 6,aspect = 1.5,palette= "viridis")
plt.ylabel("Count")
plt.xlabel("No. of Years with current manager")
st.pyplot(fig11)


# Scatter plot: Age vs Monthly Income
fig12, ax12 = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=filtered_df, x='Age', y='MonthlyIncome', color='purple', ax=ax12)
ax12.set_xlabel('Age')
ax12.set_ylabel('Monthly Income')
ax12.set_title('Scatter Plot of Age vs. Monthly Income')
st.pyplot(fig12)

# Years at Company vs. Average Salary Hike (filtered)
years_salary = filtered_df.groupby('YearsAtCompany')['PercentSalaryHike'].mean().reset_index()
fig13, ax13 = plt.subplots(figsize=(10, 6))
ax13.plot(years_salary['YearsAtCompany'], years_salary['PercentSalaryHike'], marker='o', linestyle='-', color='purple')
ax13.set_xlabel('Years at Company')
ax13.set_ylabel('Average Percent Salary Hike')
ax13.set_title('Years at Company vs. Average Salary Hike')
ax13.grid(True)
st.pyplot(fig13)
