# AI-Based Resume Analyzer

## 📌 Project Overview

The AI-Based Resume Analyzer is a Machine Learning and Natural Language Processing (NLP) based web application that helps job seekers analyze and improve their resumes. The system automatically extracts text from PDF resumes, identifies technical and soft skills, predicts suitable job roles, evaluates ATS (Applicant Tracking System) compatibility, and provides feedback for resume enhancement.

The project is developed using Python and Streamlit and demonstrates the practical application of Artificial Intelligence in recruitment and resume screening.

---

## 🎯 Objectives

* Analyze resumes automatically using AI techniques.
* Extract text from uploaded PDF resumes.
* Identify technical and soft skills from resumes.
* Predict suitable job roles using Machine Learning.
* Calculate resume scores based on detected skills.
* Evaluate ATS compatibility.
* Suggest missing skills and resume improvements.

---

## 🚀 Features

* PDF Resume Upload
* Resume Text Extraction
* Skill Detection and Analysis
* Job Role Prediction
* Resume Score Calculation
* ATS Compatibility Check
* Missing Skills Identification
* Resume Improvement Suggestions
* Pie Chart Visualization of Skills

---

## 🛠 Technologies Used

### Programming Language

* Python

### Frontend

* Streamlit

### Libraries

* Pandas
* Scikit-learn
* Matplotlib
* pdfplumber
* Joblib

### Machine Learning Techniques

* TF-IDF Vectorization
* Multinomial Naive Bayes Classifier

---

## 📂 Dataset

**Dataset Name:** UpdatedResumeDataSet.csv

### Dataset Fields

| Field Name | Description                       |
| ---------- | --------------------------------- |
| Category   | Job category/domain of the resume |
| Resume     | Resume text content               |

### Categories Included

* Data Science
* Python Developer
* Java Developer
* Web Designing
* HR
* Business Analyst
* DevOps Engineer
* Testing
* Automation Testing
* ETL Developer
* SAP Developer
* Blockchain
* Database
* Mechanical Engineer
* Civil Engineer
* Electrical Engineering
* Network Security Engineer
* Operations Manager
* PMO
* Sales
* Health and Fitness
* Advocate
* Arts

---

## ⚙️ How It Works

1. User uploads a resume in PDF format.
2. The system extracts text using pdfplumber.
3. Resume text is cleaned and preprocessed.
4. Skills are matched against a predefined skills list.
5. TF-IDF converts text into numerical vectors.
6. The trained Multinomial Naive Bayes model predicts the job category.
7. Resume score is calculated based on identified skills.
8. ATS compatibility is analyzed.
9. Missing skills and feedback are displayed.
10. Results are shown through charts and reports.

---

## 💻 Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/AI_Resume_Analyzer.git
cd AI_Resume_Analyzer
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install streamlit pandas scikit-learn matplotlib pdfplumber joblib
```

---

## ▶️ Running the Project

### Train the Machine Learning Model

```bash
python train_model.py
```

### Run the Streamlit Application

```bash
python -m streamlit run app.py
```

The application will open in your default web browser.

---

## 📊 Output

The system generates:

* Resume Score
* ATS Compatibility Status
* Predicted Job Role
* Detected Skills
* Missing Skills
* Resume Feedback
* Skill Analysis Chart

---

## 📋 Software Requirements

* Python 3.8 or above
* Streamlit
* VS Code
* Scikit-learn
* Pandas
* Matplotlib
* pdfplumber

---

## 💾 Hardware Requirements

* Processor: Intel i3 or above
* RAM: 4 GB minimum
* Storage: 500 MB free space
* Operating System: Windows 10/11

---

## 🌟 Benefits

* Helps students improve resumes before applying for jobs.
* Increases ATS compatibility.
* Identifies missing skills.
* Saves recruiter screening time.
* Supports career development through AI-based feedback.

---

## 👩‍💻 Author

**Aishwarya Poojari**

