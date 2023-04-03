"""
NETCODE DOCS

An instance of Client is created when the user
goes into the online menu. The client initially
connects to t he central lobby server and
requests the session list.

Client
 - initially connects to the central lobby
 - 

1. Player starts the game
2. Game creates an instance of Client
3. Player clicks 'create lobby'
4. The game replaces its current Client object with a Host object
5. The host client sends a message to the lobby server asking for session registration
6. Another client decides to join the session
7. Host starts the match
8. The clients exchange information with each other through the lobby server using STUN
9a. The clients initiate a direct connection with each other
9b (OPTIONAL) If a direct connection is not possible, use the lobby server as a relay
10a. The player 2 client sends events to the host
10b. The player 1 client manages the gamestate and sends it to player 2

"""