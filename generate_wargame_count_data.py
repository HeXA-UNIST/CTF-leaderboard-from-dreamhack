import requests
import json
from multiprocessing import Pool
import re


def get_score_by_user_index(user_index:int) -> list[int]:
    """
    input: user index
    output: wargame count that the user solved.
        the wargame count is returned separately by difficulty level.
        that's why the wargame count is returned as a list.
        index 0 of wargame count list is the number of lv1 wargame that the user solved.
        index 1 of wargame count list is the number of lv2 wargame that the user solved.
        and so on.
    """
    url = "https://dreamhack.io/users/{user_index}/wargame"
    pattern = r"<span class=\"current\" style=\"color:#.{6};\" data-v-0eacbf8a>([0-9]+)</span>"
    result = requests.get(url.format(user_index=user_index))
    match = re.findall(pattern=pattern, string=result.text)

    result_data = [0]*10
    for i in range(10):
        result_data[i] = int(match[i])
    print(user_index, ":", result_data)
    return result_data

def get_score_list_by_user_index_list(user_index_list:list[int]) -> list[list[int]]:
    """
    input: list of user index
    output: list of wargame count list that each user solved.
    """
    user_count = len(user_index_list)
    with Pool(user_count) as p:
        score_list = p.map(get_score_by_user_index, user_index_list)
    
    return score_list


def run(file_prefix = "initial"):
    file = open("user_index.json", "r")
    data = json.load(file)
    file.close()
    user_index_list = list(data.values())
    print(user_index_list)
    score_list = get_score_list_by_user_index_list(user_index_list=user_index_list)
    
    username_list = list(data.keys())
    user_count = len(username_list)
    result_data = {}
    for i in range(user_count):
        result_data[username_list[i]] = score_list[i]

    score_list_file = open(f"{file_prefix}_wargame_count_data.json", "w")
    score_list_file.write(json.dumps(result_data, indent=2, ensure_ascii=False))
    score_list_file.close()

if __name__ == "__main__":
    run()