# Portfolio Shortlisting System

## Overview
This project implements a **Portfolio Shortlisting System** that leverages **Generative AI** and **Large Language Models (LLMs)**. The system evaluates student portfolios against job requirements and automates the shortlisting process, sending the results via email. 
---

## The technology stack includes:

- **LLM Model**: Predefined models like `llama-3.1-70b-versatile` from the ChatGroq cloud platform.
- **Database**: `ChromaDB` to store portfolio data as embeddings and metadata.
- **LangChain**: To handle prompt structuring and LLM interaction.

---

## Features
- Use of pre-trained LLM models.
- Dynamic conversational prompts via `ChatPromptTemplate`.
- Storage of portfolio data as vector embeddings using `ChromaDB`.
- Job-based portfolio evaluation and automated email notifications.

---



---

## Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:
```env
API_KEY=<Your Groq API Key>
MODEL_NAME=llama-3.1-70b-versatile
DATABASE_PATH=./chroma_db
MAX_TOKENS=None
TEMPERATURE=0.5
MAX_RETRIES=2
```

### Database Setup
Initialize the ChromaDB database:
```python
pip install chromadb
import chromadb                                    

# Initialize client instance in ChromaDB
chroma_client = chromadb.Client()

# Create Collection
collection = chroma_client.create_collection(name="my_collection")
```

---

## Code Workflow

### 1. Initialize LLM Model
```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-70b-versatile",       
    temperature=0.5,                       
    max_tokens=None,                       
    timeout=None,                           
    max_retries=2,                         
    api_key="your groq model API key"
)
```

### 2. Use ChatPromptTemplate
```python
from langchain_core.prompts import ChatPromptTemplate 

chat_prompt = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "You are an AI assistant helping to evaluate portfolios."},
    {"role": "user", "content": "input"}
])
```

### 3. Store Portfolio Data in ChromaDB
```python
import chromadb                                    

# Initialize client instance in ChromaDB
chroma_client = chromadb.Client()

# Create Collection
collection = chroma_client.create_collection(name="my_collection")

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

chain = chat_prompt | llm
result=chain.invoke(
    {
        "input": job_post,
        
    }
)
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


