## 1. Environment Setup

To ensure stability and avoid dependency conflicts, it is highly recommended to use a **Conda** virtual environment.

### Create and Activate Environment
Open your terminal or Anaconda Prompt and run:

```bash
conda create -n qmemento python=3.10.19 -y

conda activate qmemento
```
## 2. Install Dependencies
Once the environment is active, install the required libraries using pip:
```bash
pip install qiskit qiskit-aer streamlit numpy pillow
```
## 3. Quick Start
Ensure you are in the project root directory (the folder containing interface.py), then launch the application:
```bash
streamlit run interface.py
```
The browser will automatically open the interface at `http://localhost:8501`.