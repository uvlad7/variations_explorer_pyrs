"""Type annotations for variations_explorer_pyrs."""

from typing import TypedDict


class StatInfo(TypedDict):
    """Variations statistic info."""
    number_of_variation_groups: int
    count_of_products_in_groups: int
