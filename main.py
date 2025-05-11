from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
from typing import Optional

app = FastAPI()

# Load the schedule once when the server starts
with open("schedule.json", encoding="utf-8") as f:
    schedule_data = json.load(f)


@app.get("/")
def root():
    return {"message": "Schedule API. Use /schedule/{group_name} to get data."}


@app.get("/schedule/{group_name}")
def get_schedule(group_name: str, week_type: Optional[str] = None, sub_group: Optional[str] = None):
    if group_name not in schedule_data:
        raise HTTPException(status_code=404, detail="Group not found")

    group_schedule = schedule_data[group_name]

    if week_type:
        if week_type not in group_schedule:
            raise HTTPException(status_code=404, detail="Week type not found")
        group_schedule = group_schedule[week_type]

        if sub_group:
            if sub_group not in group_schedule:
                raise HTTPException(status_code=404, detail="Subgroup not found")
            return group_schedule[sub_group]

        return group_schedule

    return group_schedule


@app.get("/groups")
def list_groups():
    return list(schedule_data.keys())

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

