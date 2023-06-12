import flet as ft
import requests


def auth_key(page, redirect):
    password_field = ft.TextField(label="Your password")
    key_field = ft.TextField(label="Your key")

    def check_password(e):
        if password_field.value:
            try:
                if key_field.value:
                    page.session.set('encrypted_private_key', key_field.value)
                else:
                    page.splash = ft.ProgressBar()
                    page.update()
                    pems = requests.post('http://localhost:5465/private_key/generation/',
                                         {'password_phrase': password_field.value}).json()
                    page.splash = None
                    page.update()

                    encrypted_private_key = pems['encrypted_pem_private_key']
                    public_key = pems['pem_public_key']

                    page.session.set('encrypted_private_key', encrypted_private_key)
                    page.session.set('public_key', public_key)

                redirect(page, None)
            except requests.exceptions.ConnectionError:
                page.splash = None
                page.update()
                page.add(ft.Text('Connection Error'))

        else:
            password_field.error_text = "Please enter your password"
            page.update()

    page.add(password_field, key_field, ft.ElevatedButton("Submit", on_click=check_password))
