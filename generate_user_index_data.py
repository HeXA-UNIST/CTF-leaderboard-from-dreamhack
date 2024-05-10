import requests
import json
from multiprocessing import Pool

def get_user_index(username:str):
    """
    input: username
    output: id(index) of the user, which is required later to send request to user page
    """
    url = "https://dreamhack.io/api/v1/services/suggestion/"
    params = {"keyword": username, "section": ""}
    result = requests.get(url, params=params)
    data = json.loads(result.text)
    print(username)

    for item in data["users"]["results"]:
        if item["nickname"] == username:
            return item["id"]

def run():
    file = open("username_list.txt", "r")
    result_data = {}

    lines = file.readlines()
    user_count = len(lines)
    usernames = list(map(lambda line: line.split("\n")[0], lines))
    with Pool(user_count) as p:
        user_indexes = p.map(get_user_index, usernames)

    for i in range(user_count):
        result_data[usernames[i]] = user_indexes[i]
        
    file.close()

    user_index_file = open("user_index.json", "w")
    user_index_file.write(json.dumps(result_data, indent=2, ensure_ascii=False))
    user_index_file.close()

if __name__=="__main__":
    run()