import json
import requests

ID = "" #Вставить id пользователя
token = "" #Вставить токен


def make_request(method_name, params):
    server_addr = f"https://api.vk.com/method/{method_name}?v=5.131&access_token={token}"
    if params:
        for param in params:
            server_addr += f"&{param}={params[param]}"
    return json.loads(requests.get(server_addr).text)["response"]


def get_user_info():
    global ID
    res = make_request("users.get", {"user_id": ID})[0]
    res_name = res["first_name"] + " " + res["last_name"]
    ID = res["id"]
    return res_name


def get_friends_ids():
    result = make_request("friends.get", {"user_id": ID})["items"]
    count = make_request("friends.get", {"user_id": ID})["count"]
    return result, count


def get_users_data(users_ids):
    return make_request("users.get", {"user_ids": json.dumps(users_ids)})


def get_photo_info():
    result = make_request("photos.getAlbums", {"owner_id": ID})["items"]
    return result


if __name__ == '__main__':
    user_name = get_user_info()
    id_list, friends_count = get_friends_ids()
    friends_data = get_users_data(id_list)
    friends = []
    print("Информация о пользователе " + user_name)
    print(f"Количество друзей пользователя: {friends_count}\n")
    for friend in friends_data:
        friends.append(friend["first_name"] + " " + friend["last_name"])
    for line in friends:
        print(line)
    photos = get_photo_info()
    print("\nФотоальбомы пользователя:")
    for album in photos:
        print(f'\"{album["title"]}\"')

