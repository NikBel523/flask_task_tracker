from functools import wraps
from flask import Flask, request, jsonify
from database import SessionLocal, engine
from models import Base, Task
from crud import get_tasks, create_task

app = Flask(__name__)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


def db_session(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = route(db, *args, **kwargs)
            return result
        finally:
            db.commit()
            db.close()
    return wrapper


@app.route("/tasks/", methods=["GET"])
@db_session
def read_tasks(db):
    tasks = get_tasks(db)
    return jsonify(
        [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed,
            } for task in tasks
        ]
    )


@app.route("/add_task/", methods=["POST"])
@db_session
def create_task_endpoint(db):
    task_data = request.json
    db_task = Task(title=task_data["title"], description=task_data["description"])
    db_task = create_task(db=db, task=db_task)
    return jsonify({"id": db_task.id, "title": db_task.title, "description": db_task.description,
                    "is_completed": db_task.is_completed}), 201


if __name__ == "__main__":
    app.run(debug=True)
