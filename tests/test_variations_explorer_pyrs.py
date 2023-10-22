import os
import random
from threading import Thread

import pytest

from conftest import hex_str, create_graph
from variations_explorer_pyrs import VariationsGraph


def test_multi(full_group, partial_group):
    assert full_group.calc_stats() == {
        "number_of_variation_groups": 1,
        "count_of_products_in_groups": 3,
    }
    assert partial_group.calc_stats() == {
        "number_of_variation_groups": 1,
        "count_of_products_in_groups": 3,
    }


def test_single(single_prods):
    assert single_prods.calc_stats() == {
        "number_of_variation_groups": 0,
        "count_of_products_in_groups": 0,
    }


def test_leaves():
    """This test isn't perfect, since here I want to check leaves that
    are iterated over in the main loop before they're visited,
    but the order in HashMap is unpredictable."""
    vg = VariationsGraph()
    for i in range(100_000):
        vg.insert(hex_str(i), [])
        vg.insert(hex_str(i + 100_000), [hex_str(i)])
    assert vg.calc_stats() == {
        "number_of_variation_groups": 100_000,
        "count_of_products_in_groups": 200_000,
    }


def test_loops(loops):
    assert loops.calc_stats() == {
        "number_of_variation_groups": 1,
        "count_of_products_in_groups": 2,
    }


def test_duplicates(duplicates):
    assert duplicates.calc_stats() == {
        "number_of_variation_groups": 1,
        "count_of_products_in_groups": 4,
    }


def test_threading(reraise):
    vg = VariationsGraph()
    for i in range(1000):
        vg.insert(hex_str(i), [])
        vg.insert(hex_str(i + 100_000), [hex_str(i)])
    expected = {
        "number_of_variation_groups": 1000,
        "count_of_products_in_groups": 2000,
    }

    def run():
        with reraise:
            assert expected == vg.calc_stats()

    threads = map(lambda _: Thread(target=run),
                  range(1000))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    vg = VariationsGraph()

    def calc_or_insert(j):
        with reraise:
            if j % 2 == 0:
                vg.insert(hex_str(j), [hex_str(j + 1)])
            else:
                vg.calc_stats()

    threads = map(lambda j: Thread(target=calc_or_insert, args=[j]),
                  range(1000))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert vg.calc_stats() == {
        "number_of_variation_groups": 500,
        "count_of_products_in_groups": 1000,
    }


def test_multi_insert():
    vg = VariationsGraph()
    with pytest.raises(ValueError):
        vg.multi_insert([
            ("1", ["2", "3"]),
            ("4", ["5", "g"]),
            ("7", ["8", "9"]),
        ])
    assert vg.calc_stats() == {
        "number_of_variation_groups": 1,
        "count_of_products_in_groups": 3,
    }

    vg_single = VariationsGraph()
    vg_multi = VariationsGraph()
    data = [
        (
            hex_str(i),
            [
                hex_str(j) for j in range(i - (i % 10), i - (i % 10) + 10) if j != i
            ]
        )
        for i in range(100)
    ]

    for prod_md5, variations_md5 in data:
        vg_single.insert(prod_md5, variations_md5)
    vg_multi.multi_insert(data)

    assert set(repr(vg_single).splitlines()[1:-1]) == set(repr(vg_multi).splitlines()[1:-1])


def test_repr(full_group):
    # Lines order is not predictable
    assert set(repr(full_group).splitlines()[1:-1]) == set("""[
  ("1", ["2", "3"]),
  ("2", ["1", "3"]),
  ("3", ["1", "2"]),
]""".splitlines()[1:-1])

    assert repr(create_graph([("10", ["20", "30"])])) == """[
  ("10", ["20", "30"]),
]"""


def test_source_nodes(source_node, virtual_source_node):
    assert source_node.calc_stats() == {
        "number_of_variation_groups": 1,
        "count_of_products_in_groups": 3,
    }

    assert virtual_source_node.calc_stats() == {
        "number_of_variation_groups": 1,
        "count_of_products_in_groups": 4,
    }


@pytest.mark.report_uss
@pytest.mark.report_tracemalloc
@pytest.mark.report_duration
@pytest.mark.skipif(os.environ.get("I_HAVE_A_LOT_OF_TIME", "false") != "true",
                    reason="I don't have a lot of time")
def test_benchmark():
    vg = VariationsGraph()
    for i in range(100_000):
        vg.insert(hex_str(i), [hex_str(random.randint(0, 100_000)) for _ in range(20)])

    vg.calc_stats()
