import streamlit as st
import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import io
import time

# --- Import tool functions and configuration ---
from config import STATIC_TOOLS
from tools.file_tools import read_csv_tool, list_directory_tool
from tools.plotting_tools import plot_data_tool
from tools.openai_tools import summarize_text
from tools.external_tools import fetch_stock_data
from tools.pdf_tools import extract_text_from_pdf

# --- Configuration and UI Setup ---
load_dotenv()
st.set_page_config(page_title="Ultimate Data Analyst Agent", layout="wide")
st.title("🚀 Ultimate Data Analyst Agent")
st.markdown("---")

# --- Memory Persistence ---
CHAT_HISTORY_FILE = "chat_history.json"

def save_chat_history():
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(st.session_state.messages, f)

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            st.session_state.messages = json.load(f)
    else:
        st.session_state.messages = [{"role": "system", "content": "You are a powerful data analyst agent with access to multiple tools. You can analyze data, create visualizations, fetch external data, and read documents."}]
        if os.path.exists("data/sales_data.csv"):
            st.session_state.messages.append({"role": "system", "content": "The default file 'data/sales_data.csv' is available for analysis."})

# --- OpenAI Client Setup ---
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

if not api_key:
    st.error("Please set your OPENAI_API_KEY in the .env file.")
    st.stop()

# --- Tool Executor and Dynamic Tool Functions ---
def execute_python_code_tool(code: str, data: str = None) -> str:
    local_vars = {}
    if data:
        try:
            local_vars['df'] = pd.read_json(data)
        except Exception as e:
            return f"Error loading data: {e}"
    restricted_globals = {
        'pd': pd,
        'plt': None, 'os': None,
        '__builtins__': {'print': print, 'len': len, 'str': str, 'int': int, 'float': float, 'list': list, 'dict': dict,}
    }
    output_buffer = io.StringIO()
    try:
        exec(code, restricted_globals, local_vars)
        captured_output = output_buffer.getvalue()
        if 'df' in local_vars:
            final_data = local_vars['df'].to_json(orient='records')
            return f"Execution successful. DataFrame updated. Output: {captured_output}\nFinal data: {final_data}"
        else:
            return f"Execution successful. Output: {captured_output}"
    except Exception as e:
        return f"Error during code execution: {e}"
    finally:
        output_buffer.close()

def generate_dynamic_tools(df: pd.DataFrame) -> list:
    dynamic_tools = []
    unique_values_tool = { "type": "function", "function": { "name": "get_unique_values", "description": "Returns a list of unique values from a specified column of the active DataFrame.", "parameters": { "type": "object", "properties": { "column": {"type": "string", "description": "The name of the column to get unique values from."} }, "required": ["column"], }, }, }
    dynamic_tools.append(unique_values_tool)
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_columns:
        calculate_stats_tool = { "type": "function", "function": { "name": "calculate_column_stats", "description": "Calculates descriptive statistics (mean, median, sum) for a specified numeric column.", "parameters": { "type": "object", "properties": { "column": { "type": "string", "description": "The name of the numeric column.", "enum": numeric_columns } }, "required": ["column"], }, }, }
        dynamic_tools.append(calculate_stats_tool)
    return dynamic_tools

def get_unique_values(column: str) -> str:
    if "df" not in st.session_state: return "No DataFrame loaded."
    df = st.session_state.df
    if column not in df.columns: return f"Error: Column '{column}' not found."
    unique_vals = df[column].unique().tolist()
    return f"Unique values in column '{column}': {unique_vals}"

def calculate_column_stats(column: str) -> str:
    if "df" not in st.session_state: return "No DataFrame loaded."
    df = st.session_state.df
    if column not in df.columns: return f"Error: Column '{column}' not found."
    if not pd.api.types.is_numeric_dtype(df[column]): return f"Error: Column '{column}' is not a numeric type."
    mean_val = df[column].mean()
    median_val = df[column].median()
    sum_val = df[column].sum()
    return (f"Statistics for column '{column}':\n" f"Mean: {mean_val}\n" f"Median: {median_val}\n" f"Sum: {sum_val}")

available_functions = {
    "read_csv_tool": read_csv_tool, "list_directory_tool": list_directory_tool, "plot_data_tool": plot_data_tool,
    "summarize_text": summarize_text, "fetch_stock_data": fetch_stock_data, "extract_text_from_pdf": extract_text_from_pdf,
    "execute_python_code_tool": execute_python_code_tool, "get_unique_values": get_unique_values, "calculate_column_stats": calculate_column_stats,
}

# --- Sidebar and File Uploads ---
st.sidebar.header("Data Uploads")
uploaded_csv = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
uploaded_pdf = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

if st.sidebar.button("Reset Chat"):
    st.session_state.clear()
    load_chat_history()
    st.rerun()

# --- Handle uploaded files
if uploaded_csv is not None:
    if "uploaded_csv_path" not in st.session_state or st.session_state.uploaded_csv_name != uploaded_csv.name:
        if not os.path.exists("data"): os.makedirs("data")
        filepath = os.path.join("data", uploaded_csv.name)
        with open(filepath, "wb") as f: f.write(uploaded_csv.getbuffer())
        st.session_state["uploaded_csv_path"] = filepath
        st.session_state["uploaded_csv_name"] = uploaded_csv.name
        st.sidebar.success(f"CSV file '{uploaded_csv.name}' uploaded and ready!")
        df = pd.read_csv(filepath)
        st.session_state.df = df
        st.session_state.dynamic_tools = generate_dynamic_tools(df)
        st.session_state.messages.append({"role": "system", "content": f"A new CSV file '{uploaded_csv.name}' is available. I've automatically generated new tools to analyze its columns."})
        st.rerun()

if uploaded_pdf is not None:
    if "uploaded_pdf_path" not in st.session_state or st.session_state.uploaded_pdf_name != uploaded_pdf.name:
        if not os.path.exists("data"): os.makedirs("data")
        filepath = os.path.join("data", uploaded_pdf.name)
        with open(filepath, "wb") as f: f.write(uploaded_pdf.getbuffer())
        st.session_state["uploaded_pdf_path"] = filepath
        st.session_state["uploaded_pdf_name"] = uploaded_pdf.name
        st.sidebar.success(f"PDF file '{uploaded_pdf.name}' uploaded and ready!")
        st.session_state.messages.append({"role": "system", "content": f"A new PDF file '{uploaded_pdf.name}' is available. Use the 'extract_text_from_pdf' tool to read its contents."})
        st.rerun()

# --- Session State and UI ---
if "messages" not in st.session_state:
    load_chat_history()
    st.session_state.dynamic_tools = []
    st.session_state.df = None

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            if message.get("plot_path"):
                st.image(message["plot_path"])
            st.markdown(message["content"])

# --- Main Chat Input and Logic ---
if user_prompt := st.chat_input("Ask me to analyze your data or a document..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        all_tools = STATIC_TOOLS + st.session_state.dynamic_tools
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        with st.status("Agent is thinking...", expanded=True) as status:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=all_tools,
                tool_choice="auto",
                stream=True,
            )
            
            tool_calls = None
            full_response = ""
            
            for chunk in response:
                delta = chunk.choices[0].delta
                if delta and delta.tool_calls:
                    if not tool_calls:
                        tool_calls = delta.tool_calls
                    else:
                        tool_calls[0].function.name += delta.tool_calls[0].function.name if delta.tool_calls[0].function.name else ""
                        tool_calls[0].function.arguments += delta.tool_calls[0].function.arguments if delta.tool_calls[0].function.arguments else ""
                
                if delta and delta.content:
                    full_response += delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            if tool_calls:
                tool_call = tool_calls[0]
                function_name = tool_call.function.name
                
                with st.expander(f"Agent's Thought Process: Calling `{function_name}`..."):
                    st.write("Arguments:", tool_call.function.arguments)
                
                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    
                    try:
                        tool_output = function_to_call(**function_args)
                        st.write(f"Tool output received.")
                        
                        messages.append({"role": "assistant", "content": full_response, "tool_calls": tool_calls})
                        messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": function_name, "content": tool_output})
                        
                        final_response_stream = client.chat.completions.create(
                            model="gpt-4o",
                            messages=messages,
                            stream=True,
                        )
                        final_full_response = ""
                        final_message_placeholder = st.empty()
                        
                        for chunk in final_response_stream:
                            delta = chunk.choices[0].delta
                            if delta and delta.content:
                                final_full_response += delta.content
                                final_message_placeholder.markdown(final_full_response + "▌")
                        final_message_placeholder.markdown(final_full_response)
                        
                        plot_path = None
                        if function_name == "plot_data_tool" and "successfully saved at: " in tool_output:
                            plot_path = tool_output.split("successfully saved at: ")[1].strip()
                        
                        if plot_path and os.path.exists(plot_path):
                            st.image(plot_path, caption=f"Visualization: {os.path.basename(plot_path)}")
                            st.session_state.messages.append({"role": "assistant", "content": final_full_response, "plot_path": plot_path})
                        else:
                            st.session_state.messages.append({"role": "assistant", "content": final_full_response})
                            
                    except Exception as e:
                        st.error(f"Error executing tool '{function_name}': {e}")
                else:
                    st.error(f"Error: Tool '{function_name}' is not recognized by the app.")
            else:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            status.update(label="Agent has finished its task!", state="complete")
    
    save_chat_history()