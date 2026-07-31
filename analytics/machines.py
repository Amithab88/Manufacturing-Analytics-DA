import pandas as pd
from database.db_connection import get_connection


class MachineAnalytics:

    @staticmethod
    def machine_status():
        connection = get_connection()

        query = """
        SELECT
            status,
            COUNT(*) AS total_machines
        FROM machines
        GROUP BY status;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df


    @staticmethod
    def factory_machine_count():
        connection = get_connection()

        query = """
        SELECT
            f.factory_name,
            COUNT(m.machine_id) AS total_machines
        FROM factories f
        JOIN machines m
            ON f.factory_id = m.factory_id
        GROUP BY f.factory_name
        ORDER BY total_machines DESC;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df