import re
import json
import csv
from library.baby import Baby


"""This module contains functions to modify CSV files and convert them to JSON format."""
def convert_csv_to_json(output_path, json_file):
     # Convert CSV to JSON
    data= []
    if not output_path:
        raise FileNotFoundError
    # 1. Read the CSV file and convert it to a list of dictionaries
    with open(output_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
             data.append({"name": row["name"], "meaning": row["meaning"].replace(";", ",")})
        
    if not data:
        raise Exception("Error", "formatting JSON format")
    # 2. Write the list of dictionaries to a JSON file
    with open(json_file, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


"""This module contains functions to modify CSV files and convert them to JSON format."""
def modify_csv(input_path, output_path):
    # read all lines from input file
    with open(input_path, 'r') as file:
        lines = file.readlines()
    
    # write modified lines to output file
    with open(output_path, 'w') as file:
        for line in lines:
            parts = line.split(',', 2)  # Splits into 3 parts: [before1st, before2nd, rest]
            if len(parts) > 2:
                # Re-joins first two with comma, then adds semicolon before the rest
                new_line = f"{parts[0]},{parts[1]};{parts[2]}"
                file.write(new_line)
            else:
                file.write(line)


"""This module contains functions to read JSON and convert to list of baby objects."""
def convert_json_to_babies(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    babies = []
    for item in data:
        baby = Baby(
            name=item["name"],
            meaning=item["meaning"]
        )
        babies.append(baby)
    return babies


"""This module contains functions to search baby's meaning by name
   Scenario 1: if meaning start with "From", go to the end of the meaning and add "From" to the end of the meaning. If the "From" is followed by "and", there two to search for meaning
   Scenario 2: if meaning start with "Form of" followed by a name, search for the meaning of that name and add "Form of" to the end of the meaning 
"""
def search_baby_meaning(babies, name):
    for baby in babies:
        if baby.name.lower() == name.lower():
            meaning_with_form_of(babies, baby)
            meaning_with_2_names(babies, baby, name)
            return baby.meaning
    return None


"""
 Example: "Form of John" -> search for "John" and add "Form of" to the end of the meaning
"""
def meaning_with_form_of(babies, baby):
    if  re.search(r"\bform of\b", baby.meaning.lower()):
        text = baby.meaning.lower().split("of")[-1].split(' ')[-1]
        baby.meaning = search_baby_meaning(babies, text)


"""
Example: "From John" -> search for "John" and add "From" to the end of the meaning
"From John and Jane" -> search for "John" and "Jane" and add "From" to the end of the meaning
"""
def meaning_with_2_names(babies, baby, name):
    if baby.meaning.lower().startswith("from"):
        if re.search(r"\band\b", baby.meaning.lower()):
            parts = baby.meaning.lower().split("and")
            meanings = []
            for part in parts:
                meaning = search_baby_meaning(babies, part.strip().split(' ')[-1])
                if meaning:
                    meanings.append(meaning)
            baby.meaning = "From " + " and ".join(meanings)
        else: 
            if name == baby.meaning.lower().split("from")[-1].strip().split(' ')[-1]:
                return baby.meaning   
            baby.meaning = search_baby_meaning(babies, baby.meaning.split(' ')[-1])




  


 
   
