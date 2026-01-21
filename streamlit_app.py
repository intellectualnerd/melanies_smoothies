# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# App title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie")

# Input
name_on_order = st.text_input("Name On Smoothie:")

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit list from Snowflake → convert to Pandas → list
df = (
    session
    .table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
    .to_pandas()
)

fruit_list = df["FRUIT_NAME"].tolist()

# Multiselect expects a list
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Create ingredients string safely
ingredients_string = " ".join(ingredients_list)

# Submit button
time_to_submit = st.button("Submit Order")

if time_to_submit:
    if not name_on_order or not ingredients_list:
        st.warning("Please enter your name and select at least one ingredient")
    else:
        session.sql(
            """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (ingredients, name_on_order)
            VALUES (?, ?)
            """,
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success("Your Smoothie is Ordered ✅")

# External API call (display correctly)
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

if smoothiefroot_response.status_code == 200:
    st.json(smoothiefroot_response.json())
else:
    st.error("Failed to fetch SmoothieFroot data")
