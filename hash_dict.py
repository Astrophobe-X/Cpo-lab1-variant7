from typing import TypeVar, Generic, Callable, Iterator, Tuple, Hashable

# K must be hashable, V can be any type
K = TypeVar('K', bound=Hashable)
V = TypeVar('V')
# R is for the accumulator type in the reduce method
R = TypeVar('R')


class HashMap(Generic[K, V]):
    """Mutable dictionary using separate chaining."""

    def __init__(self, capacity: int = 16) -> None:
        self._capacity: int = max(capacity, 1)
        # Replace Any with generics
        self._buckets: list[list[Tuple[K, V]]] = [
            [] for _ in range(self._capacity)
        ]
        self._size: int = 0

    def _bucket_index(self, key: K) -> int:
        """Calculate the bucket index for a given key."""
        return hash(key) % self._capacity

    def set(self, key: K, value: V) -> None:
        """Insert or update a key-value pair."""
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key: K) -> V:
        """Retrieve value by key. Raises KeyError if not found."""
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def member(self, key: K) -> bool:
        """Check if a key exists in the dictionary."""
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def remove(self, key: K) -> None:
        """Remove a key-value pair. Raises KeyError if missing."""
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

    def to_list(self) -> list[Tuple[K, V]]:
        """Convert the dictionary to a list of tuples."""
        result: list[Tuple[K, V]] = []
        for bucket in self._buckets:
            result.extend(bucket)
        return result

    def from_list(self, lst: list[Tuple[K, V]]) -> None:
        """Clear current state and populate from list of tuples."""
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for key, value in lst:
            self.set(key, value)

    def map(self, f: Callable[[V], V]) -> None:
        """Apply a function to all values, keeping keys."""
        for i in range(self._capacity):
            self._buckets[i] = [
                (k, f(v)) for k, v in self._buckets[i]
            ]

    def reduce(self, f: Callable[[R, V], R], initial_state: R) -> R:
        """Reduce the dictionary's values to a single value."""
        state = initial_state
        for bucket in self._buckets:
            for _, v in bucket:
                state = f(state, v)
        return state

    @classmethod
    def empty(cls) -> 'HashMap[K, V]':
        """Return an empty instance of HashMap."""
        return cls()

    def concat(self, other: 'HashMap[K, V]') -> 'HashMap[K, V]':
        """Concatenate two HashMaps (Monoid operation)."""
        result: HashMap[K, V] = HashMap()
        for key, value in self:
            result.set(key, value)
        for key, value in other:
            result.set(key, value)
        return result

    def __iter__(self) -> Iterator[Tuple[K, V]]:
        """Make HashMap iterable, yielding tuples."""
        for bucket in self._buckets:
            yield from bucket

    def __eq__(self, other: object) -> bool:
        """Compare two HashMaps for equality."""

        if not isinstance(other, HashMap):
            return False

        if self._size != other._size:
            return False

        for k, v in self:
            if not other.member(k) or other.get(k) != v:
                return False
        return True

    def __str__(self) -> str:
        """String representation of the HashMap."""
        return " : ".join(str(item) for item in self.to_list())
