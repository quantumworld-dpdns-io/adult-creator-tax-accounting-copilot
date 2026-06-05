//! RISC Zero host: build ELF, prove, verify.

use risc0_zkvm::{default_prover, ExecutorEnv, Receipt};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
struct PublicInputs {
    min_age: u32,
    dob_ts: u32,
    current_ts: u32,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = std::env::args().collect::<Vec<_>>();
    let min_age: u32 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(18);
    let dob_ts: u32 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);
    let current_ts: u32 = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)?
        .as_secs() as u32;

    let env = ExecutorEnv::builder()
        .write(&min_age)?
        .write(&dob_ts)?
        .write(&current_ts)?
        .build()?;

    let prover = default_prover();
    let prove_info = prover.prove(env, methods::RISC0_PROVE_AGE_ELF)?;
    let receipt: Receipt = prove_info.receipt;

    let pub_inputs = PublicInputs { min_age, dob_ts, current_ts };
    let pub_bytes = bincode::serialize(&pub_inputs)?;

    receipt.verify(methods::RISC0_PROVE_AGE_ID, &pub_bytes)?;

    println!("proof verified for min_age={} dob_ts={} current_ts={}", min_age, dob_ts, current_ts);
    Ok(())
}
