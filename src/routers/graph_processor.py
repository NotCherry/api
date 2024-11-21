from typing import Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging
import traceback
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


active_connections: Set[WebSocket] = set()

def decrement_bracket_numbers(match):
    # Extract the number, convert to integer, and decrement by 1
    number = int(match.group(1))
    number = (number - 1) if number > 0 else 0
    # Return the modified string
    return f"{{{number}}}"


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    logger.info(f"Number of active connections: {active_connections.__len__()}")
    try:
        while True:
            req = await websocket.receive_text()
            try:
                if (req == None or req == ""):
                    break
                req = json.loads(req)

                local = req['type'] == 'local'
                await process_nodes(req, websocket, local)
            except Exception as e:
                logger.info("Error in json or nodes")
                logger.error(e)
                error_message = traceback.format_exc()  # Capture the full traceback as a string
                logger.error(error_message)
                raise WebSocketDisconnect(code=1000, reason="Not work")
    except WebSocketDisconnect:
            active_connections.remove(websocket)
            logger.info("Peer Discnected")
            await websocket.close()

async def process_nodes(req, socket: WebSocket, local = False):
    graph_nodes = req["data"]

    # map_of_nodes - holds all nodes with all data from graph source of all information
    # nodes_to_execute - holds nodes "id" that are curently loadaed to be processed or wait until resolve earlier and then starts preocessing 
    # map_of_processed_nodes - holds only output of llm

    # for start of resolving loop
    nodes_to_execute = [x['id'] for x in graph_nodes if 'pointedBy' not in x.keys()]
    executed_nodes_in_iteration = []
    # add all input nodes
    executed_nodes_in_iteration.extend(nodes_to_execute)

    # for easy access by pointing id
    map_of_nodes = {}
    for x in graph_nodes:
        map_of_nodes[x['id']] = x

    map_of_processed_nodes = {}
    # pass input nodes data straight to context
    for x in nodes_to_execute:
        map_of_processed_nodes[x] = map_of_nodes[x]


    number_of_loops = 0    
    while len(map_of_processed_nodes.keys()) != len(map_of_nodes.keys()):
        for node_id in nodes_to_execute:
            logger.warning(map_of_nodes[node_id]['nodeType'])
            keys = map_of_processed_nodes.keys()
            if map_of_nodes[node_id]['nodeType'] == "generate" and  all(key in keys  for key in map_of_nodes[node_id]['pointedBy']):
                # ducktape prompt context
                prompt = map_of_nodes[node_id]['data']['text']

                prompt = re.sub(r"\{(\d+)\}", decrement_bracket_numbers, prompt)
                context = [node for node in map_of_nodes[node_id]['pointedBy']]
                context = [map_of_processed_nodes[idx] for idx in context]
                prompt = prompt.format(*context)
                
                if (local):
                    await socket.send_text(json.dumps({ "type": "run_local", "data": {"url": "http://localhost:1234/v1/completions", "data": {"id": node_id, "prompt": prompt}}}))
                    rr = await socket.receive_text()
                    logger.info(rr)
                    sreq = json.loads(rr)

                    if sreq['type'] == "local_llm":
                        response_LLM = sreq['data']
                else:
                    response_LLM = await askLLM(prompt)
                    await socket.send_text(json.dumps({ "type": "update_node", "data": {"id": node_id, "data": response_LLM}}))
                map_of_processed_nodes[node_id] = response_LLM
            else:        
                map_of_processed_nodes[node_id] = map_of_nodes[node_id]['data']['text']
            
            if map_of_nodes[node_id]['nodeType'] == "output":
                map_of_processed_nodes[node_id] = map_of_nodes[node_id]['data']['text']
                await socket.send_text(json.dumps({ "type": "update_node", "data": {"id": node_id, "data": response_LLM}}))
                await socket.send_text(json.dumps({ "type": "run_compleated", "data": {"text": response_LLM }}))

            executed_nodes_in_iteration.append(node_id)
            if (map_of_nodes[node_id]['nodeType'] != 'output'):
                nodes_to_execute.extend(map_of_nodes[node_id]['pointingTo'])
            nodes_to_execute = list(set(nodes_to_execute) - set(executed_nodes_in_iteration))
            executed_nodes_in_iteration = []


async def askLLM(x):
    return x