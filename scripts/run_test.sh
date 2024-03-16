#!/bin/bash

# Start services using Docker Compose
docker-compose -f docker-compose.test.yml up -d test-db

# Run tests
docker build -t sicavs-test -f Dockerfile.tests .
docker run --rm -it -e MONGO_PORT=28018 sicavs-test

# Cleanup after tests
docker-compose -f docker-compose.test.yml down --volumes