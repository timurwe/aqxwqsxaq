tasks_db = {}

_task_id_counter = 1

def get_tasks(user_id: int):
    user_id = int(user_id)
    return tasks_db.get(user_id, [])

def add_tasks(title: str, deadline: str, user_id: int):
    global _task_id_counter
    user_id = int(user_id)

    if user_id not in tasks_db:
        tasks_db[user_id] = []

    new_task = {
        "id": _task_id_counter,
        "title": title,
        "deadline": deadline,
        "user_id": user_id,
        "is_completed": False,
        "notified": False
    }

    tasks_db[user_id].append(new_task)
    _task_id_counter += 1
    return new_task

def mark_task_completed(user_id: int, task_id: int):
    user_id = int(user_id)
    task_id = int(task_id)

    if user_id in tasks_db:
        for task in tasks_db[user_id]:
            if task["id"] == task_id:
                task["is_completed"] = True
                return task

    return None