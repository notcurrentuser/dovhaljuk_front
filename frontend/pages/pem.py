import flet as ft


def pem(page, redirect):
    def user_exit(e):
        page.session.clear()
        redirect(page, None)

    encrypted_private_key = page.session.get('encrypted_private_key')
    public_key = page.session.get('public_key')

    page.add(ft.TextField(label='Private Key', read_only=True, value=encrypted_private_key))

    if public_key:
        page.add(ft.TextField(label='Public Key', read_only=True, value=page.session.get('public_key')))

    page.add(ft.ElevatedButton("Exit", on_click=user_exit))
