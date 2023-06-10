from uuid import uuid4
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse, FileResponse

router = APIRouter(prefix="/simple-API",
                   tags=["Simple API"])


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid4())

    def __str__(self):
        return self.name, self.age, self.id


people = [Person("Tom", 38),
          Person("Bob", 42),
          Person("Sam", 28)]


def find_person(id):
    for person in people:
        if person.id == id:
            return person


@router.get("/")
async def main():
    return FileResponse("template/index3.html")


@router.get("/api/users")
async def get_people_list():
    return people


@router.get("/api/users/{id}")
async def get_person_by_id(id):
    person = find_person(id)
    print(person)

    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    return person


@router.post("/api/users")
async def create_user(data = Body()):
    person = Person(data["name"], data["age"])
    people.append(person)
    return person


@router.put("/api/users")
async def update_user(data = Body()):
    pesrson = find_person(data["id"])

    if pesrson == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )

    pesrson.name = data["name"]
    pesrson.age = data["age"]
    return pesrson


@router.delete("/api/users/{id}")
async def delete_user(id):

    person = find_person(id)

    if person == None:
        return JSONResponse()

    people.remove(person)
    return person



def JsonExeption():
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not Found"}
        )

