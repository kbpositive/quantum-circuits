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
                cirq.measure(newBit, self.qubit, key=""),
            ]
        ]

    def teleport(self, newBit):
        return newBit, self.qubit


class Receiver:
    def __init__(self, entangledQubit):
        self.qubit = entangledQubit

    def decode(self, xFlip, zFlip):
        return [
            cirq.Moment([n])
            for n in [
                cirq.CNOT(xFlip, self.qubit),
                cirq.CZ(zFlip, self.qubit),
                cirq.measure(xFlip, zFlip, self.qubit, key="result"),
            ]
        ]


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

    xf, zf = tele.teleport(newBit)

    rec = Receiver(bob.qubit)
    teleportedInfo = rec.decode(xf, zf)
    circuit.extend(teleportedInfo)

    print(cirq.Circuit(circuit), end="\n\n")


if __name__ == "__main__":
    main()