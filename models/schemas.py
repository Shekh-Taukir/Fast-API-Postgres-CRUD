from pydantic import BaseModel


class NotesBase(BaseModel):
    note_title: str
    note_desc: str
    writer_fname: str
    writer_lname: str
