# Supply Chain GHG Emissions RAG System Documentation

## Project Overview
This project implements a Retrieval-Augmented Generation (RAG) system for analyzing supply chain greenhouse gas emission data. It provides an interactive interface for querying and analyzing emission data using natural language processing and advanced data analysis techniques.

## System Architecture

### Components
1. **Data Processor (`data_processor.py`)**
   - Handles CSV data loading and preprocessing
   - Supports flexible NAICS code formats (2017, 2022, etc.)
   - Provides data analysis and search functionality
   - Implements duplicate removal and data validation

2. **RAG System (`rag_system.py`)**
   - Implements the Retrieval-Augmented Generation system
   - Uses FAISS for vector storage and similarity search
   - Integrates with IBM watsonx.ai for advanced language processing
   - Handles document retrieval and response generation

3. **Web Application (`app.py`)**
   - Built with Streamlit for an interactive user interface
   - Provides file upload functionality
   - Implements query system and data analysis features
   - Offers real-time data visualization

### Data Requirements
The system accepts CSV files with the following required columns:
- NAICS Code (any year format, e.g., "2017 NAICS Code" or "2022 NAICS Code")
- NAICS Title (matching year format)
- GHG
- Unit
- Supply Chain Emission Factors without Margins
- Margins of Supply Chain Emission Factors
- Supply Chain Emission Factors with Margins

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- IBM Cloud account (for watsonx.ai integration)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with the following variables:
   ```
   IBM_API_KEY=your_api_key
   IBM_CLOUD_URL=your_cloud_url
   IBM_PROJECT_ID=your_project_id
   ```

### Running the Application
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Access the application at `http://localhost:8501`

## Usage Guide

### Data Upload
1. Click the "Upload your CSV file" button in the sidebar
2. Select your CSV file containing emission data
3. Wait for the file to be processed

### Query System
1. Navigate to the "Query System" page
2. Enter your question about GHG emissions
3. Click "Submit Query" to get the response
4. View related information below the response

### Data Analysis
1. Navigate to the "Data Analysis" page
2. View summary statistics
3. Search for specific NAICS codes or descriptions
4. Analyze emission trends for specific codes

## Features

### Data Processing
- Flexible NAICS code format support
- Automatic duplicate removal
- Data validation and error handling
- Efficient chunk-based processing for large files

### Search and Analysis
- Natural language querying
- Advanced NAICS code search
- Emission trend analysis
- Summary statistics generation

### User Interface
- Interactive file upload
- Real-time data visualization
- Responsive design
- Clear error messages and feedback

## Troubleshooting

### Common Issues
1. **File Upload Errors**
   - Ensure CSV file has all required columns
   - Check file format and encoding
   - Verify file size is within limits

2. **API Connection Issues**
   - Verify IBM Cloud credentials
   - Check internet connection
   - Ensure API key is valid

3. **Data Processing Errors**
   - Verify CSV format
   - Check for missing or invalid data
   - Ensure proper column names

### Error Messages
- "Missing required columns": Check CSV file structure
- "Could not find NAICS Code and Title columns": Verify column names
- "Error loading data": Check file format and content

## Performance Considerations
- Large files are processed in chunks
- Vector storage uses FAISS for efficient similarity search
- Duplicate removal optimizes data storage
- Caching improves response times

## Security
- API keys stored in environment variables
- Temporary file cleanup after processing
- Input validation and sanitization
- Secure file handling

## Future Improvements
1. Additional data format support
2. Enhanced visualization options
3. Batch processing capabilities
4. Advanced filtering options
5. Export functionality
6. User authentication
7. API rate limiting
8. Caching improvements 