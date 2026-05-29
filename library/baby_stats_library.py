import json
import re
from pathlib import Path
from stat import Stat

"""
This module reads all .text files (yob1990.txt) from the specified folder,
extracts the year of birth from the filename, and converts the content of each file 
into a JSON format. 
"""
def convert_txt_to_json(folder_path, json_file):
    all_data = []

    path = Path(__file__).resolve().parent.parent / folder_path
    # Find all .txt files
    for file_path in Path(path).rglob("*.txt"):
        # Extract year from filename
        # Example filename: yob1990.txt
        match = re.search(r'(\d{4})', file_path.name)

        if not match:
            continue
        year = int(match.group(1))

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    # Each row format: name,sex,rank
                    parts = line.split(",")

                    if len(parts) != 3:
                        continue

                    name, gender, rank = parts
                    data = {
                        "yob": year,
                        "name": name.strip(),
                        "gender": gender.strip(),
                        "ranking": int(rank.strip())
                    }

                    all_data.append(data)

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Convert to JSON
    json_data = json.dumps(all_data, indent=4)

    # Optional: save to file
    with open(json_file, "w", encoding="utf-8") as out:
        out.write(json_data)

"""This module contains functions to read JSON and convert to list of baby stats objects."""
def convert_json_to_babies_stats(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    stats = []
    for item in data:
        stat = Stat(
            name=item["name"],
            gender=item["gender"],
            yob=item["yob"],
            ranking=item["ranking"]
        )
        stats.append(stat)
    return stats


"""This module contains functions to group objects babies' stats by yob"""
def group_babies_by_yob(stats):
    grouped = {}
    for baby in stats:
        if baby.yob not in grouped:
            grouped[baby.yob] = []
        grouped[baby.yob].append(baby)
    return grouped

"""This module contains functions to group objects babies' stats by gender"""
def group_babies_by_gender(stats):
    grouped = {}
    for baby in stats:
        if baby.gender not in grouped:
            grouped[baby.gender] = []
        grouped[baby.gender].append(baby)
    return grouped

"""This module contains functions to group objects babies' stats by name"""
def group_babies_by_name(stats):
    grouped = {}
    for baby in stats:
        if baby.name not in grouped:
            grouped[baby.name] = []
        grouped[baby.name].append(baby)
    return grouped

"""This module contains functions to group objects babies' stats by name and gender"""
def group_babies_by_name_and_gender(stats):
    grouped = {}
    for baby in stats:
        if (baby.name, baby.gender) not in grouped:
            grouped[(baby.name, baby.gender)] = []
        grouped[(baby.name, baby.gender)].append(baby)
    return grouped


"""This module contains functions to search baby's name and gender"""
def search_baby_name_gender(stats, name, gender):
    return [baby for baby in stats if baby.name.lower() == name.lower() and baby.gender.lower() == gender.lower()]
    

"""This module contains functions to search baby's name"""
def search_baby_name(stats, name):
    return [baby for baby in stats if baby.name.lower() == name.lower()]
    
"""This module contains functions to search baby's between yob range"""
def search_baby_between_yob(stats, start_yob, end_yob):
    return [baby for baby in stats if start_yob <= baby.yob <= end_yob]

"""This module contains functions to search baby's name between yob range"""
def search_baby_between_yob_and_name(stats, start_yob, end_yob, name):
    return [baby for baby in stats if start_yob <= baby.yob <= end_yob and baby.name.lower() == name.lower()]
   