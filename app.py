import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("loan_clean.csv")

df = load_data()

# 1) عنوان ووصف
st.title("Loan Dashboard")
st.write("لوحة تعرض طلبات القروض وتتغير حسب الفلاتر.")

# 2) الفلاتر في Sidebar
st.sidebar.header("Filters")
areas = st.sidebar.multiselect("Property Area", df["Property_Area"].unique(), default=list(df["Property_Area"].unique()))
edu = st.sidebar.radio("Education", ["All"] + list(df["Education"].unique()))
max_income = st.sidebar.slider("Max Applicant Income", int(df["ApplicantIncome"].min()), int(df["ApplicantIncome"].max()), int(df["ApplicantIncome"].max()))

filtered = df[df["Property_Area"].isin(areas) & (df["ApplicantIncome"] <= max_income)]
if edu != "All":
    filtered = filtered[filtered["Education"] == edu]

# 7) لو الفلاتر ما رجعت صفوف
if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# 3) ثلاثة أرقام
c1, c2, c3 = st.columns(3)
c1.metric("Applications", len(filtered))
c2.metric("Approval Rate", f"{filtered['Loan_Status'].mean() * 100:.1f}%")
c3.metric("Median Loan Amount", f"{filtered['LoanAmount'].median():.0f}")

# 4) رسمتان في عمودين
left, right = st.columns(2)
with left:
    fig, ax = plt.subplots()
    sns.countplot(data=filtered, x="Loan_Status", ax=ax)
    ax.set_title("Loan Status Count")
    ax.set_xlabel("Loan Status (0 = Rejected, 1 = Approved)")
    ax.set_ylabel("Count")
    st.pyplot(fig)
with right:
    fig, ax = plt.subplots()
    sns.barplot(data=filtered, x="Property_Area", y="Loan_Status", ax=ax)
    ax.set_title("Approval Rate by Property Area")
    ax.set_xlabel("Property Area")
    ax.set_ylabel("Approval Rate")
    st.pyplot(fig)

# 5) selectbox لتوزيع عمود
col = st.selectbox("Choose a numeric column", filtered.select_dtypes(include="number").columns)
fig, ax = plt.subplots()
sns.histplot(data=filtered, x=col, ax=ax)
ax.set_title(f"Distribution of {col}")
ax.set_xlabel(col)
ax.set_ylabel("Count")
st.pyplot(fig)

# 6) الجدول داخل expander
with st.expander("Show filtered data"):
    st.dataframe(filtered)
    