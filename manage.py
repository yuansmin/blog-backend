# -*- coding: utf-8 -*-
"""
__author__ = 'fancy'
__mtime__ = '2018/1/31'
"""
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app, db


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_superuser():
    'create a superuser from cmd'   # help text

    import getpass

    email = raw_input('Email: ')
    for i in range(3):
        password = getpass.getpass('Password: ')
        password_1 = getpass.getpass('Retype Password: ')
        if password == password_1:
            break
        print 'Sorry, passwords do not match.'
    from api.user.models import User
    user = User(email=email, password=password)
    user.active = True
    user.is_admin = True
    db.session.add(user)
    db.session.commit()
    print 'Create superuser success.\n'


if __name__ == '__main__':
    manager.run()
