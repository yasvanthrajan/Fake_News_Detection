# 📰 Fake News Detection using Cloud Technologies

This project leverages **Cloud Computing** and **Artificial Intelligence** to detect **fake news articles** efficiently using **AWS Cloud Services**. It utilizes various AWS services to create a fully integrated system for news validation.

---

## 🚀 Features

- **Fake News Classification**: Detects whether the news article is real or fake.
- **API Gateway**: Acts as a bridge between the frontend and backend for seamless communication.
- **AWS Lambda**: Handles the backend code execution for processing news data.
- **External Fact-Checking API**: Cross-checks news content using an external API for verification.
- **Amazon S3**: Stores the results of the classification process for further analysis.
- **CloudWatch**: Monitors and logs the activity of AWS Lambda functions for better performance tracking.

---

## 🛠️ Cloud Services Used

### 1. **API Gateway**
   - Serves as a bridge between the **Frontend** and **Backend**, enabling smooth communication for incoming and outgoing requests.

### 2. **AWS Lambda**
   - Executes the backend logic and processes the data for fake news detection.

### 3. **External Fact-Checking API**
   - Utilizes an external API to verify news content based on other sources.

### 4. **Amazon S3**
   - Stores processed results and data in secure S3 buckets for future analysis.

### 5. **Amazon CloudWatch**
   - Monitors AWS Lambda functions to track performance and logs for debugging.

---

## 🧠 How It Works

1. **User Input**: The user submits a news article through the frontend.
2. **API Gateway**: The request is passed to the API Gateway, which routes it to AWS Lambda.
3. **AWS Lambda**: The Lambda function processes the news content and interacts with the **External Fact-Checking API** to verify its authenticity.
4. **Result Storage**: The results of the fake news classification are stored in **Amazon S3** for future reference.
5. **Monitoring**: CloudWatch logs any errors or issues related to Lambda function execution, ensuring smooth operation.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: AWS Lambda (Python/Node.js), API Gateway
- **Cloud Services**: AWS (API Gateway, Lambda, S3, CloudWatch)
- **External API**: Fact-Checking API (for cross-referencing news)

---


---

## 🧪 How to Run Locally

### Prerequisites:
- AWS Account with **API Gateway**, **Lambda**, **S3**, and **CloudWatch** configured
- **AWS CLI** and **Boto3** installed
- **Python/Node.js** environment for backend Lambda functions

📊 Sample Output

Input News	Prediction
"Government launches new health policy..."	✅ Real
"Aliens spotted landing in New York..."	❌ Fake

