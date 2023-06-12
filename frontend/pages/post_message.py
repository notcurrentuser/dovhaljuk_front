import flet as ft
import requests


class PickFile(ft.Row):
    def __init__(self):
        super().__init__()
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.selected_files = []
        self.selected_files_text = ft.Text()
        self.controls = [
            ft.ElevatedButton(
                "Pick files",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: self.pick_files_dialog.pick_files(
                    allow_multiple=True
                ),
            ),
            self.selected_files_text,
        ]

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        # self.selected_files.value = (
        #     ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        # )
        self.selected_files = [file.path for file in e.files]
        self.selected_files_text.value = f'selected files: {len(self.selected_files)}'
        self.selected_files_text.update()

    # happens when example is added to the page (when user chooses the FilePicker control from the grid)
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()

    # # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    # def will_unmount(self):
    #     self.page.overlay.remove(self.pick_files_dialog)
    #     self.page.update()


def post_message(page, redirect, default_message_key=None):
    default_message = None
    try:
        if type(default_message_key) is str:
            print(requests.get(f'http://localhost:5465/message/get/?hash_id={default_message_key}'))
            default_message = requests.get(f'http://localhost:5465/message/get/?hash_id={default_message_key}').json()[
                'message']
    except Exception as e:
        print(e)
    message_field = ft.TextField(label="Your message", value=default_message)
    password_field = ft.TextField(label="Your password")
    file_field = PickFile()

    def post(e):
        if not message_field.value:
            message_field.error_text = "Please enter your message"
            page.update()

        if not password_field.value:
            password_field.error_text = "Please enter your password"
            page.update()

        if message_field.value and password_field.value:
            try:
                print(file_field.selected_files)
                files = {f'file{i}': open(value,'rb') for i, value in enumerate(file_field.selected_files)}
                message_hash = requests.post('http://localhost:5465/message/send/',
                                             data={'message': message_field.value},
                                             files=files
                                             ).json()['message_hash']

                message_hash_sign = requests.post('http://localhost:5465/private_key/sign/',
                                                  data={
                                                      'password_phrase': password_field.value,
                                                      'data_hash': message_hash,
                                                      'encrypted_pem_private_key': page.session.get(
                                                          'encrypted_private_key'),
                                                  }).json()['signature']

                requests.post('http://localhost:5465/message_hash/send/',
                              data={
                                  'message_hash': message_hash,
                                  'message_hash_hash': message_hash_sign,
                              })

                redirect(page, message_hash)

            except ConnectionError:
                ft.Text('Error post message')

    page.add(message_field, password_field, file_field, ft.ElevatedButton("Post", on_click=post))
