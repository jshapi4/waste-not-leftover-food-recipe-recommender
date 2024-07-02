# Waste Not: Leftover Food Recipe Recommender

## Project Summary

**Waste Not** is a web application designed to reduce food waste by helping users find recipes based on their leftover ingredients. The app uses a comprehensive database of recipes to recommend the top ten matches for the ingredients users have on hand.

### Environmental Impact
- The U.S. wastes 92 billion pounds of food annually, equating to $473 billion in economic losses and 145 billion meals wasted.
- **Waste Not** aims to mitigate this by promoting efficient use of leftover ingredients.

## Data Summary

The dataset from Kaggle includes 179,694 recipes and 177,699 unique ingredients from Food.com (Li, 2020). Key processing steps:
- Load and preprocess data with pandas.
- Clean and standardize ingredient formatting.
- Future improvements will incorporate user feedback for enhanced recommendations.

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run app/main.py
   ```