# app.py
import streamlit as st
import pandas as pd
import base64

# ----------------- Load Dataset -----------------
df = pd.read_csv("ola_rides_cleaned.csv")

st.set_page_config(page_title="Ola Ride Insights", layout="wide")

# ----------------- Sidebar Navigation -----------------
st.sidebar.title("🚖 Ola Ride Insights")
menu = st.sidebar.radio(
    "Go to:",
    ["Overview", "SQL Insights", "Power BI Dashboard"]
)

# ----------------- Overview -----------------
if menu == "Overview":
    st.title("🚖 Ola Ride Insights Dashboard")
    st.markdown("This app provides insights from OLA ride data using SQL (via pandas), Power BI (PDF), and Streamlit.")

    st.subheader("📊 Data Preview")
    st.write(df.head())

    st.subheader("🔑 Dataset Info")
    st.write(f"Total Rides: {len(df)}")
    st.write(f"Columns: {df.shape[1]}")
    st.write(df.columns.tolist())

# ----------------- SQL Insights -----------------
elif menu == "SQL Insights":
    st.title("🗂 SQL Insights (Recreated with Pandas)")

    # 1. Successful bookings
    success = df[df['ride_status'] == 'Success']
    st.subheader("1️⃣ Successful Bookings")
    st.write(success.head())

    # 2. Average ride distance per vehicle type
    avg_distance = df.groupby("vehicle_type")["distance"].mean().reset_index()
    st.subheader("2️⃣ Average Ride Distance by Vehicle Type")
    st.write(avg_distance)

    # 3. Total customer cancellations
    cust_cancel = df[df['ride_status'] == 'Canceled by Customer'].shape[0]
    st.subheader("3️⃣ Total Customer Cancellations")
    st.metric("Customer Cancellations", cust_cancel)

    # 4. Top 5 customers by ride count
    top_customers = df.groupby("customer_id").size().sort_values(ascending=False).head(5)
    st.subheader("4️⃣ Top 5 Customers by Ride Count")
    st.write(top_customers)

    # 5. Driver cancellations by reason
    driver_cancel = df[df['ride_status'] == 'Canceled by Driver'].groupby("cancellation_reason").size().reset_index(name='count')
    st.subheader("5️⃣ Driver Cancellations by Reason")
    st.write(driver_cancel)

    # 6. Query to find Peak Demand Hours
    peak_hours = df.groupby("booking_hour").agg(
        number_of_rides=('customer_id', 'count'),
        average_fare=('fare', 'mean')
    ).sort_values(by="number_of_rides", ascending=False).reset_index()
    st.subheader("6️⃣ Peak Demand Hours by Ride Count")
    st.write(peak_hours)

        # 7. Rides paid by Card
    card_rides = df[df['payment_method'] == 'Credit Card']
    st.subheader("8️⃣ Rides Paid by Card")
    st.write(card_rides.head())

    # 8. Average customer rating per vehicle type
    avg_cust_rating = df.groupby("vehicle_type")["customer_rating"].mean().reset_index()
    st.subheader("9️⃣ Average Customer Rating per Vehicle Type")
    st.write(avg_cust_rating)

    # 9. Total revenue from successful rides
    revenue = df[df['ride_status'] == 'Success']["fare"].sum()
    st.subheader("🔟 Total Revenue (Successful Rides)")
    st.metric("Revenue", f"₹{revenue:,.2f}")

    # 10. Incomplete rides with reason
    incomplete = df[df['ride_status'].str.contains("Canceled", na=False)][["ride_status", "cancellation_reason"]]
    st.subheader("1️⃣1️⃣ Incomplete Rides with Reason")
    st.write(incomplete.head())
# ----------------- Power BI Dashboard -----------------
elif menu == "Power BI Dashboard":
    st.title("📊 Power BI Dashboard (Exported PDF)")

    # MISTAKE FIXED: Using the correct PDF filename
    pdf_file = "ola_powerbi.pdf"

    # Show PDF inside Streamlit
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

    # Download option
    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download Power BI Dashboard (PDF)", f, file_name="Ola_Dashboard.pdf")
