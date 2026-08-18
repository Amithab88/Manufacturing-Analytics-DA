# analytics/production.py

import pandas as pd
from database.db_connection import get_connection

class ProductionAnalytics:


    @staticmethod
    def get_all_batches():
        connection = get_connection()

        query = """
        SELECT *
        FROM production_batches;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df


    @staticmethod
    def get_summary(factory="All", shift="All", statuses=None):
        """
        Production summary with optional filters.

        Filters:
        - factory: All or a specific factory
        - shift: All, Morning, Afternoon, or Night
        - statuses: None/empty or a list of machine statuses
        """

        connection = get_connection()

        query = """
        SELECT
            COUNT(pb.production_id) AS total_batches,

            COALESCE(
                SUM(pb.units_produced),
                0
            ) AS total_units_produced,

            COALESCE(
                SUM(pb.defective_units),
                0
            ) AS total_defective_units,

            ROUND(
                COALESCE(
                    (SUM(pb.defective_units) * 100.0) /
                    NULLIF(SUM(pb.units_produced), 0),
                    0
                ),
                2
            ) AS defect_rate_percentage,

            ROUND(
                COALESCE(
                    AVG(pb.units_produced),
                    0
                ),
                2
            ) AS avg_units_per_batch,

            ROUND(
                COALESCE(
                    AVG(pb.production_hours),
                    0
                ),
                2
            ) AS avg_production_hours

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

        # -------------------------------------------------
        # FACTORY FILTER
        # -------------------------------------------------

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

        # -------------------------------------------------
        # SHIFT FILTER
        # -------------------------------------------------

        if shift != "All":

            conditions.append(
                "s.shift_name = %s"
            )

            params.append(shift)

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

            query += "\nWHERE "

            query += " AND ".join(
                conditions
            )

        query += ";"

        df = pd.read_sql(
            query,
            connection,
            params=params
        )

        connection.close()

        return df

    @staticmethod
    def factory_production():
        connection = get_connection()

        query = """
        SELECT
            f.factory_name,
            COUNT(pb.production_id) AS total_batches,
            SUM(pb.units_produced) AS total_units,
            SUM(pb.defective_units) AS defective_units,
            ROUND(
                (SUM(pb.defective_units) * 100.0) /
                SUM(pb.units_produced),
                2
            ) AS defect_rate
        FROM production_batches pb
        JOIN machines m
            ON pb.machine_id = m.machine_id
        JOIN factories f
            ON m.factory_id = f.factory_id
        GROUP BY f.factory_name
        ORDER BY total_units DESC;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df
