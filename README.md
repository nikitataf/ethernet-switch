# Replica of Ethernet Switch

## Client implementation
In this implementation, TCP is used for the transport layer protocol. A client has one command-line argument - its node address.  Each node address is a globally unique integer in range 1-10. After the client has specified an address, every second node sends a message to a random destination node in range 1-10. Socket instance takes two parameters: **AF_INET** and **SOCK_STREAM**. **AF_INET** refers to the address of the ipv4 family, **SOCK_STREAM** refers to the connection oriented TCP protocol. The message format for the transmitted message is the following: **‘SOURCE NODE, DESTINATION NODE’**. Message include the source and the destination node addresses and no payload.

## Switch implementation
A switch has **bind()** method, which binds it to a specific IP address and port thus it can listen to incoming requests. Also, the switch has **listen()** method, which puts the server into the listening mode. This allows the switch to listen to incoming connections. Besides, the switch has **accept()** method, which initiates a connection with the client.
