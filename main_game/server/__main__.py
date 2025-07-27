from server import setup_server

if __name__ == "__main__":
    server = setup_server()
    server.run(debug = True)