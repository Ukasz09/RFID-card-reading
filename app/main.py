# todo: controller (aktualnie gui dostaje serwer + kllienta)

from app.appLogic import Server

if __name__ == "__main__":
    server = Server()
    server.add_terminal("1111111111")
    server.add_terminal("1111111222")
    server.remove_terminal("1111111111")
    # server.remove_terminal("1")
    server.add_worker("Jan", "7")
    server.add_worker("Ania", "777")
