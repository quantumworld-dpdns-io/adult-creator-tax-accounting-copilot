//! JWT verification stub.

use jsonwebtoken::{decode, DecodingKey, Validation, Algorithm};

#[derive(Debug, serde::Deserialize)]
pub struct Claims {
    pub sub: String,
    pub aud: String,
    pub iss: String,
    pub exp: usize,
}

pub fn verify(token: &str) -> anyhow::Result<Claims> {
    let secret = std::env::var("DEV_JWT_SECRET").unwrap_or_else(|_| "dev-only-not-for-prod".into());
    let mut v = Validation::new(Algorithm::HS256);
    v.set_audience(&["copilot-api"]);
    let data = decode::<Claims>(token, &DecodingKey::from_secret(secret.as_bytes()), &v)?;
    Ok(data.claims)
}
