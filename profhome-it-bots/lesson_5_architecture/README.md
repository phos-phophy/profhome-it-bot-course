## Description

Try to design an application architecture that conforms to the following principles:

* DRY - Don't Repeat Yourself
* KISS - Keep It Simple, Stupid
* DI - Dependency Injection
* SOLID
  * S - Single Responsibility Principle, SRP
  * O - Open/Closed Principle, OCP
  * L - Liskov Substitution Principle, LSP
  * I - Interface Segregation Principle, ISP
  * D - Dependency Inversion Principle, DIP


## How to start

```
usage: main.py [-h] [-c CONFIG] [-s SERVER_CONFIG]

Bot CLI arguments

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the app configuration file
  -s SERVER_CONFIG, --server_config SERVER_CONFIG
                        Path to the server configuration file
```

1. Run `openssl rand -hex 32` to generate your secret key that will be used to sign the JWT tokens.
   And copy the output to the environment variable `SECRET_KEY`.
    ```bash
    export SECRET_KEY=$(openssl rand -hex 32)
    ```
2. Run in the command line `main.py [-h] [-c CONFIG] [-s SERVER_CONFIG]`