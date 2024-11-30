import json
import random


def new_user(user_id):
    user_id = str(user_id)

    with open('db/db.json', 'r') as file:
        data = json.load(file)

    data[user_id] = [str(i) for i in range(1, 15)]

    with open('db/db.json', 'w') as file:
        print(data)
        json.dump(data, file, indent=' ')


def get_next_question(user_id):
    with open('db/db.json', 'r') as file:
        data = json.load(file)
    if data[str(user_id)]:
        next = random.choice(data[str(user_id)])
        data[str(user_id)].remove(next)
        with open('db/db.json', 'w') as file:
            print(data)
            json.dump(data, file, indent=' ')
    else:
        next = 'None'
    return next


def get_next_in_row(user_id):
    with open('db/db.json', 'r') as file:
        data = json.load(file)
    if data[str(user_id)]:
        next = data[str(user_id)][0]
        data[str(user_id)].remove(next)
        with open('db/db.json', 'w') as file:
            print(data)
            json.dump(data, file, indent=' ')
    else:
        next = 'None'
    return next

