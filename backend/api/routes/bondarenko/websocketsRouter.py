from fastapi import APIRouter, Depends, WebSocket

ws_clients = []

def get_ws_clients():
    return ws_clients

router = APIRouter(
    prefix="/bondarenko",
    tags=["parser"],
    responses={404: {"description": "Not found"}},
)

@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, clients=Depends(get_ws_clients)):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(message)
    finally:
        clients.remove(websocket)