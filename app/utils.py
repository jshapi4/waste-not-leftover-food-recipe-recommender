import streamlit as st
import matplotlib.pyplot as plt


def display_ingredients_list(ingredients):
    if ingredients:
        st.write('Your leftover ingredients list:')
        for item in ingredients:
            st.markdown(f"- {item}")

def display_top_recipes(top_10_recipes):
    st.header('Top 10 Recipes For You:')
    for index, row in top_10_recipes.iterrows():
        with st.expander(f"{row['Recipe Name']}"):
            ingredient_list = row['Ingredients']
            st.write("Ingredients:")
            for ingredient in ingredient_list:
                st.markdown(f"- {ingredient}")
            st.write(f"Combined Score: {(row['Combined Score'] * 100):.2f} out of 100")
            st.write(f"Normalized Cosine Similarity Score: {(row['Normalized Cosine Similarity'] * 100):.2f}%")
            st.write(f"Leftover Usage Percentage: {row['Leftover Usage Percentage']:.2f}%")
            st.write(f"Ingredients Intersection: {row['Ingredient Intersection']}")
            if row['Unused Leftovers']:
                st.write(f"Unused Leftovers: {row['Unused Leftovers']}")
            else:
                st.write(f"Unused Leftovers: None!")
            st.write(f"Ingredients Needed: {row['Ingredients Needed']}")


def display_cosine_viz(recipe_data_exp):
    st.subheader('Cosine Similarity Scores Distribution')
    plt.hist(recipe_data_exp['Cosine Similarity Score'], bins=10, alpha=0.7, color='blue')
    st.pyplot(plt)