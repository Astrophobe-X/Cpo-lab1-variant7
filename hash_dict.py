from typing import Any, Callable, Iterator, Tuple


class HashMap:
    """Mutable dictionary implementation using separate chaining."""

    def __init__(self, capacity: int = 16) -> None:
        self._capacity: int = max(capacity, 1)
        self._buckets: list[list[Tuple[Any, Any]]] = [[] for _ in range(self._capacity)]
        self._size: int = 0

    def _bucket_index(self, key: Any) -> int:
        """Calculate the bucket index for a given key."""
        return hash(key) % self._capacity

    def set(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair."""
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key: Any) -> Any:
        """Retrieve value by key. Raises KeyError if not found."""
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def member(self, key: Any) -> bool:
        """Check if a key exists in the dictionary."""
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def remove(self, key: Any) -> None:
        """Remove a key-value pair by key. Raises KeyError if not found."""
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def size(self) -> int:
        """Return the number of elements in the dictionary."""
        return self._size

    def to_list(self) -> list[Tuple[Any, Any]]:
        """Convert the dictionary to a list of tuples."""
        result: list[Tuple[Any, Any]] = []
        for bucket in self._buckets:
            result.extend(bucket)
        return result

    def from_list(self, lst: list[Tuple[Any, Any]]) -> None:
        """Clear current state and populate from a list of tuples."""
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for key, value in lst:
            self.set(key, value)

    def map(self, f: Callable[[Any], Any]) -> None:
        """Apply a function to all values, keeping keys unchanged."""
        for i in range(self._capacity):
            self._buckets[i] = [(k, f(v)) for k, v in self._buckets[i]]

    def reduce(self, f: Callable[[Any, Any], Any], initial_state: Any) -> Any:
        """Reduce the dictionary's values to a single value."""
        state = initial_state
        for bucket in self._buckets:
            for _, v in bucket:
                state = f(state, v)
        return state

    @classmethod
    def empty(cls) -> 'HashMap':
        """Return an empty instance of HashMap (Monoid identity)."""
        return cls()

    def concat(self, other: 'HashMap') -> 'HashMap':
        """Concatenate two HashMaps (Monoid operation)."""
        result = HashMap()
        for key, value in self:
            result.set(key, value)
        for key, value in other:
            result.set(key, value)
        return result

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        """Make HashMap iterable, yielding tuples."""
        for bucket in self._buckets:
            yield from bucket

    def __str__(self) -> str:
        """String representation of the HashMap."""
        return " : ".join(str(item) for item in self.to_list())