// Devin playbook: write_quantum_circuit.md
//
// Steps:
// 1. Add a circuit in quantum/<module>/<circuit>.py using cudaq or qiskit
// 2. Add a unit test that asserts depth < budget, two-qubit-gate count < budget
// 3. Add a noise-robustness test
// 4. Add an OpenQASM 3 export
// 5. Add a Robot Framework test if the circuit is reachable from an HTTP tool
// 6. Add the circuit to the gallery in docs/quantum/gallery.md
// 7. PR
