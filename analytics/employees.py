from multiprocessing import connection

import pandas as pd
from database.db_connection import get_connection


class EmployeeAnalytics:

    @staticmethod
    def employee_production():
        """
        Production summary for every employee.
        """
        connection = get_connection()

        query = """
        SELECT
            e.employee_id,
            e.employee_name,
            e.designation,
            COUNT(pb.production_id) AS total_batches,
            COALESCE(SUM(pb.units_produced),0) AS total_units_produced,
            COALESCE(SUM(pb.defective_units),0) AS total_defective_units,
            ROUND(COALESCE(AVG(pb.units_produced),0),2) AS avg_units_per_batch,
            ROUND(
                COALESCE(
                    (SUM(pb.defective_units) * 100.0) /
                    NULLIF(SUM(pb.units_produced),0),
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
        connection.close()
        return df

    @staticmethod
    def top_performers(limit=10):
        """
        Top employees based on production.
        """
        connection = get_connection()

        query = f"""
        SELECT
            e.employee_name,
            e.designation,
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
    def shift_performance():
        """
        Shift-wise production analysis.
        """
        connection = get_connection()

        query = """
        SELECT
            s.shift_name,
            COUNT(pb.production_id) AS total_batches,
            SUM(pb.units_produced) AS total_units,
            SUM(pb.defective_units) AS defective_units,
            ROUND(AVG(pb.production_hours),2) AS avg_hours,
            ROUND(
                (SUM(pb.defective_units)*100.0)/
                SUM(pb.units_produced),
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

        df = pd.read_sql(query, connection)
        connection.close()
        return df

    @staticmethod
    def top_employees(limit=10):
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

        