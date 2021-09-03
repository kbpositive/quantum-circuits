import cirq
from cirq.circuits import InsertStrategy

qbits = cirq.LineQubit.range(3)
quantum_circuit = cirq.Circuit()


def entangle(a, b, circuit):
    circuit.append(cirq.H(a), strategy=InsertStrategy.NEW_THEN_INLINE)
    circuit.append(cirq.CNOT(a, b))


entangle(qbits[0], qbits[2], quantum_circuit)
print(quantum_circuit)