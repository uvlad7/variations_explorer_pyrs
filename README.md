# Package variations_explorer_pyrs

Helps to calculate product variations statistic. Implemented in rust.

# Development

Install dependencies

    pipenv install

Build and install the package into the virtual env

    pipenv run maturin develop

Build the crate into python packages

    pipenv run maturin build

Run tests

    pipenv run pytest

Run Rust linter

    cargo clippy [--fix] [-- --no-deps]

Local Rust and Python versions are managed by [rtx](.rtx.toml)