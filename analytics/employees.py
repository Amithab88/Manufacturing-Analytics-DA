import pandas as pd
from database.db_connection import get_connection


class EmployeeAnalytics:

    @staticmethod
    def employee_production(factory="All"):
        """
        Production summary for every employee.
        Can be filtered by factory.
        """
        connection = get_connection()

        if factory == "All":

            query = """
            SELECT
                e.employee_id,
                e.employee_name,
                e.designation,
                COUNT(pb.production_id) AS total_batches,
                COALESCE(SUM(pb.units_produced), 0) AS total_units_produced,
                COALESCE(SUM(pb.defective_units), 0) AS total_defective_units,
                ROUND(
                    COALESCE(AVG(pb.units_produced), 0),
                    2
                ) AS avg_units_per_batch,
                ROUND(
                    COALESCE(
                        (SUM(pb.defective_units) * 100.0) /
                        NULLIF(SUM(pb.units_produced), 0),
                        0
                    ),
                    2
                ) AS defect_rate
            FROM employees e
            LEFT JOIN production_batches pb
                ON e.employee_id = pb.employee_id
            GROUP BY
                e.employee_id,
                e.employee_name,
                e.designation
            ORDER BY total_units_produced DESC;
            """

            df = pd.read_sql(query, connection)

        else:

            query = """
            SELECT
                e.employee_id,
                e.employee_name,
                e.designation,
                COUNT(pb.production_id) AS total_batches,
                COALESCE(SUM(pb.units_produced), 0) AS total_units_produced,
                COALESCE(SUM(pb.defective_units), 0) AS total_defective_units,
                ROUND(
                    COALESCE(AVG(pb.units_produced), 0),
                    2
                ) AS avg_units_per_batch,
                ROUND(
                    COALESCE(
                        (SUM(pb.defective_units) * 100.0) /
                        NULLIF(SUM(pb.units_produced), 0),
                        0
                    ),
                    2
                ) AS defect_rate
            FROM employees e
            LEFT JOIN production_batches pb
                ON e.employee_id = pb.employee_id
            JOIN factories f
                ON e.factory_id = f.factory_id
            WHERE REPLACE(f.factory_name, ' Manufacturing Plant', '') = %s
            GROUP BY
                e.employee_id,
                e.employee_name,
                e.designation
            ORDER BY total_units_produced DESC;
            """

            df = pd.read_sql(
                query,
                connection,
                params=(factory,)
            )

        connection.close()

        return df

    @staticmethod
    def top_performers(limit=10, factory="All"):
        """
        Top employees based on total production.
        """
        connection = get_connection()

        query = f"""
        SELECT
            e.employee_name,
            e.designation,
            COUNT(pb.production_id) AS total_batches,
            SUM(pb.units_produced) AS total_units
        FROM employees e
        JOIN production_batches pb
            ON e.employee_id = pb.employee_id
        GROUP BY
            e.employee_id,
            e.employee_name,
            e.designation
        ORDER BY total_units DESC
        LIMIT {limit};
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df

    @staticmethod
    def shift_performance(
        shift="All",
        factory="All",
        start_date=None,
        end_date=None
    ):
        """
        Production summary for every shift.

        Supports filtering by:
        - Shift
        - Factory
        - Start date
        - End date
        """

        connection = get_connection()

        query = """
        SELECT
            s.shift_name,

            COUNT(pb.production_id) AS total_batches,

            COALESCE(
                SUM(pb.units_produced),
                0
            ) AS total_units,

            COALESCE(
                SUM(pb.defective_units),
                0
            ) AS defective_units,

            ROUND(
                COALESCE(
                    AVG(pb.production_hours),
                    0
                ),
                2
            ) AS avg_hours,

            ROUND(
                COALESCE(
                    (
                        SUM(pb.defective_units) * 100.0
                    ) /
                    NULLIF(
                        SUM(pb.units_produced),
                        0
                    ),
                    0
                ),
                2
            ) AS defect_rate

        FROM shifts s

        LEFT JOIN production_batches pb
            ON s.shift_id = pb.shift_id

        LEFT JOIN machines m
            ON pb.machine_id = m.machine_id

        LEFT JOIN factories f
            ON m.factory_id = f.factory_id
        """

        conditions = []
        params = []

        # -------------------------------------------------
        # SHIFT FILTER
        # -------------------------------------------------

        if shift != "All":

            conditions.append(
                "s.shift_name = %s"
            )

            params.append(shift)

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
            s.shift_id,
            s.shift_name

        ORDER BY
            total_units DESC;
        """

        df = pd.read_sql(
            query,
            connection,
            params=params
        )

        connection.close()

        return df

    @staticmethod
    def top_employees(
        limit=10,
        factory="All",
        shift="All",
        statuses=None
    ):
        """
        Top employees based on total production.

        Filters:
        - Factory
        - Shift
        - Machine Status
        """

        connection = get_connection()

        query = """
        SELECT
            e.employee_name,
            e.designation,
            COUNT(pb.production_id) AS total_batches,
            SUM(pb.units_produced) AS total_units
        FROM employees e

        JOIN production_batches pb
            ON e.employee_id = pb.employee_id

        JOIN machines m
            ON pb.machine_id = m.machine_id

        JOIN factories f
            ON e.factory_id = f.factory_id

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
            query += " AND ".join(conditions)

        # -------------------------------------------------
        # GROUPING
        # -------------------------------------------------

        query += """
        GROUP BY
            e.employee_id,
            e.employee_name,
            e.designation

        ORDER BY total_units DESC

        LIMIT %s;
        """

        params.append(limit)

        df = pd.read_sql(
            query,
            connection,
            params=params
        )

        connection.close()

        return df