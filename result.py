import json






def set_result(data):



    names = []
    scores = []

    for key, value in data['ID-2'].items():

        names.append(value["name"])
        scores.append(value["score"])
    return names, scores


with open("db.json", "r") as file:
    data = json.load(file)



max_score_name = max(data["ID-2"].items(), key=lambda x: x[1]["score"])[1]["name"]

name_count = (sum(1 for img_data in data["ID-2"].values() if img_data["name"] == max_score_name)/len(data["ID-2"].values()))*100


print("Имя участника с наибольшей суммой баллов:", max_score_name)
print(name_count)

# names, scores = set_result(data)

# print(names, scores)
#
# name = max(names, key=names.count)
# print(name)
