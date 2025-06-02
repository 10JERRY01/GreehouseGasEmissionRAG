import streamlit as st
import pandas as pd
from data_processor import DataProcessor
from rag_system import RAGSystem
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Supply Chain GHG Emissions RAG System",
    page_icon="🌍",
    layout="wide"
)

# Check IBM Cloud credentials
ibm_api_key = os.getenv("IBM_API_KEY")
ibm_cloud_url = os.getenv("IBM_CLOUD_URL")
ibm_project_id = os.getenv("IBM_PROJECT_ID")

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None

# Title and description
st.title("🌍 Supply Chain GHG Emissions RAG System")
st.markdown("""
This application allows you to query and analyze supply chain greenhouse gas emission data using natural language.
The system uses IBM watsonx.ai to provide intelligent responses to your questions about emission factors and trends.
""")

# File Upload Section
st.sidebar.header("Data Upload")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    if st.session_state.data_processor.load_from_upload(uploaded_file):
        st.sidebar.success("File uploaded successfully!")
        # Initialize RAG system with the new data
        if all([ibm_api_key, ibm_cloud_url, ibm_project_id]):
            st.session_state.rag_system = RAGSystem(st.session_state.data_processor)
        else:
            st.sidebar.warning("IBM watsonx.ai credentials not found. Some features may be limited.")
    else:
        st.sidebar.error("Error loading the file. Please check the file format.")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose a page:", ["Query System", "Data Analysis", "About"])

if page == "Query System":
    st.header("Ask Questions About GHG Emissions")
    
    if st.session_state.rag_system is None:
        if not all([ibm_api_key, ibm_cloud_url, ibm_project_id]):
            st.warning("""
            IBM watsonx.ai credentials not found. Please set the following environment variables:
            - IBM_API_KEY
            - IBM_CLOUD_URL
            - IBM_PROJECT_ID
            
            You can set these in a `.env` file in the project root.
            """)
        else:
            st.warning("Please upload a CSV file first to use the query system.")
    else:
        # Query input
        query = st.text_area("Enter your question about GHG emissions:", height=100)
        
        if st.button("Submit Query"):
            if query:
                with st.spinner("Processing your query..."):
                    try:
                        # Get RAG response
                        response = st.session_state.rag_system.query(query)
                        st.markdown("### Response")
                        st.write(response)
                        
                        # Show similar documents
                        st.markdown("### Related Information")
                        similar_docs = st.session_state.rag_system.get_similar_documents(query)
                        for doc in similar_docs:
                            st.markdown("---")
                            st.markdown(doc["content"])
                    except Exception as e:
                        st.error(f"Error processing query: {str(e)}")

elif page == "Data Analysis":
    st.header("Data Analysis")
    
    if st.session_state.data_processor.df is None:
        st.warning("Please upload a CSV file first to use the data analysis features.")
    else:
        # Get summary statistics
        summary = st.session_state.data_processor.get_emission_summary()
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", f"{summary['total_records']:,}")
        with col2:
            st.metric("Unique NAICS Codes", f"{summary['unique_naics']:,}")
        with col3:
            if 'columns' in summary:
                st.metric("NAICS Year", summary['columns']['naics_code_col'].split()[0])
        
        # Show column information
        if 'columns' in summary:
            st.subheader("Data Structure")
            st.write(f"NAICS Code Column: {summary['columns']['naics_code_col']}")
            st.write(f"NAICS Title Column: {summary['columns']['naics_title_col']}")
            st.write("Numeric Columns:", ", ".join(summary['columns']['numeric_cols']))
        
        # NAICS code search
        st.subheader("Search NAICS Codes")
        search_query = st.text_input("Enter NAICS code or description:")
        if search_query:
            results = st.session_state.data_processor.search_naics(search_query)
            if results:
                # Convert results to DataFrame for better display
                results_df = pd.DataFrame(results, columns=['NAICS Code', 'Description'])
                # Remove duplicates
                results_df = results_df.drop_duplicates()
                st.write(f"Found {len(results_df)} unique matches:")
                # Display as a table with better formatting
                st.dataframe(
                    results_df,
                    column_config={
                        "NAICS Code": st.column_config.TextColumn(
                            "NAICS Code",
                            width="medium",
                        ),
                        "Description": st.column_config.TextColumn(
                            "Description",
                            width="large",
                        ),
                    },
                    hide_index=True,
                )
            else:
                st.write("No matches found.")
        
        # Emission trends
        st.subheader("Emission Trends")
        naics_code = st.text_input("Enter NAICS code to view trends:")
        if naics_code:
            trends = st.session_state.data_processor.get_emission_trends(naics_code)
            if trends:
                st.write(f"### {trends['description']} ({trends['naics_code']})")
                st.write("Emission Factors:")
                st.write(pd.DataFrame.from_dict(trends['emission_factors'], orient='index', columns=['Value']))
            else:
                st.write("NAICS code not found.")

else:  # About page
    st.header("About the Project")
    st.markdown("""
    This project implements a Retrieval-Augmented Generation (RAG) system for analyzing supply chain greenhouse gas emission data.
    
    ### Features
    - Natural language querying of emission data
    - Advanced data analysis and visualization
    - Integration with IBM watsonx.ai for intelligent responses
    - CSV file upload support
    
    ### Data Source
    The project uses the Supply Chain GHG Emission Factors dataset which should contain:
    - NAICS codes and descriptions
    - GHG emission factors
    - USD values
    - Various emission categories and metrics
    
    ### Technology Stack
    - Python
    - Streamlit
    - IBM watsonx.ai
    - LangChain
    - FAISS for vector storage
    
    ### Setup Requirements
    To use all features, you need to set up the following environment variables in a `.env` file:
    ```
    IBM_API_KEY=your_api_key
    IBM_CLOUD_URL=your_cloud_url
    IBM_PROJECT_ID=your_project_id
    ```
    """) 