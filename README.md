# GROUP-7 - lab 1 - variant 7

Implementation of a mutable hash dictionary using separate
chaining collision resolution.

Supports arbitrary keys including `None`, with proper type
hints and comprehensive testing.

## Project structure

- `hash_dict.py` -- implementation of the `HashMap` class.
- `hash_dict_test.py` -- unit and PBT tests for `HashMap`.

## Features

- Use the built-in list for storing buckets and a bucket itself
- Support for `None` as valid key and value
- Implement functions/methods for getting/setting value by key
- Type hints included for better readability.
- Functional methods `map` to apply a function to all values,
  and `reduce` to combine values into a single result.
- Monoid interface `empty` to create an empty map, and `concat`
  to merge two maps together.

## Contribution

- Zheng Rongzhen (1661342449@qq.com) -- all work.

## Changelog

- 15.4.2026 - 7
  Sanity check.
- 15.4.2026 - 6
  Improve all.
- 4.4.2026 - 5
  Implement PBT tests.
- 2.4.2026 - 4
  Implement unit tests.
- 2.4.2026 - 3
  Implement hash dictionary.
- 1.4.2026 - 2
  Update hash_dict.
- 31.03.2026 - 1
  Update README.
- 31.03.2022 - 0
  Initial

## Design notes

- Type hints are strictly enforced to pass mypy checks.
- Map Behavior: The map method only transforms the values and
  leaves the keys completely alone. This is because changing a
  key would mess up its bucket location.
- Concat Behavior: When using concat to merge two maps,if they
  happen to share the same key, the value from the second map
  will overwrite the value from the first map.
