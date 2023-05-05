from fastapi import FastAPI, Depends, Body
from fastapi.responses import FileResponse, JSONResponse

from database import *
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def main():
    return FileResponse("public/index.html")


@app.get('/api/users')
def get_users(db: Session = Depends(get_db)):
    return db.query(Person).all()


@app.get('/api/users/{id}')
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Person).filter(Person.id == id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found!"})
    return user


@app.post('/api/users')
def create_user(data=Body(), db: Session = Depends(get_db)):
    user = Person(name=data.get('name'), age=data.get('age'))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.put('/api/users')
def edit_user(data=Body(), db: Session = Depends(get_db)):
    user = db.query(Person).filter(Person.id == data.get("id")).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found!"})
    user.name = data.get("name")
    user.age = data.get("age")
    db.commit()
    db.refresh(user)
    return user


@app.delete('/api/users/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Person).filter(Person.id == id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found!"})
    db.delete(user)
    db.commit()
    return user

