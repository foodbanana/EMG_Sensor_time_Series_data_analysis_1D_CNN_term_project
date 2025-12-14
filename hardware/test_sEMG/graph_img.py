import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import glob

def process_file(file_path):
    """Process a single CSV file and generate graphs"""
    print(f"\nProcessing: {os.path.basename(file_path)}")
    
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully")
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # 그래프 저장 폴더 생성
    save_dir = os.path.join(os.path.dirname(file_path), "graphs")
    os.makedirs(save_dir, exist_ok=True)
    print(f"Save directory: {save_dir}")

    # 그래프 1개 생성
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
                        ax.text(change, 1000, f'Borg:{val}', rotation=90,
                                verticalalignment='top', fontsize=8)

        else:
            ax.text(0.5, 0.5, 'No Data', horizontalalignment='center',
                    verticalalignment='center')
            ax.set_title(title)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # 파일 저장 (CSV 파일명 기반)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    save_path = os.path.join(save_dir, f"{base_name}.png")
    plt.savefig(save_path, dpi=200)
    plt.close()

    print(f"Saved: {save_path}")


# Main execution
if __name__ == "__main__":
    # Check if a file path is provided as command-line argument
    if len(sys.argv) > 1:
        # Process the specified file
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        process_file(file_path)
    else:
        # Process all CSV files in the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        csv_files = glob.glob(os.path.join(current_dir, "sEMG_data_*.csv"))
        
        if not csv_files:
            print("No CSV files found matching pattern 'sEMG_data_*.csv'")
            print("Usage: python graph_img.py [file_path]")
            sys.exit(1)
        
        print(f"Found {len(csv_files)} CSV file(s). Processing all...")
        for csv_file in sorted(csv_files):
            process_file(csv_file)
        
        print("\n" + "="*50)
        print("All files processed successfully!")
