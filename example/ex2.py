# Goal: find multiple secret answers (like "101" and "110") hidden among all possible answers.

import math
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

secrets = ["101", "110"]
n = len(secrets[0]) # qubits are same length

def checker(qc, secrets):
    for secret in secrets:
        for i, bit in enumerate(reversed(secret)):
            if bit == "0":
                qc.x(i)
        
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)

        for i, bit in enumerate(reversed(secret)):
            if bit == "0":
                qc.x(i)

def amplifier(qc):
    qc.h(range(n))
    qc.x(range(n))

    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    qc.x(range(n))
    qc.h(range(n))

qc = QuantumCircuit(n)
qc.h(range(n))
theta = math.asin(math.sqrt(len(secrets) / 2 ** n))
rounds = round(math.pi / (4 * theta) - 0.5)
print("Number of rounds:", rounds)

for _ in range(rounds):
    checker(qc, secrets)
    amplifier(qc)

chances = Statevector(qc).probabilities_dict()

for answer, chance in sorted(chances.items()):
    print(answer, f"{chance:.1%}")


result = sorted(chances, key=chances.get, reverse=True)[:len(secrets)]
print("Most likely answer:", result)