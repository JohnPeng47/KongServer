from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from routes.graph.route import router as graph_router
from routes.auth.route import router as auth_router
from routes.events.route import router as events_router

import os
print(os.environ.get('PYTHONPATH'))

app = FastAPI()

# Set up the CORS middleware
origins = [
    "http://localhost:3000",  # Allow requests from your local frontend
    # Add any other origins (frontend URLs) you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graph_router)
app.include_router(auth_router)
app.include_router(events_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
