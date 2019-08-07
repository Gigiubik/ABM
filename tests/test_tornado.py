from tornado.testing import AsyncHTTPTestCase
import tornado
from mesa import Model
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
import json


class TestServer(AsyncHTTPTestCase):

    def get_app(self):
        app = ModularServer(Model, [], model_params={"seed": UserSettableParameter("static_text", value="0")})
        return app

    def test_homepage(self):
        response = self.fetch('/')
        assert response.error is None

    @tornado.testing.gen_test
    def test_websocket(self):
        ws_url = "ws://localhost:" + str(self.get_http_port()) + "/ws"
        ws_client = yield tornado.websocket.websocket_connect(ws_url)

        # Now we can run a test on the WebSocket.
        response = yield ws_client.read_message()
        msg = json.loads(response)
        assert msg["type"] == "model_params"

        ws_client.write_message('{"type": "get_step"}')
        response = yield ws_client.read_message()
        msg = json.loads(response)
        assert msg["type"] == "viz_state"

        ws_client.write_message('{"type": "reset"}')
        response = yield ws_client.read_message()
        msg = json.loads(response)
        assert msg["type"] == "viz_state"

        ws_client.write_message('{"type": "submit_params", "param": "seed", "value": "12"}')

        ws_client.write_message('{"type": "Unknown"}')
