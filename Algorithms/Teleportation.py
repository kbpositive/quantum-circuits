import cirq
from cirq.circuits import InsertStrategy
import matplotlib.pyplot as plt

alice = cirq.NamedQubit("alice")
bob = cirq.NamedQubit("bob")


def entangle(initialBit, targetBit):
    cnot = cirq.H(initialBit)
    mix = cirq.CNOT(initialBit, targetBit)
    m1 = cirq.Moment([cnot])
    m2 = cirq.Moment([mix])
    return cirq.Circuit([m1, m2])


def encodeData(newBit, entangledBit):
    # connect new qubit with entangled bit
    control = cirq.Moment([cirq.CNOT(newBit, entangledBit)])
    # add H gave to new qubit for phase correction
    h = cirq.Moment([cirq.H(newBit)])
    # measure entangled bit and new bit
    m = cirq.Moment([cirq.measure(newBit, entangledBit, key="result")])
    # teleported data
    return cirq.Circuit([control, h, m])


def update(xFlip, zFlip, entangledBit):
    # return information from new bit
    teleportedInfo = []
    if xFlip:
        teleportedInfo.append(cirq.Moment([cirq.X(entangledBit)]))
    if zFlip:
        teleportedInfo.append(cirq.Moment([cirq.Z(entangledBit)]))
    teleportedInfo.append(cirq.Moment([cirq.measure(entangledBit, key="result")]))
    return cirq.Circuit(teleportedInfo)


# start with entangled pair
# aliceCircuit.append(cirq.X(alice[1]))
entangledCircuit = entangle(alice, bob)
print(entangledCircuit)
newData = encodeData(cirq.NamedQubit("new"), alice)
print(newData)
res = list(cirq.Simulator().run(newData, repetitions=1).histogram(key="result").keys())[
    0
]
print(res % 2, (res // 2) % 2)
teleportedBit = update(res % 2, (res // 2) % 2, bob)
print(teleportedBit)

sim = cirq.Simulator()
samples = sim.run(teleportedBit, repetitions=1)
results = list(samples.histogram(key="result"))[0]
print(results)

"""
0: ───X───────────@───H───M───@───M('result')───
                  │           │   │
1: ───────H───@───X───M───@───┼───M─────────────
              │           │   │   │
2: ───────────X───────────X───@───M─────────────
"""