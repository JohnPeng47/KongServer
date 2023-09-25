from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from typing import Optional

import sys
sys.path.insert(0, r'C:\Users\jpeng\Documents\business\kongyiji\kongbot')

from utils import db_conn

app = FastAPI()

class Metadata(BaseModel):
    curriculum: str
    title: str
    # optional field
    tree: str = None

@app.get("/metadata/", response_model=List[Metadata])
async def read_metadata():
    metadata_list = []
    # consider returning a cursor here to be more memory efficient
    # although the pagination limit should do the trick?
    metadatas = db_conn.get_graph_metadata(pagination=6)
    for document in metadatas:
        metadata_list.append(Metadata(**document["metadata"]))
    return metadata_list

# Run with: uvicorn filename:app --reload



