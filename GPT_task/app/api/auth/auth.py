from fastapi import Depends, HTTPException, status, APIRouter
from app.api.models.users import Users_Table
from app.api.models.base_model import Base
from ..core.config import SECRET_AUTH, ALGORITHM
from ..schemas.user_schema import UserCreate
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.DB import engine, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError

SECRET_KEY = SECRET_AUTH
ALGORITHM = ALGORITHM

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token/")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Authenticate Error"}},
)

Base.metadata.create_all(bind=engine)


def get_db():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def password_hash(password):
    if password is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="password is None")
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    if plain_password is None or hashed_password is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="failed verify password")
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(user: str, password: str, db):
    user = db.query(Users_Table).filter(Users_Table.email == user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not valid")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="password is not valid")
    return user


def create_access_token(
        username: str, user_id: int, express_delta: Optional[timedelta] = None
):
    encode = {"username": username, "id": user_id}
    if express_delta:
        expire = datetime.utcnow() + express_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


def create_refresh_token(
        username: str,
        user_id: int,
        express_delta: Optional[timedelta] = None
):
    encode = {"username": username, "id": user_id}
    if express_delta:
        expire = datetime.utcnow() + express_delta
    else:
        expire = datetime.utcnow() + timedelta(days=10)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


async def get_current_admin(token: str = Depends(oauth2_bearer),
                           db: Session = Depends(get_db)):
    pyload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    email: str = pyload.get("username")
    user_id: int = pyload.get("id")

    res = db.query(Users_Table).filter(Users_Table.email == email).first()

    if res is None:
        raise for_user_exception()

    is_super = res.is_superuser

    if is_super == False:
        raise for_user_exception()

    if email is None or user_id is None:
        raise get_user_exceptions()

    return {"sub": email, "user_id": user_id}


async def get_current_user(token: str = Depends(oauth2_bearer),
                           db: Session = Depends(get_db)):
    pyload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    email: str = pyload.get("username")
    user_id: int = pyload.get("id")

    res = db.query(Users_Table).filter(Users_Table.email == email).first()

    if res is None:
        raise for_user_exception()

    # is_super = res.is_superuser
    #
    # if is_super == False:
    #     raise for_user_exception()

    if email is None or user_id is None:
        raise get_user_exceptions()

    return {"sub": email, "user_id": user_id}



@router.post("/create_admin")
async def create_admin(user: UserCreate,
                       db: Session = Depends(get_db),
                       login: dict = Depends(get_current_admin)):

    if login is None:
        return get_user_exceptions()

    res = []
    user_model = Users_Table()
    user_model.name = user.name
    user_model.age = user.age
    user_model.email = user.email
    user_model.password = user.password
    user_model.is_active = user.is_active
    user_model.is_superuser = user.is_superuser
    user_model.is_verified = user.is_verified

    if user_model:
        user_name = db.query(Users_Table).all()
        for x in user_name:
            if user_model.email == x.email or user_model.email == x.email:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail={'msg': f"{user_model.email} user is already exists"})
    hash_password = password_hash(user.password)

    user_model.password = hash_password
    return_user_model = user_model

    get_refresh_token = create_refresh_token(user_model.email, user_model.id)
    get_access_token = create_access_token(user_model.email, user_model.id)

    db.add(user_model)
    db.commit()
    res.append(return_user_model)
    return "success"


@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(form_data.username, form_data.password, db=db)

        if not user:
            raise token_exception()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    token_expires = timedelta(minutes=20)
    token = create_access_token(user.email, user.id, express_delta=token_expires)
    get_refresh_token = create_refresh_token(user.email, user.id)

    return {"access_token": token,
            "refresh_token": get_refresh_token}


@router.post("/refresh_token")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_access_token = jwt.encode({"sub": user_id}, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": new_access_token}


@router.get("/users")
async def user_list(db: Session = Depends(get_db),
                    user: dict = Depends(get_current_admin)):
    if user is None:
        raise get_user_exceptions()


    model_ = db.query(Users_Table).all()
    return model_


# Exceptions


def get_user_exceptions():
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credential_exceptions


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response


def for_user_exception():
    credential_exceptions = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="You are not admin ",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credential_exceptions