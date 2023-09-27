from pydantic import BaseModel
from fastapi import APIRouter

from .schema import GraphMetadataResp, Graph
from .db import get_graph_metadata_db, get_graph_db

from typing import List

router = APIRouter()


@router.get("/metadata/", response_model=List[GraphMetadataResp])
def get_graph_metadata():
    metadata_list = []
    # consider returning a cursor here to be more memory efficient
    # although the pagination limit should do the trick?
    metadatas = get_graph_metadata_db(pagination=6)
    for document in metadatas:
        metadata_list.append(document)
    return metadata_list


@router.get("/graph/{graph_id}", response_model=Graph)
def get_graph(graph_id: str):
    return get_graph_db(graph_id)
