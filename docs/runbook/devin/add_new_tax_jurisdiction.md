// Devin playbook: add_new_tax_jurisdiction.md
//
// Steps:
// 1. Add a rule file to services/tax-engine/rules/<jurisdiction>.toml
// 2. Add a fixture in tests/fixtures/tax/<jurisdiction>/sample_payouts.csv
// 3. Add a unit test in services/tax-engine/tests/test_<jurisdiction>.py
// 4. Add a Robot test in tests/robot/tax/<jurisdiction>_estimate.robot
// 5. Add a vector-store corpus ingest in services/vector-router/jurisdictions/<jurisdiction>.yaml
// 6. Add an OWASP A09 audit-log emit when the new jurisdiction is first used
// 7. PR
