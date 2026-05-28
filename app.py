import streamlit as st
from diet_recommendor import calculate_bmi, filter_allergies,filter_preference, recommend_food, food_df

st.title("NutriFit🍽️")

# Input fields
weight = st.number_input("Enter your weight (kg):", min_value=0.0, max_value=500.0, step=0.1, format="%.1f")
height = st.number_input("Enter your height (cm):", min_value=0.0, max_value=300.0, step=0.1, format="%.1f")
goal = st.selectbox("Select your dietary goal:", ['Weight Loss', 'Muscle Gain', 'Balanced Diet'])
food_preference = st.selectbox("Select Food Preference:",["Veg","Non Veg","Both"])

# Allergen checkboxes
st.write("#### Select your food allergies:")
dairy_allergy = st.checkbox("Dairy")
nuts_allergy = st.checkbox("Nuts")
gluten_allergy = st.checkbox("Gluten")
seafood_allergy = st.checkbox("Seafood")

# Collect selected allergens
selected_allergies = []
if dairy_allergy:
    selected_allergies.append("dairy")
if nuts_allergy:
    selected_allergies.append("nuts")
if gluten_allergy:
    selected_allergies.append("gluten")
if seafood_allergy:
    selected_allergies.append("seafood")

# Button action
if st.button("Get Diet Plan"):
    if weight <= 0.0 or height <= 0.0:
        st.error("Please enter valid non-zero numeric values for weight and height.")
    else:
        bmi = calculate_bmi(weight, height)
        if bmi:
            st.success(f"📏 Your BMI is: {bmi}")
            
            safe_foods = filter_allergies(selected_allergies,food_df)

            safe_foods = filter_preference(food_preference,safe_foods)

            recommendations = recommend_food(goal,safe_foods)

            if recommendations.empty:
                st.warning("No suitable food found based on your inputs.")
            else:
                st.write("### Recommended Foods")
                st.dataframe(recommendations[['Food_items', 'Calories', 'Proteins', 'Fats']])
        else:
            st.error("BMI could not be calculated. Please check your inputs.")