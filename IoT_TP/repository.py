import psycopg2


class MovementDatabase:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def _connect(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            return conn, cursor
        except Exception as error:
            print(f"Error connecting to the database: {error}")
            return None, None


    def insert_person(self, id, age, weight, height):
        conn, cursor = self._connect()
        if not conn:
            return

        try:
            insert_query = """
            INSERT INTO Person (person_id, age, weight, height)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (id, age, weight, height))
            conn.commit()
            print("Row inserted successfully.")
        except Exception as error:
            print(f"Error inserting row: {error}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


    def retrieve_person(self, id):
        conn, cursor = self._connect()
        if not conn:
            return []

        try:
            select_query = "SELECT * FROM Person WHERE person_id = %s"
            cursor.execute(select_query, (id,))
            row = cursor.fetchone()
            return row
        except Exception as error:
            print(f"Error retrieving row: {error}")
            return []
        finally:
            cursor.close()
            conn.close()

    def insert_movement(self, id, acceleration_x, acceleration_y, acceleration_z,
                   gyro_x, gyro_y, gyro_z, movement_data, movement_time, activity):

        conn, cursor = self._connect()
        if not conn:
            return

        try:
            insert_query = """
            INSERT INTO Movement (user_id, activity_number, acceleration_x, acceleration_y, acceleration_z, 
                                  gyro_x, gyro_y, gyro_z, movement_data, movement_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)
            """
            cursor.execute(insert_query,
                           (id, activity, acceleration_x, acceleration_y, acceleration_z,
                            gyro_x, gyro_y, gyro_z, movement_data, movement_time))
            conn.commit()
            print("Row inserted successfully.")
        except Exception as error:
            print(f"Error inserting row: {error}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def retrieve_movement(self, id):
        conn, cursor = self._connect()
        if not conn:
            return []

        try:
            select_query = "SELECT * FROM Movement WHERE user_id = %s"
            cursor.execute(select_query, (id,))
            rows = cursor.fetchall()
            return rows
        except Exception as error:
            print(f"Error retrieving rows: {error}")
            return []
        finally:
            cursor.close()
            conn.close()