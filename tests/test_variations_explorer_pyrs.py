from variations_explorer_pyrs import VariationsGraph
from threading import Thread


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
        vg.insert(str(i), [])
        vg.insert(str(i + 100_000), [str(i)])
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
        vg.insert(str(i), [])
        vg.insert(str(i + 100_000), [str(i)])
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
                vg.insert(str(j), [str(j + 1)])
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
