import pandas as pd
import re 

nutrition_data = pd.read_csv('backend/services/data/new_data/NEW_nutrition.csv')  


def get_info(ingredient: str):
    clean_name = str(ingredient).strip("[]'\" ").split(',')[0].strip()
    clean_name = re.sub(r"[\[\]'\"]", "", clean_name).strip()

    if not clean_name:
        return None
    mask = nutrition_data['food'].str.contains(clean_name, case=False, na=False, regex=False)
    result = nutrition_data[mask]
    if result.empty:
        return None
    
    return result.iloc[0].to_dict() 

def get_protein_heavy_ingredients(min_protein: float = 20.):
    high_protein_ingredients = nutrition_data[nutrition_data['Protein'] >= min_protein]
    return high_protein_ingredients[['food', 'Protein', 'Caloric Value', 'Carbohydrates', 'Fat']].to_dict(orient='records')

def get_fiber_rich_ingredients(dietary_fiber: float = 5.0):
    fiber_rich_ingredients = nutrition_data[nutrition_data['Dietary Fiber'] >= dietary_fiber]
    return fiber_rich_ingredients[['food', 'Dietary Fiber', 'Caloric Value', 'Protein', 'Carbohydrates', 'Fat']].to_dict(orient='records')

def get_low_sodium(max_sodium: float = 0.5):
    low_sodium_ingredients = nutrition_data[nutrition_data['Sodium'] <= max_sodium]
    return low_sodium_ingredients[['food', 'Sodium', 'Caloric Value', 'Protein', 'Fat']].to_dict(orient='records')

def get_foods_by_calories(min_cal: int=0, max_cal: int=900):
    result = nutrition_data[(nutrition_data['Caloric Value'] >= min_cal) & (nutrition_data['Caloric Value'] <= max_cal)]
    return result[['food', 'Caloric Value', 'Protein', 'Carbohydrates', 'Fat']].to_dict(orient='records')

def get_ingredients_restrictions(restriction: str):
    """
    Get ingredients based on dietary restrictions.
    restriction: 'high_protein', 'high_fiber', 'low_sodium', 'low_calorie'
    """
    if restriction == 'high_protein':
        return get_protein_heavy_ingredients(20.0)
    elif restriction == 'high_fiber':
        return get_fiber_rich_ingredients(5.0)
    elif restriction == 'low_sodium':
        return get_low_sodium(0.5)
    elif restriction == 'low_calorie':
        return get_foods_by_calories(0, 200)
    else:
        return f"Unknown restriction: {restriction}"


def calculate_total_nutrition(recipe_ingredients: list, portions: dict = None):
    total_nutrition = {
        "Caloric Value": 0,
        "Protein": 0,   
        "Fat": 0,   
        "Carbohydrates": 0,
        "Sodium": 0 , 
        "Dietary Fiber": 0
    }

    for ingredient in recipe_ingredients:
        # Handle if ingredient is passed as a list or has brackets
        if isinstance(ingredient, list):
            ingredient = ingredient[0] if ingredient else ""
        # Remove brackets and quotes from string representation
            ingredient = re.sub(r"[\[\]'\"]", "", str(ingredient))
            ingredient = ingredient.split(',')[0].strip()

        
        if not ingredient:
            continue
            
        nutrition = get_info(ingredient)
        if nutrition:
            grams = portions.get(ingredient, 100) if portions else 100
            multiplier = grams /100 
            for key in total_nutrition.keys():
                total_nutrition[key] += nutrition.get(key, 0) * multiplier

    return {k: round(v, 2) for k, v in total_nutrition.items()}

def get_food_by_nutrient(nutrient: str, min_value: float = 0, max_value:float = 0): 
    if nutrient not in nutrition_data.columns:
        return f"Nutrient '{nutrient}' not found. Available nutrients: {list(nutrition_data.columns)}"
    result = nutrition_data[(nutrition_data[nutrient] >= min_value) & (nutrition_data[nutrient] <= max_value)]
    return result[['food', nutrient, 'Caloric Value', 'Protein', 'Carbohydrates', 'Fat']].to_dict(orient='records')
