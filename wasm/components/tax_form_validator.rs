//! WASM component: tax-form validator.
//! Compiled to wasm32-wasi and run inside Wasmtime or Fermyon Spin.

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Form1099 {
    pub creator_id: String,
    pub year: u16,
    pub form: String,
    pub gross: f64,
    pub fees: f64,
    pub net: f64,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ValidationResult {
    pub valid: bool,
    pub errors: Vec<String>,
}

#[no_mangle]
pub extern "C" fn alloc(size: usize) -> *mut u8 {
    let mut buf = Vec::with_capacity(size);
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);
    ptr
}

#[no_mangle]
pub extern "C" fn dealloc(ptr: *mut u8, size: usize) {
    unsafe {
        let _ = Vec::from_raw_parts(ptr, size, size);
    }
}

fn validate(form: &Form1099) -> ValidationResult {
    let mut errors = Vec::new();
    if form.creator_id.is_empty() {
        errors.push("creator_id required".into());
    }
    if form.year < 2000 || form.year > 2100 {
        errors.push("year out of range".into());
    }
    if !["1099-NEC", "1099-MISC", "1099-K"].contains(&form.form.as_str()) {
        errors.push("unknown form".into());
    }
    if (form.gross - form.fees - form.net).abs() > 0.01 {
        errors.push("net != gross - fees".into());
    }
    ValidationResult { valid: errors.is_empty(), errors }
}

#[no_mangle]
pub extern "C" fn validate_ptr(ptr: *const u8, len: usize) -> *mut u8 {
    let bytes = unsafe { std::slice::from_raw_parts(ptr, len) };
    let form: Form1099 = match serde_json::from_slice(bytes) {
        Ok(f) => f,
        Err(e) => {
            let r = ValidationResult { valid: false, errors: vec![format!("decode: {e}")] };
            return to_wasm(&r);
        }
    };
    let r = validate(&form);
    to_wasm(&r)
}

fn to_wasm(r: &ValidationResult) -> *mut u8 {
    let bytes = serde_json::to_vec(r).unwrap_or_default();
    let mut boxed = bytes.into_boxed_slice();
    let ptr = boxed.as_mut_ptr();
    std::mem::forget(boxed);
    ptr
}
