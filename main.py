from utils import print_header, extract_json, print_meal_plan, print_nutrition_summary
from agents import orchestrator_agent
from nutrition import calculate_nutrition_targets


def main():
    user_input = {
        "weight_lbs": 153,
        "height_feet": 5,
        "height_inches": 7,
        "age": 20,
        "sex": "female",
        "activity_level": "moderate",
        "ingredients": "chicken, eggs, rice, broccoli",
        "goal": "fat loss",
    }

    print_header()

    targets = calculate_nutrition_targets(user_input)

    print_nutrition_summary(targets)

    prompt = f"""
Generate a personalized daily meal plan.

Nutrition Targets:
- Calories: {round(targets["calorie_goal"])}
- Protein: {round(targets["protein_goal"])}g

Available Ingredients:
{user_input["ingredients"]}

Goal:
{user_input["goal"]}

Coordinate the available tools to produce a validated meal plan.
Return only the final meal plan.
"""
    response = orchestrator_agent(prompt)

    final_plan = response.message["content"][0]["text"]

    meal_plan = extract_json(final_plan)

    print_meal_plan(meal_plan)

if __name__ == "__main__":
    main()