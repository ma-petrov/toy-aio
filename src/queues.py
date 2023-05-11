from typing import Any, Iterable
 

class BaseQueue:
    def __init__(self, items: Iterable[Any]):
        self._items = list(items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Any:
        while len(self) > 0:
            yield self.pop()

    def push(self, item: Any) -> None: raise NotImplementedError()
    def pop(self) -> Any | None: raise NotImplementedError()
 

class SimpleQueue(BaseQueue):
    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Any | None:
        return self._items.pop(0)
