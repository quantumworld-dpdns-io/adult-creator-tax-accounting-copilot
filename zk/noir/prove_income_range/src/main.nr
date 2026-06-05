// ZK income-range proof (Noir-style pseudocode).
//
// Public inputs:
//   - creator_pubkey: Field
//   - lower_usd:      u64
//   - upper_usd:      u64
//
// Private inputs:
//   - gross_usd:      u64
//
// Assert: lower_usd <= gross_usd <= upper_usd

fn main(
    creator_pubkey: pub Field,
    lower_usd: pub u64,
    upper_usd: pub u64,
    gross_usd: u64,
) {
    assert(gross_usd >= lower_usd);
    assert(gross_usd <= upper_usd);
    let h = std::hash::poseidon::bn254::hash_1(gross_usd as Field);
    assert(h == creator_pubkey);
}
