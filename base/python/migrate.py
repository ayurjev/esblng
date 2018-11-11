import os
import mysql.connector
from time import sleep


def execute(connect_config, query, dbname=False):
    cnx = mysql.connector.connect(**connect_config)
    cursor = cnx.cursor()
    if dbname:
        cursor.execute("USE %s;" % dbname)
    list(cursor.execute(query, multi=True))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def fetchall(connect_config, query):
    cnx = mysql.connector.connect(**connect_config)
    cursor = cnx.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return rows


def insert(connect_config, query):
    cnx = mysql.connector.connect(**connect_config)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def migrate(**kwargs):

    if not os.environ.get("MYSQL_HOST") or not os.environ.get("MYSQL_USER"):
        exit()

    if not os.path.isdir("migrations"):
        exit()

    target_config = {
        'host': os.environ.get("MYSQL_HOST"),
        'port': os.environ.get("MYSQL_PORT"),
        'user': os.environ.get("MYSQL_USER"),
        'password': os.environ.get("MYSQL_PASS"),
        'dbname': os.environ.get("MYSQL_DBNAME")
    }

    connect_config = {
        'host': os.environ.get("MYSQL_HOST"),
        'port': os.environ.get("MYSQL_PORT"),
        'user': "root",
        'password': ""
    }

    if "quiet" in kwargs:
        pprint = lambda x: None
    else:
        pprint = print


    if os.environ.get("DEPLOY_MODE") != "PROD":
        attempts = 0
        while attempts < 20:
            attempts += 1
            try:
                connection = mysql.connector.connect(**connect_config)
                connection.close()
            except mysql.connector.errors.InterfaceError as err:
                print(err)
                sleep(1)

    dbname = target_config["dbname"]
    execute(connect_config, f"CREATE DATABASE IF NOT EXISTS `{dbname}`;")
    execute(
        connect_config,
        f"""USE {dbname};
        CREATE TABLE IF NOT EXISTS {dbname}.`migrations`
        (
           `PatchName` varchar(128) NOT NULL,
           PRIMARY KEY (`PatchName`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    )

    if os.environ.get("DEPLOY_MODE") != "PROD":
        user = target_config.get("user")
        password = target_config.get("password")
        execute(
            connect_config,
            f"GRANT ALL PRIVILEGES ON *.* TO '{user}'@'%' IDENTIFIED BY '{password}';"
        )

    applied_patches = fetchall(connect_config, f"""SELECT PatchName FROM {dbname}.`migrations`""")
    applied_patches = [r[0] for r in applied_patches]

    list_files = os.listdir("migrations")
    list_files.sort()

    for patch_name in list_files:

        if patch_name == "latest.sql":
            continue

        pprint(f"Applying '{patch_name}'...")

        if patch_name not in applied_patches:
            with open("migrations/%s" % patch_name) as f:
                execute(connect_config, "".join(f.readlines()), dbname)
                insert(connect_config, f"""INSERT INTO {dbname}.`migrations` VALUES ('{patch_name}');""")

            pprint(f"'{patch_name}' applied successfully...")
        else:
            pprint(f"'{patch_name}' skipped...")

    pprint("Done")



if __name__ == "__main__":
    migrate()
