"""Module to calculate product variations statistics. Implemented in Rust."""
# I don't know another way to have submodule variations_explorer_pyrs.typing written in python
# and variations_explorer_pyrs.VariationsGraph.
# PyO3 doesn't allow to export without creating a module.
# So, *so files work like directories, not like *py files
from .variations_explorer_pyrs import *
