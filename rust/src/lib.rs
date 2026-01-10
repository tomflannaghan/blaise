use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::collections::HashMap;
use std::f64::INFINITY;

fn bh_score(text: &str, n: usize, dist: &HashMap<String, f64>) -> f64 {
    if text.len() < n {
        return INFINITY;
    }

    let mut counts: HashMap<String, usize> = HashMap::new();
    for i in 0..=(text.len() - n) {
        let ngram = &text[i..i + n];
        if dist.contains_key(ngram) {
            if let Some(x) = counts.get_mut(ngram) {
                *x += 1;
            }
        }
    }
    let total: usize = counts.values().sum();
    let mut result = 0.0;
    for (k, c) in counts.iter() {
        let term: f64 = (*c as f64) * dist.get(k).unwrap();
        result += (term / total as f64).sqrt()
    }
    return -result.ln();
}

#[pyfunction]
fn bh_score_many(text: Vec<String>, n: usize, dist: HashMap<String, f64>) -> PyResult<Vec<f64>> {
    let x: Vec<f64> = text.iter().map(|s| bh_score(s, n, &dist)).collect();
    Ok(x)
}

#[pyfunction]
fn calculate_ngrams(py: Python, text: &str, n: usize) -> PyResult<PyObject> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be >= 1"));
    }
    if text.len() < n {
        return Ok(PyDict::new(py).into());
    }
    let mut counts: HashMap<String, usize> = HashMap::new();
    for i in 0..=(text.len() - n) {
        let ngram = &text[i..i + n];
        *counts.entry(ngram.to_string()).or_insert(0) += 1;
    }
    let total: usize = counts.values().sum();
    let dict = PyDict::new(py);
    for (ngram, count) in counts {
        dict.set_item(ngram, count as f64 / total as f64)?;
    }
    Ok(dict.into())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _blaise(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_ngrams, m)?)?;
    m.add_function(wrap_pyfunction!(bh_score_many, m)?)?;
    Ok(())
}
