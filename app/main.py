from app.controller import ClientController, ServerController
import app.cli as ui


# todo: raport generate function


def choose_client_or_server():
    options = "Choose application mode:\n 1) Client \n 2) Server"
    while True:
        ui.show_msg(options)
        chosen = input("Your choice: ")
        ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)
        if chosen == "1":
            ClientController().run()
        elif chosen == "2":
            ServerController().run()
        else:
            ui.show_msg("Incorrect choice. Try again")
            ui.show_msg(ui.NEW_SESSION_SEPARATOR_MSG)


if __name__ == "__main__":
    choose_client_or_server()
