import cirq

alice = cirq.NamedQubit("alice")
bob = cirq.NamedQubit("bob")


def entangle(initialBit, targetBit):
    # put initla bit into super position
    h = cirq.Moment([cirq.H(initialBit)])
    # use controlled not to create entangled pair with target bit
    cnot = cirq.Moment([cirq.CNOT(initialBit, targetBit)])
    return cirq.Circuit([h, cnot])


def encodeData(newBit, data, entangledBit):
    # connect new qubit with entangled bit
    control = cirq.Moment([cirq.CNOT(newBit, entangledBit)])
    # add H gate to new qubit for phase correction
    h = cirq.Moment([cirq.H(newBit)])
    # measure entangled bit and new bit
    m = cirq.Moment([cirq.measure(newBit, entangledBit, key="result")])
    return cirq.Circuit(data + [control, h, m])


def decodeData(xFlip, zFlip, entangledBit):
    # update circuit of teleported bit
    teleportedInfo = []
    #
    if xFlip:
        teleportedInfo.append(cirq.Moment([cirq.X(entangledBit)]))
    if zFlip:
        teleportedInfo.append(cirq.Moment([cirq.Z(entangledBit)]))
    teleportedInfo.append(cirq.Moment([cirq.measure(entangledBit, key="result")]))
    return cirq.Circuit(teleportedInfo)


# start with entangled pair
entangledCircuit = entangle(alice, bob)
print(entangledCircuit, end="\n\n")

newBit = cirq.NamedQubit("newBit")
newData = encodeData(newBit, [cirq.Moment([cirq.X(newBit)])], alice)
print(newData, end="\n\n")

res = list(cirq.Simulator().run(newData).histogram(key="result").keys())[0]
teleportedBit = decodeData(res % 2, (res // 2) % 2, bob)
print(teleportedBit, end="\n\n")

result = cirq.Simulator().sample(teleportedBit).loc[0, "result"]
print(result, end="\n\n")
