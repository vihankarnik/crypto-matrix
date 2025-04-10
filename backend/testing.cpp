#include "BlockchainCore.h"
#include <iostream>
#include <openssl/sha.h>
#include <string>

using namespace std;

int main(){
    string test = "hey this is my name Vihan";
    string test2 = "hmmst";
    string sus = "hey this is my name Vihan";

    cout << sha256(test) << endl;
    cout << endl;
    cout << sha256(sus) << endl;
}
