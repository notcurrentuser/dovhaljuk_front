import requests
import flet as ft

from frontend.common.message_description import message_description_formate
from frontend.settings import SERVER_URL


def messages(page, redirect, edit_page):
    def get_message(e):
        redirect(page, e.control.key)

    def edit_message(e):
        print(e.control.key)
        edit_page(page, e.control.key)

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    try:
        last_messages = requests.get(f'{SERVER_URL}/message/get/?last=10').json()

        for message_key in last_messages.keys():
            message_description = message_description_formate(last_messages[message_key]['message_description'])
            message_text = last_messages[message_key]['message']
            if len(message_text) > 1000:
                message_text = ' '.join(message_text.split(' ')[:100])

            lv.controls.append(ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                key=message_key,
                                leading=ft.Icon(ft.icons.ALBUM),
                                title=ft.Text(message_description),
                                subtitle=ft.Text(message_text),
                                on_click=get_message
                            ),
                            ft.Row(
                                [
                                    ft.TextButton("Edit", on_click=edit_message, key=message_key),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    width=400,
                    padding=10,
                )
            ))

        page.add(lv)

    except (ConnectionError, requests.JSONDecodeError):
        page.add(ft.Text('Connection error'))
