import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
import os
import time

class ExperimentLogger:
    def __init__(self, log_file="quantum_research_log.csv"):
        self.log_file = log_file

    def log_to_csv(self, mode, shots, prob_1):
        with open(self.log_file, "a") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp},{mode},{shots},{prob_1:.4f}\n")

class Visualizer:
    @staticmethod
    def generate_circuit_plot(output_path="circuit_diagram.png"):
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        qc.draw(output='mpl', filename=output_path)
        return output_path
