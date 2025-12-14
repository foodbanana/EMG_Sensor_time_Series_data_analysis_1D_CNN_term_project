import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

def select_file():
    """loading"""
    root = tk.Tk()
    root.withdraw()
    
    initial_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="loading data",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_path

print("loading data")
file_path = select_file()

if not file_path:
    print("no data selected")
    exit()

print(f"selected file: {file_path}")

try:
    df = pd.read_csv(file_path)
    print("data loaded")
except Exception as e:
    print(f"error: {e}")
    exit()

fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle(f'sEMG Data Graph ({os.path.basename(file_path)})', fontsize=16)
channels = [
    ('Ch1', 'Channel 0', axs[0, 0], 'orange'),
    ('Ch2', 'Channel 1', axs[0, 1], 'green'),
    ('Ch3', 'Channel 2', axs[1, 0], 'blue'),
    ('Ch4', 'Channel 3', axs[1, 1], 'purple')
]

for col_name, title, ax, color in channels:
    if col_name in df.columns:
        ax.plot(df.index, df[col_name], color=color, linewidth=0.8, alpha=0.8)
        
        ax.set_ylim(0, 1024)
        
        ax.set_title(title, fontsize=12)
        ax.set_ylabel('EMG Value')
        ax.set_xlabel('time')
        ax.grid(True, linestyle='--', alpha=0.6)
        
        target_label = 'Borg' if 'Borg' in df.columns else 'label'
        
        if target_label in df.columns:
            changes = df.index[df[target_label].diff() != 0].tolist()
            for change in changes:
                if change > 0:
                    ax.axvline(x=change, color='black', linestyle=':', alpha=0.5)
                    val = df[target_label].iloc[change]
                    ax.text(change, 1000, f'Borg:{val}', rotation=90, verticalalignment='top', fontsize=8)

    else:
        ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center')
        ax.set_title(title)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()