from datetime import datetime

import flet as ft
import requests

from frontend.common.message_description import message_description_formate as md_formate


def get_message(page, message_key):
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    message = requests.get(f'http://localhost:5465/message/get/?hash_id={message_key}').json()
    message_hash = requests.post(f'http://localhost:5465/message_hash/get/', data={
        'hash_id': message_key
    }).json()

    lv.controls.append(ft.Row([ft.Text('AI Short Description:'), ft.Text(md_formate(message['message_description']))]))
    lv.controls.append(ft.Text(message['message']))
    lv.controls.append(ft.Row([ft.Text('Time Post:'), ft.Text(str(datetime.fromtimestamp(int(message['datetime']))))]))
    lv.controls.append(ft.Row([ft.Text('Sign Hash:'), ft.TextField(read_only=True, value=message_hash['message_hash_hash'])]))

    page.add(lv)
