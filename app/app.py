import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Customer Intelligence",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "ecommerce_hackathon.db"


# ============================================================
# DATABASE FUNCTION
# ============================================================

def run_query(query):

    conn = sqlite3.connect(DB_PATH)

    result = conn.execute(query).fetchone()

    conn.close()

    return result


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 AI Powered E-Commerce Customer Intelligence System")

st.caption(
    "Data Science Final Hackathon | E-Commerce Analytics Dashboard"
)

# ============================================================
# CITY REVENUE ANALYSIS
# ============================================================

city_revenue_query = """
SELECT
    CASE
        WHEN LOWER(TRIM(c.city)) = 'karachi'
            THEN 'Karachi'
        WHEN LOWER(TRIM(c.city)) = 'lahore'
            THEN 'Lahore'
        WHEN LOWER(TRIM(c.city)) = 'islamabad'
            THEN 'Islamabad'
        WHEN LOWER(TRIM(c.city)) = 'rawalpindi'
            THEN 'Rawalpindi'
        WHEN LOWER(TRIM(c.city)) = 'faisalabad'
            THEN 'Faisalabad'
        WHEN LOWER(TRIM(c.city)) = 'multan'
            THEN 'Multan'
        WHEN LOWER(TRIM(c.city)) = 'gujranwala'
            THEN 'Gujranwala'
        WHEN LOWER(TRIM(c.city)) = 'peshawar'
            THEN 'Peshawar'
        WHEN LOWER(TRIM(c.city)) = 'quetta'
            THEN 'Quetta'
        WHEN LOWER(TRIM(c.city)) = 'hyderabad'
            THEN 'Hyderabad'
        WHEN LOWER(TRIM(c.city)) = 'bahawalpur'
            THEN 'Bahawalpur'
        ELSE TRIM(c.city)
    END AS city,

    SUM(
        o.quantity * o.unit_price *
        (1 - COALESCE(o.discount, 0))
    ) AS revenue,

    COUNT(DISTINCT o.order_id) AS orders

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

WHERE o.returned IN (
    0,
    '0',
    'false',
    'False',
    'no',
    'No'
)

GROUP BY
    CASE
        WHEN LOWER(TRIM(c.city)) = 'karachi'
            THEN 'Karachi'
        WHEN LOWER(TRIM(c.city)) = 'lahore'
            THEN 'Lahore'
        WHEN LOWER(TRIM(c.city)) = 'islamabad'
            THEN 'Islamabad'
        WHEN LOWER(TRIM(c.city)) = 'rawalpindi'
            THEN 'Rawalpindi'
        WHEN LOWER(TRIM(c.city)) = 'faisalabad'
            THEN 'Faisalabad'
        WHEN LOWER(TRIM(c.city)) = 'multan'
            THEN 'Multan'
        WHEN LOWER(TRIM(c.city)) = 'gujranwala'
            THEN 'Gujranwala'
        WHEN LOWER(TRIM(c.city)) = 'peshawar'
            THEN 'Peshawar'
        WHEN LOWER(TRIM(c.city)) = 'quetta'
            THEN 'Quetta'
        WHEN LOWER(TRIM(c.city)) = 'hyderabad'
            THEN 'Hyderabad'
        WHEN LOWER(TRIM(c.city)) = 'bahawalpur'
            THEN 'Bahawalpur'
        ELSE TRIM(c.city)
    END

ORDER BY revenue DESC;
"""

conn = sqlite3.connect(DB_PATH)
city_revenue = conn.execute(city_revenue_query).fetchall()
conn.close()

st.divider()
st.subheader("🏙️ Revenue by City")

city_revenue_df = pd.DataFrame(
    city_revenue,
    columns=["city", "revenue", "orders"]
)

st.bar_chart(
    city_revenue_df.set_index("city")["revenue"]
)

st.subheader("📋 City Performance")

st.dataframe(
    city_revenue_df,
    use_container_width=True
)

conn = sqlite3.connect(DB_PATH)
city_revenue = conn.execute(city_revenue_query).fetchall()
conn.close()

st.divider()
st.subheader("🏙️ Revenue by City")

city_revenue_df = pd.DataFrame(
    city_revenue,
    columns=["city", "revenue", "orders"]
)

st.bar_chart(
    city_revenue_df.set_index("city")["revenue"]
)

st.subheader("📋 City Performance")

st.dataframe(
    city_revenue_df,
    use_container_width=True
)

# ============================================================
# DATABASE CONNECTED
# ============================================================

st.success("SQLite database connected successfully! ✅")


# ============================================================
# TOTAL NET REVENUE
# ============================================================

revenue_query = """

SELECT

    SUM(
        quantity * unit_price *
        (1 - COALESCE(discount, 0))
    )

FROM orders

WHERE returned IN (
    0,
    '0',
    'false',
    'False',
    'no',
    'No'
);

"""


revenue_result = run_query(revenue_query)

total_revenue = revenue_result[0]


if total_revenue is None:

    total_revenue = 0


# ============================================================
# TOTAL ORDERS
# ============================================================

orders_query = """

SELECT

    COUNT(DISTINCT order_id)

FROM orders

WHERE returned IN (
    0,
    '0',
    'false',
    'False',
    'no',
    'No'
);

"""


orders_result = run_query(orders_query)

total_orders = orders_result[0]


# ============================================================
# TOTAL CUSTOMERS
# ============================================================

customers_query = """

SELECT

    COUNT(DISTINCT customer_id)

FROM customers;

"""


customers_result = run_query(customers_query)

total_customers = customers_result[0]


# ============================================================
# KPI DASHBOARD
# ============================================================

st.subheader("📌 Business Overview")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "💰 Total Net Revenue",
        f"{total_revenue:,.2f}"
    )


with col2:

    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,}"
    )


with col3:

    st.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )


# ============================================================
# SEPARATOR
# ============================================================

st.divider()


# ============================================================
# DATABASE INFORMATION
# ============================================================

st.subheader("🗄️ Database Information")

st.write(
    "The dashboard is connected to the SQLite database "
    "`ecommerce_hackathon.db`."
)
st.write(
    "The dashboard is connected to the SQLite database "
    "`ecommerce_hackathon.db`."
)
# ============================================================
# MONTHLY REVENUE TREND
# ============================================================

monthly_revenue_query = """
SELECT

    strftime('%Y-%m', order_date) AS month,

    SUM(
        quantity * unit_price *
        (1 - COALESCE(discount, 0))
    ) AS revenue

FROM orders

WHERE returned IN (
    0,
    '0',
    'false',
    'False',
    'no',
    'No'
)

GROUP BY
    strftime('%Y-%m', order_date)

ORDER BY
    month;
"""


# Run SQL query
conn = sqlite3.connect(DB_PATH)

monthly_revenue = conn.execute(
    monthly_revenue_query
).fetchall()

conn.close()


# ============================================================
# DISPLAY MONTHLY REVENUE
# ============================================================

st.divider()

st.subheader("📈 Monthly Revenue Trend")


# Convert SQL result into a DataFrame

monthly_revenue_df = pd.DataFrame(
    monthly_revenue,
    columns=["month", "revenue"]
)


# Display chart

st.line_chart(
    monthly_revenue_df.set_index("month")
)
category_revenue_query = """
SELECT
    CASE
        WHEN LOWER(TRIM(p.category)) = 'electronics'
            THEN 'Electronics'
        WHEN LOWER(TRIM(p.category)) = 'fashion'
            THEN 'Fashion'
        WHEN LOWER(TRIM(p.category)) = 'beauty'
            THEN 'Beauty'
        WHEN LOWER(TRIM(p.category)) = 'home & kitchen'
            THEN 'Home & Kitchen'
        WHEN LOWER(TRIM(p.category)) = 'baby & kids'
            THEN 'Baby & Kids'
        WHEN LOWER(TRIM(p.category)) = 'sports & fitness'
            THEN 'Sports & Fitness'
        WHEN LOWER(TRIM(p.category)) = 'groceries'
            THEN 'Groceries'
        WHEN LOWER(TRIM(p.category)) = 'books & stationery'
            THEN 'Books & Stationery'
        ELSE TRIM(p.category)
    END AS category,

    SUM(
        o.quantity * o.unit_price *
        (1 - COALESCE(o.discount, 0))
    ) AS revenue,

    SUM(o.quantity) AS quantity,

    COUNT(DISTINCT o.order_id) AS orders

FROM orders o

JOIN products p
    ON o.product_id = p.product_id

WHERE o.returned IN (
    0,
    '0',
    'false',
    'False',
    'no',
    'No'
)

GROUP BY
    CASE
        WHEN LOWER(TRIM(p.category)) = 'electronics'
            THEN 'Electronics'
        WHEN LOWER(TRIM(p.category)) = 'fashion'
            THEN 'Fashion'
        WHEN LOWER(TRIM(p.category)) = 'beauty'
            THEN 'Beauty'
        WHEN LOWER(TRIM(p.category)) = 'home & kitchen'
            THEN 'Home & Kitchen'
        WHEN LOWER(TRIM(p.category)) = 'baby & kids'
            THEN 'Baby & Kids'
        WHEN LOWER(TRIM(p.category)) = 'sports & fitness'
            THEN 'Sports & Fitness'
        WHEN LOWER(TRIM(p.category)) = 'groceries'
            THEN 'Groceries'
        WHEN LOWER(TRIM(p.category)) = 'books & stationery'
            THEN 'Books & Stationery'
        ELSE TRIM(p.category)
    END

ORDER BY revenue DESC;
"""
conn = sqlite3.connect(DB_PATH)
category_revenue = conn.execute(category_revenue_query).fetchall()
conn.close()

st.divider()
st.subheader("📊 Revenue by Product Category")

category_revenue_df = pd.DataFrame(
    category_revenue,
    columns=["category", "revenue", "quantity", "orders"]
)

st.bar_chart(
    category_revenue_df.set_index("category")["revenue"]
)

st.subheader("📋 Category Performance")

st.dataframe(
    category_revenue_df,
    use_container_width=True
)

# ============================================================
# RETURN RATE BY PRODUCT CATEGORY
# ============================================================

return_rate_query = """
SELECT
    CASE
        WHEN LOWER(TRIM(p.category)) = 'electronics'
            THEN 'Electronics'
        WHEN LOWER(TRIM(p.category)) = 'fashion'
            THEN 'Fashion'
        WHEN LOWER(TRIM(p.category)) = 'beauty'
            THEN 'Beauty'
        WHEN LOWER(TRIM(p.category)) = 'home & kitchen'
            THEN 'Home & Kitchen'
        WHEN LOWER(TRIM(p.category)) = 'baby & kids'
            THEN 'Baby & Kids'
        WHEN LOWER(TRIM(p.category)) = 'sports & fitness'
            THEN 'Sports & Fitness'
        WHEN LOWER(TRIM(p.category)) = 'groceries'
            THEN 'Groceries'
        WHEN LOWER(TRIM(p.category)) = 'books & stationery'
            THEN 'Books & Stationery'
        ELSE TRIM(p.category)
    END AS category,

    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN o.returned IN (
                1,
                '1',
                'true',
                'True',
                'yes',
                'Yes'
            )
            THEN 1
            ELSE 0
        END
    ) AS returned_orders,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN o.returned IN (
                    1,
                    '1',
                    'true',
                    'True',
                    'yes',
                    'Yes'
                )
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS return_rate

FROM orders o

JOIN products p
    ON o.product_id = p.product_id

GROUP BY
    CASE
        WHEN LOWER(TRIM(p.category)) = 'electronics'
            THEN 'Electronics'
        WHEN LOWER(TRIM(p.category)) = 'fashion'
            THEN 'Fashion'
        WHEN LOWER(TRIM(p.category)) = 'beauty'
            THEN 'Beauty'
        WHEN LOWER(TRIM(p.category)) = 'home & kitchen'
            THEN 'Home & Kitchen'
        WHEN LOWER(TRIM(p.category)) = 'baby & kids'
            THEN 'Baby & Kids'
        WHEN LOWER(TRIM(p.category)) = 'sports & fitness'
            THEN 'Sports & Fitness'
        WHEN LOWER(TRIM(p.category)) = 'groceries'
            THEN 'Groceries'
        WHEN LOWER(TRIM(p.category)) = 'books & stationery'
            THEN 'Books & Stationery'
        ELSE TRIM(p.category)
    END

ORDER BY return_rate DESC;
"""

conn = sqlite3.connect(DB_PATH)
return_rate = conn.execute(return_rate_query).fetchall()
conn.close()

st.divider()
st.subheader("🔄 Return Rate by Product Category")

return_rate_df = pd.DataFrame(
    return_rate,
    columns=[
        "category",
        "total_orders",
        "returned_orders",
        "return_rate"
    ]
)

st.bar_chart(
    return_rate_df.set_index("category")["return_rate"]
)

st.subheader("📋 Return Rate Performance")

st.dataframe(
    return_rate_df,
    use_container_width=True
)
# ============================================================
# TOP 5 PRODUCTS BY NET REVENUE
# ============================================================

top_products_query = """
SELECT
    p.product_id,
    TRIM(p.product_name) AS product_name,

    SUM(
        o.quantity * o.unit_price *
        (1 - COALESCE(o.discount, 0))
    ) AS net_revenue,

    SUM(o.quantity) AS quantity_sold,

    COUNT(DISTINCT o.order_id) AS orders

FROM orders o

JOIN products p
    ON o.product_id = p.product_id

WHERE o.returned IN (
    0,
    '0',
    'false',
    'False',
    'no',
    'No'
)

GROUP BY
    p.product_id,
    TRIM(p.product_name)

ORDER BY
    net_revenue DESC

LIMIT 5;
"""

conn = sqlite3.connect(DB_PATH)
top_products = conn.execute(top_products_query).fetchall()
conn.close()

st.divider()
st.subheader("🏆 Top 5 Products by Net Revenue")

top_products_df = pd.DataFrame(
    top_products,
    columns=[
        "product_id",
        "product_name",
        "net_revenue",
        "quantity_sold",
        "orders"
    ]
)

st.bar_chart(
    top_products_df.set_index("product_name")["net_revenue"]
)

st.dataframe(
    top_products_df,
    use_container_width=True
)
# ============================================================
# TOP 10 CUSTOMERS BY TOTAL SPENDING
# ============================================================

top_customers_query = """
SELECT
    c.customer_id,
    TRIM(c.customer_name) AS customer_name,
    TRIM(c.city) AS city,

    COUNT(DISTINCT o.order_id) AS orders,

    SUM(
        o.quantity * o.unit_price *
        (1 - COALESCE(o.discount, 0))
    ) AS total_spending

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

WHERE o.returned IN (
    0,
    '0',
    'false',
    'False',
    'no',
    'No'
)

GROUP BY
    c.customer_id,
    TRIM(c.customer_name),
    TRIM(c.city)

ORDER BY
    total_spending DESC

LIMIT 10;
"""

conn = sqlite3.connect(DB_PATH)
top_customers = conn.execute(top_customers_query).fetchall()
conn.close()

st.divider()
st.subheader("👑 Top 10 Customers by Total Spending")

top_customers_df = pd.DataFrame(
    top_customers,
    columns=[
        "customer_id",
        "customer_name",
        "city",
        "orders",
        "total_spending"
    ]
)

st.bar_chart(
    top_customers_df.set_index("customer_name")["total_spending"]
)

st.dataframe(
    top_customers_df,
    use_container_width=True
)
# ============================================================
# CHURN PREDICTION
# ============================================================

import os
import joblib
import pandas as pd
import sqlite3
from pathlib import Path

st.header("🔮 Customer Churn Prediction")

st.write(
    "Enter customer information below to predict the probability "
    "that the customer will churn."
)

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "churn_model.pkl"

DB_PATH = BASE_DIR / "ecommerce_hackathon.db"


# ------------------------------------------------------------
# Load Churn Model
# ------------------------------------------------------------

@st.cache_resource
def load_churn_model():
    return joblib.load(MODEL_PATH)


# ------------------------------------------------------------
# Check Model
# ------------------------------------------------------------

if not MODEL_PATH.exists():

    st.error(
        f"Churn model not found.\n\n"
        f"Expected location:\n{MODEL_PATH}"
    )

else:

    churn_model = load_churn_model()

    # --------------------------------------------------------
    # Get Membership Types from Database
    # --------------------------------------------------------

    conn_churn = sqlite3.connect(DB_PATH)

    membership_query = """
        SELECT DISTINCT membership_type
        FROM customers
        WHERE membership_type IS NOT NULL
        ORDER BY membership_type
    """

    membership_df = pd.read_sql_query(
        membership_query,
        conn_churn
    )

    conn_churn.close()

    membership_types = membership_df["membership_type"].tolist()

    if len(membership_types) == 0:
        membership_types = ["Standard"]


    # --------------------------------------------------------
    # Input Fields
    # --------------------------------------------------------

    st.subheader("Customer Information")

    col1, col2 = st.columns(2)

    with col1:

        total_orders = st.number_input(
            "Total Orders",
            min_value=0,
            value=5,
            step=1
        )

        total_spending = st.number_input(
            "Total Spending",
            min_value=0.0,
            value=50000.0,
            step=1000.0
        )

        average_order_value = st.number_input(
            "Average Order Value",
            min_value=0.0,
            value=10000.0,
            step=500.0
        )

        days_since_last_order = st.number_input(
            "Days Since Last Order",
            min_value=0,
            value=30,
            step=1
        )

    with col2:

        return_rate = st.number_input(
            "Return Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.05,
            step=0.01
        )

        average_delivery_days = st.number_input(
            "Average Delivery Days",
            min_value=0.0,
            value=5.0,
            step=0.5
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1
        )

        membership_type = st.selectbox(
            "Membership Type",
            membership_types
        )


    # --------------------------------------------------------
    # Create Input DataFrame
    # --------------------------------------------------------

    input_data = pd.DataFrame({

        "total_orders": [total_orders],

        "total_spending": [total_spending],

        "average_order_value": [average_order_value],

        "days_since_last_order": [days_since_last_order],

        "return_rate": [return_rate],

        "average_delivery_days": [average_delivery_days],

        "age": [age],

        "membership_type": [membership_type]

    })


    # --------------------------------------------------------
    # Prediction Button
    # --------------------------------------------------------

    if st.button(
        "🔮 Predict Customer Churn",
        type="primary"
    ):

        prediction = churn_model.predict(input_data)[0]

        # Get probability of churn = class 1
        if hasattr(churn_model, "predict_proba"):

            probabilities = churn_model.predict_proba(
                input_data
            )[0]

            classes = list(churn_model.classes_)

            churn_index = classes.index(1)

            churn_probability = probabilities[churn_index]

        else:

            churn_probability = None


        # ----------------------------------------------------
        # Display Prediction
        # ----------------------------------------------------

        st.subheader("Prediction Result")

        if prediction == 1:

            st.error("⚠️ High Churn Risk")

            st.write(
                "The model predicts that this customer is likely "
                "to churn."
            )

        else:

            st.success("✅ Low Churn Risk")

            st.write(
                "The model predicts that this customer is likely "
                "to remain active."
            )


        # ----------------------------------------------------
        # Display Probability
        # ----------------------------------------------------

        if churn_probability is not None:

            st.metric(
                "Churn Probability",
                f"{churn_probability:.2%}"
            )

            st.progress(
                float(churn_probability)
            )


        # ----------------------------------------------------
        # Show Input Data
        # ----------------------------------------------------

        with st.expander("View Customer Input"):

            st.dataframe(
                input_data,
                use_container_width=True
            )
            # ============================================================
# SENTIMENT ANALYSIS
# ============================================================

st.header("💬 Customer Review Sentiment Analysis")

st.write(
    "Enter a customer review below to predict its sentiment."
)

# ------------------------------------------------------------
# Sentiment Model Path
# ------------------------------------------------------------

SENTIMENT_MODEL_PATH = BASE_DIR / "models" / "sentiment_model.pkl"


# ------------------------------------------------------------
# Load Sentiment Model
# ------------------------------------------------------------

@st.cache_resource
def load_sentiment_model():
    return joblib.load(SENTIMENT_MODEL_PATH)


# ------------------------------------------------------------
# Check Sentiment Model
# ------------------------------------------------------------

if not SENTIMENT_MODEL_PATH.exists():

    st.error(
        f"Sentiment model not found.\n\n"
        f"Expected location:\n{SENTIMENT_MODEL_PATH}"
    )

else:

    sentiment_model = load_sentiment_model()

    # --------------------------------------------------------
    # Review Text Box
    # --------------------------------------------------------

    review_text = st.text_area(
        "Customer Review",
        placeholder="Example: The product quality was excellent and delivery was very fast.",
        height=150
    )

    # --------------------------------------------------------
    # Prediction Button
    # --------------------------------------------------------

    if st.button(
        "💬 Analyze Sentiment",
        type="primary"
    ):

        if not review_text.strip():

            st.warning(
                "Please enter a customer review first."
            )

        else:

            # Predict sentiment
            sentiment_prediction = sentiment_model.predict(
                [review_text]
            )[0]

            # ------------------------------------------------
            # Display Result
            # ------------------------------------------------

            st.subheader("Sentiment Result")

            if str(sentiment_prediction).lower() == "positive":

                st.success(
                    f"😊 Positive Sentiment: {sentiment_prediction}"
                )

            elif str(sentiment_prediction).lower() == "negative":

                st.error(
                    f"😞 Negative Sentiment: {sentiment_prediction}"
                )

            else:

                st.info(
                    f"😐 Neutral Sentiment: {sentiment_prediction}"
                )

            # ------------------------------------------------
            # Show Review
            # ------------------------------------------------

            with st.expander("View Submitted Review"):

                st.write(review_text)