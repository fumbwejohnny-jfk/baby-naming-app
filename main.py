from library.baby_library import convert_csv_to_json, convert_json_to_babies, search_baby_meaning
from library.baby_stats_library import convert_json_to_babies_stats, search_baby_name

# Main Program
if __name__ == "__main__":
    input_path = "names/names.csv"
    output_path = "names/output.csv"
    json_file = "names/output.json"
    baby_json_file = "names/babies.json"
    stat_json_file = "names/stats.json"
    file_paths = ["../names/"]  # List of file paths to upload

    convert_csv_to_json(output_path, baby_json_file)
    # convert_txt_to_json('names', stat_json_file)
    babies = convert_json_to_babies(baby_json_file)
    stats = convert_json_to_babies_stats(stat_json_file)
    name_to_search = "sandra"
    print(f"Meaning of baby name '{name_to_search}':", search_baby_meaning(babies,  name_to_search))

    print(f'---------------------------------------------------------------------------------', end='\n\n')
    list_of_babies = search_baby_name(stats, name_to_search)
    for baby in list_of_babies:
        print(f"Name: {baby.name}, Gender: {baby.gender}, YOB: {baby.yob}, Ranking: {baby.ranking}")
   
