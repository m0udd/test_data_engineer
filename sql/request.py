"""
Basic script to store some data in a local 
sqlite db and request it.
"""

import os
import sqlite3


if __name__ == "__main__":

    db_path = "./de_test.db"

    # remove database if exist
    if os.path.exists(db_path):
        os.remove(db_path)

    # connect to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # create TRANSACTION table
    # /!\ TRANSACTION is not a permitted name use in sqlite... replace it with TRANSAC
    con.execute("""
                CREATE TABLE IF NOT EXISTS TRANSAC 
                    (date DATE NOT NULL,
                    order_id INT NOT NULL,
                    client_id INT NOT NULL,
                    prop_id INT NOT NULL,
                    prod_price FLOAT NOT NULL, 
                    prod_qty INT NOT NULL);""")

    # insert data into TRANSACTION
    con.execute("""
                INSERT INTO TRANSAC (date, order_id, client_id, prop_id, prod_price, prod_qty)
                VALUES ('01-01-2020', 1234, 999, 490756, 50, 1),
                       ('01-01-2020', 1234, 999, 389728, 3.56, 4),
                       ('01-01-2020', 3456, 845, 490756, 50, 2),
                       ('01-01-2020', 3456, 845, 549380, 300, 1),
                       ('01-01-2020', 3456, 845, 293718, 10, 6);""")

    # create TRANSACTION table
    con.execute("""
                CREATE TABLE IF NOT EXISTS PRODUCT_NOMENCLATURE 
                    (product_id INT NOT NULL, 
                    product_type CHARACTER VARYING(6), 
                    product_name CHARACTER VARYING(15));
                """
                )

    # insert data into PRODUCT_NOMENCLATURE
    con.execute("""  
                INSERT INTO PRODUCT_NOMENCLATURE (product_id, product_type, product_name)
                VALUES  (490756, 'MEUBLE', 'Chaise'),
                        (389728, 'DECO', 'Boule de Noël'),
                        (549380, 'MEUBLE', 'Canapé'),
                        (293718, 'DECO', 'Mug'); 
                """
                )

    con.commit()

    cursor = con.execute(
        """
                        SELECT 
                            date,
                            SUM(prod_price * prod_qty) AS ventes
                        FROM TRANSAC
                        WHERE date BETWEEN '01-01-2020' AND '12-31-2020' 
                        GROUP BY date
                        ORDER BY date; """)

    print("""
    =================================================
    Le chiffre d’affaires (le montant total des ventes),
    jour par jour, du 1er janvier 2020 au 31 décembre 2020 :
    =================================================
    """)

    for row in cursor:
        print("date: ", row[0], ' ventes: ', row[1])

    print('')

    cursor = con.execute("""
                            SELECT 
                                t.client_id,
                                SUM(CASE WHEN product_type = 'MEUBLE' 
                                    THEN prod_price * prod_qty
                                    ELSE 0
                                    END
                                ) AS ventes_meuble,
                                SUM(CASE WHEN product_type = 'DECO' 
                                    THEN prod_price * prod_qty
                                    ELSE 0
                                    END
                                ) AS ventes_deco  
                            FROM TRANSAC AS t
                            INNER JOIN PRODUCT_NOMENCLATURE AS p
                                ON t.prop_id = p.product_id
                            WHERE date BETWEEN '01-01-2020' AND '12-31-2020'   
                            GROUP BY t.client_id;
                            """)

    print("""
    =================================================
    Les ventes meuble et déco par clients,
    du 1er janvier 2020 au 31 décembre 2020 :
    =================================================
    """)
    for row in cursor:
        print("client_id: ", row[0], ' ventes_meuble: ',
              row[1], ' ventes_deco: ', row[2])
    print('')

    con.close()
