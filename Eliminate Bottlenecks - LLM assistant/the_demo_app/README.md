# TechAdvance Solutions - Enterprise Data Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-red.svg)](https://streamlit.io/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.10+-green.svg)](https://www.llamaindex.ai/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange.svg)](https://openai.com/)

A modern enterprise data intelligence platform that demonstrates AI-powered document and database querying capabilities. Built with Streamlit, LlamaIndex, and OpenAI integration, featuring a professional corporate design.

![TechAdvance Solutions Demo](https://img.shields.io/badge/Demo-Live-success)

## 🚀 Features

- **🤖 AI-Powered Intelligence**: OpenAI GPT-3.5-turbo integration with graceful MockLLM fallback
- **📊 Dual Data Sources**: Query both structured databases and unstructured documents
- **🎨 Corporate Design**: Professional UI with modern styling and custom branding
- **🔄 Automated Setup**: One-command startup scripts for Windows PowerShell
- **🐳 Docker Ready**: Containerized deployment support
- **📱 Responsive UI**: Modern, accessible interface built with Streamlit

## 🏗️ Technical Architecture

### Core Components
- **Frontend**: Streamlit web application with custom CSS styling
- **AI Engine**: LlamaIndex with OpenAI GPT-3.5-turbo and embedding models
- **Data Layer**: SQLite database + markdown document processing
- **Server**: FastMCP server for additional tooling capabilities

### Technology Stack
- **Python 3.11+**: Core runtime environment
- **Streamlit**: Web UI framework with custom theming
- **LlamaIndex**: Document indexing and AI query processing
- **OpenAI API**: GPT-3.5-turbo for intelligent responses
- **SQLite**: Lightweight database for structured data
- **FastMCP**: Model Context Protocol server implementation

### Data Sources
1. **Structured Database**: Employee records, departments, clients, services, financial data
2. **Unstructured Documents**: HR policies, security guidelines, sales playbooks, procedures

## 📁 Project Structure

```
TechAdvance-Solutions/
├── app/
│   ├── main.py              # Simple demo application
│   ├── enterprise_app.py    # Full enterprise platform
│   └── __init__.py
├── src/
│   └── data_sources/
│       ├── database_handler.py    # SQLite database interface
│       ├── document_handler.py    # Document processing
│       └── __init__.py
├── data/
│   ├── database/
│   │   └── company.db            # SQLite database (auto-generated)
│   └── documents/
│       ├── hr/                   # HR policies and handbooks
│       ├── policies/             # Security and compliance docs
│       └── sales/                # Sales procedures and playbooks
├── scripts/
│   └── create_database.py        # Database setup and population
├── mcp_server/
│   ├── server.py                 # FastMCP server implementation
│   └── __init__.py
├── .streamlit/
│   └── config.toml               # Streamlit configuration
├── start_app.py                  # Python startup script
├── start_app.ps1                 # PowerShell startup script
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container configuration
└── README.md
```

## 🛠️ Getting Started

### Prerequisites
- **Python 3.11 or higher**
- **Git** (for cloning the repository)
- **OpenAI API Key** (optional, but recommended for full functionality)

### 📥 Download and Setup

<<<<<<< HEAD
#### Option 1: Automated Setup (Recommended)
```powershell
# 1. Clone the repository
git clone https://github.com/yourusername/TechAdvance-Solutions.git
cd TechAdvance-Solutions

# 2. Run the automated setup script
.\start_app.ps1
```

The script will automatically:
- ✅ Create and activate a virtual environment
- ✅ Install all dependencies
- ✅ Prompt for your OpenAI API key (securely stored in `.venv/`)
- ✅ Create the database
- ✅ Launch the application

#### Option 2: Manual Setup
```powershell
# 1. Clone the repository
git clone https://github.com/yourusername/TechAdvance-Solutions.git
cd TechAdvance-Solutions

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
python -m pip install -r requirements.txt

# 5. Create database
python scripts/create_database.py

# 6. Start the application
streamlit run app/enterprise_app.py
```

### 🔑 OpenAI API Key Setup
**The automated script will guide you through this process interactively.**

For manual setup:
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create your API key (requires account with credits)
3. The script will securely store it in `.venv/openai_config.txt`

**⚠️ Security**: 
- Your API key is stored locally in `.venv/` (not committed to Git)
- Never share your API key publicly
- The repository does **NOT** include any API keys
=======
#### 1. Clone the Repository
```powershell
git clone https://github.com/yourusername/TechAdvance-Solutions.git
cd TechAdvance-Solutions
```

#### 2. Create Virtual Environment
```powershell
   python -m venv .venv
```

#### 3. Activate Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```

#### 4. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

#### 5. Set Up OpenAI API Key (Recommended)
The startup scripts will automatically create a `.env` template file for you. You must:
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create your own API key
3. Add credits to your OpenAI account ($5-10 minimum recommended)
4. Edit the `.env` file and replace `your_openai_api_key_here` with your actual API key

**⚠️ Important**: The repository does **NOT** include any OpenAI API keys. All keys must be provided by the user.
>>>>>>> 90fd3198baf6326b2fee62bdd5459fd732dfde2c

#### 6. Initialize Database
```powershell
python scripts/create_database.py
```

## 🚀 How to Start the Application

### Option 1: Automated Startup (Recommended)
```powershell
# Navigate to project directory
cd "path\to\TechAdvance-Solutions"

# Run automated startup script
.\start_app.ps1
```

### Option 2: Manual Startup
```powershell
# Navigate to project directory
cd "path\to\TechAdvance-Solutions"

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies (if needed)
python -m pip install -r requirements.txt

# Create database (if needed)
python scripts/create_database.py

# Start the enterprise application
streamlit run app/enterprise_app.py
```

### Option 3: Python Script
```powershell
# Navigate to project directory
cd "path\to\TechAdvance-Solutions"

# Run Python startup script
python start_app.py
```

### 🌐 Access the Application
Once started, the application will be available at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://[your-ip]:8501

## 🔧 Configuration Options

### OpenAI Integration
- **With API Key**: Full GPT-3.5-turbo intelligence for natural language queries
- **Without API Key**: MockLLM fallback for demonstration purposes

### Application Modes
- **Enterprise App** (`app/enterprise_app.py`): Full-featured platform with database and document querying
- **Simple Demo** (`app/main.py`): Basic document intelligence demonstration

## 🐳 Docker Deployment

### Build Container
```powershell
docker build -t techadvance-solutions .
```

### Run Application
```powershell
# Run Streamlit app
docker run --rm -p 8501:8501 techadvance-solutions

# Run MCP server
docker run --rm techadvance-solutions python -m mcp_server.server
```

### With Environment Variables
```powershell
docker run --rm -p 8501:8501 -e OPENAI_API_KEY=your_key_here techadvance-solutions
```

## 💡 Usage Examples

### Database Questions
- "What is the average salary by department?"
- "How many employees work in Cloud Services?"
- "Show me all consultants in the Infrastructure team"
- "What's our total revenue from enterprise clients?"

### Document Questions
- "What is the company vacation policy?"
- "How do we handle security incidents?"
- "What are the sales qualification criteria?"
- "What benefits do employees receive?"

## 🔒 Security & Privacy

- **Local Processing**: All data remains on your local machine
- **API Key Security**: Store OpenAI keys in `.env` files (never commit to version control)
- **Data Isolation**: Each deployment uses its own database and document store
- **Graceful Degradation**: Application continues working even without API access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

#### "OpenAI quota exceeded" Error
- **Solution**: Add credits to your OpenAI account at https://platform.openai.com/settings/organization/billing
- **Alternative**: The application will automatically fall back to MockLLM

#### Virtual Environment Issues
- **Solution**: Delete `.venv` folder and recreate: `python -m venv .venv`

#### Port 8501 Already in Use
- **Solution**: Kill existing Streamlit processes or use a different port: `streamlit run app/enterprise_app.py --server.port 8502`

#### Database Not Found
- **Solution**: Run the database creation script: `python scripts/create_database.py`

## 📞 Support

For questions, issues, or feature requests:
- 📧 Email: support@techadvance-solutions.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/TechAdvance-Solutions/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/TechAdvance-Solutions/wiki)

---

**⚡ TechAdvance Solutions - We Deliver Digital Transformation**

*Built with ❤️ using Python, Streamlit, and AI*
