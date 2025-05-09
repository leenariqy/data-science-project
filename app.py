import streamlit as st
import json

# Load recipe data
def load_recipes():
    with open("recipes.json", "r") as f:
        return json.load(f)

# Save recipe data
def save_recipes(data):
    with open("recipes.json", "w") as f:
        json.dump(data, f, indent=4)

# UI
st.title("🍽️ Recipe Finder System")

recipes = load_recipes()

menu = ["Get Recommendations", "Search Recipe", "Filter Recipes", "Add New Recipe"]
choice = st.sidebar.radio("Choose an action:", menu)

if choice == "Get Recommendations":
    cuisine = st.text_input("Enter your preferred cuisine:")
    if cuisine:
        matches = [name for name, data in recipes.items() if data["Cuisine"].lower() == cuisine.lower()]
        if matches:
            st.success(f"Based on your love for {cuisine}, try these recipes:")
            for recipe in matches:
                st.markdown(f"- {recipe}")
        else:
            st.warning("No recipes found. Try another cuisine.")

elif choice == "Search Recipe":
    query = st.text_input("Search by recipe name:")
    if query:
        found = False
        for name, data in recipes.items():
            if query.lower() in name.lower():
                st.subheader(f"🍴 {name}")
                st.text(f"Cuisine: {data['Cuisine']}")
                st.text(f"Ingredients: {', '.join(data['Ingredients'])}")
                st.text(f"Prep Time: {data['Prep Time']} mins")
                st.text(f"Difficulty: {data['Difficulty']}")
                st.text(f"Rating: {data['Rating']}")
                found = True
        if not found:
            st.error("No recipe found with that name.")

elif choice == "Filter Recipes":
    difficulty = st.selectbox("Select difficulty", ["Any", "Easy", "Medium", "Hard"])
    max_time = st.slider("Max prep time (minutes)", 0, 120, 30)
    min_rating = st.slider("Minimum rating", 0.0, 5.0, 4.0)

    results = []
    for name, data in recipes.items():
        if (difficulty == "Any" or data["Difficulty"] == difficulty) and            data["Prep Time"] <= max_time and data["Rating"] >= min_rating:
            results.append((name, data))

    if results:
        for name, data in results:
            st.markdown(f"**{name}** - {data['Difficulty']} - {data['Prep Time']} mins - ⭐ {data['Rating']}")
    else:
        st.info("No recipes matched your filters.")

elif choice == "Add New Recipe":
    st.subheader("Add Your Recipe")
    name = st.text_input("Recipe Name")
    cuisine = st.text_input("Cuisine")
    ingredients = st.text_input("Ingredients (comma-separated)")
    prep_time = st.number_input("Prep Time (minutes)", min_value=0, step=1)
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    rating = st.slider("Rating", 0.0, 5.0, 0.0)

    if st.button("Add Recipe"):
        if name and cuisine and ingredients:
            recipes[name] = {
                "Cuisine": cuisine,
                "Ingredients": [i.strip() for i in ingredients.split(",")],
                "Prep Time": int(prep_time),
                "Difficulty": difficulty,
                "Rating": float(rating)
            }
            save_recipes(recipes)
            st.success(f"Recipe '{name}' added successfully!")
        else:
            st.error("Please fill in all required fields.")
