import sys
from pathlib import Path

# Add the project's root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import random
from faker import Faker
from fastapi import Depends
from sqlmodel import Session

from src.database import engine
from src.auth.models import Profile
from src.projects.models import Project
from src.auth.service import (
    create_user,
)

fake = Faker()


def populate():
    with Session(engine) as session:
        users_list = []
        profiles_ids_list = []
        emails_list = set()  # Use a set to check for unique emails
        user_id = 0
        profile_id = 0

        # generate multiples users
        for _ in range(20):
            # generate unique id
            user_id = user_id + 1

            # generate unique email
            while True:
                email = fake.email()
                if email not in emails_list:
                    emails_list.add(email)
                    break

            # generate a new user
            users_list.append(
                {
                    "id": user_id,
                    "email": email,
                    "password": fake.password(),
                }
            )

        # generate multiples users profiles
        for user in users_list:
            # save new user in DB
            create_user(session, user["email"], user["password"])

            # create a profile for this user
            # Generate defult username from email
            username = user["email"].split("@")[0]

            # Create a new Profile instance
            profile_id = profile_id + 1
            new_profile = Profile(
                id=profile_id,
                user_id=user["id"],
                username=username,
                bio=fake.paragraph(nb_sentences=random.choice([3, 4, 5])),
            )

            # Add the new user to the database session and commit
            session.add(new_profile)
            session.commit()
            session.refresh(new_profile)

            profiles_ids_list.append(profile_id)

        # generate multiples projects based on previous profiles
        for _ in range(50):
            # pick a random user profile
            random_profile_id = random.choice(profiles_ids_list)

            # Create a new project for this user
            new_project = Project(
                profile_id=random_profile_id,
                title=fake.sentence(nb_words=10),
                description=fake.paragraph(
                    nb_sentences=random.choice([10, 12, 14, 16, 18, 20])
                ),
                url=fake.url(),
                stars=random.choice([1, 2, 3, 4, 5]),
            )

            # Add the new project to the database session and commit
            session.add(new_project)
            session.commit()
            session.refresh(new_project)


if __name__ == "__main__":
    # creates the table if this file is run independently, as a script
    populate()
