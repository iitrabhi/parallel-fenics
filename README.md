# Demystifying High-Performance Computing for Finite Element Analysis Simulations

This repository contains two basic codes for understanding message passing interface and how to use that for parallel computation in FEniCS. You can read [this blogpost](https://abhigupta.io/2023/04/20/hpc-for-fea.html) for more details. If you have never worked with terminal then I would suggest you first go through this [video](https://www.youtube.com/watch?v=5XgBd6rjuDQ).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

## Installation on Linux

To install in Linux simply run the following commands in terminal:

```
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:fenics-packages/fenics
sudo apt-get update
sudo apt-get install --no-install-recommends fenics
```

These commands will just install FEniCS on your system and for all the other dependencies you have to do manual installation.

### Prerequisites

To follow along with the examples you need to install docker on your system. You need Windows 10 Education or Professional for this to work. This does not work on Windows 10 Home.

* [Docker](https://www.docker.com/products/docker-desktop)
* [Paraview](https://www.paraview.org/download/)
* [CMDER](https://cmder.net/) (Only for Windows)

After installation open `cmder` and then go-to Settings(Win+Alt+P)➡import and choose the `cmlab.xml` provided in the repository.

Once the docker system in installed and running open CMDER/terminal and run:

```
docker run -v host_system_path:/root/ -w /root/ -it iitrabhi/fenics
```

To start the notebook use:

```
docker run -p 8888:8888 -v host_system_path:/root/ -w /root/ iitrabhi/fenics_notebook
```

Note: you should replace the variable `host_system_path` with the path of the folder that contains your code. e.g. If  `D:\Codes` contains your code then to start the command line interface you have to run:

```
docker run -v D:\Codes:/root/ -w /root/ -it fenics
```

## Authors

* [Abhinav Gupta](https://abhigupta.io/)
