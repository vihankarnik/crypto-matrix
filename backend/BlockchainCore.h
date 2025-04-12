#ifndef BLOCKCHAIN_CORE_H
#define BLOCKCHAIN_CORE_H

#include <iomanip>
#include <vector>
#include <string>
#include <openssl/sha.h>

using namespace std;


//
// Fundamental datastructures and algorithms required for blockchaining
//

std::string sha256(const std::string& input) {
    /**
     * Computes the SHA256 hash of given string using sha-2 from openssl library
     * Arg: string input
     * Out: string output
     */

    unsigned char hash[SHA256_DIGEST_LENGTH];

    // Perform SHA-256 hash computation using OpenSSL
    SHA256(reinterpret_cast<const unsigned char*>(input.c_str()), input.size(), hash);

    // Convert the binary hash to a hexadecimal string
    std::ostringstream oss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i)
        oss << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(hash[i]);

    return oss.str();
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Transaction {
private:
    string sender, receiver;
    float amount;
    string signature;

public:
    Transaction() = default;
    Transaction(const std::string& sender, const std::string& receiver, float amount)
        : sender(sender), receiver(receiver), amount(amount) {}

    std::string getData() const {
        return sender + receiver + std::to_string(amount);
    }

    const std::string& getSender() const { return sender; }
    const std::string& getReceiver() const { return receiver; }
    float getAmount() const { return amount; }
    const std::string& getSignature() const { return signature; }
    void setSignature(const std::string& sig) { signature = sig; }

    bool signTransaction(const std::string& privateKeyPEM) {
        EVP_MD_CTX* mdctx = EVP_MD_CTX_new();
        if (!mdctx) return false;

        BIO* bio = BIO_new_mem_buf(privateKeyPEM.c_str(), -1);
        EVP_PKEY* pkey = PEM_read_bio_PrivateKey(bio, NULL, NULL, NULL);
        BIO_free(bio);
        if (!pkey) return false;

        if (EVP_DigestSignInit(mdctx, NULL, EVP_sha256(), NULL, pkey) != 1) return false;

        std::string data = getData();
        if (EVP_DigestSignUpdate(mdctx, data.c_str(), data.size()) != 1) return false;

        size_t sigLen;
        if (EVP_DigestSignFinal(mdctx, NULL, &sigLen) != 1) return false;

        std::string sig(sigLen, '\0');
        if (EVP_DigestSignFinal(mdctx, reinterpret_cast<unsigned char*>(&sig[0]), &sigLen) != 1) return false;

        sig.resize(sigLen);
        signature = sig;

        EVP_MD_CTX_free(mdctx);
        EVP_PKEY_free(pkey);
        return true;
    }

    bool verifySignature(const std::string& publicKeyPEM) const {
        EVP_MD_CTX* mdctx = EVP_MD_CTX_new();
        if (!mdctx) return false;

        BIO* bio = BIO_new_mem_buf(publicKeyPEM.c_str(), -1);
        EVP_PKEY* pkey = PEM_read_bio_PUBKEY(bio, NULL, NULL, NULL);
        BIO_free(bio);
        if (!pkey) return false;

        if (EVP_DigestVerifyInit(mdctx, NULL, EVP_sha256(), NULL, pkey) != 1) return false;

        std::string data = getData();
        if (EVP_DigestVerifyUpdate(mdctx, data.c_str(), data.size()) != 1) return false;

        bool result = EVP_DigestVerifyFinal(mdctx,
            reinterpret_cast<const unsigned char*>(signature.data()), signature.size()) == 1;

        EVP_MD_CTX_free(mdctx);
        EVP_PKEY_free(pkey);
        return result;
    }

    string toString() const {
        return sender + "->" + receiver + ": " + to_string(amount);
    }
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class BloomFilter {
    int size, hashCount;
    std::vector<bool> bitArray;

    // Hash combiner using std::hash and a seed multiplier
    size_t hash(const std::string& item, int seed) const {
        size_t h1 = std::hash<std::string>{}(item);
        size_t h2 = std::hash<int>{}(seed);
        return (h1 ^ (h2 << 1)) % size;
    }

public:
    BloomFilter(int s, int k) : size(s), hashCount(k), bitArray(s, false) {}

    void add(const std::string& item) {
        for (int i = 0; i < hashCount; ++i)
            bitArray[hash(item, i)] = true;
    }

    bool check(const std::string& item) const {
        for (int i = 0; i < hashCount; ++i)
            if (!bitArray[hash(item, i)])
                return false;
        return true;
    }
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class MerkleTree {
public:
    string calculateMerkleRoot(vector<string> hashes) const {
        if (hashes.empty()) return "";

        while (hashes.size() > 1) {
            if (hashes.size() & 1) // Odd number of elements
                hashes.push_back(hashes.back());

            for (size_t i = 0, j = 0; i < hashes.size(); i += 2, ++j)
                hashes[j] = sha256(hashes[i] + hashes[i + 1]);

            hashes.resize(hashes.size() / 2); // Reduce vector size
        }

        return hashes.front();
    }
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class ProofOfWork {
    int difficulty;

public:
    explicit ProofOfWork(int diff) : difficulty(diff) {}

    string mine(int& nonce, const string& data, const string& prevHash) const {
        string hashVal;
        const string prefix = string(difficulty, '0');
        const string base = data + prevHash;

        for (++nonce;; ++nonce) {
            string input = base + to_string(nonce);
            hashVal = sha256(input);
            if (hashVal.compare(0, difficulty, prefix) == 0)
                return hashVal;
        }
    }
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Block {
public:
    string previousHash, merkleRoot, hash;
    int nonce = 0;
    vector<Transaction> transactions;

    Block(vector<Transaction> txs, string prevHash)
        : previousHash(std::move(prevHash)), transactions(std::move(txs)) {
        vector<string> txHashes;
        txHashes.reserve(transactions.size()); // Avoid reallocations
        for (const auto& tx : transactions)
            txHashes.emplace_back(sha256(tx.toString()));

        MerkleTree mt;
        merkleRoot = mt.calculateMerkleRoot(txHashes);
    }

    string data() const {
        return previousHash + merkleRoot;
    }

    void setNonce(int n) { nonce = n; }
    void setHash(string h) { hash = std::move(h); }

    string calculateHash() const {
        return sha256(data() + to_string(nonce));
    }
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Blockchain {
    vector<Block> chain;
    int difficulty;

public:
    explicit Blockchain(int diff = 4) : difficulty(diff) {
        chain.emplace_back(vector<Transaction>{}, "0"); // Genesis block
    }

    void addBlock(vector<Transaction> txs) {
        const string& prevHash = chain.back().hash.empty() 
                                 ? chain.back().calculateHash()
                                 : chain.back().hash;

        Block block(std::move(txs), prevHash);
        ProofOfWork pow(difficulty);
        int nonce = 0;
        string minedHash = pow.mine(nonce, block.data(), prevHash);
        block.setNonce(nonce);
        block.setHash(std::move(minedHash));
        chain.emplace_back(std::move(block));
    }

    const vector<Block>& getChain() const {
        return chain;
    }
};

#endif
