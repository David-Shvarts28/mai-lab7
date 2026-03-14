from .task import Task


def main() -> None:
    """
    Cоздаёт одну задачу и показывает её основные свойства.
    :return: None
    """

    task = Task(id=1, description="Пример задачи", priority=7)
    print("Создана задача:", task.short_description)
    print("Готова к выполнению:", task.is_ready)
    print("Время создания:", task.created_at)


if __name__ == "__main__":
    main()
