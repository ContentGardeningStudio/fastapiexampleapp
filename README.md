# fastapiexampleapp

FastAPI example app to learn some of the best practices

## Overview

This is a demonstration of a FastAPI application using SQLAlchemy and SQLModel. The application allows users to share their projects and invite others to contribute.

## Key Features

- User registration and authentication
- User profiles with bio information
- Project creation and sharing

## Technical Choices

### Database

- SQLite in development
- PostgreSQL in production, using an instance on Supabase (https://supabase.com/database)

### User Interface

- Simple UX with Jinja2 for the initial version
- Later versions may explore using React for a more interactive interface

## Getting Started

Clone this repository & install base dependencies:

```shell
git clone https://github.com/ContentGardeningStudio/fastapiexampleapp.git
```

## Local development

1. Install dependencies:

```shell
pip install -r requirements.txt
```

2. Set up your environment:

   - Development Mode:

   - Use SQLite for the database
   - Set `DEVELOPMENT_MODE=True`

3. Run the application:

```shell
cd src
python database.py
# create database if not exists

uvicorn main:app --reload
#visit localhost:8080
```

## TODO

- Set up different configurations for SQLite in development.

Auth:

- Implement endpoints for profile creation.
- Create endpoints for user login and authentication.
- Allow users to view and edit their profiles.
- Write unit tests to ensure the functionality of endpoints and models.
- .....

Project:

- Add functionality for users to create and manage projects.
- Implement sharing features to invite others to contribute to projects.
- Write unit tests to ensure the functionality of endpoints and models.
- .....
