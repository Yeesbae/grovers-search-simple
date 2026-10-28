import math
from qiskit import QuantumCircuit

def diffusion(state_prep: QuantumCircuit) -> QuantumCircuit:
    """D = A (2|0><0| - I) A†, built from any A."""
    n = state_prep.num_qubits
    qc = QuantumCircuit(n)
    qc.append(state_prep.inverse(), range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.append(state_prep, range(n))
    return qc

def grover(oracle: QuantumCircuit, state_prep: QuantumCircuit = None,
           num_good: int = 1) -> QuantumCircuit:
    n = oracle.num_qubits
    if state_prep is None:
        state_prep = QuantumCircuit(n)
        state_prep.h(range(n))
    theta = math.asin(math.sqrt(num_good / 2**n))
    k = max(0, round(math.pi / (4 * theta) - 0.5))

    qc = QuantumCircuit(n, n)
    qc.append(state_prep, range(n))
    D = diffusion(state_prep)
    for _ in range(k):
        qc.append(oracle, range(n))
        qc.append(D, range(n))
    qc.measure(range(n), range(n))
    return qc
