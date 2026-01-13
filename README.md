## Superheroes API

A simple Flask RESTful API for managing superheroes, their powers, and the association between them. This project demonstrates the use of Flask, SQLAlchemy, Flask-Migrate, and Flask-RESTful.

## Features

Manage Heroes: Create, read, and retrieve detailed information about superheroes.

Manage Powers: Create, read, and update superhero powers.

Manage Hero-Power associations with strengths (Strong, Average, Weak).

Nested serialization to avoid infinite loops in JSON responses.

Input validation at the model level.

## Tech Stack

Python 3.x

Flask

Flask-RESTful

Flask-SQLAlchemy

Flask-Migrate

SQLite (default database)

## Project Structure
.
├── app.py               # Flask application & API routes
├── models.py            # SQLAlchemy models
├── seed.py              # Seed script to populate database
├── superhero.db         # SQLite database (auto-generated)
├── migrations/          # Database migrations folder
└── README.md

## Setup

Clone the repo

git clone git@github.com:billotiende-droid/superheroes-f-stack.git
cd /se-python/superheroes-api$


## Create a virtual environment and install dependencies

pipenv install
pipenv shell
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt


## Initialize the database

flask db init
flask db migrate
flask db upgrade


## Seed the database

python seed.py


## Run the server

python app.py


The API will be available at http://localhost:5555.

## API Endpoints
Heroes

GET /heroes – List all heroes (id, name, super_name)

GET /heroes/<id> – Get a single hero with associated powers

Powers

GET /powers – List all powers (id, name, description)

GET /powers/<id> – Get a single power

PATCH /powers/<id> – Update a power’s description

Hero Powers

POST /hero_powers – Assign a power to a hero with a strength

## Example Request
POST /hero_powers
Content-Type: application/json

{
    "hero_id": 1,
    "power_id": 2,
    "strength": "Strong"
}

## Validation Rules

strength must be one of: "Strong", "Average", "Weak"

description of a power must be at least 20 characters

## Future Recommendations

Authentication & Authorization: Add user accounts and role-based access (e.g., admin vs. user).

CRUD for Heroes & Powers: Implement POST, PUT, DELETE for heroes and powers.

Filtering & Searching: Allow filtering heroes by power, strength, or name.

Pagination: For endpoints returning large lists, implement pagination.

Advanced Relationships: Support heroes having multiple powers and vice versa more flexibly.

Deployment: Dockerize the app and deploy to a cloud platform.

Testing: Add unit and integration tests for API endpoints and models.

Swagger/OpenAPI Documentation: Auto-generate API docs for easier integration.