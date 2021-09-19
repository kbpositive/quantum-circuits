import cirq


class Sender:
    def __init__(self, name):
        self.name = name
        self.qubit = cirq.NamedQubit(name)


class Teleporter:
    def __init__(self, entangledQubit):
        self.qubit = entangledQubit

    def encode(self, newBit):
        return [
            cirq.Moment([n])
            for n in [
                cirq.CNOT(newBit, self.qubit),
                cirq.H(newBit),
                cirq.measure(newBit, self.qubit, key="result"),
            ]
        ]

    def teleport(self, data):
        result = list(
            cirq.Simulator().run(cirq.Circuit(data)).histogram(key="result").keys()
        )[0]
        return result % 2, (result // 2) % 2


class Receiver:
    def __init__(self, entangledQubit):
        self.qubit = entangledQubit

    def decode(self, xFlip, zFlip):
        teleportedInfo = []
        if xFlip:
            teleportedInfo.append(cirq.Moment([cirq.X(self.qubit)]))
        if zFlip:
            teleportedInfo.append(cirq.Moment([cirq.Z(self.qubit)]))
        for n in [
            cirq.measure(self.qubit, key="result"),
        ]:
            teleportedInfo.append(cirq.Moment([n]))
        return teleportedInfo


def entangle(initialBit, targetBit):
    return [
        cirq.Moment([n])
        for n in [
            cirq.H(initialBit),
            cirq.CNOT(initialBit, targetBit),
        ]
    ]


def main():
    alice = Sender("alice")
    bob = Sender("bob")
    circuit = []

    entangledBits = entangle(alice.qubit, bob.qubit)
    circuit.extend(entangledBits)

    tele = Teleporter(alice.qubit)
    newBit = cirq.NamedQubit("newBit")
    newData = tele.encode(newBit)
    circuit.extend(newData)

    xf, zf = tele.teleport(circuit)

    rec = Receiver(bob.qubit)

    print(cirq.Circuit(rec.decode(xf, zf)), end="\n\n")


if __name__ == "__main__":
    main()