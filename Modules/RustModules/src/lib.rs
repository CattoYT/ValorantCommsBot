#![allow(non_snake_case)] // I just don't care enough

use std::collections::HashMap;

use image::load_from_memory;
use pyo3::{prelude::*, types::{PyList, PyBytes}};
use rusty_tesseract::{Args, Image};

#[pyfunction]
fn readChat(py: Python,img: &PyBytes) -> PyResult<PyObject> {
    
    let img = load_from_memory(img.as_bytes()).unwrap();

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
    let output = rusty_tesseract::image_to_string(&fussyImg, &my_args).unwrap(); //Compile with --release so that this doesn't put the command in the console
    let valorant_chat_class: &PyAny = py.import("Modules.OverlayModule.Chat")?.getattr("ValorantChat").unwrap();

    let chatHistory = PyList::empty(py);


    let mut channel = String::new();

        //this is shitcode produced from me not knowing how to write rust
    for i in output.lines() {
        let mut line = i.to_string();
        if line.contains("(Party) ") {
            channel = "Party".to_string();
            line = line.replace("(Party) ", "");
        }
        else if line.contains("(Team) ") {
            channel = "Team".to_string();
            line = line.replace("(Team) ", "");
        }
        else if line.contains("(All) ") {
            channel = "All".to_string();
            line = line.replace("(All) ", "");
        }
        else {
            continue;
        }
        
        let mut user: String = String::new();
        for char in line.chars() {
            if char == ':' {
                line = line.replace(&(user.to_string() + ": "), "");
                break;
            }
            else {
                user.push(char);
            }
        }
        chatHistory.append(valorant_chat_class.call1((channel.clone(), user.clone(), &line))?)?;

    }



    
    Ok(chatHistory.into())


}


//The import and call1 was from ChatGPT, literally where are the docs for this lib
#[pyfunction]
fn readChatTest(py: Python) -> PyResult<PyObject> {



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
    //m.add_function(wrap_pyfunction!(readChatTest, m)?)?;
    Ok(())
}