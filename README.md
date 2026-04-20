#  AI and LLM Powered Personalized Lifestyle Risk Awareness System (Web App)

**Live Demo:** [Lifelens AI App on Hugging Face Spaces](https://huggingface.co/spaces/anukhatua15/Lifelens_AI)  
**GitHub Repository:** https://github.com/Anushka0615/lifelensaiapp 
---

## Project Overview

This project presents an AI-powered system for **analyzing lifestyle behavior and estimating health risk levels** using Machine Learning and Deep Learning techniques.

Modern digital lifestyles often involve **poor sleep, low physical activity, excessive screen time, and unhealthy routines**, which can lead to long-term health risks. Unlike traditional systems that focus on diagnosis, this platform emphasizes **preventive awareness** through personalized insights.

The web application allows users to input lifestyle data and receive:

* Risk Scores
* Behavioral Analysis
* AI-generated Personalized Insights

---

## Objectives

* Analyze daily lifestyle patterns using data-driven techniques
* Identify unhealthy habits and behavioral trends
* Predict lifestyle risk levels (Low / Medium / High)
* Provide personalized preventive recommendations
* Build a complete end-to-end AI-based web system

---

## System Architecture
                ┌────────────────────┐
                │     User Input     │
                │ (Lifestyle Data)   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │    Backend API     │
                │ (Flask / FastAPI)  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   ML/DL Model      │
                │ (Risk Prediction)  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │     Risk Score     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │     LLM Engine     │
                │ (Insight Generator)│
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Personalized       │
                │ Insights           │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Frontend Dashboard │
                │ (Visualization UI) │
                └────────────────────┘

---

## Methodology

* **Data Collection:** Public lifestyle datasets (UCI, Kaggle)
* **Preprocessing:** Cleaning, normalization, feature engineering
* **EDA:** Identifying patterns in activity, sleep, and routines
* **Modeling:**

  * Logistic Regression
  * Random Forest
  * Artificial Neural Network (ANN)
* **Evaluation:** Accuracy, Precision, Recall, F1-Score
* **Deployment:** Flask-based web application

---

## Model Details

* **Architecture:** Artificial Neural Network (ANN)
* **Loss Function:** Categorical Cross-Entropy
* **Optimizer:** Adam
* **Output:** Lifestyle Risk Classification (Low / Medium / High)

**ANN Structure:**

* Input Layer → Lifestyle Features
* Hidden Layers → Dense + ReLU
* Dropout → Regularization
* Output Layer → Softmax

---

## Dataset

### Primary Dataset

* Human Activity Recognition Using Smartphones (UCI / Kaggle)

### Additional Datasets

* Fitbit Lifestyle Tracker Data
* Daily and Sports Activities Dataset

### Data Characteristics

* 10,299 instances
* 561 features
* 6 activity classes
* Sensor-based behavioral data

---

## Model Performance

| Metric      | Value                                     |
| :---------- | :---------------------------------------- |
| Models Used | Logistic Regression / Random Forest / ANN |
| Accuracy    | *(96.16%) / (92.67%) / (91.48%)*          |
| Precision   | Balanced                                  |
| Recall      | Balanced                                  |
| Environment | Jupyter Notebook / Colab                  |

**Observations:**

* ANN provides better generalization
* Feature engineering improves prediction quality
* Lifestyle patterns strongly influence risk classification

---

## Repository Structure

```
project-name/
├── app.py                 # Flask backend
├── model/                # Trained ML/DL models
├── requirements.txt      # Dependencies
├── static/               # CSS, JS, assets
├── templates/            # HTML pages
├── utils/                # Helper functions
└── README.md
```

---

## Features

* **Risk Score Dashboard** – Visual health & lifestyle analysis
* **AI Risk Prediction** – Low / Medium / High classification
* **LLM Insights** – Personalized lifestyle recommendations
* **Analytics Visualization** – Graphs & trends
* **Full-Stack Web App** – Clean and interactive UI

---

## Note on Model Training

> Training was performed separately using Jupyter Notebook / Google Colab.
> This repository contains the **final trained models and deployment code only**.

---

## Future Enhancements

* Integration with wearable devices (Fitbit, smartwatches)
* Mobile application development
* Advanced DL models (LSTM / time-series analysis)
* Multi-user analytics & comparison
* Cloud deployment and scaling

---

## Authors
**Anushka Khatua** – M.Tech in AI & DS (KIIT University, Bhubaneswar)   
*Advanced Industry Integrated Program – LTIMindTree & KIIT University*

---

## License
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this project with proper attribution.

---
