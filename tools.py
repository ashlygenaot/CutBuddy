import json
from strands import tool
from recipes import collect_recipe_results
from utils import extract_json
from models import recipe_agent, optimizer_agent
from validators import validate_meal_plan

@tool
def recipe_finder_tool(
    calorie_target: int,
    protein_target: int,
    ingredients: str,
):
    
    """
    Finds high-protein recipes and generates meal options
    based on user nutrition targets.
    """

    search_results = recipe_search_tool(
        calorie_target=calorie_target,
        ingredients=ingredients,
    )

    prompt = f"""
You are a recipe extraction agent.

Your job:
Create realistic recipe options that a meal optimization agent can use to build a daily meal plan.

User nutrition targets:
Calories: {calorie_target} kcal
Protein: {protein_target} g

Available ingredients:
{ingredients}

Search results:
{json.dumps(search_results, indent=2)}

Recipe Requirements:

Generate realistic high-protein meal options.

Return:
- At least 2 breakfast options
- At least 3 lunch options
- At least 3 dinner options
- At least 2 snack options

Nutrition Guidelines:
- Estimate realistic calories and macros.
- Avoid extreme protein amounts.
- Do not create meals with unrealistic serving sizes.
- Include balanced combinations of protein, carbohydrates, and fats.
- Meals should be practical for everyday eating.

Ingredient Guidelines:
- Prioritize the provided ingredients.
- Use common supporting ingredients when needed.
- Do not replace the user's ingredients unnecessarily.
- Do not create recipes unrelated to the available ingredients.

Search Result Guidelines:
- Use search results only as inspiration.
- Do not copy recipes blindly.
- Extract useful meal ideas.

Output Rules:
- Return ONLY valid JSON.
- Do not include explanations.
- Do not include markdown.
- Do not include commentary.

Format:

[
    {{
        "name": "",
        "meal_type": "",
        "calories": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 0,
        "ingredients": []
    }}
]
"""

    response = recipe_agent(prompt)

    response_text = response.message["content"][0]["text"]

    return extract_json(response_text)

@tool
def recipe_search_tool(
    calorie_target: int,
    ingredients: str
):

    """
    Searches the web for high-protein recipes.
    """

    results =[]
    
    results = collect_recipe_results(
        calorie_target=calorie_target,
        ingredients=ingredients
    )


    return results

@tool
def meal_optimizer_tool(recipes, calorie_target, protein_target, feedback=""):
    
    """
    Generate a meal plan from available recipes.
    """

    feedback_section = ""

    if feedback:
        feedback_section = f"""
Previous validation feedback:
{feedback}

Revise the meal plan to satisfy this feedback.
"""

    optimizer_prompt = f"""
You are a nutrition optimization agent.

Your task:
Generate a single validated daily meal plan that satisfies the user's nutrition targets.

User nutrition targets:
Calories: {calorie_target} kcal
Protein: {protein_target} g

Available recipes:
{json.dumps(recipes, indent=2)}

{feedback_section}

CRITICAL OUTPUT RULE:

Your response is parsed automatically by Python.

You MUST NOT output:
- explanations
- calculations
- analysis
- thoughts
- progress updates
- selection reasoning
- validation comments

Your entire response MUST be a single JSON object.

MEAL STRUCTURE RULES:
- Select exactly ONE breakfast.
- Select exactly ONE lunch.
- Select exactly ONE dinner.
- Select ZERO or ONE snack only if required to reach nutrition targets.
- Never create duplicate meal types.
- Never remove required meals during revisions.
- Meals should represent realistic daily eating patterns.
- If the plan is within 10% of calories and within 15% of protein, return the plan without modifications. Do not optimize further.

Protein optimization:
- Treat protein as a minimum requirement, not the primary optimization goal.
- Once protein reaches the target, prioritize calories using carbohydrates and fats.
- Avoid adding additional chicken, eggs, or protein-heavy ingredients after protein target is met.
- Prefer calorie increases from:
  rice, oats, pasta, potatoes, avocado, olive oil, peanut butter, nuts, dairy.


Recipe modification rules:
- Do not modify recipe nutrition values unless portion changes are explicitly stated.
- If increasing calories, update ingredients to reflect the change.
- Add modifications as separate ingredients.
- Recalculate macros after modifications.
- Never silently change calories/macros.

NUTRITION RULES:
- Final calories MUST be within +/-10% of the calorie target.
- Protein should be between 100%-115% of target.
- Avoid exceeding 120% of target.
- Avoid unnecessary protein overages.
- Prioritize calorie accuracy over maximizing protein.

CALORIE ADJUSTMENT RULES:
Before returning:
1. Calculate the total calories from all meals.
2. Compare against the calorie target.
3. If calories are too low:
   - Increase portions first.
   - Add calorie-dense foods such as:
       - extra rice
       - oats
       - olive oil
       - avocado
       - peanut butter
       - nuts
       - dairy
4. If calories are too high:
   - Reduce portions or remove calorie additions.
5. Only increase protein sources if protein is below target.

REVISION RULES:
If previous validation feedback is provided:
- Fix ONLY the issues mentioned in the feedback.
- Preserve the meal structure.
- Do not replace the entire meal plan unless necessary.
- Do not ignore validation feedback.

INGREDIENT RULES:
- Use the provided recipes as the source of meals.
- Do not recreate or rewrite the recipe database.
- Do not ask for a different input format.
- Do not invent unrealistic nutrition values.
- Do not add unrelated foods unless they are calorie adjustments.

OUTPUT RULES:
Do not show your calculations.
Do not describe your selection process.
Do not explain decisions.
Do not output reasoning.

Your entire response must be ONLY the JSON meal plan.

Schema:

{{
 "meals": [
   {{
    "name": "",
    "meal_type": "",
    "calories": 0,
    "protein_g": 0,
    "carbs_g": 0,
    "fat_g": 0,
    "ingredients": []
   }}
 ],
 "daily_total": {{
    "calories": 0,
    "protein_g": 0
 }}
}}
"""


    meal_plan_result = optimizer_agent(optimizer_prompt)

    meal_plan_text = meal_plan_result.message["content"][0]["text"]

    return extract_json(meal_plan_text)
