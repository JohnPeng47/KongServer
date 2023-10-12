from pydantic import BaseModel
from fastapi import APIRouter

from .schema import GraphMetadataResp, GraphNode
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

# def merge(graphA: GraphNode, graphB: GraphNode):



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
    
    return json.loads(request.app.curr_graph.to_json_tree_repr())

# this route results in a response 405
@router.post("/graph/update")
def update_graph(graph: GraphNode, request: Request):
    old_id = graph.id
    
    kg: KnowledgeGraph = request.app.curr_graph
    old_node = kg.get_node(old_id)
    print("old_node", old_node)
    kg.add_node(graph.dict(), old_node, merge=True)

@router.get("/graph/delete/{graph_id}")
def delete_graph(graph_id: str, request: Request):
    delete_graph_db(graph_id)
    delete_graph_metadata_db(graph_id)
        
# this one no error
@router.post("/gen/subgraph/", response_model=GraphNode)
def gen_subgraph(subgraph: GraphNode, request: Request):

    kg: KnowledgeGraph = request.app.curr_graph

    kg.add_node(subgraph.dict(), merge=True)
    subtree = kg.display_tree(subgraph.id)   
    subtree_node_old = subgraph.dict()

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

    return json.loads(kg.to_json_tree_repr())