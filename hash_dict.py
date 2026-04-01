from typing import Any, Callable, Iterator, Tuple

class HashMap:
    """Mutable dictionary with separate chaining."""

    def __init__(self, capacity: int = 16) -> None:
        self._buckets: list[list[Tuple[Any, Any]]] = [[] for _ in range(capacity)]
        self._size: int = 0
        self._capacity: int = capacity

    def _bucket_index(self, key: Any) -> int:
        return hash(key) % self._capacity

    def put(self, key: Any, value: Any) -> None:
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
    
    def remove(self, key):
        index = self._bucket_index(key)
        for i, (k, _) in enumerate(self._buckets[index]):
            if k == key:
                del self._buckets[index][i]
                self._size -= 1
                return
        raise KeyError(key)

    

