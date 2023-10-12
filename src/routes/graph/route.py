from pydantic import BaseModel
from fastapi import APIRouter

from .schema import GraphMetadataResp, GraphNode, RFNode, rfnode_to_kgnode
from .db import get_graph_metadata_db, get_graph_db, delete_graph_db, delete_graph_metadata_db 

from fastapi.requests import Request
import uuid

from .utils import merge_tree_ids

from KongBot.bot.base import KnowledgeGraph
from KongBot.bot.explorationv2.llm import GenSubTreeQuery, Tree2FlatJSONQuery

from typing import List
import json

from langchain import LLMChain, PromptTemplate, OpenAI

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

@router.get("/graph/{graph_id}", response_model=GraphNode)
def get_graph(graph_id: str, request: Request):
    if not request.app.curr_graph or request.app.curr_graph != graph_id:
        request.app.curr_graph = KnowledgeGraph.load_graph(graph_id)

    kg: KnowledgeGraph = request.app.curr_graph
    
    return json.loads(kg.to_json_frontend())

@router.post("/graph/update")
def update_graph(rf_graph: RFNode, request: Request):    
    kg: KnowledgeGraph = request.app.curr_graph
    
    kg_graph = rfnode_to_kgnode(rf_graph)
    kg.add_node(kg_graph, merge=True)

@router.get("/graph/delete/{graph_id}")
def delete_graph(graph_id: str, request: Request):
    delete_graph_db(graph_id)
    delete_graph_metadata_db(graph_id)
        
@router.post("/gen/subgraph/", response_model=GraphNode)
def gen_subgraph(rf_subgraph: RFNode, request: Request):
    kg: KnowledgeGraph = request.app.curr_graph

    kg_subgraph = rfnode_to_kgnode(rf_subgraph)

    print("Tree: ", kg.display_tree())   

    kg.add_node(kg_subgraph, merge=True)
    subtree = kg.display_tree(kg_subgraph["id"])
    subtree_node_old = kg_subgraph

    # GENERATE SUBTREE
    subtree = GenSubTreeQuery(kg.curriculum,
                                subtree,
                                model="gpt3").get_llm_output()

    # TODO: need to make all of JSON query LLM implement the same DataNode interface
    # so we can just add one without running the other to graph
    # TODO: need to use DataNode more
    subtree_node_new = Tree2FlatJSONQuery(subtree,
                                        model="gpt4").get_llm_output()
    
    merge_tree_ids(subtree_node_old, subtree_node_new)
    kg.add_node(subtree_node_new, merge=True)

    return json.loads(kg.to_json_frontend())