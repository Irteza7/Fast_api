## FastAPI Application

A FastAPI-based web application with features like user authentication, post creation, and voting.

### Introduction

This project was undertaken to gain hands-on experience with various aspects of modern web development, including API development, database management with both ORM and raw SQL, continuous integration and deployment (CI/CD), unit testing, and deployment using Docker, Render, and Ubuntu. The primary goal was to build a robust and scalable application while exploring and mastering these tools.

### Documentation

For a detailed description of the project, please refer to the [PROJECT REPORT](report.md).

### Features

- **User Registration and Authentication**: Securely register and authenticate users using JWT.
- **CRUD Operations for Posts**: Create, read, update, and delete posts with ease.
- **Voting System**: Users can vote for their favorite posts.
- **Docker Support**: Easily deploy the application using Docker.

### Setup and Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Irteza7/Fast_api.git
cd Fast_api
```

#### 2. Setup Environment Variables

- Copy the sample environment file: 
  ```bash
  cp app/.env.sample app/.env
  ```
- Update the `.env` file with your database and other configurations.

#### 3. Using Docker

- For development:
  ```bash
  docker-compose -f docker-compose-dev.yml up --build
  ```
- For production:
  ```bash
  docker-compose -f docker-compose-prod.yml up --build
  ```

#### 4. Access the Application

- Open your browser and navigate to `http://localhost:8000/`.

### API Endpoints

#### User

- Register: `POST /users/`
- Retrieve User: `GET /users/{id}`

#### Authentication

- Login: `POST /login`

#### Posts

- Create: `POST /posts/`
- Retrieve All: `GET /posts/`
- Retrieve One: `GET /posts/{post_id}`
- Update: `PUT /posts/{post_id}`
- Delete: `DELETE /posts/{post_id}`

#### Votes

- Vote/Unvote: `POST /vote`

### Contributing

Feel free to fork the repository, make changes, and submit pull requests.
