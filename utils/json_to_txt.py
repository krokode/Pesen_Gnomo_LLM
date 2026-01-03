import os
from pathlib import Path
import json

def convert_json_txt(source_json, target_txt):
    # Read the JSON file
    with open(source_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract and clean the output texts
    cleaned_texts = []
    for item in data:
        text = item.get('output', '')
        # Remove the suffix if it exists
        text = text.replace('(Text is written in gnomomamochka\'s style)', '').strip()
        cleaned_texts.append(text)

    # Save to a text file
    with open(target_txt, 'w', encoding='utf-8') as f:
        for i in range(len(cleaned_texts)):
            text = cleaned_texts[i]
            f.write(text)
            f.write('\n\n')

    print(f"Saved {len(cleaned_texts)} cleaned texts to {target_txt}")

if __name__=="__main__":
    name = ["jj_gnomomamochka", "jj_gnomo_otrageniya", "jj_pesen"]
    target_dir = ["txt_gnomo", "txt_pesen"]

    source_json_name = Path("..", "data", "json_pesen_gnomo", f"{name[2]}.json")
    target_txt_name = Path("..", "data", target_dir[1], f"{name[2]}.txt")

    convert_json_txt(source_json=source_json_name, target_txt=target_txt_name)