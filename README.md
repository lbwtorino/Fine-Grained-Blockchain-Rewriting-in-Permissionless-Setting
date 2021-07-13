# Fine-Grained-Blockchain-Rewriting-in-Permissionless-Setting

A construction of practical ABET scheme, in addition to a Proof-of-Work blockchain implemented.
The ABET scheme can be used to secure blockchain rewriting, such that trapdoor holder may maliciously rewrite the blockchain without being identified.

## Prerequisites

The schemes have been tested with Python 3.6.7 on Mac OS X. First, verify that you have installed the following dependencies:

- [GMP 5.x](https://gmplib.org)
- [PBC library](https://crypto.stanford.edu/pbc/download.html)
- Charm 0.43, this can be installed from [this](https://github.com/JHUISI/charm/releases) page
- [OpenSSL](https://www.openssl.org/source)

## Overview

The instantiation includes the following primitives: an attribute-based encryption *KP-ABE*,
a hierarch identity-based encryption *HIBE*, a *chameleon hash* with ephemeral trapdoor, a *digital signature* scheme (e.g., Schnorr), a *DPSS* protocol and a running Proof-of-Work *blockchain*.

Some basic details of the implementation are:
```
scheme.py: full code of setup(), keygen(), hash(), verify(), adapt() algorithms
sharing.py: code of DPSS protocol 
blockchain/: code of blockchain with nodes
```

## Instructions to run

Clone the project,

```sh
$ git clone https://github.com/lbwtorino/Fine-Grained-Blockchain-Rewriting-in-Permissionless-Setting.git
```

Once installed all the dependencies, to run and test ABET scheme, 
```sh
$ python main.py ABET
```

You can also seperately run and test DPSS protocol, 
```sh
$ python main.py DPSS
```

<!-- ## Interaction with blockchain

Install the dependencies,

```sh
$ cd blockchain/
$ pip install -r requirements.txt
```

Start a blockchain node server,

```sh
$ export FLASK_APP=node_server.py
$ flask run --port 8001
```

One instance of our blockchain node is now up and running at port 8001.
Run the application on a different terminal session,

```sh
$ python run_app.py
```

The application should be up and running at [http://localhost:5000](http://localhost:5000).
To play around multiple custom nodes, here's a sample scenario that you might wanna try,

```sh
$ flask run --port 8002 &
$ flask run --port 8003 &
$ flask run --port 8004 &
```

Every node interacts with blockchain by sending transaction via http://localhost:{port_number}.
The chain data is saved in `./block_data`. -->

To rewrite the blockchain, a modifier needs to generate a same chameleon hash but with new message `m'`.
The correctness is proven in our paper.









