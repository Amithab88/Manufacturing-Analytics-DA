import pandas as pd
from database.db_connection import get_connection


class ProductionAnalytics:

    @staticmethod
    def get_all_batches():
        connection = get_connection()

        query = "SELECT * FROM production_batches;"

        df = pd.read_sql(query, connection)
        connection.close()

        return df


    @staticmethod
    def get_summary():
        connection = get_connection()

        query = """
        SELECT
            COUNT(*) AS total_batches,
            SUM(units_produced) AS total_units_produced,
            SUM(defective_units) AS total_defective_units,
            ROUND(
                (SUM(defective_units) * 100.0) / SUM(units_produced),
                2
            ) AS defect_rate_percentage,
            ROUND(AVG(units_produced),2) AS avg_units_per_batch,
            ROUND(AVG(production_hours),2) AS avg_production_hours
        FROM production_batches;
        """

        df = pd.read_sql(query, connection)
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
        