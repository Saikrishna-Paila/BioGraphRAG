# BioGraphRAG Docker Deployment Guide

This guide explains how to build and run the BioGraphRAG application using Docker.

## Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)
- `.env` file with your API credentials

## Quick Start

### Using Docker Compose (Recommended)

1. **Ensure your `.env` file exists with all required credentials:**
   ```env
   NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your-password
   OPENAI_API_KEY=sk-proj-...
   GROQ_API_KEY=gsk_...
   ```

2. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Using Docker CLI

1. **Build the Docker image:**
   ```bash
   docker build -t biographrag:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name biographrag-app \
     -p 8501:8501 \
     --env-file .env \
     biographrag:latest
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

4. **View logs:**
   ```bash
   docker logs -f biographrag-app
   ```

5. **Stop the container:**
   ```bash
   docker stop biographrag-app
   docker rm biographrag-app
   ```

## Docker Commands Reference

### Build Commands
```bash
# Build the image
docker build -t biographrag:latest .

# Build without cache
docker build --no-cache -t biographrag:latest .
```

### Run Commands
```bash
# Run in detached mode
docker run -d --name biographrag-app -p 8501:8501 --env-file .env biographrag:latest

# Run with interactive terminal
docker run -it --name biographrag-app -p 8501:8501 --env-file .env biographrag:latest

# Run with custom port
docker run -d --name biographrag-app -p 8080:8501 --env-file .env biographrag:latest
```

### Container Management
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop biographrag-app

# Start stopped container
docker start biographrag-app

# Restart container
docker restart biographrag-app

# Remove container
docker rm biographrag-app

# Remove container forcefully
docker rm -f biographrag-app
```

### Logs and Debugging
```bash
# View logs
docker logs biographrag-app

# Follow logs in real-time
docker logs -f biographrag-app

# View last 100 lines
docker logs --tail 100 biographrag-app

# Execute command in running container
docker exec -it biographrag-app /bin/bash

# Check container health
docker inspect --format='{{.State.Health.Status}}' biographrag-app
```

### Image Management
```bash
# List images
docker images

# Remove image
docker rmi biographrag:latest

# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a
```

## Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Build and start
docker-compose up --build

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Restart services
docker-compose restart

# View running services
docker-compose ps
```

## Environment Variables

The application requires the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEO4J_URI` | Neo4j Aura connection URI | `neo4j+s://xxx.databases.neo4j.io` |
| `NEO4J_USERNAME` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | `your-password` |
| `OPENAI_API_KEY` | OpenAI API key for embeddings | `sk-proj-...` |
| `GROQ_API_KEY` | Groq API key for LLM | `gsk_...` |

## Health Check

The Docker container includes a health check that monitors the Streamlit application:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' biographrag-app

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' biographrag-app
```

## Troubleshooting

### Container won't start
```bash
# Check logs for errors
docker logs biographrag-app

# Verify environment variables
docker exec biographrag-app env
```

### Port already in use
```bash
# Use a different port
docker run -d --name biographrag-app -p 8080:8501 --env-file .env biographrag:latest
```

### Permission issues
```bash
# Run with user permissions
docker run -d --name biographrag-app -p 8501:8501 --user $(id -u):$(id -g) --env-file .env biographrag:latest
```

### Rebuild after code changes
```bash
# Docker Compose
docker-compose up --build

# Docker CLI
docker build --no-cache -t biographrag:latest .
docker stop biographrag-app
docker rm biographrag-app
docker run -d --name biographrag-app -p 8501:8501 --env-file .env biographrag:latest
```

## Production Deployment

For production deployment, consider:

1. **Use environment variables instead of .env file:**
   ```bash
   docker run -d \
     --name biographrag-app \
     -p 8501:8501 \
     -e NEO4J_URI="neo4j+s://..." \
     -e NEO4J_USERNAME="neo4j" \
     -e NEO4J_PASSWORD="password" \
     -e OPENAI_API_KEY="sk-..." \
     -e GROQ_API_KEY="gsk_..." \
     biographrag:latest
   ```

2. **Use Docker secrets for sensitive data**

3. **Set resource limits:**
   ```bash
   docker run -d \
     --name biographrag-app \
     -p 8501:8501 \
     --memory="2g" \
     --cpus="1.5" \
     --env-file .env \
     biographrag:latest
   ```

4. **Use a reverse proxy (nginx/traefik) for SSL/TLS**

5. **Implement proper logging and monitoring**

## Notes

- The application runs on port 8501 by default
- Health checks are performed every 30 seconds
- Container automatically restarts unless stopped manually (when using docker-compose)
- All uploaded PDFs are stored in the container and will be lost when the container is removed
- Neo4j database persists data independently in Neo4j Aura

## Support

For issues or questions, check:
- Container logs: `docker logs biographrag-app`
- Health status: `docker inspect biographrag-app`
- Environment variables: `docker exec biographrag-app env`
