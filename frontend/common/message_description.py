def message_description_formate(message_description: list | None) -> str:
    if not message_description or type(message_description) is not list:
        message_description = '#HaltStore'
    else:
        message_description = '#' + ' #'.join(message_description)

    return message_description