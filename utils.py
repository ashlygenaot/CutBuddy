import json
import re

def extract_json(text):
    """Extract a JSON object or array from an LLM response."""

    text = text.strip()

    # Remove Markdown code fences if present
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)

    if match:
        return json.loads(match.group(1))

    raise ValueError("No valid JSON found.")

def print_header():
    print("""
==================================================
                  CUTBUDDY AI 
        MULTI-AGENT NUTRITION ASSISTANT
==================================================

    Powered by Strands Multi-Agent Workflow
    """)
def print_nutrition_summary(targets):
    print("""
==================================================
                NUTRITION PROFILE
==================================================
""")

    print(f"""
BMR: {targets['bmr']} kcal/day
TDEE: {targets['tdee']} kcal/day

Daily Target:
Calories: {targets['calorie_goal']} kcal
Protein: {targets['protein_goal']}g
""")
    
def print_meal_plan(meal_plan):

    print("""
==================================================
                 DAILY MEAL PLAN
==================================================
""")

    for meal in meal_plan.get("meals", []):

        print(f"""
{meal.get("meal_type", "MEAL").upper()}
--------------------------------------------------
{meal.get("name", "Unnamed Meal")}

Calories: {meal.get("calories", 0)} kcal
Protein: {meal.get("protein_g", 0)} g
Carbs: {meal.get("carbs_g", 0)} g
Fat: {meal.get("fat_g", 0)} g

Ingredients:
""")

        for ingredient in meal.get("ingredients", []):
            print(f"  • {ingredient}")

    totals = meal_plan.get("daily_total", {})

    print("""
==================================================
                  DAILY TOTALS
==================================================
""")

    print(f"""
Calories: {totals.get("calories", 0)} kcal
Protein: {totals.get("protein_g", 0)} g
Carbs: {totals.get("carbs_g", 0)} g
Fat: {totals.get("fat_g", 0)} g
""")

    print("""
==================================================
""")
    print("✓ Meal plan created successfully")