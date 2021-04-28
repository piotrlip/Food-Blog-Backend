import sqlite3
import argparse
import re
import sys


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
                          VALUES ('{element}') ; '''
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


def insert_quantity(quantity, measure, name, recipe_id):
    cur = conn.cursor()

    measures = cur.execute(f"""SELECT measure_id FROM measures WHERE measure_name = '{measure}'""").fetchall()
    ingredient = cur.execute(f"""SELECT ingredient_id FROM ingredients WHERE ingredient_name = {name} """).fetchall()

    sql1 = f"""INSERT INTO quantity(measure_id , ingredient_id , quantity , recipe_id )
                         VALUES('{measures[0][1]}', '{ingredient[0][1]}', '{quantity}', '{recipe_id}') """

    cur.execute(sql1)
    conn.commit()


def quantity_ingredient_3(quantity, measure, ingredient_name, recipe_name):
    measures_list = ["ml", "g", "l", "cup", "tbsp", "tsp", "dsp", ""]

    regexp = '(ml|g|l|cup|tbsp|tsp|dsp)'
    result = re.match(regexp, measure)

    if result is None:
        return 'The measure is not conclusive!'

    ingredient = ingredient_name
    if ingredient == 'blue':
        ingredient = 'blueberry'
    elif ingredient == 'black':
        ingredient = 'blackberry'

    sql_ingredient_name = cur.execute(f"""SELECT ingredient_name FROM ingredients """).fetchall()
    ingredient_list = tuple([sql_ingredient_name[i][0] for i in range(len(sql_ingredient_name))])
    regexp1 = str(ingredient_list).replace(',', '|').replace(' ', '').replace('\'', '')
    result = re.match(regexp1, ingredient)

    if result is None:
        return 'The ingredient is not conclusive!'

    # we have to get measure_id , ingredient_id, recipe_id
    # measure_id
    sql_measure_id = cur.execute(f"""SELECT measure_id FROM measures WHERE measure_name = '{measure}'""").fetchall()

    # ingredient_id
    sql_ingredient_id = cur.execute(
        f"""SELECT ingredient_id FROM ingredients WHERE ingredient_name = '{ingredient}' """).fetchall()

    # recipe_id
    sql_recipe_id = cur.execute(f"""SELECT recipe_id FROM recipes WHERE recipe_name = '{recipe_name}' """).fetchall()

    sql1 = f"""INSERT INTO quantity(measure_id , ingredient_id , quantity , recipe_id )
                     VALUES('{sql_measure_id[0][0]}', '{sql_ingredient_id[0][0]}', '{quantity}', '{sql_recipe_id[0][0]}') """

    cur.execute(sql1)
    conn.commit()

    return


def quantity_ingredient_2(quantity, ingredient_name, recipe_name):
    sql_ingredient_name = cur.execute(f"""SELECT ingredient_name FROM ingredients """).fetchall()
    ingredient_list = tuple([sql_ingredient_name[i][0] for i in range(len(sql_ingredient_name))])

    regexp = str(ingredient_list).replace(',', '|').replace(' ', '').replace('\'', '')
    result = re.match(regexp, ingredient_name)

    if result is None:
        return 'The ingredient is not conclusive!'
    sql_ingredient_id = cur.execute(
        f"""SELECT ingredient_id FROM ingredients WHERE ingredient_name = '{ingredient_name}' """).fetchall()
    sql_recipe_id = cur.execute(f"""SELECT recipe_id FROM recipes WHERE recipe_name = '{recipe_name}' """).fetchall()
    sql_measure_id = cur.execute(f"""SELECT measure_id FROM measures WHERE measure_name = ''""").fetchall()

    sql1 = f"""INSERT INTO quantity(measure_id , ingredient_id , quantity , recipe_id )
                     VALUES('{sql_measure_id[0][0]}', '{sql_ingredient_id[0][0]}', '{quantity}', '{sql_recipe_id[0][0]}') """

    cur.execute(sql1)
    conn.commit()


def print_meals_ing(ingredient, meals):

    sql = None
    if len(ingredient) == 1:
        first_query = f"""SELECT DISTINCT    A.recipe_name, E.meal_name		
              FROM recipes AS A
              JOIN quantity AS B
                  ON A.recipe_id = B.recipe_id
              JOIN ingredients AS C
                  ON C.ingredient_id = B.ingredient_id
              JOIN serve AS D
                  ON A.recipe_id = D.recipe_id
              JOIN meals AS E
                  ON D.meal_id = E.meal_id
			  WHERE  C.ingredient_name  = '{str(ingredient[0])}' AND E.meal_name  IN {str(meals).replace('[', '(').replace(']', ')')}"""

        sql = f"""{first_query}"""

    elif len(ingredient) == 2:
        first_query = f"""SELECT DISTINCT    A.recipe_name		
              FROM recipes AS A
              JOIN quantity AS B
                  ON A.recipe_id = B.recipe_id
              JOIN ingredients AS C
                  ON C.ingredient_id = B.ingredient_id
              JOIN serve AS D
                  ON A.recipe_id = D.recipe_id
              JOIN meals AS E
                  ON D.meal_id = E.meal_id
			  WHERE  C.ingredient_name  = '{str(ingredient[0])}' AND E.meal_name  IN {str(meals).replace('[', '(').replace(']', ')')}"""
        second_query = f"""
              INTERSECT
    
              SELECT DISTINCT    A.recipe_name	
              FROM recipes AS A
              JOIN quantity AS B
                  ON A.recipe_id = B.recipe_id
              JOIN ingredients AS C
                  ON C.ingredient_id = B.ingredient_id
              JOIN serve AS D
                  ON A.recipe_id = D.recipe_id
              JOIN meals AS E
                  ON D.meal_id = E.meal_id
			WHERE  C.ingredient_name  = '{str(ingredient[1])}' AND E.meal_name  IN {str(meals).replace('[', '(').replace(']', ')')}
            """

        sql = f"""{first_query} 
                    {second_query}"""

    answer = cur.execute(sql).fetchall()

    print_answer = ','.join([answer[i][0] for i in range(len(answer))]).replace('\'', '').replace(',', ', ')

    if len(answer) > 0:
        print(f'Recipes selected for you: {print_answer}')
        conn.close()
    else:
        print('There are no such recipes in the database.')
        conn.close()


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

existence = cur.execute(f'SELECT * FROM meals').fetchall()

if len(existence) == 0:
    insert_data_rows(conn, **data)

# sys.argv = [1,2,"--ingredients=cacao", "--meals=brunch,supper"]

if len(sys.argv) > 2:
    ingredient = sys.argv[2].replace('--ingredients=', '').split(',')
    meals = sys.argv[3].replace('--meals=', '').split(',')
    print_meals_ing(ingredient, meals)
    conn.close()

else:

    print('Pass the empty recipe name to exit')

    while True:

        name = input('Recipe name:')  # input('Recipe name:')    'Hot milk'

        if len(name) != 0:
            description = input('Recipe description:')  # input('Recipe description:')   'Boil milk'
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
            dish = input(
                'Enter proposed meals separated by a space:')  # input('Enter proposed meals separated by a space:')  '1 2 3'
            user_choice = dish.split(' ')

            for element in user_choice:
                recipe_id = cur.execute(f"""SELECT recipe_id FROM recipes WHERE recipe_name = '{name}'""")
                recipe_id_1 = recipe_id.fetchall()
                sql1 = f''' INSERT INTO serve(meal_id, recipe_id)
                              VALUES('{element}','{recipe_id_1[0][0]}') '''
                cur = conn.cursor()
                cur.execute(sql1)
                conn.commit()

            while True:

                quantity_ingredient = input(
                    'Input quantity of ingredient <press enter to stop>: ')  # input('Input quantity of ingredient <press enter to stop>: ')    '250 ml milk'
                quantity_ingredient_list = quantity_ingredient.split(' ')

                if len(quantity_ingredient_list) == 3:
                    q3 = quantity_ingredient_3(quantity_ingredient_list[0], quantity_ingredient_list[1],
                                               quantity_ingredient_list[2], name)

                    if q3 is None:
                        pass
                    else:
                        print(q3)
                    continue

                elif len(quantity_ingredient_list) == 2:
                    q2 = quantity_ingredient_2(quantity_ingredient_list[0], quantity_ingredient_list[1], name)
                    if q2 is None:
                        pass
                    else:
                        print(q2)
                    continue

                elif len(quantity_ingredient_list) == 1:
                    break

            continue

        elif len(name) == 0:
            break

    conn.close()
