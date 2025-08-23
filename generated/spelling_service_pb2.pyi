from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CorrectSpellingRequest(_message.Message):
    __slots__ = ("initial_text",)
    INITIAL_TEXT_FIELD_NUMBER: _ClassVar[int]
    initial_text: str
    def __init__(self, initial_text: _Optional[str] = ...) -> None: ...

class CorrectSpellingResponse(_message.Message):
    __slots__ = ("corrected_text",)
    CORRECTED_TEXT_FIELD_NUMBER: _ClassVar[int]
    corrected_text: str
    def __init__(self, corrected_text: _Optional[str] = ...) -> None: ...
