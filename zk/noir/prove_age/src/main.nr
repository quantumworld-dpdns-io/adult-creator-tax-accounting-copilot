// ZK proof of age (Noir-style pseudocode, run with nargo).
//
// Public inputs:
//   - creator_pubkey: Field
//   - min_age:        u32
//   - current_ts:     u32
//
// Private inputs:
//   - dob_ts:         u32
//
// Assert: current_ts - dob_ts >= min_age * 365 * 24 * 60 * 60

fn main(
    creator_pubkey: pub Field,
    min_age: pub u32,
    current_ts: pub u32,
    dob_ts: u32,
) {
    let secs_per_year: u32 = 31_536_000;
    let age_secs = current_ts - dob_ts;
    let required = min_age * secs_per_year;
    assert(age_secs as u64 >= required as u64);

    // The proof carries a Poseidon hash binding the creator to the
    // statement — this is verified in the public input.
    let h = std::hash::poseidon::bn254::hash_2([creator_pubkey, dob_ts as Field]);
    assert(h == creator_pubkey);
}
