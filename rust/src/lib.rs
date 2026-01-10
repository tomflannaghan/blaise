use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::collections::HashMap;
use std::f64::INFINITY;

#[pyfunction]
fn bd_score(text: &str, n: usize, dist: &Dist) -> f64 {
    if text.len() < n {
        return INFINITY;
    }

    let mut counts: HashMap<String, usize> = HashMap::new();
    for i in 0..=(text.len() - n) {
        let ngram = text[i..i + n].to_string();
        if dist.dist.contains_key(&ngram) {
            counts.entry(ngram).and_modify(|v| *v += 1).or_insert(1);
        }
    }
    let total: usize = counts.values().sum();
    let mut result = 0.0;
    for (k, c) in counts.iter() {
        let term: f64 = (*c as f64) * dist.dist.get(k).unwrap();
        result += (term / total as f64).sqrt()
    }
    return -result.ln();
}

#[pyclass]
struct Dist {
    dist: HashMap<String, f64>,
}

#[pyfunction]
fn to_dist(dist: HashMap<String, f64>) -> PyResult<Dist> {
    Ok(Dist { dist: dist })
}

#[pyfunction]
fn calculate_ngrams(text: &str, n: usize) -> PyResult<HashMap<String, f64>> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be >= 1"));
    }
    if text.len() < n {
        return Ok(HashMap::new());
    }
    let mut counts: HashMap<String, usize> = HashMap::new();
    for i in 0..=(text.len() - n) {
        let ngram = &text[i..i + n];
        *counts.entry(ngram.to_string()).or_insert(0) += 1;
    }
    let total: usize = counts.values().sum();
    Ok(counts
        .iter()
        .map(|(k, v)| {
            return (k.clone(), (*v as f64) / (total as f64));
        })
        .collect())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _blaise(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_ngrams, m)?)?;
    m.add_function(wrap_pyfunction!(bd_score, m)?)?;
    m.add_function(wrap_pyfunction!(to_dist, m)?)?;
    m.add_class::<Dist>()?;
    Ok(())
}
