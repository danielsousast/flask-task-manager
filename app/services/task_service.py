from app.extensions import db
from app.models.task import Task


def get_all_tasks():
    return Task.query.order_by(Task.id.desc()).all()


def get_task_by_id(task_id):
    return db.session.get(Task, task_id)


def create_task(data):
    task = Task(**data)

    db.session.add(task)
    db.session.commit()

    return task


def update_task(task, data):
    for key, value in data.items():
        setattr(task, key, value)

    db.session.commit()

    return task


def delete_task(task):
    db.session.delete(task)
    db.session.commit()