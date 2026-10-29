# Goal: find one secret answer (like "101") hidden among all possible answers.

import math
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

secret = "101101"
n = len(secret) # qubits


# ---------- STEP 1: the checker ----------
def add_checker(qc):
    # Qiskit reads bit strings right-to-left, so we reverse the secret.
    for i, bit in enumerate(reversed(secret)):
        if bit == "0":
            qc.x(i) # turn 0 to 1

    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1) # mark - if all is 1
    qc.h(n - 1)

    for i, bit in enumerate(reversed(secret)):
        if bit == "0":
            qc.x(i) # undo


# ---------- STEP 2: the amplifier ----------
def add_amplifier(qc):
    qc.h(range(n))
    qc.x(range(n))

    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    qc.x(range(n))
    qc.h(range(n))


# ---------- STEP 3: build the full circuit ----------
qc = QuantumCircuit(n)

qc.h(range(n))  # turn on all answers at equal volume

rounds = round(math.pi / 4 * math.sqrt(2 ** n))   # the "just right" number of rounds
print("Number of rounds:", rounds)

for _ in range(rounds): # amplify
    add_checker(qc)
    add_amplifier(qc)


# ---------- STEP 4: look at the result ----------
chances = Statevector(qc).probabilities_dict()

for answer, chance in sorted(chances.items()):
    print(answer, f"{chance:.1%}")

best = max(chances, key=chances.get)
print("Most likely answer:", best)
