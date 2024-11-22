import pytest
from task1.solution import sum_two


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
def test_correct_inputs(a, b, expected):
    assert sum_two(a, b) == expected


@pytest.mark.parametrize("a, b", [("1", 2), (1, 2.4), (None, 2), ([3, 4], True)])
def test_incorrect_type(a, b):
    with pytest.raises(TypeError):
        sum_two(a, b)
