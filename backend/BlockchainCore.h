#ifndef BLOCKCHAIN_CORE_H
#define BLOCKCHAIN_CORE_H

#include <iostream>
#include <iomanip>
#include <sstream>
#include <vector>
#include <string>
#include <openssl/sha.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <chrono>  // Time

//
// Fundamental datastructures and algorithms required for blockchaining
//


// sha256 - Computes the SHA256 hash of a given string using OpenSSL
inline std::string sha256(const std::string &input) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    // Compute SHA256 hash
    SHA256(reinterpret_cast<const unsigned char*>(input.c_str()), input.size(), hash);

    // Convert the binary hash to hexadecimal string
    std::ostringstream oss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i)
        oss << std::hex << std::setw(2) << std::setfill('0')
            << static_cast<int>(hash[i]);
    return oss.str();
}

// Transaction - Represents a simple transfer between two parties
enum class EventType { CREATE, TRANSFER };

class Transaction {
private:
    EventType event;
    std::string assetId, fromParty, toParty, meta, signature;
    std::string hashProof;  // Added: PoW-related hash

public:
    Transaction() = default;
    Transaction(EventType ev, std::string asset, std::string from, std::string to, std::string meta = {})
        : event(ev), assetId(std::move(asset)), fromParty(std::move(from)), toParty(std::move(to)), meta(std::move(meta)) {}

    static Transaction create(std::string assetId, std::string owner, std::string meta = {}) {
        return Transaction(EventType::CREATE, std::move(assetId), "GENESIS", std::move(owner), std::move(meta));
    }
    static Transaction transfer(std::string assetId, std::string from, std::string to, std::string meta = {}) {
        return Transaction(EventType::TRANSFER, std::move(assetId), std::move(from), std::move(to), std::move(meta));
    }

    void setProofHash(const std::string& h) { hashProof = h; }
    std::string getProofHash() const { return hashProof; }

    EventType getEvent() const { return event; }
    const std::string& getAssetId() const { return assetId; }
    const std::string& getFrom() const { return fromParty; }
    const std::string& getTo() const { return toParty; }
    const std::string& getMeta() const { return meta; }
    const std::string& getSignature() const { return signature; }

    void setSignature(const std::string& sig) { signature = sig; }

    bool signTransaction(const std::string& privateKeyPEM);
    bool verifySignature(const std::string& publicKeyPEM) const;

    std::string getData() const {
        return std::to_string(static_cast<int>(event)) + assetId + fromParty + toParty + meta;
    }

    std::string toString() const {
        std::ostringstream oss;
        oss << '[' << (event == EventType::CREATE ? "CREATE" : "TRANSFER") << "] " << assetId << ' '
            << fromParty << " -> " << toParty;
        if (!meta.empty()) oss << " | " << meta;
        return oss.str();
    }
};

// BloomFilter - Simple probabilistic data structure for membership testing
class BloomFilter {
    int size;
    int hashCount;
    std::vector<bool> bitArray;

    // Combines two hash values using a seed
    size_t hash(const std::string &item, int seed) const {
        size_t h1 = std::hash<std::string>{}(item);
        size_t h2 = std::hash<int>{}(seed);
        return (h1 ^ (h2 << 1)) % size;
    }

public:
    BloomFilter(int s, int k)
        : size(s), hashCount(k), bitArray(s, false) {}

    void add(const std::string &item) {
        for (int i = 0; i < hashCount; ++i)
            bitArray[ hash(item, i) ] = true;
    }

    bool check(const std::string &item) const {
        for (int i = 0; i < hashCount; ++i)
            if (!bitArray[ hash(item, i) ])
                return false;
        return true;
    }
};

// MerkleTree - Constructs a Merkle Tree and computes the Merkle root from given hashes
class MerkleTree {
public:
    std::string calculateMerkleRoot(std::vector<std::string> hashes) const {
        if (hashes.empty()) return "";

        while (hashes.size() > 1) {
            // If the number of hashes is odd, duplicate the last element.
            if (hashes.size() & 1)
                hashes.push_back(hashes.back());

            for (size_t i = 0, j = 0; i < hashes.size(); i += 2, ++j)
                hashes[j] = sha256(hashes[i] + hashes[i + 1]);

            // Resize vector to new computed level
            hashes.resize(hashes.size() / 2);
        }
        return hashes.front();
    }
};

// ProofOfWork - Implements a basic mining algorithm using a difficulty target
class ProofOfWork {
    int difficulty;

public:
    explicit ProofOfWork(int diff) : difficulty(diff) {}

    // Mines a hash that matches the difficulty and updates nonce
    std::string mine(int &nonce, const std::string &data, const std::string &prevHash) const {
        std::string hashVal;
        // Create a string of '0's with length equal to difficulty
        const std::string prefix(difficulty, '0');
        const std::string base = data + prevHash;

        for (++nonce;; ++nonce) {
            std::string input = base + std::to_string(nonce);
            hashVal = sha256(input);
            if (hashVal.compare(0, difficulty, prefix) == 0)
                return hashVal;
        }
    }
};

// Block - Contains transactions along with previous hash and proof-of-work details
class Block {
public:
    std::string previousHash, merkleRoot, hash, version;
    long long timestamp;
    int nonce = 0;
    std::vector<Transaction> transactions;

    Block(std::vector<Transaction> txs, std::string prevHash, std::string ver = "1.0")
        : previousHash(std::move(prevHash)), transactions(std::move(txs)), version(std::move(ver)) {

        timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(
                        std::chrono::system_clock::now().time_since_epoch()).count();

        std::vector<std::string> txHashes;
        txHashes.reserve(transactions.size());
        for (auto &tx : transactions) {
            std::string proof = sha256(tx.toString());
            tx.setProofHash(proof);
            txHashes.emplace_back(proof);
        }

        MerkleTree mt;
        merkleRoot = mt.calculateMerkleRoot(txHashes);
    }

    std::string data() const {
        return previousHash + merkleRoot + version + std::to_string(timestamp);
    }
    void setNonce(int n) { nonce = n; }
    void setHash(std::string h) { hash = std::move(h); }
    std::string calculateHash() const {
        return sha256(data() + std::to_string(nonce));
    }
};



// Blockchain - Manages the chain of blocks and the addition of new blocks
class Blockchain {
    std::vector<Block> chain;
    int difficulty;

public:
    explicit Blockchain(int diff = 3) : difficulty(diff) {
        // chain.emplace_back(std::vector<Transaction>{}, "0"); // I don't want an empty GENESIS block
    }

    void addBlock(std::vector<Transaction> txs) {
        std::string prevHash;
        if(chain.empty()){
            prevHash = "0"; // or some GENESIS_HASH constant
        }
        else{
            prevHash = chain.back().hash.empty() ? chain.back().calculateHash() : chain.back().hash;
        }
        Block block(std::move(txs), prevHash);
        ProofOfWork pow(difficulty);
        int nonce = 0;
        std::string minedHash = pow.mine(nonce, block.data(), prevHash);
        block.setNonce(nonce);
        block.setHash(std::move(minedHash));
        chain.emplace_back(std::move(block));
    }

    void loadChain(const std::vector<std::vector<std::string>>& raw_chain) {
        chain.clear();
        // chain.emplace_back(std::vector<Transaction>{}, "0");     // again, don't want empty GENESIS block
        for (const auto& blk : raw_chain) {
            std::vector<Transaction> txObjs;
            for (const auto& s : blk) {     // s = "[CREATE] Asset_ID GENESIS -> Alice | ... "
                auto e = s.find(']');
                std::string evt = s.substr(1, e - 1); 
                std::string rest = s.substr(e + 2);
                auto aidEnd = rest.find(' ');
                std::string aid = rest.substr(0, aidEnd);
                rest = rest.substr(aidEnd + 1);
                auto arrow = rest.find("->");
                std::string from = rest.substr(0, arrow - 1);
                rest = rest.substr(arrow + 3);
                std::string to, meta;
                auto pipe = rest.find('|');
                if (pipe != std::string::npos) {
                    to = rest.substr(0, pipe - 1);
                    meta = rest.substr(pipe + 2);
                } else {
                    to = rest;
                }
                txObjs.push_back(evt == "CREATE" ? Transaction::create(aid, to, meta)
                                                 : Transaction::transfer(aid, from, to, meta));
            }
            addBlock(txObjs);
        }
    }

    const std::vector<Block>& getChain() const { return chain; }
};

class P2PNode {
private:
    BloomFilter *bloom_filter;
    std::vector<P2PNode*> peers;

public:
    // Constructor to initialize the P2P node with a Bloom filter and peer nodes
    P2PNode(BloomFilter *filter) : bloom_filter(filter) {}

    // Add a peer node (another P2P node) to the network
    void add_peer(P2PNode* peer) {
        peers.push_back(peer);
    }

    // Receive a transaction, check if it's new, and propagate if necessary
    void receive_transaction(const std::string &transaction_id) {
        if (!bloom_filter->check(transaction_id)) {
            std::cout << "New transaction " << transaction_id << " received. Propagating..." << std::endl;
            bloom_filter->add(transaction_id);  // Add to the Bloom filter
            propagate(transaction_id);
        } else {
            std::cout << "Transaction " << transaction_id << " already seen. Not propagating." << std::endl;
        }
    }

    // Propagate the transaction to connected peers
    void propagate(const std::string &transaction_id) {
        for (auto peer : peers) {
            peer->receive_transaction(transaction_id);
        }
    }
};

// helper
// If you plan to expose this class to Python, export_block_txs is handy:
inline std::vector<std::vector<std::string>> export_block_txs(const Blockchain& bc) {
    std::vector<std::vector<std::string>> out;
    for (const auto& blk : bc.getChain()) {
        std::vector<std::string> txs;
        for (const auto& tx : blk.transactions)
            txs.push_back(tx.toString());
        out.push_back(std::move(txs));
    }
    return out;
}

#endif
