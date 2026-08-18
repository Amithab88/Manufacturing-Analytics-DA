# analytics/trends.py

import pandas as pd
from database.db_connection import get_connection

class TrendAnalytics:

    @staticmethod
    def daily_production(factory="All"):
        connection = get_connection()

        if factory == "All":

            query = """
            SELECT
                production_date,
                SUM(units_produced) AS total_units
            FROM production_batches
            GROUP BY production_date
            ORDER BY production_date;
            """

            df = pd.read_sql(
                query,
                connection
            )

        else:

            query = """
            SELECT
                pb.production_date,
                SUM(pb.units_produced) AS total_units
            FROM production_batches pb
            JOIN machines m
                ON pb.machine_id = m.machine_id
            JOIN factories f
                ON m.factory_id = f.factory_id
            WHERE REPLACE(
                f.factory_name,
                ' Manufacturing Plant',
                ''
            ) = %s
            GROUP BY pb.production_date
            ORDER BY pb.production_date;
            """

            df = pd.read_sql(
                query,
                connection,
                params=(factory,)
            )

        connection.close()

        return df


    @staticmethod
    def monthly_production(
        factory="All",
        shift="All",
        statuses=None
    ):
        """
        Monthly production trend.

        Filters:
        - Factory
        - Shift
        - Machine Status
        """

        connection = get_connection()

        query = """
        SELECT
            DATE_FORMAT(
                pb.production_date,
                '%Y-%m'
            ) AS month,

            SUM(pb.units_produced) AS total_units

        FROM production_batches pb

        JOIN machines m
            ON pb.machine_id = m.machine_id

        JOIN factories f
            ON m.factory_id = f.factory_id

        JOIN shifts s
            ON pb.shift_id = s.shift_id
        """

        conditions = []
        params = []

        # Factory filter
        if factory != "All":
            conditions.append(
                """
                REPLACE(
                    f.factory_name,
                    ' Manufacturing Plant',
                    ''
                ) = %s
                """
            )
            params.append(factory)

        # Shift filter
        if shift != "All":
            conditions.append(
                "s.shift_name = %s"
            )
            params.append(shift)

        # Machine status filter
        if statuses:
            placeholders = ", ".join(
                ["%s"] * len(statuses)
            )

            conditions.append(
                f"m.status IN ({placeholders})"
            )

            params.extend(statuses)

        if conditions:
            query += "\nWHERE "
            query += " AND ".join(conditions)

        query += """
        GROUP BY month
        ORDER BY month;
        """

        df = pd.read_sql(
            query,
            connection,
            params=params
        )

        connection.close()

        return df


    @staticmethod
    def daily_defect_rate(factory="All"):
        connection = get_connection()

        if factory == "All":

            query = """
            SELECT
                production_date,
                ROUND(
                    (SUM(defective_units) * 100.0) /
                    NULLIF(SUM(units_produced), 0),
                    2
                ) AS defect_rate
            FROM production_batches
            GROUP BY production_date
            ORDER BY production_date;
            """

            df = pd.read_sql(
                query,
                connection
            )

        else:

            query = """
            SELECT
                pb.production_date,
                ROUND(
                    (SUM(pb.defective_units) * 100.0) /
                    NULLIF(SUM(pb.units_produced), 0),
                    2
                ) AS defect_rate
            FROM production_batches pb
            JOIN machines m
                ON pb.machine_id = m.machine_id
            JOIN factories f
                ON m.factory_id = f.factory_id
            WHERE REPLACE(
                f.factory_name,
                ' Manufacturing Plant',
                ''
            ) = %s
            GROUP BY pb.production_date
            ORDER BY pb.production_date;
            """

            df = pd.read_sql(
                query,
                connection,
                params=(factory,)
            )

        connection.close()

        return df


    @staticmethod
    def monthly_defect_rate(factory="All"):
        connection = get_connection()

        if factory == "All":

            query = """
            SELECT
                DATE_FORMAT(
                    production_date,
                    '%Y-%m'
                ) AS month,
                ROUND(
                    (SUM(defective_units) * 100.0) /
                    NULLIF(SUM(units_produced), 0),
                    2
                ) AS defect_rate
            FROM production_batches
            GROUP BY month
            ORDER BY month;
            """

            df = pd.read_sql(
                query,
                connection
            )

        else:

            query = """
            SELECT
                DATE_FORMAT(
                    pb.production_date,
                    '%Y-%m'
                ) AS month,
                ROUND(
                    (SUM(pb.defective_units) * 100.0) /
                    NULLIF(SUM(pb.units_produced), 0),
                    2
                ) AS defect_rate
            FROM production_batches pb
            JOIN machines m
                ON pb.machine_id = m.machine_id
            JOIN factories f
                ON m.factory_id = f.factory_id
            WHERE REPLACE(
                f.factory_name,
                ' Manufacturing Plant',
                ''
            ) = %s
            GROUP BY month
            ORDER BY month;
            """

            df = pd.read_sql(
                query,
                connection,
                params=(factory,)
            )

        connection.close()

        return df


    @staticmethod
    def production_hours_trend(factory="All"):
        connection = get_connection()

        if factory == "All":

            query = """
            SELECT
                DATE_FORMAT(
                    production_date,
                    '%Y-%m'
                ) AS month,
                ROUND(
                    AVG(production_hours),
                    2
                ) AS avg_production_hours
            FROM production_batches
            GROUP BY month
            ORDER BY month;
            """

            df = pd.read_sql(
                query,
                connection
            )

        else:

            query = """
            SELECT
                DATE_FORMAT(
                    pb.production_date,
                    '%Y-%m'
                ) AS month,
                ROUND(
                    AVG(pb.production_hours),
                    2
                ) AS avg_production_hours
            FROM production_batches pb
            JOIN machines m
                ON pb.machine_id = m.machine_id
            JOIN factories f
                ON m.factory_id = f.factory_id
            WHERE REPLACE(
                f.factory_name,
                ' Manufacturing Plant',
                ''
            ) = %s
            GROUP BY month
            ORDER BY month;
            """

            df = pd.read_sql(
                query,
                connection,
                params=(factory,)
            )

        connection.close()

        return df


    @staticmethod
    def monthly_defects(
        factory="All",
        shift="All",
        statuses=None
    ):
        """
        Monthly defective units trend.

        Filters:
        - Factory
        - Shift
        - Machine Status
        """

        connection = get_connection()

        query = """
        SELECT
            DATE_FORMAT(
                pb.production_date,
                '%Y-%m'
            ) AS month,

            SUM(pb.defective_units) AS total_defects

        FROM production_batches pb

        JOIN machines m
            ON pb.machine_id = m.machine_id

        JOIN factories f
            ON m.factory_id = f.factory_id

        JOIN shifts s
            ON pb.shift_id = s.shift_id
        """

        conditions = []
        params = []

        # Factory filter
        if factory != "All":
            conditions.append(
                """
                REPLACE(
                    f.factory_name,
                    ' Manufacturing Plant',
                    ''
                ) = %s
                """
            )
            params.append(factory)

        # Shift filter
        if shift != "All":
            conditions.append(
                "s.shift_name = %s"
            )
            params.append(shift)

        # Machine status filter
        if statuses:
            placeholders = ", ".join(
                ["%s"] * len(statuses)
            )

            conditions.append(
                f"m.status IN ({placeholders})"
            )

            params.extend(statuses)

        if conditions:
            query += "\nWHERE "
            query += " AND ".join(conditions)

        query += """
        GROUP BY month
        ORDER BY month;
        """

        df = pd.read_sql(
            query,
            connection,
            params=params
        )

        connection.close()

        return df