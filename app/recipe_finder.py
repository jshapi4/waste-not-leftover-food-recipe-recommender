import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

def find_top_recipes(recipe_data, leftover_ingredients):
    # Use MultiLabelBinarizer with sparse output to one-hot encode the ingredients
    mlb = MultiLabelBinarizer(sparse_output=True)
    ingredient_matrix = mlb.fit_transform(recipe_data['Ingredients'])
    f_ingredient_names = mlb.classes_

    # Convert to sparse DataFrame
    recipe_ingredient_df = pd.DataFrame.sparse.from_spmatrix(ingredient_matrix, columns=f_ingredient_names,
                                                             index=recipe_data.index)
    recipe_data_exp = pd.concat([recipe_data, recipe_ingredient_df], axis=1)

    # Prepare the leftover ingredients as a sparse vector
    leftover_vector = pd.DataFrame.sparse.from_spmatrix(csr_matrix((1, len(f_ingredient_names))),
                                                        columns=f_ingredient_names)
    for ingredient in leftover_ingredients:
        if ingredient in leftover_vector.columns:
            leftover_vector[ingredient] = 1

    # Extract recipe vectors as sparse matrix
    recipe_vectors = ingredient_matrix

    # Calculate cosine similarity between the leftover vector and recipe vectors
    similarity_scores = cosine_similarity(leftover_vector, recipe_vectors)

    # Add similarity scores to the recipe data
    recipe_data_exp['Cosine Similarity Score'] = similarity_scores[0]

    # Prepare the leftover ingredients as a set
    leftover_set = set(leftover_ingredients)

    # Apply the function to calculate the usage percentage for each recipe and store the intersections
    leftover_usage_data = recipe_data_exp['Ingredients'].apply(calculate_leftover_usage, args=(leftover_set,))
    recipe_data_exp['Leftover Usage Percentage'] = leftover_usage_data.apply(lambda x: x[0])
    recipe_data_exp['Ingredient Intersection'] = leftover_usage_data.apply(lambda x: x[1])
    recipe_data_exp['Unused Leftovers'] = leftover_usage_data.apply(lambda x: x[2])
    recipe_data_exp['Ingredients Needed'] = leftover_usage_data.apply(lambda x: x[3])

    # Normalize the scores to the range [0, 1]
    recipe_data_exp['Normalized Cosine Similarity'] = (recipe_data_exp['Cosine Similarity Score'] - recipe_data_exp['Cosine Similarity Score'].min()) / (recipe_data_exp['Cosine Similarity Score'].max() - recipe_data_exp['Cosine Similarity Score'].min())
    recipe_data_exp['Normalized Leftover Usage'] = recipe_data_exp['Leftover Usage Percentage'] / 100

    # find the ingredient use ratio
    recipe_data_exp['Ingredients Use Count'] = recipe_data_exp['Ingredient Intersection'].apply(len)
    recipe_data_exp['Ingredients Needed Count'] = recipe_data_exp['Ingredients Needed'].apply(len)
    recipe_data_exp['Ingredient Ratio'] = recipe_data_exp['Ingredients Use Count'] / recipe_data_exp['Ingredients'].apply(len)

    # Combine the scores with equal weights (1/3 each)
    recipe_data_exp['Combined Score'] = (recipe_data_exp['Normalized Cosine Similarity'] + recipe_data_exp['Normalized Leftover Usage'] + recipe_data_exp['Ingredient Ratio']) / 3

    # Sort recipes by the combined score in descending order
    sorted_recipes = recipe_data_exp.sort_values(by='Combined Score', ascending=False)

    # Limit the output to the top 10 recipes
    top_10_recipes = sorted_recipes.head(10)
    # return the top 100 for heatmap
    top_1000_recipes = sorted_recipes.head(1000)

    # Include necessary fields for radar chart
    radar_chart_data = top_10_recipes[
        ['Recipe Name', 'Cosine Similarity Score', 'Combined Score', 'Leftover Usage Percentage', 'Ingredients Needed',
         'Ingredient Intersection', 'Ingredients Use Count', 'Ingredient Ratio']].copy()
    #radar_chart_data['Ingredients Needed Count'] = radar_chart_data['Ingredients Needed'].apply(len)
    #radar_chart_data['NumIngredUsed'] = radar_chart_data['Ingredient Intersection'].apply(len)
    radar_chart_data['Leftover Usage Percentage'] /= 100
    # radar_chart_data['Ingredient Ratio'] = radar_chart_data['NumIngredUsed'] / (
    #         radar_chart_data['Ingredients Needed Count'] + radar_chart_data['NumIngredUsed'])

    return top_10_recipes, radar_chart_data, top_1000_recipes
def calculate_leftover_usage(ingredients, leftover_set):
    ingredients_set = set(ingredients)
    intersection = ingredients_set.intersection(leftover_set)
    unused_leftovers = leftover_set.difference(ingredients_set)
    ingredients_to_buy = ingredients_set.difference(leftover_set)
    return len(intersection) / len(leftover_set) * 100, intersection, unused_leftovers, ingredients_to_buy