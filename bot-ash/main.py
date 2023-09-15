from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from . import gpt
import openai

app = FastAPI()

class Data(BaseModel):
    id: UUID
    to: str
    body: str
    from_: str = Field(alias="from")  # "from" is a reserved keyword in Python
    step_id: Optional[UUID]
    language: Optional[str]
    direction: Literal["OUTBOUND"] | Literal["INBOUND"]
    channel_id: UUID
    contact_id: UUID
    created_at: datetime
    updated_at: datetime
    attachments: List[str] = []
    campaign_id: Optional[UUID]
    conversation_id: UUID
    delivery_status: Literal["pending"] | Literal["delivered"] | Literal["sent"] | Literal["webhook_delivered"]
    step_contact_id: Optional[UUID]
    translated_body: Optional[str]
    campaign_contact_id: Optional[UUID]
    translation_language: Optional[str]

class MessageEvent(BaseModel):
    data: Data
    event: Literal["message.created"] | Literal["message.updated"]  
    request_id: UUID


@app.get("/")
def get_conversations():
    return gpt.get_messages()

@app.post("/", status_code=200)
def whippy_webhook_callback(message: MessageEvent):
    # if Whippy texts someone, 
    if message.data.direction == "INBOUND" and message.event == "message.created" and message.data.delivery_status == "webhook_delivered":
        user_id = message.data.from_
        print(f'Got a message from {user_id}')

        is_done = gpt.process_new_message_and_send(user_id, message.data.body)
        if is_done:
            print("The conversation ended with {user_id}")
            gpt.clear_history(user_id)
        return "inbound message processed"
    # if we receive a text from someone, process a response
    print(message)
    return "Uninterested"
        # gpt.process_new_message_and_send(user_id, message.data.body)
