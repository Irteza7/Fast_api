# FastAPI Project Report

## Introduction

This project was undertaken to gain hands-on experience with various aspects of modern web development, including API development, database management with both ORM and raw SQL, continuous integration and deployment (CI/CD), unit testing, and deployment using Docker, Render, and Ubuntu. The primary goal was to build a robust and scalable application while exploring and mastering these technologies.

## Overview

The project is a web application built using the FastAPI framework. It offers features such as user registration, authentication, post creation, voting, and more. The application is designed to be containerized using Docker, making it scalable and easy to deploy.

## Key Features

### 1. User Management

- **Registration**: Users can register themselves in the system.
- **Authentication**: Implemented JWT-based authentication. Users can log in to get an access token, which is then used to authenticate subsequent requests.

### 2. Posts

- **CRUD Operations**: Users can create, read, update, and delete posts.
- **Voting System**: A voting mechanism where users can vote or unvote posts.

### 3. Configuration Management

- Uses environment variables for configuration.
- Configuration includes database connection details, JWT settings, and more.

### 4. Database Management

- Utilizes SQLAlchemy for database operations.
- Database models for users, posts, and votes are defined.
- Raw SQL is also used in certain parts for more complex queries or operations.

### 5. Docker Integration

- The application is designed to run inside Docker containers.
- Separate Docker Compose files are provided for development and production environments.

## Code Structure

### Main Application (`app/main.py`)

- Initializes the FastAPI application.
- Includes routers.
- Sets up CORS middleware.

### Configuration (`app/config.py`)

- Manages application configuration using environment variables.

### Database (`app/database.py`)

- Handles database connections and sessions.

### Models (`app/models.py`)

- Defines the database models for users, posts, and votes.

### Authentication (`app/oauth2.py`)

- Contains utility functions for JWT token creation and verification.

### Routers

- **Auth (`app/routers/auth.py`)**: Endpoints related to user authentication.
- **Posts (`app/routers/post.py`)**: Endpoints for post CRUD operations.
- **Users (`app/routers/user.py`)**: Endpoints for user management.
- **Votes (`app/routers/vote.py`)**: Endpoints related to post voting.

### Utilities (`app/utils.py`)

- Contains utility functions, including those for password hashing and verification.

### Docker and Deployment

- `Dockerfile` for building a Docker image of the application.
- Docker Compose files for orchestrating the application and its dependencies.

### Dependencies (`requirements.txt`)

- Lists all the Python packages and libraries required for the application.

## CI/CD and Testing

- The project integrates CI/CD practices using GitHub Actions.
- The `.github/workflows/build-deploy.yml` file defines the CI/CD pipeline.
- There's a `tests/` directory, indicating the presence of unit tests to ensure the application's robustness.

## Deployment

- The application is designed to be deployed on Render, a cloud platform.
- It can also be deployed on an Ubuntu server using Docker for containerization.

## Conclusion

This project serves as a comprehensive exploration into modern web development practices, from API development to deployment. It showcases the power of FastAPI, the flexibility of Docker, and the importance of CI/CD in today's development landscape.

