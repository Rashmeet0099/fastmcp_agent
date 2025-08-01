import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from fastmcp import FastMCP

# Import all tool functions as plain functions
from tools.file_tools import read_csv_tool, list_directory_tool
from tools.plotting_tools import plot_data_tool
from tools.openai_tools import summarize_text

# Create a FastMCP instance.
mcp = FastMCP("Data Analyst and Text Agent",
              instructions="You are a powerful agent with access to local files, plotting, and an external LLM for text analysis. Use your tools to answer user questions and visualize data.")

# Apply the decorators to the imported functions
@mcp.tool()
def read_csv(filepath: str) -> str:
    """Reads a local CSV file and returns its contents as a JSON string.
    The filepath should be a relative path from the project root (e.g., 'data/sales_data.csv').
    """
    return read_csv_tool(filepath)

@mcp.tool()
def list_directory(path: str) -> str:
    """Lists all files and directories in a given path."""
    return list_directory_tool(path)

@mcp.tool()
def plot_data(data: str, plot_type: str, x_axis: str, y_axis: str) -> str:
    """Generates a plot from structured data and saves it as an image.
    data: A JSON string of records, as returned by read_csv_tool.
    plot_type: The type of plot, e.g., 'bar', 'line', 'scatter'.
    x_axis: The column name for the x-axis.
    y_axis: The column name for the y-axis.
    Returns the path to the saved plot image.
    """
    return plot_data_tool(data, plot_type, x_axis, y_axis)

@mcp.tool()
def summarize_text_tool(text: str) -> str:
    """Summarizes a given text using a powerful LLM."""
    return summarize_text(text)

if __name__ == "__main__":
    mcp.run()