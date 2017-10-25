"""Migrations script to handle changes in data models."""

from app import db, app
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from bucketlist.models import User, Bucketlist, Item # noqa

# Manager instance
manager = Manager(app)

# Set up migrate commands
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    """Create all tables."""
    db.create_all()
    print('Initialised the database')


@manager.command
def dropdb():
    """Clear all the data in the tables."""
    if prompt_bool("Are you sure you want to loose all your data?"):
        db.drop_all()
        print("Dropped the database")


if __name__ == "__main__":
    manager.run()
