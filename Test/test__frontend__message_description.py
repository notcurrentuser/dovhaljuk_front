from frontend.common.message_description import message_description_formate


def test_type_message_description_formate():
    assert type(message_description_formate(['test'])) is str


def test_message_description_formate():
    assert message_description_formate(None) == '#HaltStore'
    assert message_description_formate(['HaltStore']) == '#HaltStore'
