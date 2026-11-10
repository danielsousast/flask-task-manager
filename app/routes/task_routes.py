from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.schemas.task_schema import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskResponseSchema
)

from app.services import task_service


task_bp = Blueprint("tasks", __name__)


@task_bp.get("/")
def list_tasks():
    tasks = task_service.get_all_tasks()

    return jsonify([
        TaskResponseSchema.model_validate(task).model_dump()
        for task in tasks
    ]), 200


@task_bp.get("/<int:task_id>")
def get_task(task_id):
    task = task_service.get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(
        TaskResponseSchema.model_validate(task).model_dump()
    ), 200


@task_bp.post("/")
def create_task():
    try:
        data = TaskCreateSchema.model_validate(
            request.get_json()
        )

        task = task_service.create_task(
            data.model_dump()
        )

        return jsonify(
            TaskResponseSchema.model_validate(task).model_dump()
        ), 201

    except ValidationError as error:
        return jsonify({
            "error": "Validation error",
            "details": error.errors()
        }), 400


@task_bp.patch("/<int:task_id>")
def update_task(task_id):
    task = task_service.get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    try:
        data = TaskUpdateSchema.model_validate(
            request.get_json()
        )

        updated_task = task_service.update_task(
            task,
            data.model_dump(exclude_unset=True)
        )

        return jsonify(
            TaskResponseSchema.model_validate(
                updated_task
            ).model_dump()
        ), 200

    except ValidationError as error:
        return jsonify({
            "error": "Validation error",
            "details": error.errors()
        }), 400


@task_bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = task_service.get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    task_service.delete_task(task)

    return jsonify({
        "message": "Task deleted successfully"
    }), 200