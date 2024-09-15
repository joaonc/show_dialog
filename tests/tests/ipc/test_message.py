from pytest_params import params

from src.show_dialog.ipc.message import Message, MessageType


@params(
    'message, expected',
    (
        ('type only', Message(MessageType.MESSAGE), '{"type": "message"}'),
        ('type as str', Message('timeout'), '{"type": "timeout"}'),
        (
            'with message',
            Message(MessageType.MESSAGE, message='foo'),
            '{"type": "message", "message": "foo"}',
        ),
        (
            'with data',
            Message(MessageType.MESSAGE, data={'foo': 1}),
            '{"type": "message", "data": {"foo": 1}}',
        ),
        (
            'with message and data',
            Message(MessageType.MESSAGE, message='foo', data={'bar': 'baz'}),
            '{"type": "message", "message": "foo", "data": {"bar": "baz"}}',
        ),
    ),
)
def test_to_json(message, expected):
    message_json = message.to_json()
    assert message_json == expected
