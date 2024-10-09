from flask import Flask, request, jsonify
from database import SessionLocal, engine
from models import Base, Task
from crud import get_tasks, create_task

app = Flask(__name__)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.route("/tasks/", methods=["GET"])
def read_tasks():
    db = next(get_db())
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
def create_task_endpoint():
    task_data = request.json
    db = next(get_db())
    # Создаём новый объект Task
    db_task = Task(title=task_data["title"], description=task_data["description"])
    db_task = create_task(db=db, task=db_task)
    return jsonify({"id": db_task.id, "title": db_task.title, "description": db_task.description,
                    "is_completed": db_task.is_completed}), 201


if __name__ == "__main__":
    app.run(debug=True)
