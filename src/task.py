from datetime import datetime

from .descriptors import (
    DescriptionField,
    IdField,
    PriorityField,
    RdCreatTime,
    ValidatField,
    TaskValidatError,
)


TASK_NEW = "new"
TASK_PROGRESS = "progress"
TASK_DONE = "done"
TASK_FAILED = "failed"


class StatusField(ValidatField):
    """
    Статус задачи. Разрешены только значения TaskStatus.
    """

    def _validate(self, value: object) -> None:
        allowed = {
            TASK_NEW,
            TASK_PROGRESS,
            TASK_DONE,
            TASK_FAILED,
        }
        if value not in allowed:
            raise TaskValidatError("Недопустимый статус задачи")


class Task:
    """Модель задачи"""

    task_id = IdField()
    description = DescriptionField()
    priority = PriorityField()
    status = StatusField()
    created_at = RdCreatTime()

    def __init__(self, task_id: int | str, description: str, priority = 5, status = TASK_NEW, created_at = None) -> None:
        """
        Создаёт новую задачу.

        :param task_id: идентификатор задачи
        :param description: текст описания задачи
        :param priority: приоритет от 1 до 10
        :param status: статус задачи
        :param created_at: время создания
        :return: None
        """

        self._created_at = created_at or datetime.now()
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.status = status

    @property
    def is_ready(self) -> bool:
        """
        Вычисляемое свойство
        :return: True, если задача готова к выполнению
        """

        return self.status == TASK_NEW and self.priority > 0 #type: ignore

    @property
    def short_description(self) -> str:
        """
        Короткое текстовое представление задачи.
        :return: строка с коротким описанием
        """

        return f"[{self.task_id}] {self.description} (priority={self.priority}, status={self.status})"

    def start(self) -> None:
        """
        Переводит задачу в статус progress.
        :return: None
        """

        if self.status not in (TASK_NEW, TASK_FAILED):
            raise TaskValidatError(
                "Перевести в progress можно только новую или неудавшуюся задачу",
            )
        self.status = TASK_PROGRESS

    def finish(self, success: bool = True) -> None:
        """
        Завершает задачу с успешным или неуспешным результатом.
        :param success: True для DONE, False для FAILED
        :return: None
        """

        if self.status not in (TASK_NEW, TASK_PROGRESS):
            raise TaskValidatError("Завершить можно только активную задачу")
        self.status = TASK_DONE if success else TASK_FAILED

    def to_dict(self) -> dict:
        """
        Представление задачи.
        :return: словарь с полями задачи
        """

        return {
            "id": self.task_id,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat(), #type: ignore
        }

    def __repr__(self) -> str:
        return f"Task({self.short_description})"
