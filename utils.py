from __future__ import annotations

import hashlib
from enum import Enum, auto
from pathlib import Path
from typing import (
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
)

# ---------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------

Grid = List[str]
RowCol = Tuple[int, int]

T = TypeVar("T")


# ---------------------------------------------------------------------
# Math helpers
# ---------------------------------------------------------------------


def cap(value: int, cap_value: int) -> int:
    """
    Equivalent to Int.cap(cap).
    Wraps positive integers 1..cap_value (never returns 0).
    """
    r = value % cap_value
    return cap_value if r == 0 else r


def hex_to_binary(ch: str) -> str:
    """
    Equivalent to Char.hexToBinary().
    ch should be a single hex character.
    """
    return bin(int(ch, 16))[2:].zfill(4)


def gcd(a: int, b: int) -> int:
    """Euclidean algorithm (like the Kotlin version)."""
    while b != 0:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """Least common multiple (like the Kotlin version)."""
    return abs(a * b) // gcd(a, b)


# ---------------------------------------------------------------------
# Interval / range helpers
# ---------------------------------------------------------------------


def int_range_intersects(a: range, b: range) -> bool:
    """
    Rough equivalent of IntRange.intersects(r: IntRange).

    NOTE: Python range is [start, stop) while Kotlin IntRange is inclusive.
    This function treats the ranges as integer intervals and checks if
    they share at least one integer.
    """
    if a.start >= a.stop or b.start >= b.stop:
        # empty ranges (like range(5, 5))
        return False

    a_start, a_end_inclusive = a.start, a.stop - 1
    b_start, b_end_inclusive = b.start, b.stop - 1
    return a_start <= b_end_inclusive and a_end_inclusive >= b_start


def float_interval_intersects(a: Tuple[float, float], b: Tuple[float, float]) -> bool:
    """
    Equivalent to Pair<Double, Double>.intersects(r).
    Treats (first, second) as a closed interval [first, second].
    """
    return a[0] <= b[1] and a[1] >= b[0]


# ---------------------------------------------------------------------
# Permutations with repetition
# ---------------------------------------------------------------------


def permute(
    curr: List[T],
    max_length: int,
    result: List[List[T]],
    ops: Set[T],
) -> None:
    """
    Equivalent to the Kotlin permute function:

    fun <T> permute(
        curr: MutableList<T>,
        maxLength: Int,
        result: MutableList<List<T>>,
        ops: Set<T>
    )

    Generates sequences (with repetition) of length max_length,
    appending each to result.
    """
    if len(curr) == max_length:
        # Append a copy to avoid later mutation issues
        result.append(list(curr))
        return

    for op in ops:
        curr.append(op)
        permute(curr, max_length, result, ops)
        curr.pop()


# ---------------------------------------------------------------------
# Direction enum and operations
# ---------------------------------------------------------------------


class Dir(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def rotate(self) -> "Dir":
        """Equivalent to Kotlin Dir.rotate(). (Clockwise 90°)"""
        if self is Dir.UP:
            return Dir.RIGHT
        if self is Dir.DOWN:
            return Dir.LEFT
        if self is Dir.LEFT:
            return Dir.UP
        if self is Dir.RIGHT:
            return Dir.DOWN
        raise ValueError(f"Unknown direction: {self}")

    def clockwise(self) -> "Dir":
        """Alias for rotate()."""
        return self.rotate()

    def counter_clockwise(self) -> "Dir":
        """Equivalent to Kotlin Dir.counterClockwise()."""
        if self is Dir.UP:
            return Dir.LEFT
        if self is Dir.DOWN:
            return Dir.RIGHT
        if self is Dir.LEFT:
            return Dir.DOWN
        if self is Dir.RIGHT:
            return Dir.UP
        raise ValueError(f"Unknown direction: {self}")


# ---------------------------------------------------------------------
# Coordinate and grid helpers
# ---------------------------------------------------------------------


def get_distance(a: RowCol, b: RowCol) -> int:
    """Manhattan distance between two cells."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def next_pos(rc: RowCol, d: Dir) -> RowCol:
    """Equivalent of RowCol.next(d) in Kotlin."""
    r, c = rc
    if d is Dir.UP:
        return r - 1, c
    if d is Dir.DOWN:
        return r + 1, c
    if d is Dir.LEFT:
        return r, c - 1
    if d is Dir.RIGHT:
        return r, c + 1
    raise ValueError(f"Unknown direction: {d}")


def grid_rows(grid: Grid) -> int:
    return len(grid)


def grid_cols(grid: Grid) -> int:
    return len(grid[0]) if grid else 0


def grid_is_inbound(grid: Grid, rc: RowCol) -> bool:
    """Check if a coordinate is inside the grid."""
    r, c = rc
    if not grid:
        return False
    max_r = len(grid) - 1
    max_c = len(grid[0]) - 1
    return 0 <= r <= max_r and 0 <= c <= max_c


def grid_get(grid: Grid, r: int, c: int) -> str:
    """
    Rough equivalent of Grid.get(r, c) (without Result).
    Raises IndexError if out of bounds.
    """
    return grid[r][c]


def grid_get_or_none(grid: Grid, rc: RowCol) -> Optional[str]:
    """Equivalent to Grid.getOrNull(rc) in Kotlin."""
    r, c = rc
    try:
        return grid[r][c]
    except IndexError:
        return None


def grid_int(grid: Grid, r: int, c: int) -> Optional[int]:
    """Equivalent to Grid.int(r, c) using digitToInt()."""
    try:
        return int(grid[r][c])
    except (IndexError, ValueError):
        return None


def grid_int_rc(grid: Grid, rc: RowCol) -> Optional[int]:
    r, c = rc
    return grid_int(grid, r, c)


def grid_long(grid: Grid, r: int, c: int) -> Optional[int]:
    """Same as grid_int but returns Python int (arbitrary precision)."""
    return grid_int(grid, r, c)


def grid_long_rc(grid: Grid, rc: RowCol) -> Optional[int]:
    r, c = rc
    return grid_long(grid, r, c)


def grid_set(grid: Grid, r: int, c: int, v: str) -> None:
    """
    Equivalent to Grid.set(r, c, v) which rebuilds the row string.
    v must be a single-character string.
    """
    row_list = list(grid[r])
    row_list[c] = v
    grid[r] = "".join(row_list)


def grid_set_rc(grid: Grid, rc: RowCol, v: str) -> None:
    r, c = rc
    grid_set(grid, r, c, v)


def grid_sequence(grid: Grid) -> Iterator[RowCol]:
    """
    Equivalent of Grid.sequence() – yields all (row, col) pairs.
    """
    for r in range(grid_rows(grid)):
        for c in range(grid_cols(grid)):
            yield (r, c)


def grid_swap(grid: Grid, x: RowCol, y: RowCol) -> None:
    """
    Equivalent of Grid.swap(x, y).
    Swaps two cells if both are in bounds.
    """
    xv = grid_get_or_none(grid, x)
    yv = grid_get_or_none(grid, y)
    if xv is not None and yv is not None:
        grid_set_rc(grid, x, yv)
        grid_set_rc(grid, y, xv)


def print_grid(grid: Grid) -> None:
    """
    Equivalent of Grid.print() where each cell is spaced.
    """
    for row in grid:
        print(" ".join(row))


# ---------------------------------------------------------------------
# List helpers
# ---------------------------------------------------------------------


def unique_pairs(lst: Sequence[T]) -> Iterator[Tuple[T, T]]:
    """
    Equivalent to List<T>.uniquePairs().
    Yields all (x, y) with x < y by index.
    """
    n = len(lst)
    for i in range(n):
        for j in range(i + 1, n):
            yield lst[i], lst[j]
