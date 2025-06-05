# Tic-Tac-Toe P2P Game

## Overview

This project implements a peer-to-peer (P2P) Tic-Tac-Toe game using Python and MongoDB. The game allows users to connect to a central server for user management and data storage, while the game logic is executed on the peers. The server handles user authentication, connection management, and persistent storage of user information and game history in a MongoDB database. The project focuses on socket programming, P2P communication, and server-side management to ensure a seamless gaming experience.

## Features

- User Authentication: Users can register a new account or log in with existing credentials to connect to the server.



- P2P Gameplay: After connecting, users can view a list of online players, invite another player to a game, and play Tic-Tac-Toe in turns. The game logic runs on the peers, with the server facilitating connections.



- Server Management: The server manages user connections, handles disconnections gracefully, and stores game-related data.



- Persistent Storage: MongoDB is used to store user information and game history, ensuring data persists even after the server restarts.


- Spectator Mode: Users can choose to be a spectator, viewing a list of ongoing games and observing gameplay in real-time .




![P2P](https://github.com/user-attachments/assets/0fe61657-75b3-49f7-bf66-b6c0cc3db68a)
