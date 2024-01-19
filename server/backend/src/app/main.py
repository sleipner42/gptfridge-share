from app.modules.ingredients.routes import router as ingredient_router
from app.modules.recipes.routes import router as recipe_router
from app.settings import Environment, settings
from fastapi import FastAPI

fast_api_config = {}

if settings.ENVIRONMENT == Environment.DEV:
    fast_api_config["docs_url"] = "/docs"

app = FastAPI(**fast_api_config)

app.include_router(ingredient_router, prefix="/ingredients")
app.include_router(recipe_router, prefix="/recipes")
