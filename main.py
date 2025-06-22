from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator, AsyncIterator, List

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_engine, async_session
from models import Base, RecipeModel
from schemas import RecipeIn, RecipeOutDetail, RecipeOutShort


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await async_session().close()
        await async_engine.dispose()


app = FastAPI(lifespan=lifespan, title="Website about recipes")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.get(
    "/recipes",
    response_model=list[RecipeOutDetail],
    summary="Получение всех рецептов",
    tags=["Информация об рецептах"],
)
async def get_all_recipes(session: SessionDep) -> List[RecipeOutDetail]:
    query = select(RecipeModel)
    res = await session.execute(query)
    recipes = res.scalars().all()

    return [
        RecipeOutDetail.model_validate(row, from_attributes=True) for row in recipes
    ]


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeOutDetail,
    summary="Получение рецепта по id",
    tags=["Операции с рецептами"],
)
async def get_by_id(recipe_id: int, session: SessionDep) -> RecipeOutDetail:
    res = await session.get(RecipeModel, recipe_id)
    if res:
        res.views_count += 1
    await session.commit()

    return RecipeOutDetail.model_validate(res, from_attributes=True)


@app.post(
    "/recipes",
    response_model=RecipeOutDetail,
    summary="Добавление рецепта",
    tags=["Операции с рецептами"],
)
async def add_new_recipe(recipe: RecipeIn, session: SessionDep) -> RecipeModel:
    new_recipe = RecipeModel(**recipe.model_dump())
    session.add(new_recipe)
    await session.commit()
    return new_recipe


@app.get(
    "/screen1",
    response_model=List[RecipeOutShort],
    tags=["Информация об рецептах"],
    summary="Получение всех рецептов",
)
async def screen_1(session: SessionDep) -> List[RecipeOutShort]:
    query = select(RecipeModel).order_by(
        RecipeModel.views_count.desc(), RecipeModel.cooking_time.asc()
    )
    res = await session.execute(query)

    return [
        RecipeOutShort.model_validate(row, from_attributes=True)
        for row in res.scalars().all()
    ]


@app.get(
    "/screen2",
    response_model=list[RecipeOutDetail],
    tags=["Информация об рецептах"],
    summary="Детальная информация об рецептах",
)
async def screen_2(session: SessionDep) -> List[RecipeOutDetail]:
    query = select(RecipeModel)
    res = await session.execute(query)
    return [
        RecipeOutDetail.model_validate(row, from_attributes=True)
        for row in res.scalars().all()
    ]
