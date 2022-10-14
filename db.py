import psycopg2
import psycopg2.extras
import psycopg2.extensions

class Database():
    def query(sql):
        conn = None
        cur = None
        try:
            print('Connecting to postgreSQL database ...')
            # conn = psycopg2.connect(
            #     host="localhost", dbname="postgres", user="postgres", password='', port=5432)
            conn = psycopg2.connect(
                host="ec2-54-75-184-144.eu-west-1.compute.amazonaws.com", dbname="d93j7108i25c4r", user="uyyeuxzzemwmns", password='ec771a13fbb3aab018ad883ab54a8ac1b3a27dda5d1b6511bfa77b6a1d189f48', port=5432)

            cur = conn.cursor()
            # conn.autocommit = True
            cur.execute(sql)

            # create_table = '''CREATE TABLE IF NOT EXISTS "FaceRecog".users (
	        # id int4 PRIMARY KEY,
	        # first_name text NOT NULL,
	        # last_name text NOT NULL,
	        # nickname text NOT NULL,
	        # "password" text NOT NULL,
	        # images_count int4 NULL
            # );'''
            # cur.execute(create_table)
            conn.commit();
            results = cur.fetchall()
            return results
        except Exception as err:
            print(err)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()