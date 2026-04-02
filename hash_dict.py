from typing import Any, Callable, Iterator, Tuple

class HashMap:
    """Mutable dictionary with separate chaining."""

    def __init__(self, capacity: int = 16) -> None:
        self._buckets: list[list[Tuple[Any, Any]]] = [[] for _ in range(capacity)]
        self._size: int = 0
        self._capacity: int = capacity

    def _bucket_index(self, key: Any) -> int:
        return hash(key) % self._capacity

    def set(self, key: Any, value: Any) -> None:
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key: Any) -> Any:
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def member(self, key: Any) -> bool:
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def remove(self, key):
        index = self._bucket_index(key)
        for i, (k, _) in enumerate(self._buckets[index]):
            if k == key:
                del self._buckets[index][i]
                self._size -= 1
                return
        raise KeyError(key)
    
    def size(self) -> int:
        return self._size
    
    def to_list(self) -> list[Tuple[Any, Any]]:
        result: list[Tuple[Any, Any]] = []
        for bucket in self._buckets:
            for item in bucket:
                result.append(item)
        return result

    def from_list(self, lst: list[Tuple[Any, Any]]) -> None:
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for key, value in lst:
            self.set(key, value)

    def map(self, f: Callable[[Any], Any]) -> None:
        for i in range(self._capacity):
            self._buckets[i] = [(k, f(v)) for k, v in self._buckets[i]]

    @classmethod
    def empty(cls) -> 'HashMap':
        return cls()

    def concat(self, other: 'HashMap') -> 'HashMap':
        result = HashMap()
        for key, value in self:
            result.set(key, value)
        for key, value in other:
            result.set(key, value)
        return result
    
    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        for bucket in self._buckets:
            for item in bucket:
                yield item

    def __str__(self) -> str:
        return " : ".join(str(item) for item in self.to_list())






