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
    def shift_performance(shift="All", factory="All"):
        """
        Production summary for every shift.
        Can be filtered by factory.
        """

        connection = get_connection()

        # -------------------------------------------------
        # ALL FACTORIES
        # -------------------------------------------------

        if factory == "All":

            if shift == "All":

                query = """
                SELECT
                    s.shift_name,
                    COUNT(pb.production_id) AS total_batches,
                    COALESCE(SUM(pb.units_produced), 0) AS total_units,
                    COALESCE(SUM(pb.defective_units), 0) AS defective_units,
                    ROUND(
                        COALESCE(AVG(pb.production_hours), 0),
                        2
                    ) AS avg_hours,
                    ROUND(
                        COALESCE(
                            (SUM(pb.defective_units) * 100.0) /
                            NULLIF(SUM(pb.units_produced), 0),
                            0
                        ),
                        2
                    ) AS defect_rate
                FROM shifts s
                LEFT JOIN production_batches pb
                    ON s.shift_id = pb.shift_id
                GROUP BY
                    s.shift_id,
                    s.shift_name
                ORDER BY total_units DESC;
                """

                df = pd.read_sql(
                    query,
                    connection
                )

            else:

                query = """
                SELECT
                    s.shift_name,
                    COUNT(pb.production_id) AS total_batches,
                    COALESCE(SUM(pb.units_produced), 0) AS total_units,
                    COALESCE(SUM(pb.defective_units), 0) AS defective_units,
                    ROUND(
                        COALESCE(AVG(pb.production_hours), 0),
                        2
                    ) AS avg_hours,
                    ROUND(
                        COALESCE(
                            (SUM(pb.defective_units) * 100.0) /
                            NULLIF(SUM(pb.units_produced), 0),
                            0
                        ),
                        2
                    ) AS defect_rate
                FROM shifts s
                LEFT JOIN production_batches pb
                    ON s.shift_id = pb.shift_id
                WHERE s.shift_name = %s
                GROUP BY
                    s.shift_id,
                    s.shift_name
                ORDER BY total_units DESC;
                """

                df = pd.read_sql(
                    query,
                    connection,
                    params=(shift,)
                )

        # -------------------------------------------------
        # SPECIFIC FACTORY
        # -------------------------------------------------

        else:

            if shift == "All":

                query = """
                SELECT
                    s.shift_name,
                    COUNT(pb.production_id) AS total_batches,
                    COALESCE(SUM(pb.units_produced), 0) AS total_units,
                    COALESCE(SUM(pb.defective_units), 0) AS defective_units,
                    ROUND(
                        COALESCE(AVG(pb.production_hours), 0),
                        2
                    ) AS avg_hours,
                    ROUND(
                        COALESCE(
                            (SUM(pb.defective_units) * 100.0) /
                            NULLIF(SUM(pb.units_produced), 0),
                            0
                        ),
                        2
                    ) AS defect_rate
                FROM shifts s
                JOIN production_batches pb
                    ON s.shift_id = pb.shift_id
                JOIN machines m
                    ON pb.machine_id = m.machine_id
                JOIN factories f
                    ON m.factory_id = f.factory_id
                WHERE REPLACE(
                    f.factory_name,
                    ' Manufacturing Plant',
                    ''
                ) = %s
                GROUP BY
                    s.shift_id,
                    s.shift_name
                ORDER BY total_units DESC;
                """

                df = pd.read_sql(
                    query,
                    connection,
                    params=(factory,)
                )

            else:

                query = """
                SELECT
                    s.shift_name,
                    COUNT(pb.production_id) AS total_batches,
                    COALESCE(SUM(pb.units_produced), 0) AS total_units,
                    COALESCE(SUM(pb.defective_units), 0) AS defective_units,
                    ROUND(
                        COALESCE(AVG(pb.production_hours), 0),
                        2
                    ) AS avg_hours,
                    ROUND(
                        COALESCE(
                            (SUM(pb.defective_units) * 100.0) /
                            NULLIF(SUM(pb.units_produced), 0),
                            0
                        ),
                        2
                    ) AS defect_rate
                FROM shifts s
                JOIN production_batches pb
                    ON s.shift_id = pb.shift_id
                JOIN machines m
                    ON pb.machine_id = m.machine_id
                JOIN factories f
                    ON m.factory_id = f.factory_id
                WHERE s.shift_name = %s
                AND REPLACE(
                        f.factory_name,
                        ' Manufacturing Plant',
                        ''
                    ) = %s
                GROUP BY
                    s.shift_id,
                    s.shift_name
                ORDER BY total_units DESC;
                """

                df = pd.read_sql(
                    query,
                    connection,
                    params=(shift, factory)
                )

        connection.close()

        return df


    @staticmethod
    def top_employees(limit=10, factory="All"):
        """
        Top employees based on total production.
        Can be filtered by factory.
        """
        connection = get_connection()

        if factory == "All":

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

        else:

            query = f"""
            SELECT
                e.employee_name,
                e.designation,
                COUNT(pb.production_id) AS total_batches,
                SUM(pb.units_produced) AS total_units
            FROM employees e
            JOIN production_batches pb
                ON e.employee_id = pb.employee_id
            JOIN factories f
                ON e.factory_id = f.factory_id
            WHERE REPLACE(f.factory_name, ' Manufacturing Plant', '') = %s
            GROUP BY
                e.employee_id,
                e.employee_name,
                e.designation
            ORDER BY total_units DESC
            LIMIT {limit};
            """

            df = pd.read_sql(
                query,
                connection,
                params=(factory,)
            )

        connection.close()

        return df