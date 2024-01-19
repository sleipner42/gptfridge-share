import json

import pandas as pd
from app.core.db_session import get_db_session
from app.modules.ingredients.model import IngredientDB
from app.modules.recipes.model import Association, RecipeDB
from sqlalchemy import delete, insert, select

session = next(get_db_session())

# # Delete database
stmt = delete(Association)
session.execute(stmt)
session.commit()

stmt = delete(RecipeDB)
session.execute(stmt)
session.commit()

stmt = delete(IngredientDB)
session.execute(stmt)
session.commit()

# # Insert ingredients
df = pd.read_csv("seed.csv")
ingredients = (
    df["parsed_ingredients"].str.replace("'", '"').apply(json.loads).explode().unique()
)

ingredients = [{"name": obj} for obj in ingredients]
stmt = insert(IngredientDB).values(ingredients)
session.execute(stmt)
session.commit()

# Insert recipes

# Get all ingredients

stmt = select(IngredientDB)
objs = session.execute(stmt).scalars()

lookup = {obj.name: obj for obj in objs}

df = pd.read_csv("seed.csv")
df["parsed_ingredients"] = (
    df["parsed_ingredients"].str.replace("'", '"').apply(json.loads)
)
df["parsed_ingredients"] = df["parsed_ingredients"].apply(
    lambda x: [lookup[n] for n in x]
)

df = df[["canonical_url", "title", "image", "parsed_ingredients"]]
df = df.rename(
    columns={
        "canonical_url": "url",
        "title": "name",
        "image": "image_url",
        "parsed_ingredients": "ingredients",
    }
)

recipes_items = [RecipeDB(**obj) for obj in df.to_dict(orient="records")]

for item in recipes_items:
    session.add(item)

session.commit()

# stmt = insert(RecipeDB).values(recipes_items)
# output = session.execute(stmt)
# print(recipes_items)
