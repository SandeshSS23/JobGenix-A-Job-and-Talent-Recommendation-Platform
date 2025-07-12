# 💼 JobGenix – Intelligent Resume Shortlister & Job Recommendation System

JobGenix is an AI-driven web application built to streamline the recruitment process for both job seekers and recruiters. The system automates job data extraction, resume parsing, and provides intelligent, personalized job and candidate recommendations using state-of-the-art machine learning and NLP techniques.

---

## 🚀 Features

- 🔍 **Personalized Job Recommendations** based on candidate skills, experience, and preferences.
- 🤝 **Resume Shortlisting for Recruiters** using semantic and contextual analysis.
- 🤖 **Hybrid Recommendation Engine** combining:
  - Content-Based Filtering (TF-IDF, BERT)
  - Collaborative Filtering
  - Word Embeddings (Word2Vec, FastText)
- 📄 **Automated Resume Parsing** using NLP techniques.
- 🌐 **Web Scraping** of job listings using Selenium.
- 🔄 **Daily Job Updates** via CI/CD-scheduled fetch pipeline (corn jobs).
- 📊 **Performance Evaluation** with metrics like Precision@K, Recall, RMSE, NDCG, and F1-score.

---

## 🧠 Tech Stack

### 🔹 Frontend
- React.js
- Redux (if used)
- Tailwind CSS / Bootstrap

### 🔹 Backend
- Node.js
- Express.js
- MongoDB (Mongoose)
- JWT for Auth
- Firebase / Google OAuth (optional)

### 🔹 Machine Learning / NLP
- Python (Jupyter Notebooks for training/testing)
- Scikit-learn, BERT (transformers), TF-IDF, KNN
- Pandas, NumPy

### 🔹 Automation
- Selenium (Web Scraping)
- CI/CD (GitHub Actions / Cron for scheduled job fetch)

---

## 📈 Results

| Model         | RMSE  | Precision | Recall | F1-Score | NDCG |
|---------------|-------|-----------|--------|----------|------|
| Random        | 0.96  | 0.58      | 0.05   | 0.09     | 0.38 |
| Content-Based | 1.04  | 0.72      | 0.47   | 0.57     | 0.55 |
| Collaborative | 1.66  | 0.62      | 0.55   | 0.53     | 0.48 |
| **Hybrid**    | 0.76  | 0.72      | **1.00**| **0.84** | **0.81** |

---

Contributors
Sandesh Sahane : SandeshSS23
Vedang Khedekar : vedang1010

