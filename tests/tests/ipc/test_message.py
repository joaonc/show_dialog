from src.show_dialog.ipc.message import Message, MessageType


def test_to_json():
    message = Message(MessageType.MESSAGE, message='foo')
    message_json = message.to_json()
    assert message_json == '{"type": "message", "message": "foo", "data": {}}'
