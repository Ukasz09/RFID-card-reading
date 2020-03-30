from app.controller import ClientController, ServerController

# todo: refactor (packages, cli)
# todo: menu for running program as client or server
# todo: raport generate function
if __name__ == "__main__":
    client = ClientController()
    # client.run()

    server = ServerController()
    server.run()
