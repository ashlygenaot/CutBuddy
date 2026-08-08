from strands import tool
@tool
def validate_meal_plan(
    meals: list,
    calorie_target: int,
    protein_target: int
):

    total_calories = sum(
        meal["calories"]
        for meal in meals
    )

    total_protein = sum(
        meal["protein_g"]
        for meal in meals
    )


    calories_valid = (
        abs(total_calories - calorie_target)
        <= calorie_target * 0.10
    )


    protein_valid = (
        total_protein >= protein_target
    )


    meal_types = [
        meal["meal_type"].lower()
        for meal in meals
    ]


    structure_valid = (
        meal_types.count("breakfast") == 1
        and meal_types.count("lunch") == 1
        and meal_types.count("dinner") == 1
        and meal_types.count("snack") <= 1
    )

    macro_calories_valid = True

    for meal in meals:
        calculated = (
            meal["protein_g"] * 4 +
            meal["carbs_g"] * 4 +
            meal["fat_g"] * 9
        )

        if abs(calculated - meal["calories"]) > 75:
            macro_calories_valid = False


    is_valid = (
        calories_valid
        and protein_valid
        and structure_valid
        and macro_calories_valid
    )


    feedback = []


    if not calories_valid:
        difference = total_calories - calorie_target

        feedback.append(
            f"Calories are {abs(difference)} kcal "
            f"{'over' if difference > 0 else 'under'} target."
        )


    if not protein_valid:
        difference = total_protein - protein_target

        feedback.append(
            f"Protein is {abs(difference)}g below target."
        )


    if not structure_valid:
        feedback.append(
            "Meal structure invalid. Need exactly one breakfast, lunch, dinner, and optional snack."
        )


    return {
        "is_valid": is_valid,
        "feedback": " ".join(feedback),
        "daily_totals": {
            "calories": total_calories,
            "protein_g": total_protein
        },
        "meals": meals
    }