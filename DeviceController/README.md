# Device Controller Project

This project enables control of a laptop and desktop when they are connected to the same home network.

## Components

### 1. Server
Each device to be controlled will run a server that provides a simple API. 

#### Core Functions:
- **Send custom shell commands:** Execute shell commands on the target device.
- **Save a command under an alias:** Save frequently used commands with an easy-to-remember alias.
- **Modify commands or aliases:** Edit saved commands or their aliases.
- **Delete commands:** Remove commands or aliases from the system.
- **List commands:** Retrieve a list of all saved commands and aliases.
- **Persist data:** Save command and alias mappings in a JSON file on the system for persistence.

### 2. Client
A simple Android app that serves as the user interface for controlling the devices.

#### Core Functions:
- **Make API calls:** Interact with the server API to execute or manage commands.
- **List available commands:** Display all commands and aliases retrieved from the server.
- **Switch between targets:** Easily toggle control between the laptop and desktop.

