####################### this test case needs correction ###########################
############################## PYTEST APPROACH ####################################
##########################also unittest in the bottom##############################

import os
import pytest
import django

from django.core.management import call_command
from django.db import connection
from django.contrib.auth import get_user_model


# Ensure that Django is setup correctly before running tests
os.environ['DJANGO_SETTINGS_MODULE'] = 'bms.settings'
django.setup()

@pytest.fixture(scope='session', autouse=True)
def setup_django_environment():
    # Setup Phase: Apply migrations and create the test table
    call_command('migrate', verbosity=0, interactive=False)

    with connection.cursor() as cursor:
        cursor.execute(
            ''
        #     '''
        #     CREATE TABLE IF NOT EXISTS users_users (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         password VARCHAR(255) NOT NULL,
        #         last_login DATETIME,
        #         username VARCHAR(50) UNIQUE NOT NULL,
        #         email VARCHAR(255),
        #         is_owner BOOLEAN NOT NULL DEFAULT 0,
        #         is_active BOOLEAN NOT NULL DEFAULT 1,
        #         is_employee BOOLEAN NOT NULL DEFAULT 1
        #     )
        # '''
        )
    connection.commit()

    yield  # Yield control back to the test

    # # Teardown Phase: Drop the table after tests
    with connection.cursor() as cursor:
        cursor.execute(
            ''
            # 'DROP TABLE IF EXISTS users_users'
            )
    connection.commit()

@pytest.fixture(autouse=True)
def flush_database():
    # Ensure the test database is flushed before each test
    call_command('flush', verbosity=0, interactive=False)

def test_create_superuser():
    User = get_user_model()
    user = User.objects.create_superuser(
        username='username01',
        email='username@email.com',
        password='12345678',
        is_owner=True,
        owner_passkey='1300'
    )
    assert user.username == 'username01'
    assert user.email == 'username@email.com'
    assert user.check_password('12345678')
    assert user.is_owner

def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(
        username='normaluser01',
        email='normal@user.com',
        password='foo'
    )
    assert user.username == 'normaluser01'
    assert user.email == 'normal@user.com'
    assert user.is_active
    assert user.is_employee
    assert not user.is_owner
    with pytest.raises(TypeError):
        User.objects.create_user()
    with pytest.raises(TypeError):
        User.objects.create_user(email="")
    with pytest.raises(ValueError):
        User.objects.create_user(username="", email="", password="foo")



###################################################################################
############################## UNITTEST APPROACH #################################
###################################################################################


"""
import os
import unittest
from django.conf import settings
from django.db import connection, transaction
from django.contrib.auth import get_user_model

class UserModelTests(unittest.TestCase):

    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'bms.settings'
        settings.DEBUG = False
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password VARCHAR(255) NOT NULL,
                    last_login DATETIME,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(255),
                    is_owner BOOLEAN NOT NULL DEFAULT 0,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    is_employee BOOLEAN NOT NULL DEFAULT 1
                )
            ''')
        transaction.commit()


    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('''
                    DELETE FROM users_users WHERE username = "username01" and username = "normaluser01";
                ''')
        transaction.commit()
   
        
    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='username01',
            email='username@email.com',
            password='12345678',
            is_owner=True,
            owner_passkey='1300'
        )
        self.assertEqual(user.username, 'username01')
        self.assertEqual(user.email, 'username@email.com')
        self.assertTrue(user.check_password('12345678'))
        self.assertTrue(user.is_owner)

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='normaluser01',
            email='normal@user.com',
            password='foo'
        )
        self.assertEqual(user.username, 'normaluser01')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_employee)
        self.assertFalse(user.is_owner)
        try:
            self.assertIsNone(user.username) #checks if username is empty
        except:
            pass
        with self.assertRaises(TypeError): #checks if test fails if no args passed
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username= "", email="", password="foo") # checks invalid values

if __name__ == '__main__':
    unittest.main()
"""
