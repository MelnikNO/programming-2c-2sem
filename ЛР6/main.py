from http.client import HTTPException
from typing import Union, Optional, List
from fastapi import FastAPI, HTTPException
import locale
from datetime import datetime
from pydantic import BaseModel

from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

class TermDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str = Field(index=True, unique=True)
    description: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


engine = create_engine('mysql+pymysql://user:3570@db/mysqldb')


app = FastAPI()

class Valute(BaseModel):
    name: str
    time_n_date: Union[str, None] = ""
    price: float


class Term(BaseModel):
    description: str


def init_default_terms():
    default_terms = {
        'REST': '«передача репрезентативного состояния» или «передача „самоописываемого“ состояния») — архитектурный стиль взаимодействия компонентов распределённого приложения в сети.',
        'RPC': 'Удалённый вызов процедур (Remote Procedure Call, RPC) — это механизм, который позволяет одной программе вызывать процедуры или функции другой программы, расположенной на другом компьютере в сети.'
    }

    with Session(engine) as session:
        for keyword, description in default_terms.items():
            existing = session.exec(select(TermDB).where(TermDB.keyword == keyword)).first()
            if not existing:
                db_term = TermDB(keyword=keyword, description=description)
                session.add(db_term)
        session.commit()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    init_default_terms()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/author/{author_name}")
def read_author(author_name: str):
    locale.setlocale(locale.LC_ALL,'ru-RU')
    return {"author_name": author_name, "datetime": datetime.now().strftime("%d.%m.%Y %H:%M")}


@app.get("/valute/{valute_id}")
def read_valute(valute_id: str, _valute: Valute):
    return {"valute_id": valute_id, "valute": _valute.name, "value": _valute.value}

@app.put("/valute/{valute_id}")
def update_valute(valute_id: str, _valute: Valute):
    return {"valute_name": _valute.name, "valute_id": valute_id}


@app.get("/terms", response_model=List[TermDB])
def get_all_terms():
    with Session(engine) as session:
        return session.exec(select(TermDB)).all()


@app.get("/terms/{keyword}", response_model=TermDB)
def get_term(keyword: str):
    with Session(engine) as session:
        term = session.exec(select(TermDB).where(TermDB.keyword == keyword)).first()
        if not term:
            raise HTTPException(status_code=404, detail="Term not found")
        return term


@app.post("/terms/{keyword}", response_model=TermDB)
def create_term(keyword: str, term: Term):
    with Session(engine) as session:
        # Проверка на существующий термин
        existing = session.exec(select(TermDB).where(TermDB.keyword == keyword)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Term already exists")

        db_term = TermDB(keyword=keyword, description=term.description)
        session.add(db_term)
        session.commit()
        session.refresh(db_term)
        return db_term


@app.put("/terms/{keyword}", response_model=TermDB)
def update_term(terms: str, term: Term):
    with Session(engine) as session:
        db_term = session.exec(select(TermDB).where(TermDB.terms == terms)).first()
        if not db_term:
            raise HTTPException(status_code=404, detail="Term not found")

        db_term.description = term.description
        db_term.updated_at = datetime.now()
        session.add(db_term)
        session.commit()
        session.refresh(db_term)
        return db_term


@app.delete("/terms/{keyword}")
def delete_term(keyword: str):
    with Session(engine) as session:
        db_term = session.exec(select(TermDB).where(TermDB.keyword == keyword)).first()
        if not db_term:
            raise HTTPException(status_code=404, detail="Term not found")

        session.delete(db_term)
        session.commit()
        return {"message": "Term deleted successfully"}

