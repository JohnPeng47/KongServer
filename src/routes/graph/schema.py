from pydantic import BaseModel

class GraphMetadata(BaseModel):
    curriculum: str
    title: str
    # optional field
    # tree: str = None

class GraphMetadataResp(BaseModel):
    id: str
    metadata: GraphMetadata