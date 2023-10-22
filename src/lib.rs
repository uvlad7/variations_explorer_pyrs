use std::cell::UnsafeCell;
use std::collections::hash_map::Entry;
use std::collections::HashMap;
use std::collections::VecDeque;

use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyString};

struct VariationsGraphNode {
    edges: Vec<u128>,
    group_number: u32,
}

/// Stores graph of product MD5 values and their variants
#[pyclass]
struct VariationsGraph {
    adjacency_map: HashMap<u128, UnsafeCell<VariationsGraphNode>>,
    need_cleanup: bool,
}

#[pymethods]
impl VariationsGraph {
    #[new]
    fn new() -> Self {
        Self { adjacency_map: HashMap::new(), need_cleanup: false }
    }

    #[pyo3(name = "__repr__")]
    fn repr(&self) -> String {
        let mut serialized = "[".to_string();
        for (index, node_ptr) in &self.adjacency_map {
            serialized.push_str("\n  (\"");
            serialized.push_str(&*index.to_string());
            serialized.push_str("\", [");
            unsafe {
                for node in &(*node_ptr.get()).edges {
                    serialized.push_str("\"");
                    serialized.push_str(&*node.to_string());
                    serialized.push_str("\", ");
                }
            }
            serialized.replace_range((serialized.len() - 2).., "]),");
        }
        serialized.push_str("\n]");
        return serialized;
    }

    /// Adds a node and its leaves into the graph. If the node already exist, leaves are concatenated.
    /// Duplicates and self-pointing references are allowed.
    /// :param prod_md5: MD5 string of the product.
    /// :param variations_md5: List of MD5 strings of the leaves
    /// :raises ValueError: If one of the strings cannot be converted into unsigned 128-bit int.
    /// :raises TypeError: If prod_md5 cannot be converted to String, variations_md5 cannot
    /// be converted to Sequence or one of the variations_md5 elements cannot be converted to string.
    /// type: (str, list[str] | typing.Sequence[str]) -> None
    fn insert(&mut self, prod_md5: &str, variations_md5: Vec<&str>) -> PyResult<()> {
        self.insert_impl(prod_md5, variations_md5)
    }

    fn multi_insert(&mut self, data: Vec<(&str, Vec<&str>)>) -> PyResult<()> {
        for (prod_md5, variations_md5) in data {
            let res = self.insert_impl(prod_md5, variations_md5);
            if res.is_err() {
                return res;
            }
        }
        Ok(())
    }

    /// Calculates statistic. Can be safely called multiple times.
    /// type: () -> variations_explorer_pyrs.typing.StatInfo
    fn calc_stats(&mut self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        let stats = self.calc_stats_impl().map_err(|error|
            PyRuntimeError::new_err(error.to_string())
        )?;
        let res: &PyDict = PyDict::new(py);
        res.set_item(PyString::new(py, "number_of_variation_groups"), stats.0)?;
        res.set_item(PyString::new(py, "count_of_products_in_groups"), stats.1)?;
        Ok(res.into())
    }
}

impl VariationsGraph {
    fn insert_impl(&mut self, prod_md5: &str, variations_md5: Vec<&str>) -> PyResult<()> {
        let prod: u128 = u128::from_str_radix(prod_md5, 16).map_err(|error|
            PyValueError::new_err(error.to_string())
        )?;
        let variations_map: Result<Vec<u128>, _> = variations_md5.iter().map(|&val|
            u128::from_str_radix(val, 16)
        ).collect();

        let mut variations: Vec<u128> = variations_map.map_err(|error|
            PyValueError::new_err(error.to_string())
        )?;
        match self.adjacency_map.get_mut(&prod) {
            Some(existing_variations) => {
                unsafe { (*existing_variations.get()).edges.append(&mut variations); }
            }
            None => {
                self.adjacency_map.insert(prod, UnsafeCell::new(VariationsGraphNode {
                    edges: variations,
                    group_number: 0,
                }));
            }
        };
        Ok(())
    }

    fn calc_stats_impl(&mut self) -> Result<(u32, u32), &str> {
        let mut num_groups: u32 = 0;
        let mut prod_count: u32 = 0;
        let mut queue: VecDeque<u128> = VecDeque::new();
        let mut virtual_nodes: HashMap<u128, u32> = HashMap::new();
        if self.need_cleanup {
            for value in self.adjacency_map.values() {
                unsafe { (*value.get()).group_number = 0; }
            }
        }
        self.need_cleanup = true;
        for (index, node_ptr) in &self.adjacency_map {
            unsafe {
                // let Some(node) = self.adjacency_map.get(index) else { continue; };
                let node = node_ptr.get();
                // Just skip single prods
                // If this prod has no variations, but is itself a variation of some prod,
                // we will discover it later.
                if (*node).group_number != 0 ||
                    (*node).edges.is_empty() ||
                    // This should be more efficient, than remove loops on insert
                    !(*node).edges.iter().any(|edge| edge != index) { continue; }
            }

            queue.push_back(*index);
            // match num_groups.checked_add(1) {
            //     Some(v) => num_groups = v,
            //     None => return Err("num_groups overflow")
            // };
            num_groups += 1;

            // Handle source nodes: nodes which don't have any incoming edge
            let mut has_collision = false;
            while let Some(bfs_index) = queue.pop_front() {
                match self.adjacency_map.get(&bfs_index) {
                    Some(bfs_node_ptr) => unsafe {
                        let bfs_node = bfs_node_ptr.get();
                        if (*bfs_node).group_number != 0 {
                            if (*bfs_node).group_number < num_groups { has_collision = true; }
                        } else {
                            (*bfs_node).group_number = num_groups;
                            // match prod_count.checked_add(1) {
                            //     Some(v) => prod_count = v,
                            //     None => return Err("prod_count overflow")
                            // };
                            prod_count += 1;
                            for bfs_edge in &(*bfs_node).edges {
                                queue.push_back(*bfs_edge);
                            }
                        }
                    }
                    None => {
                        match virtual_nodes.entry(bfs_index) {
                            Entry::Occupied(_) => { num_groups -= 1; }
                            Entry::Vacant(entry) => {
                                entry.insert(num_groups);
                                // match prod_count.checked_add(1) {
                                //     Some(v) => prod_count = v,
                                //     None => return Err("prod_count overflow")
                                // };
                                prod_count += 1;
                            }
                        }
                    }
                };
            }
            if has_collision { num_groups -= 1; }
        }
        Ok((num_groups, prod_count))
    }
}

#[pymodule]
fn variations_explorer_pyrs(_py: Python, m: &PyModule) -> PyResult<()> {
    // m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<VariationsGraph>()?;
    Ok(())
}
