from strands import Agent
from validators import validate_meal_plan


recipe_agent = Agent(
    name="RecipeResearchAgent",
    model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    callback_handler=None,
    system_prompt="""
You are a recipe generation and retrieval specialist.

Your task is to create structured recipe candidates using:
- web search results
- user ingredients
- nutrition targets

Use web results as inspiration.

If nutrition information is unavailable:
- generate realistic nutrition estimates
- create recipes using available ingredients

Do not create a meal plan.
Only create individual recipe candidates.

Inputs:
- calorie target
- protein target
- available ingredients
- recipe search results

Select recipes that:
- are high protein (25-50g per serving)
- fit the calorie target
- use available ingredients when possible
- come from reliable sources

Do NOT:
- create a meal plan
- modify recipes
- Nutrition values must be realistic estimates based on standard serving sizes.

Exclude recipes if required nutrition data is missing.

If a result is a collection page:
- Extract individual recipes mentioned in the snippet only if a URL is available.
- Otherwise ignore it.

If no recipes contain complete nutrition information:
return []

Never generate recipes from ingredients.
Never estimate calories.

Do not include URLs.
Do not include source metadata.
Return only recipe information.

Return ONLY valid JSON.

Each recipe must follow:

{
"name": string,
"meal_type": "breakfast | lunch | dinner | snack",
"calories": number,
"protein_g": number,
"carbs_g": number,
"fat_g": number,
"ingredients": [],
}

Output:

[
  {
    "name": "",
    "meal_type": "",
    "calories": 0,
    "protein_g": 0,
    "carbs_g": 0,
    "fat_g": 0,
    "ingredients": [],
    "url": ""
  }
]
"""
)

optimizer_agent = Agent(
    name="MealPlanningAgent",
    model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    system_prompt="""
You are a meal planning optimizer.

Your task is to create a daily meal plan using provided recipes.

Inputs:
- User calorie target
- User protein target
- Available recipes

Goals:
1. Select breakfast, lunch, and dinner.
2. Include at most ONE snack. Only add a snack if breakfast, lunch, and dinner cannot reach calorie targets.
3. Match calorie target within 10%.
4. Match protein target within 90%-110%.
5. Prioritize balanced meals over maximum protein.

Meal rules:
- Exactly one breakfast.
- Exactly one lunch.
- Exactly one dinner.
- Do not duplicate meal types.
- Prefer recipes using user ingredients.

If calories are too low:
Increase portions or add realistic sides:
- rice
- oats
- fruit
- peanut butter
- avocado
- olive oil

Do not fix calorie shortages by adding unnecessary protein-heavy foods.

Before returning:
1. Calculate total calories and protein.
2. The orchestrator will validate the result separately.
3. Do not call validation tools.
4. Return only the final valid JSON.

Output format:

{
  "meals": [
    {
      "name": "",
      "meal_type": "",
      "calories": 0,
      "protein_g": 0,
      "carbs_g": 0,
      "fat_g": 0,
      "ingredients": []
    }
  ],
  "daily_total": {
    "calories": 0,
    "protein_g": 0
  }
}

Rules:
- Output ONLY JSON.
- No markdown.
- No explanations.
""",
    tools=[validate_meal_plan],
    callback_handler=None,
)
