# client-server
Lite Messenger for localhost

## Launching:  
* Firstly, launch server by `python server.py` (for Python-Server) or `go build main.go` (for Go-Server),
* Secondly launch Client by `python messenger.py` for each user and etc.

## Status:
* Client: Works! ✔️
* Python-Server: Works! ✔️
* Go-Server: Works, but coordination of the transmitted data with the Сlient is required. ⚠️


## Requirements:  
* Flask - for Python-Server,
* PyQt5 - for Client,
* gorilla/mux - for Go-Server.
