# 🚀 Elite Data Analyst Agent

An advanced, multimodal AI agent built with Streamlit and OpenAI that can analyze data, create visualizations, and interact with files and external APIs. This project serves as a powerful, interactive chat interface for complex data analysis tasks.

## ✨ Key Features

* **Multimodal Capabilities:** Upload and analyze images directly within the chat using a vision-enabled model.
* **Dynamic Tool-Use:** The agent intelligently chooses from a suite of custom tools to perform tasks like reading files, fetching stock data, and summarizing text.
* **File Handling:** Seamlessly upload and process CSV and PDF files from the sidebar. The agent gains instant access to the uploaded data.
* **Data Visualization:** Generate and display elegant plots (bar, line, scatter, histogram, boxplot) directly in the chat.
* **Python Code Interpreter:** Execute Python code to perform complex data manipulation on an active DataFrame.
* **Persistent Memory:** Chat history is saved to a local `chat_history.json` file, so your conversations and uploaded data are remembered between sessions.
* **Intuitive UI:** A clean and modern user interface with real-time feedback on the agent's thought process and tool-use.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+**
* **pip** (Python package installer)
* An **OpenAI API Key**
* An **Alpha Vantage API Key** (optional, but required for the stock data tool)

## 📦 Installation

1.  **Clone the project:**
    ```bash
    git clone [https://github.com/your-username/data-analyst-agent-elite.git](https://github.com/your-username/data-analyst-agent-elite.git)
    cd data-analyst-agent-elite
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API keys:**
    Create a file named `.env` in the root directory of the project and add your API keys:
    ```
    OPENAI_API_KEY="sk-..."
    ALPHA_VANTAGE_API_KEY="..."
    ```

4.  **Create the necessary directories:**
    The project expects the following directory structure. Create them manually if they don't exist:
    ```
    data/
    data/plots/
    tools/
    ```

## 🚀 Usage

To start the agent, run the following command from the project's root directory:

```bash
streamlit run streamlit_app.py
The application will open in your web browser. You can then interact with the agent by:

Typing a prompt in the chat box.

Uploading a CSV or PDF file using the sidebar.

Dragging and dropping an image into the chat area.

📂 Project Structure
.
├── .env                     # API keys
├── requirements.txt         # Project dependencies
├── streamlit_app.py         # Main application file
├── config.py                # Tool definitions and configurations
├── ui_components.py         # UI rendering functions
├── tools/                   # Custom tool functions
│   ├── __init__.py
│   ├── file_tools.py
│   ├── plotting_tools.py
│   ├── openai_tools.py
│   ├── external_tools.py
│   ├── pdf_tools.py
│   └── image_tools.py
├── data/                    # For uploaded and example files
│   ├── sales_data.csv       # (Example CSV file)
│   └── plots/               # Generated plots are saved here
└── chat_history.json        # Persistent chat memory
🤖 Tool Reference
The agent has access to the following tools:

read_csv_tool: Reads a CSV file and returns its content.

list_directory_tool: Lists files in a specified directory.

plot_data_tool: Creates and saves various types of plots from a given dataset.

summarize_text: Summarizes a block of text using a large language model.

fetch_stock_data: Fetches real-time stock data from an external API.

extract_text_from_pdf: Extracts text content from a PDF file.

execute_python_code_tool: Runs Python code for data manipulation.

analyze_image_tool: Analyzes an image and answers questions about its content.

get_unique_values (Dynamic): Returns unique values from a column in the active DataFrame.

calculate_column_stats (Dynamic): Calculates statistics for a numeric column.
