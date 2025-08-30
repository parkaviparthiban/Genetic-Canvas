import os
import matplotlib.pyplot as plt

def gc_content(seq):
    gc = seq.count('G') + seq.count('C')
    return gc / len(seq) * 100 if len(seq) > 0 else 0

def ensure_output_dir():
    if not os.path.exists("output"):
        os.makedirs("output")

def plot_gc_distribution(sequences, show_plot=False):
    if not sequences:
        print("⚠️ No sequences provided for GC distribution.")
        return
    ensure_output_dir()
    gc_values = [gc_content(str(record.seq)) for record in sequences]
    plt.figure()
    plt.hist(gc_values, bins=30, color='skyblue', edgecolor='black')
    plt.title("GC Content Distribution")
    plt.xlabel("GC%")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("output/gc_distribution.png")
    print("📊 GC plot saved to output/gc_distribution.png")
    if show_plot:
        plt.show()

def plot_length_distribution(sequences, show_plot=False):
    if not sequences:
        print("⚠️ No sequences provided for length distribution.")
        return
    ensure_output_dir()
    lengths = [len(record.seq) for record in sequences]
    plt.figure()
    plt.hist(lengths, bins=30, color='salmon', edgecolor='black')
    plt.title("Sequence Length Distribution")
    plt.xlabel("Length")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("output/length_distribution.png")
    print("📊 Length plot saved to output/length_distribution.png")
    if show_plot:
        plt.show()