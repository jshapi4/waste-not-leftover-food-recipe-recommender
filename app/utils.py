import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def display_ingredients_list(ingredients):
    if ingredients:
        st.write('Your leftover ingredients list:')
        for item in ingredients:
            st.markdown(f"- {item}")

def display_top_recipes(top_10_recipes):
    st.header('Top 10 Recipes For You:')
    for i, (index, row) in enumerate(top_10_recipes.iterrows(), 1):
        with st.expander(f"#{i}: {row['Recipe Name']} --- \t\t Match Score: {(row['Combined Score'] * 100):.2f}"):

            # Ingredients list
            st.subheader("Ingredients:")
            st.write(", ".join(row['Ingredients']))

            # Other scores
            # st.write(f"Normalized Cosine Similarity Score: {(row['Normalized Cosine Similarity'] * 100):.2f}%")
            st.write(f"Leftover Usage: {row['Leftover Usage Percentage']:.2f}%")

            # Ingredients Intersection
            st.subheader("Ingredients Intersection:")
            st.write(", ".join(row['Ingredient Intersection']))

            # Unused Leftovers
            st.subheader("Unused Leftovers:")
            if row['Unused Leftovers']:
                st.write(", ".join(row['Unused Leftovers']))
            else:
                st.write("None!")

            # Ingredients Needed
            st.subheader("Ingredients Needed:")
            st.write(", ".join(row['Ingredients Needed']))