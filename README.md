# fastapiexampleapp

FastAPI example app to showcase some of the best practices.

## Overview

This is a demonstration of a FastAPI application using SQLAlchemy and SQLModel. The application allows users to share their projects and invite others to contribute to those projects.

## Key Features

- User registration and authentication
- User profiles (name, email, bio text, etc)
- Project creation and sharing

## Technical Choices

### Database

- SQLite in development
- PostgreSQL in production, using an instance on Supabase (https://supabase.com/database)

### User Interface

- Simple UX with Jinja2 and Htmx for the initial version
- Later versions may explore using React for a more interactive interface

## Getting Started

You need a Python 3.10 (?) virtual environment.

Clone this repository & install base dependencies:

   ```shell
   git clone https://github.com/ContentGardeningStudio/fastapiexampleapp.git
   ```

## Local development

Ensure that your virtual environment is activated.

1. Install dependencies:

   ```shell
   pip install -r requirements.txt
   ```

2. Set up your environment:

   - Use SQLite for the database

   ```shell
   cp .env.example .env
   ```

3. Create database with Alembic

   ```shell
   # will create ./development.db
   alembic upgrade head
   ```

4. Run the application:

   ```shell
   uvicorn src.main:app --reload
   #visit localhost:8080
   ```

### Populating the Database

For testing purposes, you can populate the database with initial data. Run the following command in your virtual environment:

   ```shell
   python src/populate.py
   ```

### Tests

Tests are located in the `tests` directory.

Run the tests using `pytest`:

   ```shell
   pytest
   ```

## TODO

Project:

   - Add functionality for users to create and manage projects.
   - Implement sharing features to invite others to contribute to projects.
   - Write unit tests to ensure the functionality of endpoints and models.
   - .....
