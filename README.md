# Setup

I dockerized the application using docker-compose.
So to run the application docker is required.
To run the application complete the following steps:

Clone the repo https://github.com/xeneta/ratestask and build the docker image by running the following command in the terminal:

```bash
docker build -t ratestask .
```

Clone this repo and then run the following in the repo's directory:

```bash
docker-compose build
```

```bash
docker-compose up -d
```

The application should now be hosted on http://localhost:5000/
Navigating to this url should display "The server is running!"