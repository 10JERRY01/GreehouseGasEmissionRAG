# Supply Chain GHG Emissions RAG System

A powerful tool for analyzing and querying supply chain greenhouse gas emission data using Retrieval-Augmented Generation (RAG) technology.

## 🌟 Features

- **Flexible Data Support**: Works with NAICS codes from any year (2017, 2022, etc.)
- **Natural Language Queries**: Ask questions about emission data in plain English
- **Advanced Analysis**: Get detailed insights and trends from your data
- **Interactive UI**: User-friendly interface built with Streamlit
- **Smart Search**: Find relevant NAICS codes and descriptions quickly
- **Duplicate Prevention**: Automatic handling of duplicate records

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**:
   Create a `.env` file with your IBM Cloud credentials:
   ```
   IBM_API_KEY=your_api_key
   IBM_CLOUD_URL=your_cloud_url
   IBM_PROJECT_ID=your_project_id
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📋 Project Submission

### Required Files
1. Source Code:
   - `app.py`
   - `data_processor.py`
   - `rag_system.py`
   - `requirements.txt`

2. Documentation:
   - `README.md`
   - `documentation.md`

3. Sample Data:
   - Include a sample CSV file with the required format

### Submission Steps
1. Create a GitHub repository
2. Push all project files to the repository
3. Ensure the repository is public
4. Include a link to the live demo (if available)
5. Submit the repository URL to the hackathon platform

### Demo Video
Create a short video (3-5 minutes) demonstrating:
1. Project setup
2. Data upload process
3. Query system usage
4. Data analysis features
5. Key functionalities

## 📚 Documentation

For detailed documentation, please refer to:
- [Documentation.md](documentation.md) for technical details
- [Setup Guide](documentation.md#setup-instructions) for installation steps
- [Usage Guide](documentation.md#usage-guide) for how to use the system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- IBM watsonx.ai for the language model integration
- Streamlit for the web application framework
- FAISS for vector storage
- All contributors and supporters of the project 