import pandas as pd
from database.db_connection import get_connection


class QualityAnalytics:

    @staticmethod
    def quality_summary():
        connection = get_connection()

        query = """
        SELECT
            SUM(units_produced) AS total_units_produced,
            SUM(defective_units) AS total_defective_units,
            ROUND(
                (SUM(defective_units) * 100.0) /
                SUM(units_produced),
                2
            ) AS defect_rate_percentage
        FROM production_batches;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df

    @staticmethod
    def factory_quality():
        connection = get_connection()

        query = """
        SELECT
            f.factory_name,
            SUM(pb.units_produced) AS units_produced,
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
        ORDER BY defect_rate DESC;
        """

        df = pd.read_sql(query, connection)
        connection.close()

        return df