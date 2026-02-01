from qiskit import QuantumCircuit, transpile

def swap_test(qc1, qc2, backend, shots):
    """
    Run Swap Test to estimate overlap between states prepared by qc1 and qc2.
    Returns: 2 * P(ancilla=0) - 1, which estimates |<psi|phi>|^2.
    """
    n = qc1.num_qubits
    # 1 ancilla + n for psi + n for phi
    qc = QuantumCircuit(2 * n + 1, 1) # Measure only ancilla
    
    # Ancilla is q0
    qc.h(0)
    
    # Append state preparations.
    # q1..qn for psi
    qc.compose(qc1, range(1, n + 1), inplace=True)
    # q(n+1)..q(2n) for phi
    qc.compose(qc2, range(n + 1, 2 * n + 1), inplace=True)
    
    # CSWAP (Fredkin) gates
    # Control: q0, Target 1: q(i+1), Target 2: q(i+n+1)
    for i in range(n):
        qc.cswap(0, i + 1, i + n + 1)
        
    qc.h(0)
    qc.measure(0, 0) # Measure q0 into c0

    # Execute
    t_qc = transpile(qc, backend)
    result = backend.run(t_qc, shots=shots).result()
    counts = result.get_counts()
    
    # Counts keys are strings like '0', '1'.
    # We measured 1 bit.
    zeros = counts.get('0', 0)
    p0 = zeros / shots
    
    return 2 * p0 - 1
