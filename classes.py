from fastapi import Query
from pydantic import BaseModel, validator
from typing import Annotated


class Notes(BaseModel):
    body: str = "add note" 
    hour: Annotated[int ,   Query(description="Should be less than 12", lt=13, gt=-1)]
    min: Annotated[int , Query(description="Should be between 0 and 59", lt=60, gt=-1)] 
    am: Annotated[str, Query(max_length=2)]  = "am/pm"
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "body": "Add a note",
    #                 "hour": 12,
    #                 "min": 30,
    #                 "am": "am"
    #             }
    #         ]
    #     }
    # }
class Notes_update(BaseModel):
    body: Annotated[str |None ,Query(alias="Note")]=None
    hour: Annotated[int |None , Query(description="Should be less than 12", lt=13, gt=-1)]=None
    min: Annotated[int |None , Query(description="Should be between 0 and 59", lt=60, gt=-1)] =None
    am: Annotated[str |None, Query(max_length=2)] =None

class Medicine(BaseModel):
    medicine_name: str
    dosage: str
    start_time: str
    repeat_interval_hours: int
    days_to_repeat: int