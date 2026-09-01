import pandas as pd
from database.db_connection import get_connection


class QualityAnalytics:

    @staticmethod
    def quality_summary(
        factory="All",
        shift="All",
        statuses=None,
        start_date=None,
        end_date=None
    ):
        """
        Overall quality summary with optional filters.

        Filters:
        - Factory
        - Shift
        - Machine Status
        - Start Date
        - End Date
        """

        connection = get_connection()

        query = """
        SELECT
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
            ) AS defect_rate_percentage

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

            conditions.append("""
                REPLACE(
                    f.factory_name,
                    ' Manufacturing Plant',
                    ''
                ) = %s
            """)

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
        # DATE FILTER
        # -------------------------------------------------

        if start_date is not None:

            conditions.append(
                "pb.production_date >= %s"
            )

            params.append(start_date)

        if end_date is not None:

            conditions.append(
                "pb.production_date <= %s"
            )

            params.append(end_date)

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
    def factory_quality(
        factory="All",
        shift="All",
        statuses=None,
        start_date=None,
        end_date=None
    ):
        """
        Factory-wise quality analysis.

        Supports filtering by:
        - Factory
        - Shift
        - Machine Status
        - Start Date
        - End Date
        """

        connection = get_connection()

        query = """
        SELECT
            REPLACE(
                f.factory_name,
                ' Manufacturing Plant',
                ''
            ) AS factory_name,

            COALESCE(
                SUM(pb.units_produced),
                0
            ) AS units_produced,

            COALESCE(
                SUM(pb.defective_units),
                0
            ) AS defective_units,

            ROUND(
                COALESCE(
                    (SUM(pb.defective_units) * 100.0) /
                    NULLIF(SUM(pb.units_produced), 0),
                    0
                ),
                2
            ) AS defect_rate

        FROM factories f

        LEFT JOIN machines m
            ON f.factory_id = m.factory_id

        LEFT JOIN production_batches pb
            ON m.machine_id = pb.machine_id

        LEFT JOIN shifts s
            ON pb.shift_id = s.shift_id
        """

        conditions = []
        params = []

        # -------------------------------------------------
        # FACTORY FILTER
        # -------------------------------------------------

        if factory != "All":

            conditions.append("""
                REPLACE(
                    f.factory_name,
                    ' Manufacturing Plant',
                    ''
                ) = %s
            """)

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
        # DATE FILTER
        # -------------------------------------------------

        if start_date is not None:

            conditions.append(
                "pb.production_date >= %s"
            )

            params.append(start_date)

        if end_date is not None:

            conditions.append(
                "pb.production_date <= %s"
            )

            params.append(end_date)

        # -------------------------------------------------
        # WHERE CLAUSE
        # -------------------------------------------------

        if conditions:

            query += "\nWHERE "

            query += " AND ".join(
                conditions
            )

        # -------------------------------------------------
        # GROUP + ORDER
        # -------------------------------------------------

        query += """
        GROUP BY
            f.factory_id,
            f.factory_name

        ORDER BY
            defect_rate DESC;
        """

        df = pd.read_sql(
            query,
            connection,
            params=params
        )

        connection.close()

        return df