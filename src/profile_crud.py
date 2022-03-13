from datetime import datetime
import psycopg2
conn = psycopg2.connect('dbname=robot user=postgres password=root')
cur = conn.cursor()


def execute(query: str):
    cur.execute(query)
    try:
        result = cur.fetchall()
    except:
        result = None
    conn.commit()
    return result


def create_profiles_table():
    execute('''
create table if not exists profiles (
    id serial PRIMARY KEY,
    first_name varchar,
    last_name varchar,
    gender varchar,
    birthday timestamptz,
    username varchar,
    password varchar,
    created_at timestamptz,
    updated_at timestamptz,
    has_instagram_account boolean,
    has_google_account boolean,
    last_instagram_login timestamptz,
    last_google_login timestamptz
    )
''')


def add_column(column_name_datatypes: list[tuple[str, str]]):
    add_columns_statement = ', '.join(
        [' '.join(column_name_datatype) for column_name_datatype in column_name_datatypes])
    execute('''
alter table robot.public.profiles
add {};
'''.format(add_columns_statement))


def insert_profile(profile):
    return insert_profiles([profile])


def insert_profiles(profiles: list[dict]):
    keys = list(profiles[0].keys())
    column_statement = ', '.join(keys)
    values_statement = ', '.join(['({})'.format(', '.join(
        ['\'{}\''.format(profile.get(key)) for key in keys])) for profile in profiles])
    return execute('''insert into robot.public.profiles ({}) values {}'''.format(
        column_statement, values_statement))


def update_profile(profile: dict):
    if not profile.get('id'):
        print('cannot update profile where id is not specified ')
        return
    set_statement = ', '.join(['{}={}'.format(key, f'\'{value}\'' if value is not None else 'null')
                              for key, value in profile.items()])
    execute('''update robot.public.profiles set {} where id={} '''.format(
        set_statement, profile.get('id')))


def select_all_columns():
    return [x[3] for x in execute('select * from information_schema.columns where table_schema = \'public\' and table_name = \'profiles\'')]


def select_all_profiles():
    columns = select_all_columns()
    profiles = [dict(zip(columns, record)) for record in execute('select * from robot.public.profiles')]
    for profile in profiles:
        for key, value in profile.items():
            if isinstance(value, datetime):
                profile[key] = value.isoformat()
    return profiles


def select_profile_by_id(id: int):
    return next(iter([profile for profile in select_all_profiles() if profile.get('id') == id]))
