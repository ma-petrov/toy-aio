from typing import Any, Generator, List

from .queues import SimpleQueue


class Task:
    def __init__(self, task: Generator):
        if not isinstance(task, Generator):
            raise TypeError(f'task is expected to be <Generator>, but got {type(task)}')
        self._task = task
        self._result = None

    def get_result(self) -> Any:
        return self._result


class Loop:
    def __init__(self, tasks: Generator | List[Generator]) -> None:
        if isinstance(tasks, Generator):
            tasks = [tasks]
        self._tasks = [Task(t) for t in tasks]
        self._queue = SimpleQueue(self._tasks)
        
    def run(self):
        for curr_task in self._queue:
            try:
                next(curr_task._task)
                self._queue.push(curr_task)
            except StopIteration as e:
                curr_task._result = e.value
        return [t.get_result() for t in self._tasks]