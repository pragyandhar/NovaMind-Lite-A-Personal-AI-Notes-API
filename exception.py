class NoteNotFoundException(Exception):
    def __init__(self, note_id):
        self.note_id = note_id

class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
