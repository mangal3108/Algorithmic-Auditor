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

### 1. Repository Setup
Clone the repository to your local machine to get started.

### 2. Backend Setup (Python)
Navigate to the `backend` folder. You will need to install the required dependencies listed in the requirements file (FastAPI, Uvicorn, Pandas, Scikit-Learn, Fairlearn). Once installed, start the Uvicorn server to launch the API.

### 3. Frontend Setup (React)
Navigate to the `frontend` folder. Install the necessary Node.js modules (Axios, Recharts). Once the installation is complete, start the application to launch the user interface in your browser.

---

## 📊 How to Use
1.  **Launch the App:** Open the dashboard in your browser.
2.  **Upload Data (Optional):** Drag and drop a CSV file containing a sensitive attribute (like gender) and a target label.
    * *Note: If no file is uploaded, the system automatically uses a synthetic "Loan Approval" dataset.*
3.  **Phase 1 (Audit):** Click the "Train Standard Model" button.
    * Observe the bar charts. You will likely see a significant gap in approval rates between groups (e.g., Male vs. Female).
4.  **Phase 2 (Mitigate):** Click the "Apply Bias Mitigation" button.
    * The system retrains the model using the **Exponentiated Gradient** reduction algorithm.
    * Observe how the new chart equalizes the approval rates (Fairness) with minimal loss in accuracy.

---

## 📂 Project Structure
* **backend/** - Contains the FastAPI server, machine learning logic, and API endpoints.
* **frontend/** - Contains the React.js user interface, styling, and charts.
* **README.md** - Project documentation and overview.

---

## 👨‍💻 Author
**Mangal Bhaduriya**
* *AI Ethics & Full-Stack Developer*
* [GitHub Profile](https://github.com/mangal3108)
