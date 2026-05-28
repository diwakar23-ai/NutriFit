import pandas as pd
from sklearn.neighbors import NearestNeighbors
import re

# Load the food dataset
food_df = pd.read_csv('foodset.csv')


ALLERGY_SYNONYMS = {
    'dairy': ['milk', 'cheese', 'cream', 'butter', 'yogurt', 'curd', 'paneer', 'ghee'],
    'nuts': ['almond', 'cashew', 'peanut', 'hazelnut', 'walnut'],
    'gluten': ['wheat', 'barley', 'rye', 'maida', 'semolina', 'starch'],
    'seafood': ['fish', 'prawn', 'shrimp', 'oyster']
}

def calculate_bmi(weight_kg, height_cm):
    if weight_kg <= 0 or height_cm <= 0:
        return None
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def filter_allergies(allergy_list, df):
    allergy_free = df.copy()
    if 'Ingredients' in df.columns:
        ingredients_col = df['Ingredients'].str.lower().fillna("")
        for allergy in allergy_list:
            allergy = allergy.strip().lower()
            keywords = ALLERGY_SYNONYMS.get(allergy, [allergy])
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                allergy_free = allergy_free[~ingredients_col.str.contains(pattern, regex=True)]
    return allergy_free

def filter_preference(preference, df):

    if preference == "Veg":
        return df[df["Category"]=="Veg"]

    elif preference == "Non Veg":
        return df[df["Category"]=="Non Veg"]

    return df

def recommend_food(user_goal, df, top_n=5):
    df = df.dropna(subset=['Calories', 'Proteins', 'Fats'])

    # Apply goal-specific filters
    if user_goal == 'Weight Loss':
        df = df[(df['Calories'] <= 200) & (df['Fats'] <= 10)]
        target = [[100, 10]]
    elif user_goal == 'Muscle Gain':
        df = df[(df['Calories'] >= 400) & (df['Proteins'] >= 20)]
        target = [[500, 30]]
    else:  # Balanced Diet
        df = df[(df['Calories'] >= 250) & (df['Calories'] <= 500) &
                (df['Proteins'] >= 10) & (df['Fats'] <= 20)]
        target = [[350, 15]]

    if df.empty:
        return pd.DataFrame()

    # Nearest Neighbor recommendation
    features = df[['Calories', 'Proteins']]
    model = NearestNeighbors(n_neighbors=min(top_n, len(features)))
    model.fit(features)

    distances, indices = model.kneighbors(target)
    result =  df.iloc[indices[0]].reset_index(drop=True)
    result.index = result.index+1
    return result