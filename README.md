# crypto-matrix


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
* Run `build.sh` to build the compiled libraries for the backend:
```
./build.sh
```
* Run `run.sh` with a port for the api to use to start the program:
```
./run.sh 8001
```
* Run `run.sh` again with a bootstrap port to start another peer instance that will communicate with the given port to gain information about the blockchain:

### Usage
