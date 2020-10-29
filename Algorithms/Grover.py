import cirq
import math

# Creates quantum circuit with n line qubits
# then finds the correct number of iterations
# to find a given target number.

def grover(circuit, qbts, item, length):
	circuit.append(cirq.H(qubit) for qubit in qbts)  # Initialize all qubits in superposition
	step(circuit, qbts, item, length)
	if length > 2:
		for t in range(int(math.ceil((2**length)**0.5))-1):
			step(circuit, qbts, item, length)
	circuit.append(cirq.measure(*qbts, key='result'))  # Measure outputs


def step(circuit, qbts, item, length):
	circuit.append(oracle(qbts, item, length), strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
	amplify(circuit, qbts)


def oracle(qbts, item, length):  # Oracle function
	item = 2**length - (item+1)
	binary = '{0:0' + str(length) + 'b}'
	indices = binary.format(item)
	active_qbts = [qbts[index] for index, active in enumerate(indices) if int(active)]
	yield [cirq.X(i) for i in active_qbts]
	yield cirq.Z(qbts[0]).controlled_by(*qbts[1:])
	yield [cirq.X(i) for i in active_qbts]


def amplify(circuit, qbts):  # Amplification
	circuit.append([cirq.H(qubit) for qubit in qbts], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
	circuit.append(cirq.X(qubit) for qubit in qbts)
	circuit.append(cirq.Z(qubits[0]).controlled_by(*qubits[1:]))
	circuit.append([cirq.X(qubit) for qubit in qbts], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
	circuit.append(cirq.H(qubit) for qubit in qbts)


# Determine target and reate circuit with n qubits
target = 12
n = 10
qubits = cirq.LineQubit.range(n)
quantum_circuit = cirq.Circuit()

# Configure circuit for Grover's algorithm
grover(quantum_circuit, qubits, target, n)

# Initialize Simulator and print test results
sim = cirq.Simulator()
print(sim.simulate(quantum_circuit), end='\n\n')

# Run circuit and sample results
samples = sim.run(quantum_circuit, repetitions=10)
print(samples.histogram(key='result'), end='\n\n')

# print circuit
print(quantum_circuit)
