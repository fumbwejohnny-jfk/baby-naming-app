from library.baby_library import convert_csv_to_json, convert_json_to_babies, search_baby_meaning
from library.baby_stats_library import convert_json_to_babies_stats, convert_txt_to_json, search_baby_name

# Main Program
if __name__ == "__main__":
   
    output_path = "names/output.csv"
    json_file = "names/output.json"
    baby_json_file = "names/babies.json"
    stat_json_file = "names/stats.json"

    convert_csv_to_json(output_path, baby_json_file) # Convert CSV to JSON for baby names
    convert_txt_to_json('names', stat_json_file) # Convert .txt to JSON for baby name stats
   
  