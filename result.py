import json






def set_result(data):

    for key in data.keys():
        max_score = max(data[key].items(), key=lambda x: x[1]["score"])[1]
        max_score_name = max_score['name']
        max_score_value = max_score['score']
        name_count = sum(1 for img_data in data[key].values() if img_data["name"] == max_score_name)
        sum_max_score = sum(img_data["score"] for img_data in data[key] if img_data["name"] == max_score_name)
        sum_scores = sum(img_data["score"] for img_data in data[key])
        len_data = len(data[key].values())

        if max_score_value > 60 and name_count/len_data > 0.7:
            result = {
                key: {
                    "name": max_score_name,
                    "score": max_score_value
                }
            }
        elif max_score_value > 50 and sum_max_score/len_data > 0.8:
            result = {
                key: {
                    "name": max_score_name,
                    "score": max_score_value
                }
            }
        else:
            result = {
                key: {
                    "name": 'unknown',
                    "score": max_score_value
                }
            }
        return result


with open("db.json", "r") as file:
    data = json.load(file)

    results = set_result(data)
    print(results)


