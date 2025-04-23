# CryptoMatrix – Decentralized Blockchain-Based Supply Chain Tracker

**CryptoMatrix** is a decentralized blockchain-based web application developed using **C++**, **Python**, **Streamlit**, **FastAPI** and **Pybind11**. It demonstrates how blockchain can be applied to supply chain management for secure, immutable, and transparent asset tracking across multiple stakeholders. The app supports asset creation, transfers, and blockchain visualization, all powered by a lightweight proof-of-work blockchain core written in C++.


## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup and Installation](#how-to-execute)
- [Usage](#usage)
- [Blockchain Implementation Details](#blockchain-implementation-details)
- [Future Improvements](#future-improvements)


## Features

- **Asset Lifecycle Tracking**: Create and transfer supply chain assets with complete traceability.
- **Blockchain Explorer UI**: View the blockchain as a horizontal sequence of blocks, each showing its transactions.
- **Decentralized Nodes**: Each node operates independently and can sync with other peers over HTTP.
- **Immutable Ledger**: All transactions are recorded immutably using cryptographic hashes.
- **Proof-of-Work Consensus**: Each block is mined through a simple proof-of-work mechanism.
- **Chain Synchronization**: Nodes fetch the longest valid chain from known peers to ensure consistency.


## Technologies

| Layer            | Technology                       |
|------------------|-----------------------------------|
| 🧠 Core Logic     | C++ (Blockchain engine)           |
| 🔗 Python Bindings| Pybind11 (C++ ↔ Python bridge)    |
| 🖥 Backend API    | Python (Flask)                    |
| 🎨 Frontend UI    | Python (Streamlit)                |
| 🔐 Hashing        | SHA-256 (implemented in C++)      |
| 🌐 Networking     | REST API for peer-to-peer sync    |


### How to execute
To build on Windows, follow the steps:
* Recommended to use [MSYS2](https://www.msys2.org/) which provides a Unix-like environment and a command-line interface for compiling and building on Linux software that runs on Windows.
* Run the `MinGW64` environment that comes with `MSYS2`.
* Install and set up git:
```
pacman -S git
```
* Clone repository to your computer using SSH:
```
git clone git@github.com:vihankarnik/crypto-matrix.git
```
* Go to the new folder created and install all the dependencies for the `MINGW64` environment:
```
cd crypto-matrix
./install_dependencies.sh
```
* Run `build.sh` to build C++ compiled shared libraries for the backend:
```
./build.sh
```
* Run `run.sh` with a port for the api to use to start the program:
```
./run.sh 8001
```
* Run `run.sh` again on a different port with a bootstrap port to start another peer instance that will communicate with the given port to gain information about the blockchain:
```
./run.sh 8002 8001
```


### Usage
* Upon running the program, you will be presented with a simple web-based user interface in your browser. This UI allows you to:
    * Create new assets by entering an asset ID, owner, and optional metadata.
    * Transfer assets between parties by specifying the asset ID, current owner, new owner, and any notes.
    * View the blockchain ledger, including all blocks, their hashes, and the transactions they contain.
    * See the current world state, showing which assets are owned by whom.
* You can run multiple nodes by starting the program on different ports. Each node will automatically connect to the network (if you provide a bootstrap peer) and synchronize its blockchain data.
* No command-line interaction is required after startup—everything can be done through the web UI.
