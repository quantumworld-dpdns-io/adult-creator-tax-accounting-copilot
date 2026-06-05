// Devin playbook: add_new_payment_provider.md
//
// Goal: add a new payment-platform adapter to svc/payout-aggregator.
//
// Steps Devin must follow:
// 1. Create services/payout-aggregator/src/adapters/<provider>.py
// 2. Add a row to the providers table in docs/data/providers.csv
// 3. Add a new method to the Provider interface (services/payout-aggregator/src/adapters/__init__.py)
// 4. Add a fixture in tests/fixtures/<provider>/sample_webhook.json
// 5. Add a Robot Framework test in tests/robot/payments/<provider>_webhook.robot
// 6. Run `pytest` and `robot` to verify
// 7. Open a PR with the conventional-commits prefix `feat(pay):`
