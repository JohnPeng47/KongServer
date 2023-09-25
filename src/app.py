from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.graph.route import router as graph_router

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