import os
import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS         
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document  # Import Document class
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Load API keys
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Streamlit title
st.title("Portfolio Shortlisting and Email Generation")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.1-70b-versatile",       
    temperature=0.5,                       
    max_tokens=None,                        
    timeout=None,                          
    max_retries=2,                         
    api_key=groq_api_key
)

# Chat Prompt Template for Questions
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided portfolio context only.
    Please provide the most accurate response based on the given information.
    <context>
    {context}
    <context>
    Questions: {input}
    """
)

# Chat Prompt Template for Email Generation
prompt_email = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """We are working as a placement officer in placement consultancy Codespyder Technology.
            We have shortlisted candidates' portfolios as per the requirements in the TCS job post.
            Create an email to the recruitment team of TCS mentioning that we have the best suitable candidates for this job post.
            Do not provide unnecessary extra information.
            """,
        ),
        ("human", "{input}"),
    ]
)

def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.data = pd.read_csv(st.session_state.uploaded_file)
        st.session_state.docs = []
        
        for idx, row in st.session_state.data.iterrows():
            doc = Document(
                page_content=f"Portfolio: {row['name']}, Skills: {row['skills']}, Experience: {row['experience']}, Location: {row['location']}",
                metadata={"source": f"portfolio_{idx}"}
            )
            st.session_state.docs.append(doc)
        
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# Upload file
uploaded_file = st.file_uploader("Upload Portfolio Data (CSV)", type="csv")
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file

# Button to create vector store
if st.button("Create Vector Store"):
    if uploaded_file is None:
        st.error("Please upload a portfolio data file first.")
    else:
        vector_embedding()
        st.write("Vector Store DB is ready!")

# Input field for user query
prompt1 = st.text_input("What do you want to ask about the portfolios?")

if prompt1:
    if "vectors" not in st.session_state:
        st.error("Please create the vector store first by clicking the button.")
    else:
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = st.session_state.vectors.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        start = time.process_time()
        response = retrieval_chain.invoke({"input": prompt1})
        end = time.process_time()

        # Handle response and generate email
        if "answer" in response:
            st.write(f"Answer: {response['answer']}")
            st.write(f"Response Time: {end - start:.2f} seconds")

            # Generate email using email prompt
            chain_email = prompt_email | llm
            email_input = f"Details: {response['answer']}"
            result_email = chain_email.invoke({"input": email_input})

            # Display the generated email
            st.subheader("Generated Email:")
            st.text_area("Email Content", result_email.content, height=300)
        else:
            st.error("Unable to generate a response. Please refine your query.")
