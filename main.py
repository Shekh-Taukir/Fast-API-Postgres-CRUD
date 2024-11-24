from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models.database import engine, of_get_db
from models.models import Notes, Base
from models.schemas import NotesBase


app = FastAPI()

Base.metadata.create_all(bind=engine)


""" ** Notes **
Have to pass this parameter in all the API functions "db: Session = Depends(of_get_db)"
Instead we can make a annotation of this like
    i.e. db_dependency = Annotated[Session, Depends(of_get_db)]
and use the db_dependency directly, for eg:
    async def of_add_note(note: NotesBase, db: db_dependency):
"""


@app.post("/add_note")
async def of_add_note(note: NotesBase, db: Session = Depends(of_get_db)):
    db_note = Notes(
        note_title=note.note_title,
        note_desc=note.note_desc,
        writer_fname=note.writer_fname,
        writer_lname=note.writer_lname,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {"result": db_note, "Success": True}


@app.get("/get_notes")
async def of_get_notes(db: Session = Depends(of_get_db)):
    db_notes = db.query(Notes).order_by(Notes.tran_id.desc()).all()
    return {
        "result": db_notes,
        "Success": True,
        "Total Rows": len(db_notes),
    }


@app.put("/update_note/{note_id}")
async def of_update_note(
    note_id: int,
    ao_note: NotesBase,
    db: Session = Depends(of_get_db),
):
    db_note = db.query(Notes).filter(Notes.tran_id == note_id).first()

    if not db_note:
        return {"Message": "No such note found for update."}

    db_note.note_title = ao_note.note_title  # type: ignore
    db_note.note_desc = ao_note.note_desc  # type: ignore
    db_note.writer_fname = ao_note.writer_fname  # type: ignore
    db_note.writer_lname = ao_note.writer_lname  # type: ignore

    db.commit()
    db.refresh(db_note)

    return {
        "Updated Note": db_note,
        "Success": True,
    }


@app.delete("/delete_note")
async def of_delete_note(note_id: int, db: Session = Depends(of_get_db)):
    db_note = db.query(Notes).filter(Notes.tran_id == note_id).first()
    if not db_note:
        return {"Message": "No such note found for delete."}

    db.delete(db_note)
    db.commit()

    return {"Deleted Note": db_note, "Success": True}
