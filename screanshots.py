import logging

from aiortc import RTCSessionDescription, RTCPeerConnection, RTCIceCandidate
from sanic import Sanic, Request
from sanic.response import json, file
from screen_stream.peer_connection import create_local_tracks

app = Sanic("app")

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level="INFO", format=LOG_FORMAT)
logger = logging.getLogger()


@app.route('/')
async def index(request):
    return await file("templates/index.html")


@app.route("/client.js")
async def javascript(request):
    return await file("static/js/client.js")


@app.route("/offer", methods=['POST'])
async def get_offer(request: Request):
    params = request.json
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()

    @pc.on("datachannel")
    def on_datachannel(channel):
        print(channel)

        @channel.on("message")
        async def on_message(message):
            print(message)

    video = create_local_tracks()
    await pc.setRemoteDescription(offer)
    pc.addTrack(video)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return json(body={"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
