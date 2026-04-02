import pytest
from hypothesis import given, strategies as st
from hash_dict import HashMap


class TestHashMapUnit:
    """Example-based unit tests for specific edge cases."""

    def test_none_key_and_value(self):
        """Verify that None is safely handled as both key and value."""
        h = HashMap()
        h.set(None, "none_value")
        assert h.member(None) is True
        assert h.get(None) == "none_value"

        h.set("none_key", None)
        assert h.member("none_key") is True
        assert h.get("none_key") is None

    def test_key_error_raised(self):
        """Verify that missing keys raise KeyError instead of returning None."""
        h = HashMap()
        with pytest.raises(KeyError):
            h.get("missing_key")
        with pytest.raises(KeyError):
            h.remove("missing_key")

    def test_set_updates_existing_key(self):
        """Verify that setting an existing key updates value without increasing size."""
        h = HashMap()
        h.set("a", 1)
        h.set("a", 99)
        assert h.size() == 1
        assert h.get("a") == 99

    def test_remove_decreases_size(self):
        """Verify that removing an element decreases size and subsequent remove fails."""
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





