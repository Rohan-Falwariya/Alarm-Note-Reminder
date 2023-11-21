from typing import Annotated
from fastapi import BackgroundTasks, FastAPI, HTTPException,Body, Query
from pydantic import EmailStr
from database import db 
from alarm_audio import Alarm, NotificationThread 
import datetime 
from classes import Notes, Notes_update

app = FastAPI()

@app.get("/")
async def root():
    return [ "/notes", "/email","/link" ]

@app.get("/noteAlarm")
async def get_note_alarm():
    note_alarm = db.search_by_value('notesapp', 'notes', 'id', '*', get_attributes=['*'])
    return note_alarm

next_note_id = 0
@app.post("/notes")
async def add_notes(background_tasks: BackgroundTasks, 
                    note_alarm: Annotated[
                    Notes,
                    Body(
                        examples=[
                            {
                                "body": "Add a note",
                                "hour": 12,
                                "min": 30,
                                "am": "am"
                            }
                        ],
                    )]):
    global next_note_id
    body = note_alarm.body
    hour = note_alarm.hour
    min = note_alarm.min
    am = note_alarm.am
    # Check if the time is in the correct format
    if am not in ["am", "pm"]:
        raise HTTPException(status_code=400, detail="Invalid time format. It must be either AM or PM.")
    
    if am.lower() == "pm" and hour != 12:
        hour += 12
    
    requested_time = datetime.datetime.now().replace(hour=hour, minute=min)

    # Check if the requested alarm time is in the future
    if requested_time < datetime.datetime.now():
        raise HTTPException(status_code=400, detail="Invalid alarm time. It must be in the future.")
    
    alarm_time = f"{hour} : {min} {am}"
    
    next_note_id += 1
    db.insert('notesapp', 'notes', [{"Note_id":next_note_id,"body": body, "alarm": alarm_time}]) 
    # notes = db.search_by_value('notesapp', 'notes', 'id', '*', get_attributes=['*'])   // If we want to show all the notes.
    response_data = {"notes": body, "message": f"Note added successfully. Reminder set for {alarm_time}"}
    alarm = Alarm()
    background_tasks.add_task(alarm.set_alarm, hour, min, am)
    return response_data

@app.delete("/notes/delete")
async def delete_Notes( Note_id:str ):

    if not db.search_by_value('notesapp', 'notes', 'id', Note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete( 'notesapp', 'notes', [Note_id])
    response_data = { "notes": Note_id, "message": "Note deleted successfully"}
    return response_data

@app.put("/notes/Update")
async def update_Notes(background_tasks: BackgroundTasks, id:str,
            notes_update:Annotated [ Notes_update, Body(
                openapi_examples={
                    "Update Note": {
                        "summary": "Update the note",
                        "value": {
                            "body":"Update the note"
                        },
                    }
                },
            ),
            ]
        ):
    body = notes_update.body
    hour = notes_update.hour
    min = notes_update.min
    am = notes_update.am

    a=f"{hour} : {min} {am}"
    notes = None

    if body :
        db.update( 'notesapp', 'notes', [{ "id":id, "body":body }])
        notes = db.search_by_value( 'notesapp', 'notes', 'id', id, get_attributes=['Note_id','body','alarm'] ) 
        response_data = { "updated_notes": notes, "message": "Note updated successfully"}
        return response_data
    else:
        return {"message": "No updates performed."}
    

# take a break and drink water

notification_thread = NotificationThread()

@app.post("/start_notifications/")
async def start_notifications(background_tasks: BackgroundTasks ,summary="Start Notifications", description="For drink water."):

    if notification_thread.is_alive():
        raise HTTPException(status_code=400, detail="Notification thread is already running")

    background_tasks.add_task(notification_thread.start)
    return {"message": "Notification thread started"}

@app.post("/stop_notifications/")
async def stop_notifications(background_tasks: BackgroundTasks ,summary="Stop Notifications", description="To stop drink water request."):

    if not notification_thread.is_alive():
        raise HTTPException(status_code=400, detail="Notification thread is not running")

    notification_thread.stop_notification = True

    background_tasks.add_task(notification_thread.join)
    return {"message": "Notification thread stopped"}


@app.post("/email")
async def add_email(background_tasks: BackgroundTasks, data: str, 
                    subject: str ,hour: Annotated[int , Query(alias="Time-Hour")], 
                    min: Annotated[int , Query(alias="Time-Minutes")] , 
                    am: Annotated[str, Query(alias="Time-AM-PM")], 
                    to:EmailStr
                    ):
    a=f"{hour} : {min} {am}" 
    db.insert( 'noteEmail', 'email', [{"data":data,"subject":subject,"to":to, "alarm":a}])
    data_email = db.search_by_value( 'noteEmail', 'email', 'id', '*', get_attributes=['*'])
    alarm = Alarm()
    background_tasks.add_task(alarm.set_email,hour, min, am, data, subject,to )
    return {"Data":data_email,"message": "Email will be sent."}