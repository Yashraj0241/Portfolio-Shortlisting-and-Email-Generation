# Portfolio Shortlisting System

## Overview
This project implements a **Portfolio Shortlisting System** that leverages **Generative AI** and **Large Language Models (LLMs)**. The system evaluates student portfolios against job requirements and automates the shortlisting process, sending the results via email. 

## The technology stack includes:

- **LLM Model**: Predefined models like `llama-3.1-70b-versatile` from the ChatGroq cloud platform.
- **Database**: `ChromaDB` to store portfolio data as embeddings and metadata.
- **LangChain**: To handle prompt structuring and LLM interaction.

## Features
- Use of pre-trained LLM models.
- Dynamic conversational prompts via `ChatPromptTemplate`.
- Storage of portfolio data as vector embeddings using `ChromaDB`.
- Job-based portfolio evaluation and automated email notifications.

---

## Installation

### Prerequisites
1. Python 3.8 or higher.
2. Install dependencies:
   ```bash
   pip install langchain chromadb openai
   ```
3. Access to the ChatGroq cloud platform API.

### Clone the Repository
```bash
git clone https://github.com/your-repository/portfolio-shortlisting.git
cd portfolio-shortlisting
```

---

## Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:
```env
API_KEY=<Your ChatGroq API Key>
MODEL_NAME=llama-3.1-70b-versatile
DATABASE_PATH=./chroma_db
MAX_TOKENS=1000
TEMPERATURE=0.7
MAX_RETRIES=3
SMTP_SERVER=smtp.example.com
EMAIL_USER=<Your Email Address>
EMAIL_PASSWORD=<Your Email Password>
```

### Database Setup
Initialize the ChromaDB database:
```python
from chromadb.config import Settings
from chromadb import Client

# Initialize ChromaDB
client = Client(Settings(persist_directory='./chroma_db'))

# Create Collection
collection = client.create_collection("my_collection")
```

---

## Code Workflow

### 1. Initialize LLM Model
```python
from langchain.llms import OpenAI

llm = OpenAI(
    model_name="llama-3.1-70b-versatile",
    api_key="<Your API Key>",
    max_tokens=1000,
    temperature=0.7,
    max_retries=3
)
```

### 2. Use ChatPromptTemplate
```python
from langchain.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "You are an AI assistant helping to evaluate portfolios."},
    {"role": "user", "content": "Provide portfolio details for evaluation."}
])
```

### 3. Store Portfolio Data in ChromaDB
```python
import chromadb

client = chromadb.Client(Settings(persist_directory='./chroma_db'))
collection = client.get_collection("my_collection")

# Example data
portfolio_data = {
    "student_id": "12345",
    "portfolio": "Sample portfolio content here",
    "job_post": "Job description here"
}

# Store data
vector = llm.embed_text(portfolio_data["portfolio"])
collection.add(
    embeddings=[vector],
    metadatas=[{"student_id": portfolio_data["student_id"]}],
    documents=[portfolio_data["portfolio"]]
)
```

### 4. Combine Prompt with LLM
```python
from langchain.chains import LLMChain

chain = LLMChain(prompt=chat_prompt, llm=llm)
response = chain.run("Evaluate this portfolio for the job requirements.")
```



---

## How It Works

1. **Input**: The user uploads portfolio data and job descriptions.
2. **Processing**:
   - Portfolio content is stored in `ChromaDB`.
   - `ChatPromptTemplate` structures the conversation for evaluation.
   - The LLM evaluates the portfolio against the job description.
3. **Output**:
   - Shortlisted results are determined.
   - Notifications are sent via email.

---


