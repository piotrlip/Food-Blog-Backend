import sqlite3
import argparse


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn, create_table_sql):
    c = conn.cursor()
    c.execute(create_table_sql)
    conn.commit()


def insert_data_rows(conn, **kwargs):
    for key, value in kwargs.items():
        if key == 'meals':
            for element in value:
                sql = f''' INSERT INTO meals(meal_name)
                          VALUES ('{element}'); '''
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()

        if key == "ingredients":
            for element in value:
                sql = f''' INSERT INTO ingredients(ingredient_name)
                          VALUES('{element}') '''
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()

        if key == 'measures':
            for element in value:
                sql = f''' INSERT INTO measures(measure_name)
                          VALUES('{element}') '''
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()


# parser = argparse.ArgumentParser()
# parser.add_argument("--file", type=argparse.FileType("r"))

# database = parser.parse_args()


conn = create_connection('food_blog.db')

sql_create_table_meals = """ CREATE TABLE IF NOT EXISTS meals (
                            meal_id integer PRIMARY KEY,
                            meal_name text NOT NULL
                            );"""
sql_create_table_ingredients = """ CREATE TABLE IF NOT EXISTS ingredients (
                            ingredient_id integer PRIMARY KEY,
                            ingredient_name text NOT NULL 
                            );"""
sql_create_table_measures = """ CREATE TABLE IF NOT EXISTS measures (
                            measure_id integer PRIMARY KEY,
                            measure_name text 
                            );"""
sql_create_table_recipes = """ CREATE TABLE IF NOT EXISTS recipes (
                            recipe_id integer PRIMARY KEY,
                            recipe_name text NOT NULL,
                            recipe_description text
                            );"""
# with conn:
create_table(conn, sql_create_table_meals)
create_table(conn, sql_create_table_ingredients)
create_table(conn, sql_create_table_measures)
create_table(conn, sql_create_table_recipes)

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}


insert_data_rows(conn, **data)

print('Pass the empty recipe name to exit')

while True:

    name = input('Recipe name:')

    if len(name) != 0:
        description = input('Recipe description:')
        sql = f''' INSERT INTO recipes(recipe_name, recipe_description)
                          VALUES('{name}', '{description}') '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        continue
    else:
        break

conn.close()
