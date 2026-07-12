"""
Unit tests for function_matcher class.
"""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.function_matcher import FunctionMatcher


@pytest.fixture
def matcher() -> FunctionMatcher:
    """
    Create a FunctionMatcher instance for tests.
    """
    return FunctionMatcher(db=None, visualizer=None)


@pytest.fixture
def train_data() -> pd.DataFrame:
    """
    Create simple training data with two training functions.
    """
    return pd.DataFrame(
        {
            "x": [2.0, 0.0, 1.0],
            "y1": [2.0, 0.0, 1.0],
            "y2": [4.0, 0.0, 2.0],
        }
    )


@pytest.fixture
def ideal_data() -> pd.DataFrame:
    """
    Create ideal data with clear best matches.
    """
    return pd.DataFrame(
        {
            "x": [0.0, 1.0, 2.0],
            "y10": [0.0, 1.0, 2.0],
            "y11": [10.0, 10.0, 10.0],
            "y20": [0.0, 2.0, 4.0],
            "y21": [0.0, 3.0, 6.0],
        }
    )


def test_select_best_ideal_functions(
    matcher: FunctionMatcher,
    train_data: pd.DataFrame,
    ideal_data: pd.DataFrame,
) -> None:
    """
    Test that each training function is matched to the best ideal function.
    """
    result = matcher.select_best_ideal_functions(
        train_data=train_data,
        ideal_data=ideal_data,
    )

    expected = pd.DataFrame(
        {
            "training_function": ["y1", "y2"],
            "ideal_function": ["y10", "y20"],
            "squared_error": [0.0, 0.0],
            "max_deviation": [0.0, 0.0],
        }
    )

    assert_frame_equal(result, expected)


def test_match_test_data(
    matcher: FunctionMatcher,
    ideal_data: pd.DataFrame,
) -> None:
    """
    Test that test data is matched to the closest valid ideal function.
    """
    test_data = pd.DataFrame(
        {
            "x": [1.0, 1.0],
            "y": [1.1, 2.1],
        }
    )
    selected_functions = pd.DataFrame(
        {
            "training_function": ["y1", "y2"],
            "ideal_function": ["y10", "y20"],
            "squared_error": [0.0, 0.0],
            "max_deviation": [0.5, 0.5],
        }
    )

    result = matcher.match_test_data(
        test_data=test_data,
        ideal_data=ideal_data,
        selected_functions=selected_functions
    )

    expected = pd.DataFrame(
        {
            "x": [1.0, 1.0],
            "y": [1.1, 2.1],
            "delta_y": [0.1, 0.1],
            "ideal_function": ["y10", "y20"],
        }
    )

    assert_frame_equal(result, expected)


def test_match_test_data_ignores_points_without_matching_x(
    matcher: FunctionMatcher,
    ideal_data: pd.DataFrame,
) -> None:
    """
    Test that test points without matching ideal x-values are ignored.
    """
    test_data = pd.DataFrame(
        {
            "x": [99.0],
            "y": [1.0],
        }
    )
    selected_functions = pd.DataFrame(
        {
            "training_function": ["y1"],
            "ideal_function": ["y10"],
            "squared_error": [0.0],
            "max_deviation": [1.0],
        }
    )

    result = matcher.match_test_data(
        test_data=test_data,
        ideal_data=ideal_data,
        selected_functions=selected_functions,
    )

    assert result.empty
    assert list(result.columns) == ["x", "y", "delta_y", "ideal_function"]


def test_match_test_data_ignores_points_outside_allowed_deviation(
    matcher: FunctionMatcher,
    ideal_data: pd.DataFrame,
) -> None:
    """
    Test that test points outside the allowed deviation are ignored.
    """
    test_data = pd.DataFrame(
        {
            "x": [1.0],
            "y": [50.0],
        }
    )
    selected_functions = pd.DataFrame(
        {
            "training_function": ["y1"],
            "ideal_function": ["y10"],
            "squared_error": [0.0],
            "max_deviation": [0.5],
        }
    )

    result = matcher.match_test_data(
        test_data=test_data,
        ideal_data=ideal_data,
        selected_functions=selected_functions,
    )

    assert result.empty


def test_prepare_function_data_sorts_by_x_and_uses_x_as_index(
    matcher: FunctionMatcher,
) -> None:
    """
    Test that function data is sorted by x and indexed by x.
    """
    dataframe = pd.DataFrame(
        {
            "x": ["2.0", "0.0", "1.0"],
            "y1": ["2.0", "0.0", "1.0"],
        }
    )

    result = matcher._prepare_function_data(dataframe)

    assert list(result.index) == [0.0, 1.0, 2.0]
    assert list(result["y1"]) == [0.0, 1.0, 2.0]