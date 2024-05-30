from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logs = open("data.log", "w");
    while True:
        req = await websocket.receive_text()
        
        if (req == None or req == ""):
            break
        try:
          req = json.loads(req)
        except WebSocketDisconnect:
            WebSocketDisconnect(code=1000, reason=None)
        except Exception as e:
            logs.write(str(e))
            
            next()
        
        process_nodes(req)

def process_nodes(req):
    graph_nodes = dict(req["data"])
    nodes_to_execute = []
    map_of_processed_nodes = {}
    
    print(graph_nodes.keys())