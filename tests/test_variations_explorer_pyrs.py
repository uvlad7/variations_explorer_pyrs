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
