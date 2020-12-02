import cirq
import math

# Given an integer n, this code defines the smallest
# quantum circuit necessary to find n in an unordered
# list of integers in as few attempts as possible.

# The oracle function returns 1 if x is the target and 0 otherwise.
# This function defines a circuit that will produce this result.
def oracle(qbts, item, length):
	item = 2**length - (item+1)
	binary = '{0:0' + str(length) + 'b}'
	indices = binary.format(item)
	active_qbts = [qbts[index] for index, active in enumerate(indices) if int(active)]
	yield [cirq.X(i) for i in active_qbts]
	yield cirq.Z(qbts[0]).controlled_by(*qbts[1:])
	yield [cirq.X(i) for i in active_qbts]


# After the oracle function, the output probabilities are amplified.
def amplify(circuit, qbts):  # Amplification
	circuit.append([cirq.H(qubit) for qubit in qbts], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
	circuit.append(cirq.X(qubit) for qubit in qbts)
	circuit.append(cirq.Z(qbts[0]).controlled_by(*qbts[1:]))
	circuit.append([cirq.X(qubit) for qubit in qbts], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
	circuit.append(cirq.H(qubit) for qubit in qbts)


# Grover's algorithm takes in a superposition,
# repeats the oracle and amplify functions above sqrt(2^n) times
# (where n is the number of bits required), then measures the output.
def grover(circuit, qbts, item, length):
	# Initialize all qubits in superposition
	circuit.append(cirq.H(qubit) for qubit in qbts)
	circuit.append(oracle(qbts, item, length), strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
	amplify(circuit, qbts)
	if length > 2:
		# repeat oracle function and amplify sqrt(2^n)-1 times
		for t in range(int(math.ceil((2**length)**0.5))-1):
			circuit.append(oracle(qbts, item, length), strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
			amplify(circuit, qbts)
	# Measure outputs
	circuit.append(cirq.measure(*qbts, key='result'))


# Running the algorithm returns the most frequent output, the fraction
# of said value over all values, and the circuit from which they were produced.
def run_algorithm(target, attempts):
	# Determine number of qubits needed, and create circuit
	n = int(math.ceil(math.log2(target)+1)) if target else 1
	qubits = cirq.LineQubit.range(n)
	quantum_circuit = cirq.Circuit()

	# Configure circuit for Grover's algorithm
	grover(quantum_circuit, qubits, target, n)

	# Initialize Simulator
	sim = cirq.Simulator()

	# Run circuit and sample results
	samples = sim.run(quantum_circuit, repetitions=attempts)
	res = max(samples.histogram(key='result'), key=samples.histogram(key='result').get)
	return res, samples.histogram(key='result')[res]/attempts, quantum_circuit, n

# print results
def results(target, attempts):
	result, accuracy, circuit, bits = run_algorithm(target, attempts)
	print('Most likely value: ', result)
	print('Success/Attempts: ', accuracy)
	print('Quantum steps: ', int(math.ceil((2**bits)**0.5))*attempts)
	print('Classical steps: ', int(math.ceil((2**bits)/2)), end='\n\n')

target = 32306
attempts = 10
results(target, attempts)
