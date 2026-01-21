# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# App title
st.title("🥤 Customize Your Smoothie! 🥤")

# App description
st.write("Choose the fruits you want in your custom smoothie")

# User input
name_on_order = st.text_input("Name On Smoothie :")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options
my_dataframe = (
    session
    .table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"), col("SEARCH_ON"))
)
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


# Multiselect for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients :",
    my_dataframe,
    max_selections=5
)

# Show selected ingredients
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

# Build ingredients string
ingredients_string = ""
for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + " "

    search_on=pd_df.loc[pd_df['FRUIT_NAME']==fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen, 'is', search_on, '.')
    
    st.subheader(fruit_chosen + ' Nutrition Information')
    #fruityvice_response= requests.get("https://fruityvice.com/api/fruit/"+ fruit_chosen)
    smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}" )
    sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# Insert statement
my_insert_stmt = f"""
INSERT INTO smoothies.public.orders (ingredients, name_on_order)
VALUES ('{ingredients_string}', '{name_on_order}')
"""

# Submit button
time_to_submit = st.button("Submit Order")

if time_to_submit:
    session.sql(my_insert_stmt).collect()
    st.success("Your Smoothie is Ordered", icon="✅")

# External API call
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

st.text(smoothiefroot_response)
