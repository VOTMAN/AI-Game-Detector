from .models import PredResults
from sqlmodel import Session, SQLModel, create_engine, select

SQLLITE_URL = "sqlite:///results.db"
engine = create_engine(SQLLITE_URL)

def initDB():
    SQLModel.metadata.create_all(engine)

def saveResult(result: PredResults):
    try:
        with Session(engine) as session:
            session.add(result)
            session.commit()
    except Exception as e:
        print(e)
        return { "success": False, "error": e }    
    return { "success": True }

def getResult(id: str):
    try:
        with Session(engine) as session:
            # statement = select(PredResults).where(PredResults.id == id)
            # res = session.exec(statement).first()
            # print(res)
            # return res
            return session.get(PredResults, id)
    except Exception as e:
        print(e)
        return { "success": False, "error": e }    

def getAllResults() -> list[PredResults]:
    try:
        with Session(engine) as session:
            statement = select(PredResults)
            results = session.exec(statement)
            res = results.all()
            return res
    except Exception as e:
        print(e)
        return { "success": False, "error": e }    
