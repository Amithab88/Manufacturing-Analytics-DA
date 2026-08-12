# analytics/machines.py

import pandas as pd
from database.db_connection import get_connection

class MachineAnalytics:

    @staticmethod
    def machine_status(factory="All"):
        """
        Machine status distribution.

        If factory is 'All', returns machine status
        across all factories.

        Otherwise, returns machine status
        for the selected factory.
        """

        connection = get_connection()

        if factory == "All":

            query = """
            SELECT
                status,
                COUNT(*) AS total_machines
            FROM machines
            GROUP BY status
            ORDER BY total_machines DESC;
            """

            df = pd.read_sql(
                query,
                connection
            )

        else:

            query = """
            SELECT
                m.status,
                COUNT(*) AS total_machines
            FROM machines m
            JOIN factories f
                ON m.factory_id = f.factory_id
            WHERE REPLACE(
                f.factory_name,
                ' Manufacturing Plant',
                ''
            ) = %s
            GROUP BY m.status
            ORDER BY total_machines DESC;
            """

            df = pd.read_sql(
                query,
                connection,
                params=(factory,)
            )

        connection.close()

        return df


    @staticmethod
    def factory_machine_count():
        """
        Number of machines in each factory.
        """

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

        df = pd.read_sql(
            query,
            connection
        )

        connection.close()

        return df

