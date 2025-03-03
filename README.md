# fusionCl_dataset

This repository provides tools and datasets for generating, compiling, and benchmarking various compute-intensive application kernels. It offers an end-to-end pipeline for creating workload variants, executing them on CPU and GPU, and classifying their suitability based on runtime performance.

## 📂 Directory and File Descriptions

### 🔹 `Generated_Dataset/`
Contains various **generated variants** of compute-intensive applications. These datasets are created using `generator.py`, modifying the raw kernels to produce diverse workload configurations.

---

### 🔹 `POLYBENCH_KERNELS/`
Holds the original **raw compute-intensive kernels** sourced from **PolyBench**. These kernels serve as the baseline input for `generator.py` to produce the datasets in `Generated_Dataset/`.

---

### 🔹 `generator.py`
This script is responsible for:
- Setting up compute-intensive applications.
- Generating multiple **variants** of each kernel.
- Compiling the kernels for execution on target platforms (CPU/GPU).

---

### 🔹 `speedup_computer.py`
This script handles the **execution and benchmarking** of various kernels. It:
- Runs kernels on both **CPU** and **GPU**.
- Measures and records **runtime performance**.
- Classifies each kernel as **CPU-suitable** or **GPU-suitable** based on observed speedups.

---

### 🔹 `speedup_data-Augmented-dataset-MINI_XXSMALL.csv`
A sample dataset generated from benchmarking results. It contains:
- Metadata of various kernel runs.
- Runtime measurements.
- CPU/GPU suitability classifications.

---

## 🚀 Getting Started
1. Place raw kernels inside `POLYBENCH_KERNELS/`.
2. Run `generator.py` to create variant workloads into `Generated_Dataset/`.
3. Execute `speedup_computer.py` to benchmark workloads and classify them.
4. Analyze the generated CSV dataset for insights.

---

## 📌 Notes
- Ensure required compilers and GPU drivers are set up before execution.


---
