use std::collections::HashMap;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyBytes, PyList, PyTuple};
use rusty_tesseract::{Args, Image};
use image::load_from_memory;


#[pyfunction]
fn readChat(py: Python,img: &PyBytes) -> String {
    let img = load_from_memory(img.as_bytes()).unwrap();

    img.save("test.png").unwrap();
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
    let fussyImg = Image::from_dynamic_image(&img).unwrap();
    let output = rusty_tesseract::image_to_string(&fussyImg, &my_args).unwrap();

    for i in 0..output.len() {
        if output.contains("(Party) ") {
            let channel = "(Party) ";
            output.replace("(Party) ", "")
        } //finish rest klater
    }

    println!("The String output is: {:?}", output);

    output

}


//The import and call1 was from ChatGPT, literally where are the docs for this lib
#[pyfunction]
fn readChatTest(py: Python) -> PyResult<(PyObject)> {



    Python::with_gil(|py| {
        let valorant_chat_class = py.import("Modules.Chat")?.getattr("ValorantChat").unwrap(); //fix later

        let args = ("(Party)", "Rust", "LOL");
        if valorant_chat_class.is_callable() {
            let instance = valorant_chat_class.call1(args)?;
            Ok(instance.into())
        } else {
            println!("The attribute 'ValorantChat' is not callable. Ensure it's a class or function.");

            Err(PyErr::new::<pyo3::exceptions::PyAttributeError, _>(
                "The attribute 'ValorantChat' is not callable. Ensure it's a class or function.",
            ))
        }
    })
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