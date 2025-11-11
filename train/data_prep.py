# train/data_prep.py
# simple script to create sample files
import os
os.makedirs("../sample_data", exist_ok=True)
orig = "The quick brown fox jumps over the lazy dog. Machine learning is fun. Python is great."
sub = "The quick brown fox jumps over the lazy dog. I like pizza and Python is great."
with open("../sample_data/original.txt","w",encoding="utf-8") as f:
    f.write(orig)
with open("../sample_data/submission.txt","w",encoding="utf-8") as f:
    f.write(sub)
print("sample_data created in ../sample_data")
