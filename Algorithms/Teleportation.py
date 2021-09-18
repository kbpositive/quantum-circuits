import cirq


class Sender:
    def __init__(self, name):
        self.name = name
        self.qubit = cirq.NamedQubit(name)
        self.circuit = cirq.Circuit()


class Teleporter:
    def __init__(self):
        pass


def entangle(initialBit, targetBit):
    # put initlal bit into super position
    cirq.H(initialBit)
    # use controlled not to create entangled pair with target bit
    cirq.CNOT(initialBit, targetBit)


def encodeData(newBit, data, entangledBit):
    # connect new qubit with entangled bit
    control = cirq.Moment([cirq.CNOT(newBit, entangledBit)])
    # add H gate to new qubit for phase correction
    h = cirq.Moment([cirq.H(newBit)])
    # measure entangled bit and new bit
    m = cirq.Moment([cirq.measure(newBit, entangledBit, key="result")])
    return cirq.Circuit(data + [control, h, m])


class Reciever:
    def __init__(self):
        pass


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


def main():
    alice = Sender("alice")
    bob = Sender("bob")
    # start with entangled pair
    # entangle(alice, bob)
    # print(entangledCircuit, end="\n\n")

    newBit = cirq.NamedQubit("newBit")
    newData = encodeData(newBit, [cirq.Moment([cirq.H(newBit)])], alice.qubit)
    print(newData, end="\n\n")

    res = list(cirq.Simulator().run(newData).histogram(key="result").keys())[0]
    teleportedBit = decodeData(res % 2, (res // 2) % 2, bob.qubit)
    print(teleportedBit, end="\n\n")

    result = cirq.Simulator().sample(teleportedBit).loc[0, "result"]
    print(result, end="\n\n")


if __name__ == "__main__":
    main()