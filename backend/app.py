import os
import random
import warnings
# Suppress deprecation warnings from legacy packages
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (like local GEMINI_API_KEY)
load_dotenv()

# Configure template and static folders relative to the frontend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))

app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND_DIR, 'static'),
    template_folder=os.path.join(FRONTEND_DIR, 'templates')
)

# Load the food dataset from the local backend directory
DATASET_PATH = os.path.join(BASE_DIR, 'food_dataset.csv')

def load_food_data():
    try:
        return pd.read_csv(DATASET_PATH)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return pd.DataFrame()

# Calculation Functions
def calculate_bmi(weight, height_cm):
    """Calculate Body Mass Index (BMI)."""
    height_m = height_cm / 100.0
    bmi = weight / (height_m ** 2)
    
    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi < 24.9:
        status = "Normal weight"
    elif 25.0 <= bmi < 29.9:
        status = "Overweight"
    else:
        status = "Obese"
        
    return round(bmi, 1), status

def calculate_calories(weight, height, age, gender, activity_level, goal):
    """
    Calculate BMR using Mifflin-St Jeor equation, scale by TDEE activity factor,
    and adjust for weight goal.
    """
    # BMR calculation
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
    # Activity multiplier
    multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'extra': 1.9
    }
    tdee = bmr * multipliers.get(activity_level.lower(), 1.2)
    
    # Goal adjustment
    if goal.lower() == 'loss':
        target_calories = tdee - 500
    elif goal.lower() == 'gain':
        target_calories = tdee + 500
    else:
        target_calories = tdee
        
    # Keep target calories realistic (minimum 1200 kcal for safety)
    return max(int(target_calories), 1200)

def calculate_macros(calories, goal):
    """
    Determine target macros based on weight goal.
    Returns protein, carbs, fat in grams.
    """
    # Nutrient calories: Protein (4 kcal/g), Carbs (4 kcal/g), Fat (9 kcal/g)
    if goal.lower() == 'loss':
        p_pct, c_pct, f_pct = 0.35, 0.35, 0.30  # High protein for muscle retention
    elif goal.lower() == 'gain':
        p_pct, c_pct, f_pct = 0.25, 0.50, 0.25  # High carbs for fuel and growth
    else:
        p_pct, c_pct, f_pct = 0.30, 0.40, 0.30  # Balanced split
        
    protein_g = (calories * p_pct) / 4
    carbs_g = (calories * c_pct) / 4
    fat_g = (calories * f_pct) / 9
    
    return {
        'protein': round(protein_g, 1),
        'carbs': round(carbs_g, 1),
        'fat': round(fat_g, 1)
    }

def recommend_meals(df, diet_pref, target_calories):
    """
    Filter foods by dietary preference, sample separate combinations for 7 days
    (Monday to Sunday) and scale portions using NumPy to meet target calories.
    """
    if df.empty:
        return {}
        
    # Filter by dietary preference
    if diet_pref.lower() == 'vegan':
        filtered_df = df[df['diet_type'].str.lower() == 'vegan']
    elif diet_pref.lower() == 'vegetarian':
        filtered_df = df[df['diet_type'].str.lower().isin(['vegan', 'vegetarian'])]
    else:
        filtered_df = df  # Non-Vegetarian includes everything
        
    # Meal categories and calorie splits
    meal_splits = {
        'Breakfast': 0.25,
        'Lunch': 0.35,
        'Snack': 0.10,
        'Dinner': 0.30
    }
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_plan = {}
    
    for day in days:
        weekly_plan[day] = {}
        for category, split in meal_splits.items():
            cat_df = filtered_df[filtered_df['category'].str.lower() == category.lower()]
            
            if cat_df.empty:
                cat_df = filtered_df
                
            # Select one random food item from this category using pandas sample
            selected_food = cat_df.sample(n=1).iloc[0]
            
            meal_calorie_target = target_calories * split
            food_calories_per_100g = selected_food['calories']
            
            # Calculate portion weight in grams using NumPy for scaling calculation
            portion_g = np.round((meal_calorie_target / food_calories_per_100g) * 100, 0)
            
            # Scale nutrition metrics
            scaled_calories = int(np.round((food_calories_per_100g * portion_g) / 100, 0))
            scaled_protein = np.round((selected_food['protein'] * portion_g) / 100, 1)
            scaled_carbs = np.round((selected_food['carbs'] * portion_g) / 100, 1)
            scaled_fat = np.round((selected_food['fat'] * portion_g) / 100, 1)
            
            weekly_plan[day][category.lower()] = {
                'name': selected_food['name'],
                'portion_g': int(portion_g),
                'calories': scaled_calories,
                'protein': float(scaled_protein),
                'carbs': float(scaled_carbs),
                'fat': float(scaled_fat)
            }
            
    return weekly_plan

def get_ai_coaching(age, gender, height, weight, activity, goal, diet_pref, calories, macros, weekly_plan, api_key):
    """Call the Gemini API to get weekly recipe instructions and coaching tips."""
    if not api_key:
        return None
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Format weekly details for prompt
        weekly_text = ""
        for day, meals in weekly_plan.items():
            weekly_text += f"\n### {day}\n"
            for cat, details in meals.items():
                weekly_text += f"- {cat.capitalize()}: {details['name']} ({details['portion_g']}g) - {details['calories']} kcal (P: {details['protein']}g, C: {details['carbs']}g, F: {details['fat']}g)\n"
            
        prompt = f"""
        You are a highly experienced nutritionist and chef. Based on the user's details and the generated 7-day weekly meal plan below, generate a personalized response.

        User Profile:
        - Age: {age}
        - Gender: {gender}
        - Height: {height} cm
        - Weight: {weight} kg
        - Activity Level: {activity}
        - Goal: {goal}
        - Dietary Preference: {diet_pref}
        - Target Daily Intake: {calories} kcal (Protein: {macros['protein']}g, Carbs: {macros['carbs']}g, Fat: {macros['fat']}g)

        System Suggested Weekly Meal Plan:
        {weekly_text}

        Please provide the following four sections in your response, formatted in clean Markdown with icons:
        1. **Weekly Nutrition Assessment**: A brief professional assessment of the weekly plan for the user's fitness goals.
        2. **Weekly Prep Strategy**: Concise, easy meal prep strategies to cook and prepare these meals for the week.
        3. **Healthy Ingredient Substitutions**: 2-3 general ingredient swaps for convenience or variety.
        4. **Structured Weekly Shopping List**: A comprehensive grocery checklist categorized by section (Produce, Protein/Dairy, Grains, Snacks/Nuts, etc.) needed to execute this 7-day plan.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"*(Optional AI Coaching unavailable: {str(e)})*"

# Flask Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/plan', methods=['POST'])
def generate_plan():
    data = request.get_json() or {}
    
    # Input validation and defaults
    try:
        age = int(data.get('age', 25))
        gender = str(data.get('gender', 'male'))
        height = float(data.get('height', 170))
        weight = float(data.get('weight', 70))
        activity = str(data.get('activity', 'moderate'))
        goal = str(data.get('goal', 'maintenance'))
        diet_pref = str(data.get('diet_pref', 'vegetarian'))
    except (ValueError, TypeError) as e:
        return jsonify({'status': 'error', 'message': f'Invalid input values: {str(e)}'}), 400
        
    # Calculations
    bmi, bmi_status = calculate_bmi(weight, height)
    target_calories = calculate_calories(weight, height, age, gender, activity, goal)
    macro_targets = calculate_macros(target_calories, goal)
    
    # Meal Recommendations for the entire week using Pandas and NumPy
    df = load_food_data()
    weekly_plan = recommend_meals(df, diet_pref, target_calories)
    
    # Calculate daily actual totals from recommendations
    weekly_actual_totals = {}
    for day, day_meals in weekly_plan.items():
        actual_calories = sum(meal['calories'] for meal in day_meals.values())
        actual_protein = sum(meal['protein'] for meal in day_meals.values())
        actual_carbs = sum(meal['carbs'] for meal in day_meals.values())
        actual_fat = sum(meal['fat'] for meal in day_meals.values())
        
        weekly_actual_totals[day] = {
            'calories': actual_calories,
            'protein': round(actual_protein, 1),
            'carbs': round(actual_carbs, 1),
            'fat': round(actual_fat, 1)
        }
    
    # Gemini AI integration (optional, loads from local environment variable)
    env_key = os.getenv('GEMINI_API_KEY', '')
    
    ai_coaching = None
    if env_key:
        ai_coaching = get_ai_coaching(
            age, gender, height, weight, activity, goal, diet_pref,
            target_calories, macro_targets, weekly_plan, env_key
        )
        
    return jsonify({
        'status': 'success',
        'bmi': bmi,
        'bmi_status': bmi_status,
        'target_calories': target_calories,
        'macro_targets': macro_targets,
        'weekly_plan': weekly_plan,
        'weekly_actual_totals': weekly_actual_totals,
        'ai_coaching': ai_coaching
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
