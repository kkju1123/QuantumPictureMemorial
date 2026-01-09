from qiskit import QuantumCircuit
from qiskit_aer import Aer

# 1. 创建量子电路
qc = QuantumCircuit(1, 1)
qc.h(0)         # 制造叠加态
qc.measure(0, 0) # 观测/坍缩

# 2. 运行模拟
backend = Aer.get_backend('qasm_simulator')
result = backend.run(qc, shots=1).result()
counts = result.get_counts()

# 3. 打印结果
print("\n" + "="*30)
print(f"量子随机数生成成功！")
print(f"测量结果: {counts}")
print("="*30 + "\n")
