import pandas as pd
import os

# 📂 Load CSV from 'exports' subfolder
input_filename = "products_export_3.csv"
input_path = os.path.join("exports", input_filename)
df = pd.read_csv(input_path)


# 🧹 Remove tags containing "chatgpt"
def clean_tags(tag_str):
    if pd.isna(tag_str):
        return ""
    tags = [tag.strip() for tag in tag_str.split(",")]
    filtered = [tag for tag in tags if "chtgptapp" not in tag.lower()]
    return ", ".join(filtered)


df["Tags"] = df["Tags"].apply(clean_tags)

# 🏷️ Define keyword categories
categories = {
    "Exterior": [
        "bumper",
        "spoiler",
        "grille",
        "mirror",
        "light",
        "headlamp",
        "lamp",
        "windshield",
        "moulding",
        "door",
        "door strut",
        "door assembly",
        "carbon fibre",
        "carbon fiber",
        "cf",
        "camera bezel",
        "centre cap",
        "undertray",
        "under tray",
        "center cap",
        "side repeater",
        "chassis",
        "wheel",
        "tyre",
        "Lotus Winglet-splitter",
        "indicator light",
        "turn signal",
        "tailgate",
        "tail gate",
        "side indicator",
        "duct",
        "plate",
        "side panel",
        "intake",
        "mirror light",
    ],
    "Interior": [
        "seat",
        "trim",
        "infotainment",
        "console",
        "upholstery",
        "car play",
        "instrument",
        "insert",
        "carplay",
        "silent channel",
        "android auto kit",
        "switch pack",
    ],
    "Performance": ["exhaust", "engine", "transmission"],
    "Mechanical": [
        "oil filter",
        "brake",
        "brake-pad",
        "brake pad",
        "suspension",
        "Lotus Rear spring/damper",
        "radiator",
        "bearing",
        "bolt",
        "assy",
        "pump",
        "damper",
        "cv joint",
        "vacuum",
        "fuel distributor",
        "fuel",
        "camshaft",
        "clutch",
        "shock absorber",
        "caliper",
        "drive shaft",
        "catalyst",
        "filter",
        "heater",
        "cylinder head",
        "wishbone",
        "wishbone-trailing",
        "brkt",
    ],
    "Electrical": [
        "battery",
        "ecu",
        "sensor",
        "wiring loom",
        "electrical harness",
        "wiring",
        "silencer",
        "wiring harness",
        "relay",
        "fuse",
        "control unit",
        "control",
        "cruise control",
        "alarm",
        "tcu",
        "bcm",
        "module",
        "electronic control",
        "controller",
    ],
    "Accessories": ["branded", "cover", "mat", "key fob", "badge", "sateen", "leather"],
}


# 🧠 Generate category tags from Title, Vendor, Product Category
def classify_tags(row):
    text = " ".join(
        str(row[col]) for col in ["Title", "Vendor", "Product Category"]
    ).lower()
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


# 🏷️ Apply tag enrichment
df["Tags"] = df.apply(lambda row: append_tags(row["Tags"], classify_tags(row)), axis=1)

# 💾 Save processed CSV
output_filename = input_filename.replace(".csv", "-processed.csv")
output_path = os.path.join("exports", output_filename)
df.to_csv(output_path, index=False)

print(f"✅ Processed file saved as: {output_filename}")
