//! RISC Zero guest program: prove that the creator is at least `min_age`.

use risc0_zkvm::guest::env;

fn main() {
    let min_age: u32 = env::read();
    let dob_ts: u32 = env::read();
    let current_ts: u32 = env::read();

    let secs_per_year: u64 = 31_536_000;
    let age_secs: u64 = (current_ts - dob_ts) as u64;
    let required: u64 = (min_age as u64) * secs_per_year;
    assert!(age_secs >= required, "under min age");

    env::commit(&min_age);
}
