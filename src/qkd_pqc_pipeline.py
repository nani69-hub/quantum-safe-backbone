"""
Unified Quantum-Safe Communication Framework
Simulation for UC-024, UC-025, and UC-030
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def simulate_qkd_channel(n_bits=32, eavesdropping=False):
    simulator = AerSimulator()
    
    alice_bits = np.random.randint(2, size=n_bits)
    alice_bases = np.random.randint(2, size=n_bits)
    bob_bases = np.random.randint(2, size=n_bits)
    bob_results = []
    
    for i in range(n_bits):
        qc = QuantumCircuit(1, 1)
        
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 1:
            qc.h(0)
            
        if eavesdropping:
            eve_basis = np.random.randint(2)
            if eve_basis == 1:
                qc.h(0)
            qc.measure(0, 0)
            result_eve = simulator.run(qc, shots=1).result().get_counts()
            collapsed_state = int(list(result_eve.keys())[0])
            
            qc = QuantumCircuit(1, 1)
            if collapsed_state == 1:
                qc.x(0)
            if eve_basis == 1:
                qc.h(0)

        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure(0, 0)
        
        counts = simulator.run(qc, shots=1).result().get_counts()
        bob_results.append(int(list(counts.keys())[0]))
        
    sifted_alice = [alice_bits[i] for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
    sifted_bob = [bob_results[i] for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
    
    if len(sifted_alice) == 0:
        return None, 1.0, False

    errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
    qber = errors / len(sifted_alice)
    is_secure = qber <= 0.11
    
    if is_secure:
        key_bits = sifted_alice[:16]
        key_bytes = bytes(np.packbits(key_bits).tolist())
        derived_key = (key_bytes * (32 // len(key_bytes) + 1))[:32]
        return derived_key, qber, True
    else:
        return None, qber, False

def hybrid_encrypt_payload(key_bytes, plaintext_str):
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext_str.encode()) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag

if __name__ == "__main__":
    print("=" * 65)
    print("   UNIFIED QUANTUM-SAFE COMMUNICATION FRAMEWORK (UC-024/025/030)")
    print("=" * 65)
    
    print("\n[TEST 1] Initiating Normal QKD Transmission over Dark Fiber...")
    key, qber, secure = simulate_qkd_channel(n_bits=64, eavesdropping=False)
    print(f"-> Measured QBER: {qber * 100:.2f}% | Threshold: <= 11.0%")
    print(f"-> Physical Link Status: {'SECURE (Verified)' if secure else 'COMPROMISED'}")
    
    if secure:
        secret_record = "CONFIDENTIAL: AP State Land Record #AP-521001-REGISTRY"
        iv, ciphertext, tag = hybrid_encrypt_payload(key, secret_record)
        print(f"-> Layer 3 Encrypted Payload: {ciphertext.hex()[:32]}... [AES-256-GCM]")
    
    print("\n" + "-" * 65)
    print("[TEST 2] Simulating Optical Line Tapping by Adversary (Eve)...")
    key_eve, qber_eve, secure_eve = simulate_qkd_channel(n_bits=64, eavesdropping=True)
    print(f"-> Measured QBER: {qber_eve * 100:.2f}% | Threshold: <= 11.0%")
    print(f"-> Physical Link Status: {'SECURE' if secure_eve else 'INTRUSION DETECTED: KEY ABORTED'}")
    print("=" * 65)
