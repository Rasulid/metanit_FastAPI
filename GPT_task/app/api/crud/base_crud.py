from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ..auth.auth import password_hash, get_current_user
from ..models.users import Users_Table
from ..schemas.user_schema import UserUpdate, UserCreate
from app.DB import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter(tags=["functionality"],
                   prefix="/api")


@router.post("/register")
async def register_user(user: UserCreate,
                        db: Session = Depends(get_db)):

    user_model = Users_Table()
    user_model.name = user.name
    user_model.age = user.age
    user_model.email = user.email
    user_model.password = user.password
    user_model.password = password_hash(user.password)
    user_model.is_active = True
    user_model.is_superuser = False
    user_model.is_verified = user.is_verified

    check = db.query(Users_Table).filter(Users_Table.email == user.email).first()

    if check is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"massage": "Your email address is already exists"})

    db.add(user_model)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created successfully"}
    )


@router.get("/list")
async def list_users(db: Session = Depends(get_db),
                     login: dict = Depends(get_current_user)):
    res = db.query(Users_Table).all()
    return res


@router.put("/update")
async def updata_user(user: UserUpdate,
                      id: int,
                      db: Session = Depends(get_db)):
    res = db.query(Users_Table).filter(Users_Table.id == id).first()

    res.name = user.name
    res.email = user.email
    res.age = user.age

    db.add(res)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User updated successfully"}
    )


@router.delete("/delete")
async def delete_user(id: int,
                      db: Session = Depends(get_db)):
    chack = db.query(Users_Table).filter(Users_Table.id == id).first()

    if not chack:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "User Not Found"})

    res = db.query(Users_Table).filter(Users_Table.id == id).delete()

    db.commit()

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": "User deleted successfully"}
    )
