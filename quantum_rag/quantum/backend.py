from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

class QuantumBackend:
    def __init__(self, shots=1024, noisy=False):
        self.shots = shots

        if noisy:
            noise = NoiseModel()
            noise.add_all_qubit_quantum_error(
                depolarizing_error(0.01, 1), ["ry", "h"]
            )
            noise.add_all_qubit_quantum_error(
                depolarizing_error(0.05, 3), ["cswap"]
            )
            self.backend = AerSimulator(noise_model=noise)
        else:
            self.backend = AerSimulator()
