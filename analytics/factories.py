import pandas as pd
from database.db_connection import get_connection


class FactoryAnalytics:

    @staticmethod
    def factory_production(factory="All"):
        """
        Factory-wise production summary.
        """
        connection = get_connection()

        if factory == "All":
            query = """
            SELECT
                REPLACE(f.factory_name, ' Manufacturing Plant', '') AS factory_name,
                COUNT(pb.production_id) AS total_batches,
                SUM(pb.units_produced) AS total_units_produced,
                SUM(pb.defective_units) AS total_defective_units,
                ROUND(
                    (SUM(pb.defective_units) * 100.0) /
                    SUM(pb.units_produced),
                    2
                )AS defect_rate_percentage
            FROM factories f
            LEFT JOIN machines m
                ON f.factory_id = m.factory_id
            LEFT JOIN production_batches pb
                ON m.machine_id = pb.machine_id
            GROUP BY f.factory_id, f.factory_name
            ORDER BY SUM(pb.units_produced) DESC;
            """
        else:
            query = f"""
            SELECT
                REPLACE(f.factory_name, ' Manufacturing Plant', '') AS factory_name,
                COUNT(pb.production_id) AS total_batches,
                SUM(pb.units_produced) AS total_units_produced,
                SUM(pb.defective_units) AS total_defective_units,
                ROUND(
                    (SUM(pb.defective_units) * 100.0) /
                    NULLIF(SUM(pb.units_produced), 0),
                    2
                ) AS defect_rate_percentage
            FROM factories f
            LEFT JOIN machines m
                ON f.factory_id = m.factory_id
            LEFT JOIN production_batches pb
                ON m.machine_id = pb.machine_id
            WHERE f.factory_name = '{factory} Manufacturing Plant'
            GROUP BY f.factory_id, f.factory_name
            ORDER BY SUM(pb.units_produced) DESC;
            """

        df = pd.read_sql(query, connection)
        connection.close()

        return df

    @staticmethod
    def machine_count():
        """
        Number of machines in each factory.
        """
        connection = get_connection()

        query = """
        SELECT
            f.factory_id,
            REPLACE(f.factory_name, ' Manufacturing Plant', '') AS factory_name,
            COUNT(m.machine_id) AS total_machines
        FROM factories f
        LEFT JOIN machines m
            ON f.factory_id = m.factory_id
        GROUP BY f.factory_id, f.factory_name
        ORDER BY total_machines DESC;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df

    @staticmethod
    def employee_count():
        """
        Number of employees in each factory.
        """
        connection = get_connection()

        query = """
        SELECT
            f.factory_id,
            REPLACE(f.factory_name, ' Manufacturing Plant', '') AS factory_name,
            COUNT(e.employee_id) AS total_employees
        FROM factories f
        LEFT JOIN employees e
            ON f.factory_id = e.factory_id
        GROUP BY f.factory_id, f.factory_name
        ORDER BY total_employees DESC;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df

    @staticmethod
    def factory_performance():
        """
        Overall factory performance report.
        """
        connection = get_connection()

        query = """
        SELECT
            REPLACE(f.factory_name, ' Manufacturing Plant', '') AS factory_name,
            COUNT(DISTINCT m.machine_id) AS total_machines,
            COUNT(DISTINCT e.employee_id) AS total_employees,
            COUNT(pb.production_id) AS total_batches,
            SUM(pb.units_produced) AS total_units,
            SUM(pb.defective_units) AS defective_units,
            ROUND(
                (SUM(pb.defective_units) * 100.0) /
                SUM(pb.units_produced),
                2
            ) AS defect_rate
        FROM factories f
        LEFT JOIN machines m
            ON f.factory_id = m.factory_id
        LEFT JOIN employees e
            ON f.factory_id = e.factory_id
        LEFT JOIN production_batches pb
            ON m.machine_id = pb.machine_id
        GROUP BY f.factory_id, f.factory_name
        ORDER BY total_units DESC;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df

    @staticmethod
    def get_factory_names():
        """
        Returns a list of factory names.
        """
        connection = get_connection()

        query = """
        SELECT
            REPLACE(factory_name, ' Manufacturing Plant', '') AS factory_name
        FROM factories
        ORDER BY factory_name;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df["factory_name"].tolist()