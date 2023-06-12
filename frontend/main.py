import flet as ft

from .pages import messages, auth_key, get_message, pem, post_message, search_message
from .addons import window_prevent_close_event


def page_manager(page_func):
    def inner(*args, **kwargs):
        page, _ = args

        page.clean()
        menu = ft.ResponsiveRow(
            [
                ft.ElevatedButton("Home", on_click=lambda _: messages_page(page, _), col={"md": 3}),
                ft.ElevatedButton("Profile", on_click=lambda _: auth_page(page, _) if not page.session.get(
                    'encrypted_private_key') else pem_page(page, _), col={"md": 3}),
                ft.ElevatedButton("Post", on_click=lambda _: post_message_page(page, _), col={"md": 3}),
                ft.ElevatedButton("Search", on_click=lambda _: search_message_page(page, _), col={"md": 3}),
            ],
            run_spacing={"xs": 14}
        )
        page.add(menu)
        page_func(*args, **kwargs)

    return inner


@page_manager
def pem_page(page, _):
    pem(page, redirect=messages_page)


@page_manager
def auth_page(page, _):
    auth_key(page, redirect=pem_page)


@page_manager
def get_message_page(page, message_key):
    get_message(page, message_key=message_key)


@page_manager
def messages_page(page, _):
    messages(page, redirect=get_message_page, edit_page=post_message_page)


@page_manager
def post_message_page(page, default_message):
    post_message(page, redirect=get_message_page, default_message_key=default_message)


@page_manager
def search_message_page(page, _):
    search_message(page, get_message_page)


def start_up(page):
    page.title = "HaltStore"
    window_prevent_close_event(page)
    messages_page(page, None)


def run_client():
    ft.app(target=start_up, view=ft.WEB_BROWSER, port=8000)


if __name__ == '__main__':
    run_client()
