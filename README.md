# Daily Bread
## a calories tracking app

### Description:
Daily Bread: a basic calories tracking app built using Django. The app integrates a third-party API, NutritionIX, to fetch nutritional data which users can then perform CRUD actions with.

After users create an account and accompanying profile, users can then search for different foods, categorize them by meal, and create entries, tracking nutrional data: calories, fats, proteins, carbs.

### Background:
This project grew from a personal interest in health and fitness. A healthy lifestyle constitutes exercise and proper diet. This app aims to help users reach their diet and nutrition goals by tracking the three main nutrients (macronutrients): fats, proteins, and carbohyrates, as well as calories.

By tracking these elements, users can gain a better sense of their day-to-day, even meal-to-meal, progress toward their goals. Whether they follow a 40-40-20 (40% protein, 40% carbohydrates, 20%) plan, or a a stricter 50-35-15 plan, users can make sure they hit their macro and calorie goals consistently.

### Development:
Development of the app did not come without challenges. The two main challenges encountered came when trying to integrate forsets into meal forms and when trying to add more forms when updating an existing meal.

#### Formset integration:
When creating a meal entry, users can add one or multiple food items. Users search and fetch the food item data, which automatically populates a form of the formset upon selection. The challenges arose when adding another form for multiple food items. Three functions () helped by creating, removing, and updating the total form count.