import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(input_file, output_file):
    # Read data from the file
    df = pd.read_csv(input_file, sep="\t")

    # Plotting the data
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plotting npeaks vs qscore
    ax1.plot(df["qscore"], df["npeaks"], marker='o', color='b')
    ax1.set_title("npeaks vs qscore")
    ax1.set_xlabel("qscore")
    ax1.set_ylabel("npeaks")

    # Plotting avelpeak vs qscore
    ax2.plot(df["qscore"], df["avelpeak"], marker='o', color='r')
    ax2.set_title("avelpeak vs qscore")
    ax2.set_xlabel("qscore")
    ax2.set_ylabel("avelpeak")

    plt.tight_layout()

    # Save the plot as a PDF
    plt.savefig(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file.txt output_file.pdf")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        plot_data(input_file, output_file)

