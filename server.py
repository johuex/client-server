import time
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)  # создаем сервер
# список, где хранятся сообщения (в виде словарика)
messages = [
    {'username': 'Messenger', 'text': 'Please, login to send messages!', 'time': time.time()}
]
# словарик для авторизации
users = {
    # username: password
    'jack': 'qwerty1',
    'mary': '1111'

}


@app.route("/")  # локаторы сайта (то есть по пути в строке сайта вызываем функцию)
def hello():
    """
    просто привет
    """
    return "Server is working!"


@app.route("/status")  # локаторы сайта (то есть по пути сайт/status вызываем функцию stasus)
def status():
    """
        просто статус
    """
    return {
        'status': True,
        'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'messages_count': len(messages),
        'users_count': len(users)
    }


@app.route("/send", methods=['POST'])
def send():
    """
    метод отправки сообщения от клиента на сервер
    request: {"username": "str", "password": "str", "text": "str", "time": "float"}
    response: {"ok": true}
    """
    data = request.json  # JSON -> dist
    username = data["username"]
    password = data['password']
    text = data["text"]

    # если такой пользователь не сущесвует, то автоматически регистрируется в системе
    # иначе проверяем пароль
    if username in users:
        real_password = users[username]
        if real_password != password:
            return {"ok", False}
    else:
        users[username] = password

    new_message = {'username': username, 'text': text, 'time': time.time()}
    messages.append(new_message)

    return {"ok": True}


@app.route("/history")
def history():
    """
    отображение всех сообщений чата
    request: ?after=float
    response: {"messages": []}
    """
    after = float(request.args['after'])
    # фильтр, который выводит только свежие сообщения
    filtered_messages = [message for message in messages if after < message['time']]

    return {'messages': filtered_messages}


app.run()
