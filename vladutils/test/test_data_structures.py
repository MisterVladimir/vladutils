# -*- coding: utf-8 -*- 
from enum import IntFlag, auto
import pytest
from typing import List, Set

from vladutils import data_structures as ds


# setting up constants
class ExampleFlag(IntFlag):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()


ARGS = ['first', 'second', 'third']
EXAMPLE_ENUM_DICT_KEYS = [
    ExampleFlag.FIRST, ExampleFlag.SECOND, ExampleFlag.THIRD]


@pytest.fixture
def example_set():
    return set(ARGS)


@pytest.fixture
def example_tracked_set():
    return ds.TrackedSet(ARGS)


@pytest.fixture
def example_enum_dict():
    return ds.EnumDict(zip(EXAMPLE_ENUM_DICT_KEYS, ARGS))


class TestTrackedSet(object):
    def test_add(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        assert example_set == example_tracked_set
        assert example_set == example_tracked_set.added
        assert set() == example_tracked_set.removed

    def test_remove(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        to_remove: str = 'first'
        example_set.remove(to_remove)
        example_tracked_set.remove(to_remove)
        assert example_set == example_tracked_set
        assert set() == example_tracked_set.removed
        assert example_set == example_tracked_set.added

    def test_clear(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        example_tracked_set.clear()
        assert example_tracked_set == set()
        assert example_tracked_set.removed == example_set

    def test_difference_update(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        pass

    def test_discard(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        pass

    def test_intersection_update(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        pass

    def test_symmetric_difference_update(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        pass

    def test_pop(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        pass

    def test_update(self, example_set: Set[str], example_tracked_set: Set[str]) -> None:
        pass


class TestEnumDict(object):
    def test_get_item(self, example_enum_dict) -> None:
        assert example_enum_dict[ExampleFlag.FIRST] == [ARGS[0]]
        assert example_enum_dict[ExampleFlag.SECOND] == [ARGS[1]]

        first_and_second_flag = ExampleFlag.FIRST | ExampleFlag.SECOND
        assert example_enum_dict[first_and_second_flag] == ARGS[:2]

    def test_set_item(self, example_enum_dict) -> None:
        new_first: str = 'first changed'
        example_enum_dict[ExampleFlag.FIRST] = new_first
        assert example_enum_dict[ExampleFlag.FIRST] == [new_first, ]

        # test resetting multiple items
        first_and_second_flag = ExampleFlag.FIRST | ExampleFlag.SECOND
        new_first_and_second: str = 'new first and second'
        example_enum_dict[first_and_second_flag] = new_first_and_second
        assert example_enum_dict[first_and_second_flag] == [
            new_first_and_second, new_first_and_second]

