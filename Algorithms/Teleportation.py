import cirq
from cirq.circuits import InsertStrategy
import matplotlib.pyplot as plt

qbits = cirq.LineQubit.range(3)
quantum_circuit = cirq.Circuit()


def entangle(a, c, circuit):
    circuit.append(cirq.H(a), strategy=InsertStrategy.NEW_THEN_INLINE)
    for b in c:
        circuit.append(cirq.CNOT(a, b))


# teleported bit
quantum_circuit.append(cirq.X(qbits[0]))

# start with entangled pair
entangle(qbits[1], qbits[2:], quantum_circuit)

# connect new qubit with entangled bit
quantum_circuit.append(cirq.CNOT(qbits[0], qbits[1]))

# add H gave to new qubit for phase correction
quantum_circuit.append(cirq.H(qbits[0]))

# measure entangled bit and new bit
quantum_circuit.append(cirq.measure(qbits[0]))
quantum_circuit.append(cirq.measure(qbits[1]))

quantum_circuit.append(cirq.CNOT(qbits[1], qbits[2]))
quantum_circuit.append(cirq.CZ(qbits[0], qbits[2]))


quantum_circuit.append(cirq.measure(*qbits, key="result"))
sim = cirq.Simulator()
samples = sim.run(quantum_circuit, repetitions=1000)
results = [[a, b] for (a, b) in samples.histogram(key="result").items()]
plt.bar([i[0] for i in results], [i[1] for i in results])
for i, j in enumerate(results):
    plt.text(j[0], j[1], j[0])
plt.savefig("./results.png")
"""
0: ───X───────────@───H───M───@───M('result')───
                  │           │   │
1: ───────H───@───X───M───@───┼───M─────────────
              │           │   │   │
2: ───────────X───────────X───@───M─────────────
"""