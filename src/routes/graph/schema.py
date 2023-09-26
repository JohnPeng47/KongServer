from pydantic import BaseModel
from typing import Optional, List, Dict

class GraphNodeData(BaseModel):
    title: str
    node_type: str
    description: Optional[str]
    entity_relations: Optional[List[Dict]]
    concept: Optional[str]
    children: Optional[List["GraphNode"]]  

class GraphNode(BaseModel):
    id: str
    show: Optional[bool]  
    node_data: GraphNodeData

# used to resolve the forward reference in the children field
GraphNodeData.update_forward_refs()

class Graph(BaseModel):
    id: str
    show: Optional[str]
    node_data: GraphNodeData
    children: Optional[List[GraphNode]]
    
class GraphMetadata(BaseModel):
    curriculum: str
    title: str
    # optional field
    # tree: str = None

class GraphMetadataResp(BaseModel):
    id: str
    metadata: GraphMetadata
