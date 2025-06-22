from pydantic import BaseModel, ConfigDict


class BaseRecipe(BaseModel):
    name: str
    cooking_time: int


class RecipeIn(BaseRecipe):
    description: str
    ingredients: str


class RecipeOutShort(BaseRecipe):
    model_config = ConfigDict(from_attributes=True)
    id: int
    views_count: int


class RecipeOutDetail(RecipeIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
