# analytics/machines.py

import pandas as pd
from database.db_connection import get_connection

class MachineAnalytics:

    @staticmethod
    def machine_status(factory="All", statuses=None):
        """
        Machine status distribution.

        Supports filtering by:
        - Factory
        - One or more machine statuses

        If factory is 'All', returns machines across all factories.

        If statuses is None or empty, all machine statuses are included.
        """

        connection = get_connection()

        query = """
        SELECT
            m.status,
            COUNT(m.machine_id) AS total_machines
        FROM machines m
        """

        params = []
        conditions = []

        # -------------------------------------------------
        # FACTORY FILTER
        # -------------------------------------------------

        if factory != "All":

            query += """
            JOIN factories f
                ON m.factory_id = f.factory_id
            """

            conditions.append("""
            REPLACE(
                f.factory_name,
                ' Manufacturing Plant',
                ''
            ) = %s
            """)

            params.append(factory)

        # -------------------------------------------------
        # MACHINE STATUS FILTER
        # -------------------------------------------------

        if statuses:

            placeholders = ", ".join(
                ["%s"] * len(statuses)
            )

            conditions.append(
                f"m.status IN ({placeholders})"
            )

            params.extend(statuses)

        # -------------------------------------------------
        # WHERE CLAUSE
        # -------------------------------------------------

        if conditions:

            query += " WHERE "

            query += " AND ".join(
                conditions
            )

        # -------------------------------------------------
        # GROUPING
        # -------------------------------------------------

        query += """
        GROUP BY
            m.status
        ORDER BY
            total_machines DESC;
        """

        df = pd.read_sql(
            query,
            connection,
            params=params
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

