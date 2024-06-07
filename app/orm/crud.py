from sqlalchemy.orm import Session

from . import models


def create_users(db: Session) -> None:
    db_user1 = models.User(
        first_name="Jordan", last_name="Peterson", email="jordan.peterson@gmail.com"
    )
    db.add(db_user1)
    db_user2 = models.User(
        first_name="Michael", last_name="Jordan", email="michael.jordan@gmail.com"
    )
    db.add(db_user2)

    db.commit()

    print("Users successfully created!")
