import os
import warnings
from typing import List, Dict
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_ibm import WatsonxLLM
from ibm_watsonx_ai.foundation_models import Model
import urllib3
import certifi
import torch

# Suppress torch warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

class RAGSystem:
    def __init__(self, data_processor):
        """Initialize the RAG system with a data processor."""
        load_dotenv()
        self.data_processor = data_processor
        self.embeddings = None
        self.vector_store = None
        self.qa_chain = None
        self.setup_rag()
    
    def setup_rag(self):
        """Set up the RAG system by creating embeddings for the data."""
        try:
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            # Create documents from the data
            documents = []
            for _, row in self.data_processor.df.iterrows():
                try:
                    doc = f"NAICS Code: {row[self.data_processor.naics_code_col]}\n"
                    doc += f"Title: {row[self.data_processor.naics_title_col]}\n"
                    doc += f"GHG: {row['GHG']}\n"
                    doc += f"Unit: {row['Unit']}\n"
                    doc += f"Supply Chain Emission Factors without Margins: {row['Supply Chain Emission Factors without Margins']}\n"
                    doc += f"Margins of Supply Chain Emission Factors: {row['Margins of Supply Chain Emission Factors']}\n"
                    doc += f"Supply Chain Emission Factors with Margins: {row['Supply Chain Emission Factors with Margins']}\n"
                    documents.append(doc)
                except KeyError as e:
                    print(f"Warning: Missing column in data: {str(e)}")
                    continue
            
            if not documents:
                raise ValueError("No valid documents could be created from the data")
            
            # Create embeddings and store them in FAISS
            self.vector_store = FAISS.from_texts(documents, self.embeddings)
            
            # Initialize watsonx.ai model
            api_key = os.getenv("IBM_API_KEY")
            cloud_url = os.getenv("IBM_CLOUD_URL")
            project_id = os.getenv("IBM_PROJECT_ID")
            
            if not all([api_key, cloud_url, project_id]):
                print("Warning: IBM Cloud credentials not found. Some features may be limited.")
                return
                
            try:
                # Configure SSL verification
                urllib3.disable_warnings()
                os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
                
                # Update cloud URL if needed
                if not cloud_url.startswith('https://'):
                    cloud_url = f'https://{cloud_url}'
                
                # Create credentials dictionary
                credentials = {
                    "apikey": api_key,
                    "url": cloud_url
                }
                
                # Initialize the model with proper parameters
                model = Model(
                    model_id="meta-llama/llama-3-405b-instruct",
                    credentials=credentials,
                    project_id=project_id
                )
                
                # Create QA chain
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=WatsonxLLM(model=model),
                    chain_type="stuff",
                    retriever=self.vector_store.as_retriever()
                )
            except Exception as e:
                print(f"Warning: Failed to initialize IBM watsonx.ai model: {str(e)}")
                print("The system will continue to work with basic search functionality.")
                
        except Exception as e:
            print(f"Error setting up RAG system: {str(e)}")
            raise
    
    def query(self, question: str, k: int = 3) -> List[str]:
        """Query the RAG system with a question."""
        if not self.vector_store:
            return ["Error: RAG system not properly initialized"]
            
        try:
            if self.qa_chain:
                # Use watsonx.ai for advanced querying
                response = self.qa_chain.run(question)
                return [response]
            else:
                # Fallback to basic search
                docs = self.vector_store.similarity_search(question, k=k)
                return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Error in query processing: {str(e)}")
            # Fallback to basic search
            try:
                docs = self.vector_store.similarity_search(question, k=k)
                return [doc.page_content for doc in docs]
            except Exception as e:
                return [f"Error processing query: {str(e)}"]
    
    def get_similar_documents(self, query: str, k: int = 3) -> List[Dict]:
        """Get similar documents from the vector store."""
        if not self.vector_store:
            return [{"error": "RAG system not properly initialized"}]
            
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
        except Exception as e:
            return [{"error": str(e)}] 