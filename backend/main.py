from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# Import Routers
from routers import meetings, tasks, audit, demo, approvals

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meeting-to-Execution Autopilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For hackathon demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meetings.router)
app.include_router(tasks.router)
app.include_router(audit.router)
app.include_router(demo.router)
app.include_router(approvals.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Meeting-to-Execution Autopilot is running"}
