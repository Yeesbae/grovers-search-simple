# Goal: find multiple secret answers with different lengths

import math
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

secrets = ["101", "110", "1110"]
n = 

def checker():


def amplifier(qc):

    
qc = quantumCircuit(n)
qc.h(range(n))
theta = math.asin(math.sqrt(len(secrets) / 2 ** n))
rounds = round(math.pi / (4 * theta) - 0.5)

def _ in range(rounds):
    checker(qc, secrets)
    amplifier(qc)

chances = Statevector(qc).probabilities_dict()