import pandas as pd

def load_labels(csv_path):
    """
    Loads labels from a CSV file with columns: id,label
    """
    try:
        df = pd.read_csv(csv_path)
        label_map = dict(zip(df['id'], df['label']))
        print(f"✅ Loaded {len(label_map)} labels from {csv_path}")
        return label_map
    except Exception as e:
        print(f"❌ Failed to load labels: {e}")
        return {}
