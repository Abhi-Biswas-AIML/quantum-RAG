import numpy as np
from qiskit import QuantumCircuit

def angle_encode(vec):
    qc = QuantumCircuit(len(vec))
    for i, v in enumerate(vec):
        qc.ry(np.pi * v, i)
    return qc
