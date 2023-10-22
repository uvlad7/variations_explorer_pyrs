import pytest

from variations_explorer_pyrs import VariationsGraph


def create_graph(data):
    vg = VariationsGraph()
    for prod_md5, variations_md5 in data:
        vg.insert(prod_md5, variations_md5)
    return vg


@pytest.fixture
def full_group():
    return create_graph([
        ("1", ["2", "3"]),
        ("2", ["1", "3"]),
        ("3", ["1", "2"]),
    ])


@pytest.fixture
def single_prods():
    return create_graph([
        ("1", []),
        ("2", []),
        ("3", []),
    ])


@pytest.fixture
def partial_group():
    return create_graph([
        ("1", ["2", "3"]),
        ("2", ["1", "3"]),
        ("3", ["1", "2"]),
    ])


@pytest.fixture
def loops():
    return create_graph([
        ("1", ["1"]),
        ("2", ["2", "3"]),
        ("3", ["2", "3"]),
    ])


@pytest.fixture
def duplicates():
    return create_graph([
        ("1", ["2", "3"]),
        ("1", ["1", "3", "4"]),
        ("2", ["1", "3"]),
        ("3", ["1", "2"]),
    ])


@pytest.fixture
def source_node():
    return create_graph([
        ("1", ["2"]),
        ("2", ["1"]),
        ("3", ["1", "2"])  # source node
    ])


@pytest.fixture
def virtual_source_node():
    return create_graph([
        ("1", ["2"]),
        # 2 - virtual node, that connects 1 and 3 source nodes
        ("3", ["2"])
    ])
