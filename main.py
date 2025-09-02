import pandas as pd
import os
import json

# 📖 Load config
with open("config.json") as f:
    config = json.load(f)

input_folder = config["input_folder"]
output_suffix = config["output_suffix"]
tag_column = config["tag_column"]
text_columns = config["text_columns"]

# 🏷️ Define keyword categories
categories = config["categories"]


# 🧹 Remove tags containing "chatgpt"
def clean_tags(tag_str):
    if pd.isna(tag_str):
        return ""
    tags = [tag.strip() for tag in tag_str.split(",")]
    filtered = [tag for tag in tags if "chtgptapp" not in tag.lower()]
    return ", ".join(filtered)


# 🧠 Generate category tags from configured columns
def classify_tags(row):
    text = " ".join(str(row[col]) for col in text_columns).lower()
    matched = [
        category
        for category, keywords in categories.items()
        if any(keyword in text for keyword in keywords)
    ]
    return ", ".join(matched) if matched else "Unclear"


# 🔗 Append new tags without duplication
def append_tags(existing, new):
    existing_tags = set(tag.strip() for tag in str(existing).split(",") if tag.strip())
    new_tags = set(tag.strip() for tag in str(new).split(",") if tag.strip())
    combined = existing_tags.union(new_tags)
    return ", ".join(sorted(combined))


# 🚀 Process all CSVs in input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        input_path = os.path.join(input_folder, filename)
        df = pd.read_csv(input_path)

        # Clean and enrich tags
        df[tag_column] = df[tag_column].apply(clean_tags)
        df[tag_column] = df.apply(
            lambda row: append_tags(row[tag_column], classify_tags(row)), axis=1
        )

        # Save processed file
        output_filename = filename.replace(".csv", output_suffix)
        output_path = os.path.join(input_folder, output_filename)
        df.to_csv(output_path, index=False)
        print(f"✅ Processed: {filename} → {output_filename}")
