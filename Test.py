import pytest
import sqlite3
def test_insert(db_connection, create_table):
    cursor = db_connection.cursor()
    cursor.execute('''INSERT INTO test_table (name) VALUES ('Alex');''')
    db_connection.commit()

    cursor.execute('''SELECT * FROM test_table;''')
    result = cursor.fetchall()

    assert len(result) == 1
    assert result[0][1] == 'Alex'



def test_update(db_connection, create_table):
    cursor = db_connection.cursor()
    cursor.execute('''INSERT INTO test_table (name) VALUES ('Bob');''')
    db_connection.commit()

    cursor.execute('''UPDATE test_table SET name = 'Migran' WHERE name = 'Bob';''')
    db_connection.commit()

    cursor.execute('''SELECT * FROM test_table WHERE name = 'Migran';''')
    result = cursor.fetchall()

    assert len(result) == 1
    assert result[0][1] == 'Migran'


def test_delete(db_connection, create_table):
    cursor = db_connection.cursor()
    cursor.execute('''INSERT INTO test_table (name) VALUES ('Dave');''')
    db_connection.commit()

    cursor.execute('''DELETE FROM test_table WHERE name = 'Dave';''')
    db_connection.commit()

    cursor.execute('''SELECT * FROM test_table WHERE name = 'Dave';''')
    result = cursor.fetchall()

    assert len(result) == 0


def test_select(db_connection, create_table):
    cursor = db_connection.cursor()
    cursor.execute('''INSERT INTO test_table (name) VALUES ('Grigoriy');''')
    db_connection.commit()

    cursor.execute('''SELECT * FROM test_table WHERE name = 'Grigoriy';''')
    result = cursor.fetchall()

    assert len(result) == 1
    assert result[0][1] == 'Grigoriy'

def test_dogs_limit(db_connection, create_table):
    cursor = db_connection.cursor()


    for i in range(5):
        cursor.execute(f"INSERT INTO dogs (name, breed) VALUES ('Dog {i}', 'Breed {i}');")
    db_connection.commit()


    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO dogs (name, breed) VALUES ('Dog 6', 'Breed 6');")
        db_connection.commit()


def test_dogs_sorted_by_name(db_connection, create_table):
    cursor = db_connection.cursor()


    cursor.execute("INSERT INTO dogs (name, breed) VALUES ('Bob', 'Breed1');")
    cursor.execute("INSERT INTO dogs (name, breed) VALUES ('Alice', 'Breed2');")
    cursor.execute("INSERT INTO dogs (name, breed) VALUES ('Charlie', 'Breed3');")
    db_connection.commit()


    cursor.execute("SELECT name FROM dogs ORDER BY name;")
    result = cursor.fetchall()
    expected_result = [('Alice',), ('Bob',), ('Charlie',)]
    assert result == expected_result


def test_buyers_preferred_breeds_limit(db_connection, create_table):
    cursor = db_connection.cursor()


    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO buyers (name, preferred_breeds) VALUES ('Buyer1', 'Breed1, Breed2, Breed3, Breed4');")
        db_connection.commit()

    cursor.execute("INSERT INTO buyers (name, preferred_breeds) VALUES ('Buyer2', 'Breed1, Breed2, Breed3');")
    db_connection.commit()


    cursor.execute("SELECT * FROM buyers;")
    result = cursor.fetchall()
    assert len(result) == 1


def test_buyer_selects_one_dog(populate_nursery_with_dogs, db_connection):
    cursor = db_connection.cursor()


    cursor.execute("INSERT INTO buyers (name, preferred_breeds) VALUES ('Buyer1', 'Breed1');")
    db_connection.commit()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO buyers (name, preferred_breeds) VALUES ('Buyer1', 'Breed2');")
        db_connection.commit()


def test_buyer_takes_dog_from_nursery(populate_nursery_with_dogs, db_connection):
    cursor = db_connection.cursor()


    cursor.execute("INSERT INTO buyers (name, preferred_breeds, dog_id, nursery_id) VALUES ('Buyer2', 'Breed3', 1, 1);")
    db_connection.commit()


    cursor.execute("SELECT * FROM dogs;")
    result = cursor.fetchall()
    assert len(result) == 2


    cursor.execute("SELECT * FROM buyers WHERE name='Buyer2';")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][3] == 1  #
    assert result[0][4] == 1