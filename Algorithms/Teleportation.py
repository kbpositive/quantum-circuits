import cirq

alice = cirq.NamedQubit("alice")
bob = cirq.NamedQubit("bob")


def entangle(initialBit, targetBit):
    h = cirq.Moment([cirq.H(initialBit)])
    cnot = cirq.Moment([cirq.CNOT(initialBit, targetBit)])
    return cirq.Circuit([h, cnot])


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
entangledCircuit = entangle(alice, bob)
print(entangledCircuit)

newData = encodeData(cirq.NamedQubit("newBit"), alice)
print(newData)

res = list(cirq.Simulator().run(newData).histogram(key="result").keys())[0]
teleportedBit = update(res % 2, (res // 2) % 2, bob)
print(teleportedBit)

result = cirq.Simulator().sample(teleportedBit).loc[0, "result"]
print(result)

"""
0: ───X───────────@───H───M───@───M('result')───
                  │           │   │
1: ───────H───@───X───M───@───┼───M─────────────
              │           │   │   │
2: ───────────X───────────X───@───M─────────────
"""