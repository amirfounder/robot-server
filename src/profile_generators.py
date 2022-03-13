from gc import get_freeze_count
import json
from os import listdir
from os.path import isfile, join
from random import Random
import datetime
import string
import secrets

random = Random()


def get_first_names_male():
    return [x.removesuffix('\n') for x in open('data/first_names_male.txt', 'r').readlines()]


def get_first_names_female():
    return [x.removesuffix('\n') for x in open('data/first_names_female.txt', 'r').readlines()]


def get_last_names():
    return [x.removesuffix('\n') for x in open('data/last_names.txt', 'r').readlines()]


def generate_username(firstname: str, lastname: str):
    random_int = random.randint(10000, 99999)
    random_int = str(random_int)
    return '{}{}{}'.format(firstname, lastname, random_int).lower()


def generate_password(length: int = 12):
    chars = list(string.ascii_letters + '0123456789' + '!@#$%^&*()')
    return ''.join([secrets.choice(chars) for _ in range(length)])


def generate_birthday():
    start_date = datetime.date(1980, 1, 1)
    end_date = datetime.date(2001, 1, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    birthday = start_date + datetime.timedelta(days=random_number_of_days)
    return str(birthday)


def generate_bot():
    fnames_female = get_first_names_female()
    fnames_male = get_first_names_male()
    lnames = get_last_names()
    
    fname_index = random.randint(0, 999)
    lname_index = random.randint(0, 999)
    gender_index = random.randint(0, 1)

    lname = lnames[lname_index]
    gender = ('FEMALE', 'MALE')[gender_index == 0]
    fname = (fnames_male[fname_index], fnames_female[fname_index])[gender == 'FEMALE']

    return {
        'first_name': fname,
        'last_name': lname,
        'gender': gender,
        'username': generate_username(fname, lname),
        'birthday': generate_birthday(),
        'password': generate_password(),
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
    }

def generate_bots(count: int):
    return [generate_bot() for _ in range(count)]