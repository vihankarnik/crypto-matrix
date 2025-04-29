# CryptoMatrix – Decentralized Blockchain-Based Supply Chain Tracker

**CryptoMatrix** is a decentralized blockchain-based web application developed using **C++**, **Python**, **Streamlit**, **FastAPI** and **Pybind11**. It demonstrates how blockchain can be applied to supply chain management for secure, immutable, and transparent asset tracking across multiple stakeholders. The app supports asset creation, transfers, and blockchain visualization, all powered by a lightweight proof-of-work blockchain core written in C++.

<div align="center"><img align="center" width=700px src=Picture1.png></div>

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
| 🖥 Backend API    | Python (FastAPI served via Uvicorn)  |
| 🎨 Frontend UI    | Python (Streamlit)                |
| 🔐 Hashing        | SHA-256 (implemented in C++)      |
| 🌐 Networking     | REST API for peer-to-peer sync    |


## How to execute
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


## Usage
* Upon running the program, you will be presented with a simple web-based user interface in your browser. This UI allows you to:
    * Create new assets by entering an asset ID, owner, and optional metadata.
    * Transfer assets between parties by specifying the asset ID, current owner, new owner, and any notes.
    * View the blockchain ledger, including all blocks, their hashes, and the transactions they contain.
    * See the current world state, showing which assets are owned by whom.
* You can run multiple nodes by starting the program on different ports. Each node will automatically connect to the network (if you provide a bootstrap peer) and synchronize its blockchain data.
* No command-line interaction is required after startup—everything can be done through the web UI.


## Blockchain Implementation Details

This project implements a fully functional blockchain system tailored to a supply chain use case, written in modern C++ and exposed to Python via pybind11. A breakdown of the key blockchain features:

#### 🧱 Block Structure
Each block includes:
- A list of signed transactions (e.g., asset creation or ownership transfer)
- A Merkle root hash to ensure transaction integrity
- A reference to the previous block's hash
- Timestamp, version, and nonce (for PoW mining)
- Block hash generated via SHA-256

#### 🔐 Transaction Signing
Transactions are cryptographically signed using OpenSSL:
- Each transaction (Create or Transfer) includes metadata and ownership details.
- The sender signs the transaction using a private key.
- The signature is later verified using the sender's public key during validation.

#### 🌲 Merkle Tree
A Merkle Tree is used to compress and hash all transaction data into a single root hash. This provides:
- Efficient transaction validation
- Tamper-proof grouping of transactions

#### 🔨 Proof-of-Work (PoW)
To simulate real-world consensus:
- A Proof-of-Work algorithm is used to "mine" blocks.
- The mining process searches for a nonce such that the resulting block hash starts with a defined number of leading zeroes (difficulty).
- This deters spamming and reinforces chain integrity.

#### 🌐 Decentralization Support (P2P)
- Includes a basic Peer-to-Peer (P2P) simulation using a Bloom filter to propagate transactions efficiently across nodes.
- Each node maintains its own blockchain copy and filters duplicate transactions.

---

### 🚀 Future Improvements

While the core blockchain infrastructure is in place, there are several exciting features planned to elevate the system to production-level standards:

#### 🔁 1. Full Peer-to-Peer Networking
- Build actual socket-based P2P nodes for decentralized blockchain syncing.
- Enable nodes to discover, broadcast, and validate new blocks from peers.

#### 🗂️ 2. Persistent Storage
- Currently, the blockchain exists in memory only.
- Future versions will store blocks in a file or database (e.g., SQLite or LevelDB).

#### 📄 3. Smart Contract Layer
- Introduce a lightweight smart contract interpreter for advanced supply chain logic (e.g., conditional transfers, automated audits).

#### 🔑 4. Key Management
- Add UI-based key generation and storage using encrypted local keystores.
- Improve security by abstracting OpenSSL handling from users.

#### 📉 5. Analytics and Visualization
- Show asset flow timelines and block analytics using Streamlit charts.
- Add visual Merkle Tree explorers.

#### 🛠️ 6. Enhanced UI
- Transition from prototype UI to a more polished web interface using React or Next.js (optional alternative to Streamlit).

#### 🧪 7. Testing and CI/CD
- Write automated unit tests for C++ and Python bindings.
- Set up GitHub Actions or similar CI/CD for builds, testing, and deployments.
