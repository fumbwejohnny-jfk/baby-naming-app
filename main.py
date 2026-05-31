from library.baby_library import convert_csv_to_json, convert_json_to_babies, search_baby_meaning
from library.baby_stats_library import convert_json_to_babies_stats, convert_txt_to_json, search_baby_name

# Main Program
if __name__ == "__main__":
    input_path = "names/names.csv"
    output_path = "names/output.csv"
    json_file = "names/output.json"
    baby_json_file = "names/babies.json"
    stat_json_file = "names/stats.json"
    file_paths = ["../names/"]  # List of file paths to upload

    convert_csv_to_json(output_path, baby_json_file)
    convert_txt_to_json('names', stat_json_file)
    # babies = convert_json_to_babies(baby_json_file)
    # stats = convert_json_to_babies_stats(stat_json_file)
    # name_to_search = "sandra"
  