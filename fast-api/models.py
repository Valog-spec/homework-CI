from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RecipeModel(Base):
    __tablename__ = "Recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    ingredients: Mapped[int]
    cooking_time: Mapped[str]
    description: Mapped[str]
    views_count: Mapped[int] = mapped_column(default=0)
