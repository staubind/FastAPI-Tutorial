from typing import Optional
from fastapi import BackgroundTasks, FastAPI, Depends

app = FastAPI()

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f'notification for {email}: {message}'
        email_file.write(content)

def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f'found query: {q}\n'
        background_tasks.add_task(write_notification, message)
    return q

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
    q: str = Depends(get_query)
    ):
    # fastapi creates BackgroundTask object for you and passes it as that param.
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}