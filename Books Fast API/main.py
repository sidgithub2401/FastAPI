from fastapi import FastAPI
import json 
from fastapi.responses import JSONResponse
from schema.schema import Books, Members

def load_data():
    with open(r"D:\Fast API\Books Fast API\Data\data.json",'r') as f:
        data = json.load(f)
    return data 


def save_data(data):
    with open(r"D:\Fast API\Books Fast API\Data\data.json",'w') as f:
        json.dump(data,f)


app = FastAPI()

@app.get("/fetch_all", tags=["Books"])
async def getdata():
    data = load_data()
    return JSONResponse(status_code=200, content=data)

@app.get("/books", tags=["Books"])
async def get_book_details():
    data = load_data()
    return JSONResponse(status_code=200, content=data["books"])

@app.post("/create/book", tags=["Books"])
async def create_book(book:Books):
    data = load_data()
    books = data["books"]

    for i in books:
        if book.bookId == i["bookId"]:
            return JSONResponse(status_code=400, content="Book cannot be created as it is present already")
        
    books.append(book.model_dump())
    save_data(data)
    return JSONResponse(status_code=201, content="Book details added succesfully")

@app.put("/books/{id}", tags=["Books"])
async def update_books_id(book:Books,id:str):
    data = load_data()
    books = data["books"]

    for i in books:
        if book.bookId == i["bookId"]:
            i["bookId"] = book.model_dump(exclude=book.bookId)
            save_data(data)
            return JSONResponse(status_code=201 , content="Book Data Updated Succefully")
    return JSONResponse(status_code=404, content="Book not found")

@app.delete("/books/{id}",tags=["Books"])
async def delete_book_id(id:str):
    data = load_data()
    books = data["books"]
    for i in books:
        if i["bookId"] == id:
            del i
            save_data(data)
            return JSONResponse(status_code=201 , content="Book deleted Succesfully")
    return JSONResponse(status_code=404, content="Book Not Found")

@app.get("/books/{id}", tags=["Books"])
async def get_book_id(id:str):
    data = load_data()
    books = data["books"]
    for i in books:
        if id in i["bookId"]:
            return JSONResponse(status_code=200, content= i)
    return JSONResponse(status_code=404, content="Not Found")

@app.get("/members", tags=["Members"])
async def get_all_members():
    data = load_data()
    return JSONResponse(status_code=200, content=data["members"])

@app.get("/members/{id}",tags=["Members"])
async def get_members_id(id:str):
    data = load_data()
    members = data["members"]
    for i in members:
        if id in i["memberId"]:
            return JSONResponse(status_code=200, content=i)
    return JSONResponse(status_code=404 , content="Not Found")

@app.post("/create_members", tags=["Members"])
async def create_new_member(member:Members):
    pass




@app.get('/staff', tags=["Staff"])
async def get_all_staff():
    data = load_data()
    return JSONResponse(content=data["staff"])

@app.get("/staff/{id}", tags=["Staff"])
async def get_staff_id(id:str):
    data = load_data()
    staff = data["staff"]
    for i in staff:
        if id in i["staffId"]:
            return JSONResponse(content=i, status_code=200)
    return JSONResponse(content="Not Found", status_code=404)





