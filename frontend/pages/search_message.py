import flet as ft


def search_message(page, redirect):
    key_field = ft.TextField(label="Enter message key")

    def check_password(e):
        if key_field.value:
            redirect(page, key_field.value)
        else:
            key_field.error_text = "Please enter your password"
            page.update()

    page.add(key_field, ft.ElevatedButton("Search", on_click=check_password))
