from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import schemas, models
from .dababase import engine, SessionLocal
from .models import Snippet_code, Category, User

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_dateBase():
    dateBase = SessionLocal()
    try:
        yield dateBase
    finally:
        dateBase.close()



@app.get("/")
async def root(dateBase: Session = Depends(get_dateBase)):
    all_snippets = dateBase.query(Snippet_code).join(
        Category).all()

    result = [
        {
            "snippet_code_id": snippet.ID,
            "title": snippet.title,
            "user_Id": snippet.UserId,
            "category": snippet.category.Name,
            "user": snippet.user,

        }
        for snippet in all_snippets
    ]

    return result

@app.get("/{id}")
async def root(dateBase: Session = Depends(get_dateBase), id: str = None):
    all_snippets = dateBase.query(Snippet_code).join(
        Category).where(Snippet_code.ID == id).all()

    result = [
        {
            "snippet_code_id": snippet.ID,
            "title": snippet.title,
            "user_Id": snippet.UserId,
            "category": snippet.category.Name,
            "user": snippet.user,   
        }
        for snippet in all_snippets
    ]

    return result


@app.post("/createCode")
async def create_code(code: schemas.SnippetBase, category: schemas.CategoryBase, dateBase: Session = Depends(get_dateBase)):
    existing_category = dateBase.query(Category).filter(
        Category.Name == category.Name).first()
    if not existing_category:
        # Assuming your CategoryBase schema is correct
        new_category = Category(**category.model_dump())
        dateBase.add(new_category)
        dateBase.commit()
        dateBase.refresh(new_category)
    else:
        new_category = existing_category

    new_code = Snippet_code(**code.model_dump())
    new_code.CategoryId = new_category.id
    dateBase.add(new_code)
    dateBase.commit()
    dateBase.refresh(new_code)

    return {"Snippet_code": new_code, "category": new_category}


@app.post("/createUser")
async def create_user(user: schemas.UserCreate, dateBase: Session = Depends(get_dateBase)):
    new_user = User(**user.model_dump())
    dateBase.add(new_user)
    dateBase.commit()
    dateBase.refresh(new_user)
    result = [
        {
            "User Name": user.FullName,
            "Email": user.Email,
            "Role": user.Role,

        }]

    return {"user": result}
