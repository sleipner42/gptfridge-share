# Running the Python Backend Locally

This guide is intended for experienced developers. Follow these steps to get the backend running locally:

## Prerequisites
Ensure you have the following installed:
- Docker
- Docker Compose
- Make

## Setup and Execution

1. **Environment Variables**:
   - Copy the `example.env` file to a new file named `.env`.
   - Update the `.env` file with the necessary environment variables.

2. **Database Password**:
   - Create a `password.txt` file inside the `db` folder.
   - Write your database password into `password.txt`.

3. **Build and Start Containers**:
   ```bash
   make start-dev
   ```
   This command builds and starts the necessary Docker containers for the development environment.

4. **Database Migrations**:
   ```bash
   make dev-migrate
   ```
   Run this command to apply database migrations.

5. **Database Seeding**:
   ```bash
   make dev-seed
   ```
   Use this command to populate the database with initial data.

6. **Swagger Documentation**:
   - Access the Swagger documentation by visiting [localhost:8085/docs](http://localhost:8085/docs) in your web browser.


For any issues or further instructions, please refer to the project documentation or contact the development team.
