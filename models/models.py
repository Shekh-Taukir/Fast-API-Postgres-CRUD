from models.database import Base
from sqlalchemy import Integer, Column, String


class Notes(Base):
    __tablename__ = "notes_master"

    tran_id = Column(Integer, primary_key=True)
    note_title = Column(String)
    note_desc = Column(String)
    writer_fname = Column(String)
    writer_lname = Column(String)
