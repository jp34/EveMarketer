from api.server import EveServer
import threading


def start_server():
    server = EveServer()
    server.start()
    server.authorize()


def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()


if __name__ == "__main__":
    main()
