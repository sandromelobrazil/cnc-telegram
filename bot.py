import os
import requests
import json
from authorization import TOKEN

URL = "https://api.telegram.org/bot{}".format(TOKEN)
output = "<b>Directory Listing</b>\n<i>Dir: {}</i>\n<b>Items:</b>\n\n"
MAX_MESSAGE_LENGTH = 4000


def get_status():
    answer = requests.get(URL + "/getme")
    if answer.status_code == 200:
        print("Connection works")
    else:
        print("Connection does not work")


def get_json(url):
    request = requests.get(url)
    print(request.content.decode("utf8"))
    if request.status_code == 200:
        return json.loads(request.content)
    return None


def mark_read(offset):
    answer = get_json(URL + "/getUpdates?offset={}".format(offset))


def get_updates():
    answer = get_json(URL + "/getUpdates")
    if (answer is None) or (not answer["ok"]):
        print("Wrong request for Updates")
        return

    print(answer)

    for result in answer["result"]:
        yield result


def list_files(path):
    return os.listdir(path)


def get_active_users():
    stream = os.popen('w')
    stream.readline()
    stream.readline() # get rid of a header and stats

    users = []
    for line in stream.readlines():
        splitted = line.split()
        users.append(splitted[0])
    return users


def get_running_processes():
    stream = os.popen('ps -aux')
    stream.readline()  # get rid of a header and stats

    processes = []
    for line in stream.readlines():
        splitted = line.split()
        processes.append(splitted[-1])
    return processes


def write_to_file(file, data):
    stream = os.popen('echo {} > {}'.format(data, file))


def parse_payload(command):
    if command == "ls":
        files = list_files("./")
        out = output
        for file in files:
            out = out + file + "\n"
        print(files)
        return out
    return None


def send_answer(message, chat_id):
    start = 0
    end = min(message.len(), MAX_MESSAGE_LENGTH)
    while True:
        answer = get_json(URL + "/sendMessage?text={}&chat_id={}&parse_mode={}".format(message[start, end], chat_id, "html"))
        if (answer is None) or (not answer["ok"]):
            print("Wrong answer")
            return

        if message.len() - end < MAX_MESSAGE_LENGTH:
            break
        start = end
        end = min(message.len(), start + MAX_MESSAGE_LENGTH)


if __name__ == "__main__":
    # test of new methods
    print(get_active_users())
    print(get_running_processes())
    write_to_file("out.txt", "TEST")


    # update_id = 0
    #
    # for update in get_updates():
    #     update_id = update["update_id"] + 1
    #     message = update["message"]
    #     chat_id = message["chat"]["id"]
    #     print(update)
    #
    #     response = parse_payload(message["text"])
    #     if response is None:
    #         continue
    #
    #     print(response)
    #     send_answer(response, chat_id)

    # mark_read(update_id)
