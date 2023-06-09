from datetime import datetime
from typing import List
from fastapi import FastAPI, Response, Path, Query, status, Body, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, FileResponse
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from DataBase import engine, Base
from simple_API import router as SimpleAPI

app = FastAPI(docs_url="/",
              title="Title")
app.include_router(SimpleAPI)

Base.metadata.create_all(bind=engine)

@app.get("/api")
async def root():
    return "root"


@app.post("/api/get")
async def get_info(naem: str, lname: str):
    return {"name": naem, "lastname": lname}


@app.get("/test")
def root_1():
    data = {"message": "Hello METANIT.COM"}
    json_data = jsonable_encoder(data)
    return JSONResponse(content=json_data)  # return JSONResponse


@app.get("/media-type")
async def media_type():
    date = "Hello metanit.com"
    return Response(content=date, media_type="text/plain")  # text mode


@app.get("/plainTextResponse")
async def PTX():
    data = "Hello metanit.com"
    return PlainTextResponse(content=data)  # text mode with plain text response


@app.get("/plainTextResponse_", response_class=PlainTextResponse)
async def PTX_():
    data = "Hello metanit.com"
    return data  # text mode with plain text response


@app.get("/htmlResponse")
async def htmlResponse():
    html_code = "<h2>Hello Metanit.com</h2>"
    return HTMLResponse(content=html_code)  # html mode


@app.get("/htmlResponse_")
async def htmlResponse_():
    html_code = "<h2>Hello Metanit.com</h2>"
    return HTMLResponse(content=html_code)  # html mode


# ---------------------------------------------------------------- SEND HTML FILE ----------------------------------------------------------------


@app.get("/sendhtml", response_class=FileResponse)
async def sendhtml():
    return "template/index.html"  # send html file


@app.get("/sendimage", response_class=FileResponse)
async def sendimage():
    return "static/Rasul Abduvaitov.pdf"  # send media


# download

@app.get("/download")
async def download_file():
    return FileResponse(
        "static/Rasul Abduvaitov.pdf",
        filename="something.pdf",
        media_type="application/octet-stream"
    )


# ---------------------------------------------------------------- Path Option (Параметры Пути) ----------------------------------------------------------------

@app.get("/user_id/{id}")
async def userId(id):
    return {"users_id": id}  # one parameter


@app.get("/user_id/{id}-{age}-{name}")
async def eser_info(id, age, name):
    return {
        "user_id": id,
        "user_name": name,
        "user_age": age
    }  # many parameters


@app.get("/users/admin")
async def admin(admin):
    return {"Hello admin": admin}


@app.get("/users/{id}")
async def id_valid(id: int):
    return id


"""
Path
Дополнительно для работы с параметрами пути фреймворк FastAPI предоставляет класс Path из пакета fastapi. 
Класс Path позволяет валидировать значения параметров. 
В частности, через конструктор Path можно установить следующие параметры для валидации значений:

        min_length: устанавливает минимальное количество символов в значении параметра

        max_length: устанавливает максимальное количество символов в значении параметра

        regex: устанавливает регулярное выражение, которому должно соответствовать значение параметра

        lt: значение параметра должно быть меньше определенного значения

        le: значение параметра должно быть меньше или равно определенному значению

        gt: значение параметра должно быть больше определенного значения

        ge: значение параметра должно быть больше или равно определенному значению
        
"""


@app.get("/Path/{name}/{age}/{gmail}")
async def get_Path(name: str = Path(min_length=3, max_length=10),
                   age: int = Path(gt=16, lt=50),
                   gmail: str = Path(regex=r"^[a-zA-Z0-9_.+-]+@gmail\.com$")):
    return {"Name": name,
            "Age": age,
            "Gmail": gmail}


# ---------------------------------------------------------------- Path Params Query ----------------------------------------------------------------


"""
"Path" используется для извлечения параметров из самого пути URL. 
Это означает, что значения параметров будут частью URL-адреса и встроены в него. 
Например, если у вас есть маршрут /items/{item_id}, где item_id является параметром "Path", 
то URL будет выглядеть так: /items/42. Параметры "Path" обычно используются для идентификации ресурсов и представления их в URL.

"Query" используется для извлечения параметров из строки запроса URL. 
Параметры "Query" добавляются к URL после символа вопроса (?) и имеют формат key=value. 
Например, в URL /items?category=books, category является параметром "Query", а его значение - books. 
Параметры "Query" обычно используются для фильтрации, сортировки или настройки запросов.

Разница между "Path" и "Query" заключается в способе передачи параметров и их роли в URL. 
"Path" является частью самого пути URL, в то время как "Query" добавляется к URL в виде строки запроса. 
Выбор между ними зависит от вашего конкретного случая использования и того, как вы хотите представить параметры в URL.
"""

"""
Query
Дополнительно для работы с параметрами строки запроса фреймворк предоставляет класс Query из пакета fastapi. 
Класс Query позволяет прежде всего валидировать значения параметров строки запроса. 
В частности, через конструктор Query можно установить следующие параметры для валидации значений:

        min_length: устанавливает минимальное количество символов в значении параметра

        max_length: устанавливает максимальное количество символов в значении параметра

        regex: устанавливает регулярное выражение, которому должно соответствовать значение параметра

        lt: значение параметра должно быть меньше определенного значения

        le: значение параметра должно быть меньше или равно определенному значению

        gt: значение параметра должно быть больше определенного значения

        ge: значение параметра должно быть больше или равно определенному значению
"""


@app.get("/Query")
async def get_Query(name: str = Query(min_length=3, max_length=10),
                    age: int = Query(gt=16, lt=50),
                    gmail: str = Query(regex=r"^[a-zA-Z0-9_.+-]+@gmail\.com$"),
                    dalb: bool = False):
    return {"Name": name,
            "Age": age,
            "Gmail": gmail,
            "dalb": dalb}


# list


@app.get("/Workers")
async def get_Workers(people: List[str] = Query()):
    return {"People": people}


# Сщчитания Query и Path

@app.get("/users/test/{name}")
def users(name: str = Path(min_length=3, max_length=20),
          age: int = Query(ge=18, lt=111)):
    return {"name": name, "age": age}


# ---------------------------------------------------------------- Status Code ----------------------------------------------------------------


"""Одной из расспространненых задач в веб-приложении является отправка статусных кодов, 
которые указывают на статус выполнения операции на сервере.

        1xx: предназначены для информации. Ответ с таким кодом не может иметь содержимого

        2xx: указывает на успешноее выполнение операции

        3xx: предназначены для переадресации

        4xx: предназначены для отправки информации об ошибок клиента

        5xx: предназначены для информации об ошибках сервера

По умолчанию функции обработки отправляют статусный код 200, но при необходимости мы можем отправить любой статусный код. 
Для этого у методов get(), post(), put(), delete(), options(), head(), patch(), trace() 
в классе FastAPI применяется параметр status_code, который принимает числовой код статуса HTTP. 
Например:
"""


@app.get("/not_found", status_code=status.HTTP_404_NOT_FOUND)
async def not_found():
    return {"message": "Resource Not Found"}


"""
HTTP_100_CONTINUE (код 100)

HTTP_101_SWITCHING_PROTOCOLS (код 101)

HTTP_102_PROCESSING (код 102)

HTTP_103_EARLY_HINTS (код 103)

HTTP_200_OK (код 200)

HTTP_201_CREATED (код 201)

HTTP_202_ACCEPTED (код 202)

HTTP_203_NON_AUTHORITATIVE_INFORMATION (код 203)

HTTP_204_NO_CONTENT (код 204)

HTTP_205_RESET_CONTENT (код 205)

HTTP_206_PARTIAL_CONTENT (код 206)

HTTP_207_MULTI_STATUS (код 207)

HTTP_208_ALREADY_REPORTED (код 208)

HTTP_226_IM_USED (код 226)

HTTP_300_MULTIPLE_CHOICES (код 300)

HTTP_301_MOVED_PERMANENTLY (код 301)

HTTP_302_FOUND (код 302)

HTTP_303_SEE_OTHER (код 303)

HTTP_304_NOT_MODIFIED (код 304)

HTTP_305_USE_PROXY (код 305)

HTTP_306_RESERVED (код 306)

HTTP_307_TEMPORARY_REDIRECT (код 307)

HTTP_308_PERMANENT_REDIRECT (код 308)

HTTP_400_BAD_REQUEST (код 400)

HTTP_401_UNAUTHORIZED (код 401)

HTTP_402_PAYMENT_REQUIRED (код 402)

HTTP_403_FORBIDDEN (код 403)

HTTP_404_NOT_FOUND (код 404)

HTTP_405_METHOD_NOT_ALLOWED (код 405)

HTTP_406_NOT_ACCEPTABLE (код 406)

HTTP_407_PROXY_AUTHENTICATION_REQUIRED (код 407)

HTTP_408_REQUEST_TIMEOUT (код 408)

HTTP_409_CONFLICT (код 409)

HTTP_410_GONE (код 410)

HTTP_411_LENGTH_REQUIRED (код 411)

HTTP_412_PRECONDITION_FAILED (код 412)

HTTP_413_REQUEST_ENTITY_TOO_LARGE (код 413)

HTTP_414_REQUEST_URI_TOO_LONG (код 414)

HTTP_415_UNSUPPORTED_MEDIA_TYPE (код 415)

HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE (код 416)

HTTP_417_EXPECTATION_FAILED (код 417)

HTTP_418_IM_A_TEAPOT (код 418)

HTTP_421_MISDIRECTED_REQUEST (код 421)

HTTP_422_UNPROCESSABLE_ENTITY (код 422)

HTTP_423_LOCKED (код 423)

HTTP_424_FAILED_DEPENDENCY (код 424)

HTTP_425_TOO_EARLY (код 425)

HTTP_426_UPGRADE_REQUIRED (код 426)

HTTP_428_PRECONDITION_REQUIRED (код 428)

HTTP_429_TOO_MANY_REQUESTS (код 429)

HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE (код 431)

HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS (код 451)

HTTP_500_INTERNAL_SERVER_ERROR (код 500)

HTTP_501_NOT_IMPLEMENTED (код 501)

HTTP_502_BAD_GATEWAY (код 502)

HTTP_503_SERVICE_UNAVAILABLE (код 503)

HTTP_504_GATEWAY_TIMEOUT (код 504)

HTTP_505_

HTTP_VERSION_NOT_SUPPORTED (код 505)

HTTP_506_VARIANT_ALSO_NEGOTIATES (код 506)

HTTP_507_INSUFFICIENT_STORAGE (код 507)

HTTP_508_LOOP_DETECTED (код 508)

HTTP_510_NOT_EXTENDED (код 510)

HTTP_511_NETWORK_AUTHENTICATION_REQUIRED (код 511)
"""


@app.get("/not_found_")
async def not_found_():
    return JSONResponse(content={"message": "Resource Not Found"}, status_code=404)


@app.get("/user/{id}", status_code=200)
async def user_ident(response: Response, id: int = Path()):
    if id < 10:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Incorrect Data"}
    return {"message": f"Id = {id}"}


# ---------------------------------------------------------------- Переодрисация (Redirect) ----------------------------------------------------------------

# @app.get("/redirect1", response_class=RedirectResponse)
# async def redirect1():
#     return "/redirect2"

@app.get("/redirect1")
async def redirect2():
    return RedirectResponse("/redirect2")


@app.get("/redirect2")
async def redirect2():
    return PlainTextResponse("new")


# ---------------------------------------------------------------- Static files ----------------------------------------------------------------


app.mount("/template", StaticFiles(directory="template", html=True))


# ---------------------------------------------------------------- Получения данных запроса ----------------------------------------------------------------


@app.get("/hello_get")
def send():
    return FileResponse("template/index.html")


@app.post("/hello")
async def hello(data=Body()):
    name = data["name"]
    age = data["age"]
    return {"message": f"{name}, ваш возраст - {age}"}


# ---------------------------------------------------------------- Получения данных запроса в виде класа ----------------------------------------------------------------

# class Person(BaseModel):
#     name: str #= Field(default="dalbayob", min_length=3, max_length=20)
#     age: int #= Field(default=18, ge=18, lt=111)
#     languages: list = ["Java", "Python", "JavaScript"] #= Field(default)


class Company(BaseModel):
    name: str


class Person(BaseModel):
    name: str
    company: Company


@app.get("/class-request")
async def class_request():
    return FileResponse("template/index2.html")


@app.post("/class-request")
async def class_Request_Post(person: Person):#person: Person):
    # if person.age == None:
    #     return {"message": f"{person.name} ты чорт "}
    # return {"message": f"Привет ,{person.name} , тебе точно {person.age}"}
    return {"message": f"Name: {person.name}. Company: {person.company.name}"}


# ---------------------------------------------------------------- Headers ----------------------------------------------------------------

@app.get("/api/headers")
async def get_headers():
    data = "Hello world"
    return Response(content=data ,media_type="text/plain",headers={"Secret-key":"123-324-12"})

# ---------------------------------------------------------------- Cookie ----------------------------------------------------------------

"""
Для установки куки на сервере у объекта Response и его классов-наследников применяется метод set_cookie(). Этот метод принимает ряд параметров:

        key: ключ или имя куки. Обязательный параметр

        value: значение куки, значение по умолчанию - пустая строка

        max_age: максимальное время жизни куки в секундах. Это может быть либо число, либо значение None (ограничивает время жизни куки текущей сессией браузера, является значением по умолчанию).

        expires: когда истекает действие куки. Это может быть либо число, либо значение None (ограничивает время жизни куки текущей сессией браузера, является значением по умолчанию).

        path: путь, для которого устанавливаются куки. Значение по умолчанию - корень веб-приложения "/"

        domain: домен, к которому применяются куки. значение по умолчанию None

        secure: устанавливает используемый протокол. Так, если имеет значение True, то куки будут посылаться на сервер только в запросе по протоколу https. Значение по умолчанию False

        httponly: устанавлиет доступность для скриптов javascript на клиенте. Так, значение True предотвращает доступ к куки из кода javascript на клиенте. Значение по умолчанию False

        samesite: устанавливает разрешения на отправку куки в кроссдоменных запросах. Так, значение lax (значение по умолчанию) указывают браузеру не посылать куки в кроссдоменных запросах.
        
    """

@app.get("/api/cookie")
async def get_cookie(response:Response):
    now = datetime.now()
    response.set_cookie(key="last_visit", value=now)
    return {"massage": "sat the cookie"}

# ---------------------------------------------------------------- Form Send ----------------------------------------------------------------


@app.get("/api/form-send")
async def form_send():
    return FileResponse("template/index4.html")


@app.post("/api/postdata")
async def postdata(username: str = Form(), userage: int = Form()):
    return {"name": username, "age": userage}

# ---------------------------------------------------------------- Complate FastAPI TUtorial ----------------------------------------------------------------
# ---------------------------------------------------------------- Complate FastAPI TUtorial ----------------------------------------------------------------
# ---------------------------------------------------------------- Complate FastAPI TUtorial ----------------------------------------------------------------


