import os
import re
import csv

# Change this to your directory with .cat files
cat_directory = "cat_files"
output_csv = "unique_words.csv"

# Header row includes number of lines now
rows = [("filename", "lines", "total_words", "unique_words", "unique_headwords")]

for filename in os.listdir(cat_directory):
    if filename.endswith(".cat") or filename.endswith(".txt"):
        file_path = os.path.join(cat_directory, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            data = ''.join(lines)

        # Extract and clean surface words
        words = re.findall(r'\s([A-Za-z\'\-]+)\{\*', data)
        words = [re.sub(r'[^\w\-]', '', word) for word in words]

        # Extract headwords (lemmas)
        headwords = re.findall(r'\{\*([a-z]+)@', data, re.IGNORECASE)

        # Count stats
        num_lines = len(lines)
        total_words = len(words)
        unique_words = len(set(words))
        unique_headwords = len(set(headwords))

        # Append result
        rows.append((filename, num_lines, total_words, unique_words, unique_headwords))

# Write to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Saved stats to {output_csv}")

