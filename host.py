"""
NETCODE DOCS

An instance of Client is created when the user
goes into the online menu. The client initially
connects to the central lobby server and
requests the session list.

If the user chooses to create a session, their
client will be marked as a host and a session will
be initiated on the lobby server. The user will 
then have the option of leaving the session, or
starting the match once another player connects.

When the match is started, the clients exchange info
with each other through the lobby server using STUN
to initiate a direct connection before loading into the
online_play scene.

The host is assigned player_1 and client is assigned 
player_2. Once the client sends the host a 'READY' 
message, a countdown begins and the match starts.

The host processes its own events as well as the 
client's events. The host sends a gamestate update 
to the client every frame.

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