# GROUP-7 - lab 1 - variant 7

Implementation of a mutable hash dictionary using separate
chaining collision resolution.

Supports arbitrary keys including `None`, with proper type
hints and comprehensive testing.

## Project structure

- `hash_dict.py` -- implementation of the `HashMap` class.
  Stateful. Uses built-in lists for buckets.
- `hash_dict_test.py` -- unit and PBT tests for `HashMap`.

## Features

- PBT: `test_concat_associativity` (Monoid law)
- PBT: `test_set_get_roundtrip` (State consistency)
- Use the built-in list for storing buckets and a bucket itself
- Support for `None` as valid key and value
- Implement functions/methods for getting/setting value by key

## Contribution

- Zheng Rongzhen (1661342449@qq.com) -- all work.

## Changelog

- 2.4.2026 - 1
  - Implement hash dictionary.
- 1.4.2026 - 1
  - Update hash_dict.
- 31.03.2026 - 1
  - Update README.
- 31.03.2022 - 0
  - Initial

## Design notes

- The dictionary implements the Monoid interface with `empty`
  and `concat` methods.
- Type hints are strictly enforced to pass mypy checks.
