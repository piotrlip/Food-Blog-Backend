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
                            meal_id integer PRIMARY KEY UNIQUE,
                            meal_name TEXT  NOT NULL UNIQUE
                            );"""
sql_create_table_ingredients = """ CREATE TABLE IF NOT EXISTS ingredients (
                            ingredient_id integer PRIMARY KEY,
                            ingredient_name TEXT NOT NULL UNIQUE
                            );"""
sql_create_table_measures = """ CREATE TABLE IF NOT EXISTS measures (
                            measure_id integer PRIMARY KEY,
                            measure_name TEXT UNIQUE
                            );"""
sql_create_table_recipes = """ CREATE TABLE IF NOT EXISTS recipes (
                            recipe_id integer PRIMARY KEY,
                            recipe_name TEXT NOT NULL,
                            recipe_description TEXT
                            );"""
sql_create_table_serve = """ CREATE TABLE IF NOT EXISTS serve (
                            serve_id integer PRIMARY KEY,
                            recipe_id integer NOT NULL,
                            meal_id integer NOT NULL,
                            FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
                            FOREIGN KEY(meal_id) REFERENCES meals(meal_id)
                            );"""
sql_create_table_quantity = """ CREATE TABLE IF NOT EXISTS quantity (
                            quantity_id integer PRIMARY KEY,
                            measure_id integer NOT NULL,
                            ingredient_id integer NOT NULL,
                            quantity integer NOT NULL,
                            recipe_id integer NOT NULL,
                            FOREIGN KEY(measure_id) REFERENCES measures(measure_id),
                            FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id),
                            FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
                            );"""

# with conn:
create_table(conn, sql_create_table_meals)
create_table(conn, sql_create_table_ingredients)
create_table(conn, sql_create_table_measures)
create_table(conn, sql_create_table_recipes)
create_table(conn, sql_create_table_serve)
create_table(conn, sql_create_table_quantity)
cur = conn.cursor()
cur.execute('PRAGMA foreign_keys = ON')

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

        meals = cur.execute(f'SELECT * FROM meals')
        all_meals = meals.fetchall()

        print(f"{all_meals[0][0]}) {all_meals[0][1]} "
              f"{all_meals[1][0]}) {all_meals[1][1]} "
              f"{all_meals[2][0]}) {all_meals[2][1]} "
              f"{all_meals[3][0]}) {all_meals[3][1]}")
        dish = input('Enter proposed meals separated by a space:')
        user_choice = dish.split(' ')

        for element in user_choice:
            recipe_id = cur.execute(f"""SELECT recipe_id FROM recipes WHERE recipe_name = '{name}'""")
            sql1 = f''' INSERT INTO serve(meal_id, recipe_id)
                          VALUES('{element}') '''
            cur = conn.cursor()
            cur.execute(sql1)
            conn.commit()

        #while True:
            #measures = ["ml", "g", "l", "cup", "tbsp", "tsp", "dsp"]
            #quantity_ingredient = input()

        continue
    else:
        break

conn.close()
