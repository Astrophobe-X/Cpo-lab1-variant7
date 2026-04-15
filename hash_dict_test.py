import pytest
from hypothesis import given, strategies as st
from hash_dict import HashMap


class TestHashMapUnit:
    """Example-based unit tests for specific edge cases."""

    def test_none_key_and_value(self):
        """Verify that None is safely handled 
        as both key and value."""
        h = HashMap()
        h.set(None, "none_value")
        assert h.member(None) is True
        assert h.get(None) == "none_value"

        h.set("none_key", None)
        assert h.member("none_key") is True
        assert h.get("none_key") is None

    def test_key_error_raised(self):
        """Verify that missing keys raise KeyError 
        instead of returning None."""
        h = HashMap()
        with pytest.raises(KeyError):
            h.get("missing_key")
        with pytest.raises(KeyError):
            h.remove("missing_key")

    def test_set_updates_existing_key(self):
        """Verify that setting an existing key updates value 
        without increasing size."""
        h = HashMap()
        h.set("a", 1)
        h.set("a", 99)
        assert h.size() == 1
        assert h.get("a") == 99

    def test_get_retrieves_correct_value(self):
        """Verify that get returns the value bound to a given key."""
        h = HashMap()
        h.set("x", 42)
        assert h.get("x") == 42

    def test_member_returns(self):
        """Verify that member returns True for present keys
        and False for absent ones."""
        h = HashMap()
        h.set("x", 42)
        assert h.member("x") is True
        assert h.member("y") is False

    def test_remove_decreases_size(self):
        """Verify that removing an element decreases 
        size and subsequent remove fails."""
        h = HashMap()
        h.set("a", 1)
        h.set("b", 2)
        h.remove("a")
        assert h.size() == 1
        with pytest.raises(KeyError):
            h.remove("a")

    def test_monoid_empty_and_concat(self):
        """Verify basic Monoid behaviors: empty identity and concatenation."""
        h1 = HashMap()
        h1.set("a", 1)
        h2 = HashMap()
        h2.set("b", 2)

        assert HashMap.empty().concat(h1).size() == 1

        h3 = h1.concat(h2)
        assert h3.size() == 2
        assert h3.get("b") == 2


class TestHashMapPBT:
    """Property-based tests using Hypothesis."""

    key_strategy = st.one_of(st.none(), st.integers(), st.text())
    value_strategy = st.one_of(st.none(), st.integers(), st.text())
    dict_strategy = st.dictionaries(key_strategy, value_strategy)

    @given(dict_strategy)
    def test_roundtrip_from_to_list(self, data: dict):
        """Property: from_list and to_list are inverse operations."""
        h = HashMap()
        h.from_list(list(data.items()))
        # Convert both to dict to ignore ordering
        assert dict(h.to_list()) == data

    @given(st.lists(st.tuples(key_strategy, value_strategy)))
    def test_size_equals_unique_keys(self, pairs: list):
        """Property: size must equal the number of unique keys."""
        h = HashMap()
        for k, v in pairs:
            h.set(k, v)
        assert h.size() == len({k for k, _ in pairs})

    @given(dict_strategy)
    def test_reduce_count_equals_size(self, data: dict):
        """Property: reduce with a counting function must equal size."""
        h = HashMap()
        h.from_list(list(data.items()))
        assert h.reduce(lambda acc, _: acc + 1, 0) == h.size()

    @given(dict_strategy)
    def test_map_preserves_keys_and_structure(self, data: dict):
        """Property: map applies function to values but 
        preserves keys and structure."""
        h = HashMap()
        h.from_list(list(data.items()))

        h.map(lambda v: str(v))

        for k, v_original in data.items():
            assert h.get(k) == str(v_original)
        assert h.size() == len(data)

    @given(dict_strategy, dict_strategy, dict_strategy)
    def test_concat_associativity(self, d1: dict, d2: dict, d3: dict):
        """Property: concat satisfies the associativity 
        law (a+b)+c == a+(b+c)."""
        h1, h2, h3 = HashMap(), HashMap(), HashMap()
        h1.from_list(list(d1.items()))
        h2.from_list(list(d2.items()))
        h3.from_list(list(d3.items()))

        left = h1.concat(h2).concat(h3)
        right = h1.concat(h2.concat(h3))

        assert dict(left.to_list()) == dict(right.to_list())