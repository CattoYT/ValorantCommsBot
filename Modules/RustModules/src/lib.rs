use std::collections::HashMap;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyBytes, PyTuple};
use rusty_tesseract::{Args, Image};

#[pyfunction]
fn readChat(img: &Image) -> String {
    // string output
    let my_args = Args {
        lang: "eng".to_string(),
        config_variables: HashMap::from([(
            "tessedit_char_whitelist".into(),
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789():<>?!&- ".into(),
        )]),
        dpi: None,
        psm: Some(6),
        oem: None,
    };

    let output = rusty_tesseract::image_to_string(img, &my_args).unwrap();
    println!("The String output is: {:?}", output);
    output
}


/// Formats the sum of two numbers as string.
#[pyfunction]
fn readChatTest(py: Python) -> PyResult<(PyObject)> {
    let valorant_chat_class = py.import("Modules.Chat")?.get("ValorantChat")?; //fix later
    let args = PyTuple::new(py, ["(Party)", "Rust", "LOL"]);
    let instance = valorant_chat_class.call1(args)?;

    Ok(instance.into())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn RustModules(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(readChat, m)?)?;
    m.add_function(wrap_pyfunction!(readChatTest, m)?)?;
    Ok(())
}