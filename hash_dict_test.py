import pytest
from hypothesis import given, strategies as st
from hash_dict import HashMap


K_PBT = int | str | None
V_PBT = int | str | None


class TestHashMapUnit:
    """Example-based unit tests for edge cases."""

    def test_none_key_and_value(self):
        """Verify None is safely handled as key and value."""
        h: HashMap[str | None, str | None] = HashMap()
        h.set(None, "none_value")
        assert h.member(None) is True
        assert h.get(None) == "none_value"

        h.set("none_key", None)
        assert h.member("none_key") is True
        assert h.get("none_key") is None

    def test_key_error_raised(self):
        """Verify missing keys raise KeyError."""
        h = HashMap()
        with pytest.raises(KeyError):
            h.get("missing_key")
        with pytest.raises(KeyError):
            h.remove("missing_key")

    def test_set_updates_existing_key(self):
        """
        Verify setting an existing key updates value
        without increasing size.
        """
        h: HashMap[str, int] = HashMap()
        h.set("a", 1)
        h.set("a", 99)
        assert h.size() == 1
        assert h.get("a") == 99

    def test_get_retrieves_correct_value(self):
        """Verify get returns the value bound to a key."""
        h: HashMap[str, int] = HashMap()
        h.set("x", 42)
        assert h.get("x") == 42

    def test_member_returns(self):
        """
        Verify member returns True for present keys
        and False for absent ones.
        """
        h: HashMap[str, int] = HashMap()
        h.set("x", 42)
        assert h.member("x") is True
        assert h.member("y") is False

    def test_remove_decreases_size(self):
        """
        Verify removing an element decreases size
        and subsequent remove fails.
        """
        h: HashMap[str, int] = HashMap()
        h.set("a", 1)
        h.set("b", 2)
        h.remove("a")
        assert h.size() == 1
        with pytest.raises(KeyError):
            h.remove("a")

    def test_monoid_empty_and_concat(self):
        """Verify Monoid behaviors: identity and concat."""
        h1: HashMap[str, int] = HashMap()
        h1.set("a", 1)
        h2: HashMap[str, int] = HashMap()
        h2.set("b", 2)

        assert HashMap.empty().concat(h1).size() == 1

        h3 = h1.concat(h2)
        assert h3.size() == 2
        assert h3.get("b") == 2

    def test_eq_method(self):
        """Verify the custom __eq__ method works."""
        h1: HashMap[str, int] = HashMap()
        h1.set("a", 1)
        h2: HashMap[str, int] = HashMap()
        h2.set("a", 1)
        h3: HashMap[str, int] = HashMap()
        h3.set("a", 2)

        assert h1 == h2
        assert h1 != h3
        # Different types
        assert h1 != "not a hashmap"


class TestHashMapPBT:
    """Property-based tests using Hypothesis."""

    key_strategy = st.one_of(
        st.none(), st.integers(), st.text()
    )
    value_strategy = st.one_of(
        st.none(), st.integers(), st.text()
    )
    dict_strategy = st.dictionaries(
        key_strategy, value_strategy
    )

    @given(dict_strategy)
    def test_roundtrip_from_to_list(self, data: dict):
        """Property: from_list and to_list are inverses."""
        h: HashMap[K_PBT, V_PBT] = HashMap()
        h.from_list(list(data.items()))
        # Since data is a native dict, convert to dict
        # via to_list for comparison
        assert dict(h.to_list()) == data

    @given(st.lists(st.tuples(key_strategy, value_strategy)))
    def test_size_equals_unique_keys(self, pairs: list):
        """Property: size must equal unique keys count."""
        h: HashMap[K_PBT, V_PBT] = HashMap()
        for k, v in pairs:
            h.set(k, v)
        assert h.size() == len({k for k, _ in pairs})

    @given(dict_strategy)
    def test_reduce_count_equals_size(self, data: dict):
        """Property: reduce counting must equal size."""
        h: HashMap[K_PBT, V_PBT] = HashMap()
        h.from_list(list(data.items()))
        assert h.reduce(lambda acc, _: acc + 1, 0) == h.size()

    @given(dict_strategy)
    def test_map_preserves_keys_and_structure(
        self, data: dict
    ):
        """
        Property: map applies func to values but
        preserves keys and structure.
        """
        def run_test(data: dict[str, str]):
            h: HashMap[str, str] = HashMap()
            h.from_list(list(data.items()))
            h.map(lambda v: v.upper())
            for k, v_original in data.items():
                assert h.get(k) == v_original.upper()
            assert h.size() == len(data)

        # Because map signature constraint changed,
        # we use a pure str dict here for testing
        is_str_dict = all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in data.items()
        )
        if is_str_dict:
            run_test(data)

    @given(dict_strategy, dict_strategy, dict_strategy)
    def test_concat_associativity(
        self, d1: dict, d2: dict, d3: dict
    ):
        """
        Property: concat satisfies associativity
        law (a+b)+c == a+(b+c).
        """
        h1: HashMap[K_PBT, V_PBT] = HashMap()
        h2: HashMap[K_PBT, V_PBT] = HashMap()
        h3: HashMap[K_PBT, V_PBT] = HashMap()

        h1.from_list(list(d1.items()))
        h2.from_list(list(d2.items()))
        h3.from_list(list(d3.items()))

        left = h1.concat(h2).concat(h3)
        right = h1.concat(h2.concat(h3))

        # Directly use == to trigger custom __eq__
        assert left == right
