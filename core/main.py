from tornado import websocket, web, ioloop
from queue import PikaClient
from uuid import uuid4
import motor

class MainHandler(web.RequestHandler):
    def get(self):
        self.render('template/connector.html')

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def _get_sess_id(self):
        return self.sess_id

    def open(self):
        self.sess_id = uuid4().hex
        self.application.pc.register_websocket(self._get_sess_id(), self)

    def on_message(self, message):
        self.application.pc.redirect_incoming_message(self._get_sess_id(), message)

    def on_close(self):
        """
        remove connection from pool on connection close.
        """
        self.application.pc.unregister_websocket(self._get_sess_id())

def make_app():
    return web.Application([
        (r"/", MainHandler),
        (r'/ws', SocketHandler),
    ])  

if __name__ == "__main__":
    db = motor.motor_tornado.MotorClient('db', 27017).task_db
    io = ioloop.IOLoop.current()
    pc = PikaClient(io, db)
    pc.connect()
    app = make_app()
    app.listen(8888)
    app.pc = pc
    io.start()