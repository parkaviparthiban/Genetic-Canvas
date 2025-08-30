import os

def check_file(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        exit()
