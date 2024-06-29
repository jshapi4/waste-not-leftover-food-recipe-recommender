import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def display_ingredients_list(ingredients):
    if ingredients:
        st.write('Your leftover ingredients list:')
        for item in ingredients:
            st.markdown(f"- {item}")

# def display_top_recipes(top_10_recipes):
#     st.header('Top 10 Recipes For You:')
#     for i, (index, row) in enumerate(top_10_recipes.iterrows(), 1):
#         with st.expander(f"#{i}: {row['Recipe Name']}"):
#             ingredient_list = row['Ingredients']
#             st.write("Ingredients:")
#             for ingredient in ingredient_list:
#                 st.markdown(f"- {ingredient}")
#             st.write(f"Combined Score: {(row['Combined Score'] * 100):.2f} out of 100")
#             st.write(f"Normalized Cosine Similarity Score: {(row['Normalized Cosine Similarity'] * 100):.2f}%")
#             st.write(f"Leftover Usage Percentage: {row['Leftover Usage Percentage']:.2f}%")
#             st.write(f"Ingredients Intersection: {row['Ingredient Intersection']}")
#             if row['Unused Leftovers']:
#                 st.write(f"Unused Leftovers: {row['Unused Leftovers']}")
#             else:
#                 st.write(f"Unused Leftovers: None!")
#             st.write(f"Ingredients Needed: {row['Ingredients Needed']}")

def display_top_recipes(top_10_recipes):
    st.header('Top 10 Recipes For You:')
    for i, (index, row) in enumerate(top_10_recipes.iterrows(), 1):
        with st.expander(f"#{i}: {row['Recipe Name']}"):
            # Display combined score with custom styling
            with stylable_container(
                    key=f"score_container_{i}",
                    css_styles="""
                    {
                        background-color: #f0f0f0;
                        border-radius: 10px;
                        padding: 10px;
                        text-align: center;
                        justify-content: center;
                        margin-bottom: 10px;
                    }
                    p {
                        font-family: 'Helvetica', sans-serif;
                        font-size: 16px;
                        color: #053463;
                        margin: 0;
                    }
                """
            ):
                st.markdown(f"<p>Combined Score: {(row['Combined Score'] * 100):.2f}/100</p>", unsafe_allow_html=True)

            # Ingredients list
            st.subheader("Ingredients:")
            st.write(", ".join(row['Ingredients']))

            # Other scores
            st.write(f"Normalized Cosine Similarity Score: {(row['Normalized Cosine Similarity'] * 100):.2f}%")
            st.write(f"Leftover Usage Percentage: {row['Leftover Usage Percentage']:.2f}%")

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

def bootstrap_button(label, button_type):
    return f'''
    <button type="submit" class="btn btn-{button_type} btn-block w-100" style="height: 44px;">
        {label}
    </button>
    '''