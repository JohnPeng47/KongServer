from routes import db_conn
from pydantic import BaseModel
from fastapi import APIRouter

from .schema import GraphMetadataResp

from typing import List

router = APIRouter()

@router.get("/metadata/", response_model=List[GraphMetadataResp])
async def read_metadata():
    metadata_list = []
    # consider returning a cursor here to be more memory efficient
    # although the pagination limit should do the trick?
    metadatas = db_conn.get_graph_metadata(pagination=6)
    for document in metadatas:
        metadata_list.append(document)
    return metadata_list
