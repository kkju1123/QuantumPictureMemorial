import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from analytics import ExperimentLogger

class QuantumImageProcessor:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')
        self.logger = ExperimentLogger()

    def run_quantum_sampling(self, shots=1024):
        """执行量子采样，获取概率分布"""
        qc = QuantumCircuit(1, 1)
        qc.h(0) 
        qc.measure(0, 0)
        return self.backend.run(qc, shots=shots).result().get_counts()

    def process_image(self, img_array, counts, mode_key="collapse"):
        """量子驱动的图像演化算法"""
        float_img = img_array.astype(float)
        h, w, c = float_img.shape
        prob_1 = counts.get('1', 0) / sum(counts.values())
        
        # 记录实验数据
        self.logger.log_to_csv(mode_key, sum(counts.values()), prob_1)

        if mode_key == "collapse":
            num_slices = int(prob_1 * 60) + 10
            for _ in range(num_slices):
                y = np.random.randint(0, h-30)
                slice_h = np.random.randint(10, 50)
                shift = int(np.random.randint(200, 500) * prob_1)
                float_img[y:y+slice_h, :, :] = np.roll(float_img[y:y+slice_h, :, :], shift, axis=1)
            float_img[:,:,0] *= 0.4

        elif mode_key == "tunneling":
            density = 0.05 + (prob_1 * 0.15)
            mask = np.random.rand(h, w) < density
            shift_y, shift_x = int(50 * prob_1), int(50 * prob_1)
            tunnel_layer = np.roll(float_img, shift_y, axis=0)
            tunnel_layer = np.roll(tunnel_layer, shift_x, axis=1)
            tunnel_layer[:, :, 1:3] *= 1.5 
            tunnel_layer[:, :, 0] *= 0.2
            float_img[mask] = tunnel_layer[mask]
            float_img[~mask] *= (0.95 + 0.05 * (1-prob_1))

        elif mode_key == "entanglement":
            mid = w // 2
            mix = 1.0 - abs(prob_1 - 0.5) * 2
            left = float_img[:, :mid, :].copy()
            right = 255 - np.flip(float_img[:, mid:mid*2, :], axis=1).copy()
            float_img[:, :mid, :] = left * (1-mix) + right * mix
            float_img[:, mid:mid*2, :] = np.flip(float_img[:, :mid, :], axis=1)
            float_img = float_img[:, :, [2, 1, 0]]

        return np.clip(float_img, 0, 255).astype(np.uint8)
