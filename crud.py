from sqlalchemy.orm import Session
from models import Task


def get_tasks(db: Session):
    return db.query(Task).all()


def create_task(db: Session, task: Task):
    db.add(task)
    return task
