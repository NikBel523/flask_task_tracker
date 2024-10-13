from sqlalchemy.orm import Session
from models import Task


def get_tasks(db: Session):
    return db.query(Task).all()


def create_task(db: Session, title: str, description: str):
    task = Task(title=title, description=description)
    db.add(task)
    return task
