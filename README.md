# MultiThread-TCP-chat
A minimal multi-threaded TCP chat server and client in Python. Pick a name, then chat with everyone connected. No dependencies, standard library only.

## Files
`server.py` - the server (one thread per connected client)

`client.py` - a simple terminal client
## Usage

Start the server (default port 5000):

bash

`python server.py [port]`

Connect one or more clients, each in its own terminal:

bash

`python chat_client.py [host] [port]`

Defaults are 127.0.0.1 and 5000. When connected, enter your name, then type messages and press Enter. Press Ctrl+C to leave.

Any plain TCP client works too, for example nc localhost 5000.

## How it works

The main thread accepts connections and starts a new thread for each client.
Each client thread reads lines from its socket and broadcasts them to everyone else.
A shared dictionary maps each socket to a name, protected by a lock.
The client uses one thread to print incoming messages while the main thread reads the keyboard.
The server also prints all messages, joins and leaves to its own terminal.

## Notes

Your own messages are not echoed back to you.
Names are not checked for uniqueness, and are cut to 20 characters.
Messages are not encrypted. Use it on a trusted network only.
