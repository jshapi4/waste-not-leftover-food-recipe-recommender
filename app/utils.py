import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time


def delete_ingredient(index):
    st.session_state.leftover_list.pop(index)

def edit_ingredient(index):
    st.session_state['edit_index'] = index
    st.session_state['edit_ingredient'] = st.session_state.leftover_list[index]

def display_ingredients_list(ingredients):
    if ingredients:
        st.write('Your leftover ingredients list:')
        for index, item in enumerate(ingredients):
            col1, col2, col3 = st.columns([8, 1, 1])
            with col1:
                st.markdown(f"#### {item}")
            with col2:
                st.button('✏️', key=f'edit_{index}', on_click=edit_ingredient, args=(index,))
            with col3:
                st.button('🗑️', key=f'delete_{index}', on_click=delete_ingredient, args=(index,))

def edit_ingredient_popup():
    if 'edit_index' in st.session_state:
        with st.form(key='edit_form'):
            st.write(f"Editing: {st.session_state['edit_ingredient']}")
            new_ingredient = st.text_input('Update ingredient', value=st.session_state['edit_ingredient'], key='new_ingredient_input')
            col1, col2 = st.columns(2)
            with col1:
                update_button = st.form_submit_button('Update')
            with col2:
                cancel_button = st.form_submit_button('Cancel')

        if update_button:
            st.session_state.leftover_list[st.session_state['edit_index']] = new_ingredient
            del st.session_state['edit_index']
            del st.session_state['edit_ingredient']

        if cancel_button:
            del st.session_state['edit_index']
            del st.session_state['edit_ingredient']

def display_top_recipes(top_10_recipes, radar_chart_data):
    st.header('Top 10 Recipes For You:')
    categories = ['Cosine Similarity Score', 'Leftover Usage Percentage', 'Ingredient Ratio']

    for i, (index, row) in enumerate(top_10_recipes.iterrows(), 1):
        # Create a container for each recipe
        with st.container():
            # Display the recipe title and match score
            col1, col2 = st.columns([3, 1])
            with col1:
                st.metric(f"#{i}:", f"{row['Recipe Name']}")
                #st.subheader(f"#{i}: {row['Recipe Name']}")
            with col2:
                st.metric("Match Score", f"{(row['Combined Score'] * 100):.2f}")

            # Create an expander for the recipe details
            with st.expander("View Recipe Details", expanded=False):
                # Ingredients list
                st.write("##### Ingredients:")
                st.write(", ".join(row['Ingredients']))

                # Ingredients Intersection
                st.write("##### Leftovers Used:")
                st.write(", ".join(row['Ingredient Intersection']))

                # Unused Leftovers
                st.write("##### Unused Leftovers:")
                if row['Unused Leftovers']:
                    st.write(", ".join(row['Unused Leftovers']))
                else:
                    st.write("None!")

                # Ingredients Needed
                st.write("##### Ingredients Needed:")
                st.write(", ".join(row['Ingredients Needed']))

                # Radar chart for the current recipe
                radar_data = radar_chart_data.loc[index]
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=[radar_data['Cosine Similarity Score'], radar_data['Leftover Usage Percentage'], radar_data['Ingredient Ratio']],
                    theta=categories,
                    fill='toself',
                    name=row['Recipe Name']
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1]  # Set range from 0 to 1 for normalized values
                        )
                    ),
                    showlegend=False,
                    title=row['Recipe Name']
                )
                st.plotly_chart(fig)

        # Add a separator between recipes
        st.markdown("---")

# Visualizations of Cosine Similarity!
def display_top_recipes_similarity_bar_chart(top_10_recipes):
    plt.figure(figsize=(10, 6))
    plt.barh(top_10_recipes['Recipe Name'], top_10_recipes['Cosine Similarity Score'], color='green')
    plt.xlabel('Cosine Similarity Score')
    plt.ylabel('Recipe Name')
    plt.title('Top 10 Recipes by Cosine Similarity')
    plt.gca().invert_yaxis()
    st.pyplot(plt.gcf())