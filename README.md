# 🕵️‍♀️ The Algorithmic Auditor
### Advanced Bias Detection & Mitigation Engine

**Made with ❤️ by Mangal Bhaduriya**

---

## 📖 Project Overview
The **Algorithmic Auditor** is a full-stack web application designed to evaluate Machine Learning models for ethical fairness. In high-stakes industries like banking and hiring, AI models often inadvertently discriminate against protected groups (e.g., rejecting loans for women at higher rates than men).

This tool allows users to:
1.  **Train a Standard Model:** Visualize how historical data bias creeps into AI predictions.
2.  **Audit for Fairness:** Measure "Disparate Impact" and accuracy trade-offs in real-time.
3.  **Mitigate Bias:** Apply post-processing algorithms (Exponentiated Gradient) to reduce discrimination while maintaining model utility.
4.  **Test Custom Data:** Upload any CSV dataset to audit external models.

---

## 🚀 Key Features
* **Real-Time Bias Auditing:** Instantly calculates Demographic Parity and Selection Rates.
* **Algorithmic Mitigation:** Uses Microsoft's `fairlearn` library to retrain models with fairness constraints.
* **Dynamic File Upload:** Supports custom CSV datasets for testing different scenarios.
* **Interactive Dashboard:** Built with React.js and Recharts for clear, stakeholder-friendly visualizations.
* **Synthetic Data Fallback:** Automatically generates test data if no file is provided.

---

## 🛠️ Tech Stack
* **Frontend:** React.js, Recharts, Axios
* **Backend:** Python, FastAPI, Uvicorn
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **AI Ethics:** Fairlearn (Bias Metrics & Mitigation Algorithms)

---

## ⚙️ Installation & Setup

### Prerequisites
* Node.js & npm
* Python 3.8+

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/algorithmic-auditor.git](https://github.com/your-username/algorithmic-auditor.git)
cd algorithmic-auditor
