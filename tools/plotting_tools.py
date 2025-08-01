import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

def plot_data_tool(data: str, plot_type: str, x_axis: str, y_axis: str) -> str:
    # ... (rest of your function code remains the same)
    try:
        df = pd.read_json(data)
        
        plt.figure(figsize=(10, 6))
        
        if plot_type == 'bar':
            sns.barplot(x=x_axis, y=y_axis, data=df)
        elif plot_type == 'line':
            sns.lineplot(x=x_axis, y=y_axis, data=df)
        # ... (rest of the function)
        plot_path = f"plots/{plot_type}_{x_axis}_{y_axis}.png"
        plt.title(f"{plot_type.capitalize()} Plot of {y_axis} vs {x_axis}")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        
        return f"Plot successfully saved at: {plot_path}"
    except Exception as e:
        return f"Error generating plot: {e}"