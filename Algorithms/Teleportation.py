import cirq
from cirq.circuits import InsertStrategy
import matplotlib.pyplot as plt

qbits = cirq.LineQubit.range(3)
quantum_circuit = cirq.Circuit()


def entangle(initialBit, targetBits, circuit):
    circuit.append(cirq.H(initialBit), strategy=InsertStrategy.NEW_THEN_INLINE)
    for bit in targetBits:
        circuit.append(cirq.CNOT(initialBit, bit))


def encodeData(entangledBit, newBit, circuit):
    # connect new qubit with entangled bit
    circuit.append(cirq.CNOT(newBit, entangledBit))
    # add H gave to new qubit for phase correction
    circuit.append(cirq.H(newBit))
    # measure entangled bit and new bit
    circuit.append(cirq.measure(newBit))
    circuit.append(cirq.measure(entangledBit))
    # teleported data
    return entangledBit, newBit


def update(xFlip, zFlip, entangledBit, circuit):
    # information from new bit
    circuit.append(cirq.CNOT(xFlip, entangledBit))
    circuit.append(cirq.CZ(zFlip, entangledBit))


# teleported bit
quantum_circuit.append(cirq.X(qbits[0]))

# start with entangled pair
entangle(qbits[1], qbits[2:], quantum_circuit)

# encode new bit with entangled bit
xf, zf = encodeData(qbits[1], qbits[0], quantum_circuit)

# update other entangled bit with new (teleported) info
update(xf, zf, qbits[2], quantum_circuit)

# measure results
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