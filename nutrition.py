LBS_TO_KG = 0.453592
INCH_TO_CM = 2.54


def lbs_to_kg(weight_lbs: float) -> float:
    """Convert weight from pounds to kilograms."""
    return weight_lbs * LBS_TO_KG


def feet_inches_to_cm(feet: int, inches: int) -> float:
    """Convert height from feet/inches to centimeters."""
    total_inches = (feet * 12) + inches
    return total_inches * INCH_TO_CM

def calculate_nutrition_targets(user_input):
    weight_lbs = user_input["weight_lbs"]
    age = user_input["age"]
    sex = user_input["sex"]
    activity = user_input["activity_level"]
    goal = user_input["goal"]

    weight_kg = lbs_to_kg(weight_lbs)
    height_cm = feet_inches_to_cm(
        user_input["height_feet"],
        user_input["height_inches"]
    )

    if sex.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    activity_levels = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9,
    }

    tdee = bmr * activity_levels[activity]

    if goal.lower() == "fat loss":
        calorie_goal = tdee * 0.80
    elif goal.lower() == "muscle gain":
        calorie_goal = tdee * 1.10
    else:
        calorie_goal = tdee

    protein_goal = weight_lbs

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "calorie_goal": round(calorie_goal),
        "protein_goal": round(protein_goal),
    }