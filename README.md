# CutBuddy
---

## Introduction

CutBuddy is a multi-agent AI nutrition assistant built to generate personalized daily meal plans based on a user's nutrition targets and available ingredients. I created it to explore how multiple specialized AI agents can work together to complete a structured workflow rather than relying on a single model response.

The project uses Strands Agents and AWS Bedrock to coordinate recipe searching, meal optimization, and meal plan validation. It has given me hands-on experience working with agentic AI workflows, tool calling, prompt engineering, structured JSON outputs, web scraping, nutrition calculations, and AWS infrastructure.

---

## Demo

<img src="assets/demo.gif" width="1000">

---
## Features

- **Nutrition Calculation:**
  - Calculates Basal Metabolic Rate (BMR)
  - Calculates Total Daily Energy Expenditure (TDEE)
  - Generates a daily calorie target
  - Calculates a daily protein target
  - Supports personalized nutrition inputs

- **Recipe Search:**
  - Searches the web for recipe options
  - Filters results from trusted recipe websites
  - Searches based on user ingredients and nutrition targets
  - Extracts recipe information for use by the AI agents
  
- **Multi-Agent Workflow:**
  - Specialized recipe-finding agent
  - Meal optimization agent
  - Meal plan validation tool
  - Orchestrator agent responsible for coordinating the workflow
  - Agents communicate through structured tool calls

- **Meal Optimization:**
  - Generates breakfast, lunch, and dinner
  - Supports an optional snack
  - Optimizes meals around calorie and protein targets
  - Uses available recipes as the source of meals
  - Revises meal plans when validation requirements are not met

- **Meal Plan Validation:**
  - Verifies calories are within ±10% of the target
  - Verifies protein requirements are met
  - Ensures correct meal structure
  - Checks that meal-level macros are reasonably consistent with calories
  - Provides feedback to the optimizer when a plan fails validation

- **Structured Output:**
  - Meal plans are returned as JSON
  - Consistent meal and nutrition data structure
  - Separates application logic from terminal presentation
    
---

## Technologies Used:

### AI / Machine Learning
- Python
- Strands Agents
- AWS Bedrock
- Anthropic Claude Haiku
- Agentic workflows
- Prompt engineering
- Structured JSON outputs
  
### Backend / Data Processing
- Python
- Requests
- BeautifulSoup
- JSON
- Pydantic
  
### AWS
- Amazon Bedrock
- AWS IAM
- Bedrock model invocation
  
### Development
- Jupyter Notebook
- Virtual environments
---

## Architecture
```
CutBuddy
│
├── main.py
│   └── Application entry point
│
├── agents.py
│   └── Recipe, optimizer, and orchestrator agents
│
├── tools.py
│   └── Agent tools and workflow functions
│
├── recipes.py
│   └── Recipe searching and web scraping
│
├── nutrition.py
│   └── BMR, TDEE, and nutrition calculations
│
├── validators.py
│   └── Meal plan validation
│
├── models.py
│   └── Data models
│
├── utils.py
│   └── JSON parsing and terminal formatting
│
└── notebooks/
    └── Original development notebook
```

---
## Multi-Agent Workflow
```
                    User Profile
                         │
                         ▼
              ┌─────────────────────┐
              │ Recipe Finder Agent │
              │                     │
              │ Searches for recipe │
              │ options             │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Meal Optimizer Agent│
              │                     │
              │ Creates daily meal  │
              │ plan                │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Validation Tool     │
              │                     │
              │ Checks calories,    │
              │ protein & structure │
              └──────────┬──────────┘
                         │
                    ┌────┴────┐
                    │         │
                  Valid     Invalid
                    │         │
                    ▼         │
              Final Plan      │
                              │
                              └──────► Optimizer
                                        │
                                        ▼
                                   Revalidate
```

The orchestrator controls this workflow and prevents an invalid meal plan from being returned.

---

## Validation Workflow

Meal plans must satisfy:
- Calories within ±10% of the user's calorie target
- Protein meets the user's target
- Exactly one breakfast
- Exactly one lunch
- Exactly one dinner
- Zero or one snack

Meal calories are reasonably consistent with the listed protein, carbohydrate, and fat values

If validation fails, the validation feedback is passed back to the meal optimizer so it can revise the plan.

The orchestrator allows up to three optimization and validation attempts before returning the result.

---


## Example Output

For example, given a daily target of approximately 1,856 calories and 153g of protein, CutBuddy can generate:
```

==================================================
                 DAILY MEAL PLAN
==================================================

BREAKFAST
--------------------------------------------------
Egg and Chicken Breakfast Skillet

Calories: 480 kcal
Protein: 42 g
Carbs: 18 g
Fat: 22 g

LUNCH
--------------------------------------------------
Chicken and Broccoli Rice Bowl

Calories: 550 kcal
Protein: 45 g
Carbs: 48 g
Fat: 14 g

DINNER
--------------------------------------------------
Baked Chicken, Rice, and Broccoli Casserole

Calories: 580 kcal
Protein: 52 g
Carbs: 42 g
Fat: 18 g

SNACK
--------------------------------------------------
Chicken and Rice Cakes

Calories: 260 kcal
Protein: 28 g
Carbs: 22 g
Fat: 6 g

==================================================
                  DAILY TOTALS
==================================================

Calories: 1870 kcal
Protein: 167 g
Carbs: 130 g
Fat: 60 g
==================================================

✓ Meal plan created successfully
```

---

## Development

CutBuddy was initially developed and tested in two Jupyter Notebooks before being refactored into a modular Python application.

The original development notebooks are included in:

notebooks/

The final application separates the AI agents, tools, recipe searching, nutrition calculations, validation logic, and terminal output into individual modules.

---

## How to Run Locally
### Prerequisites

Install:
- Python 3.10+
- AWS account with access to Amazon Bedrock
- Anthropic Claude model access through Bedrock

### Clone the repository
```
git clone https://github.com/ashlygenaot/CutBuddy.git
-cd cutbuddy
```
### Create a virtual environment
```
python3 -m venv venv
```
### Activate it:

### macOS/Linux:
```
source venv/bin/activate
```
### Windows:
```
venv\Scripts\activate
```

### Install dependencies
```
pip install -r requirements.txt
```
### Configure environment variables

Create a .env file based on .env.example.

Configure your AWS credentials and required environment variables.

### Run CutBuddy
```
python main.py
```

---

Thanks for reading! If you have any feedback, don't hesitate to reach out.
