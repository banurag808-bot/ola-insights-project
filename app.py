import streamlit as st
import pandas as pd
import base64

# Page Configuration
st.set_page_config(
    page_title="Ola Ride Insights",
    page_icon="f0\x9f\x9a\x96",
    layout="wide"
)

# Sidebar for navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Overview", "SQL Insights", "Power BI Dashboard"])

# Load Data
try:
    df = pd.read_csv("ola_rides_cleaned.csv")
except FileNotFoundError:
    st.error("Error: 'ola_rides_cleaned.csv' not found. Make sure it's in your GitHub repository.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()


# ----------------- Overview Page -----------------
if menu == "Overview":
    st.title("Welcome to the Ola Ride Insights Project")
    st.markdown("This app provides insights from Ola ride data using SQL (via Pandas), Power BI, and Streamlit.")
    
    st.header("Data Preview")
    st.dataframe(df.head())
    
    st.header("Dataset Info")
    st.write(f"Total Rides: {len(df)}")
    st.write("Columns:", df.columns.tolist())

# ----------------- SQL Insights Page -----------------
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

    # 6. Peak Demand Hours
    peak_hours = df.groupby("booking_hour").agg(
        number_of_rides=('customer_id', 'count'),
        average_fare=('fare', 'mean')
    ).sort_values(by="number_of_rides", ascending=False).reset_index()
    st.subheader("6️⃣ Peak Demand Hours by Ride Count")
    st.write(peak_hours)

       # 8. Rides paid by Card
    card_rides = df[df['payment_method'] == 'Credit Card']
    st.subheader("8️⃣ Rides Paid by Card")
    st.write(card_rides.head())

    # 9. Average customer rating per vehicle type
    avg_cust_rating = df.groupby("vehicle_type")["customer_rating"].mean().reset_index()
    st.subheader("9️⃣ Average Customer Rating per Vehicle Type")
    st.write(avg_cust_rating)

    # 10. Total revenue from successful rides
    revenue = df[df['ride_status'] == 'Success']["fare"].sum()
    st.subheader("🔟 Total Revenue (Successful Rides)")
    st.metric("Revenue", f"₹{revenue:,.2f}")

    # 11. Incomplete rides with reason
    incomplete = df[df['ride_status'].str.contains("Canceled", na=False)][["ride_status", "cancellation_reason"]]
    st.subheader("1️⃣1️⃣ Incomplete Rides with Reason")
    st.write(incomplete.head())

# ----------------- Power BI Dashboard Page -----------------
elif menu == "Power BI Dashboard":
    st.title("📊 Power BI Dashboard (Exported PDF)")

    # Using the correct PDF filename
    pdf_file = "ola_powerbi_dashboard.pdf"

    try:
        with open(pdf_file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

        # Download option
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Power BI Dashboard (PDF)", f, file_name="Ola_Dashboard.pdf")
            
    except FileNotFoundError:
        st.error(f"Error: Could not find the file '{pdf_file}'. Please make sure it has been uploaded to your GitHub repository with this exact name.")