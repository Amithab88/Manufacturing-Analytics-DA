import pandas as pd
from database.db_connection import get_connection


class TrendAnalytics:

    @staticmethod
    def daily_production():
        connection = get_connection()

        query = """
        SELECT
            production_date,
            SUM(units_produced) AS total_units
        FROM production_batches
        GROUP BY production_date
        ORDER BY production_date;
        """

        df = pd.read_sql(query, connection)
        connection.close()
        return df

    @staticmethod
    def monthly_production():
        connection = get_connection()

        query = """
        SELECT
            DATE_FORMAT(production_date,'%Y-%m') AS month,
            SUM(units_produced) AS total_units
        FROM production_batches
        GROUP BY month
        ORDER BY month;
        """

        df = pd.read_sql(query, connection)
        connection.close()
        return df

    @staticmethod
    def daily_defect_rate():
        connection = get_connection()

        query = """
        SELECT
            production_date,
            ROUND(
                (SUM(defective_units)*100.0)/
                SUM(units_produced),
                2
            ) AS defect_rate
        FROM production_batches
        GROUP BY production_date
        ORDER BY production_date;
        """

        df = pd.read_sql(query, connection)
        connection.close()
        return df

    @staticmethod
    def monthly_defect_rate():
        connection = get_connection()

        query = """
        SELECT
            DATE_FORMAT(production_date,'%Y-%m') AS month,
            ROUND(
                (SUM(defective_units)*100.0)/
                SUM(units_produced),
                2
            ) AS defect_rate
        FROM production_batches
        GROUP BY month
        ORDER BY month;
        """

        df = pd.read_sql(query, connection)
        connection.close()
        return df

    @staticmethod
    def production_hours_trend():
        connection = get_connection()

        query = """
        SELECT
            DATE_FORMAT(production_date,'%Y-%m') AS month,
            ROUND(AVG(production_hours),2) AS avg_production_hours
        FROM production_batches
        GROUP BY month
        ORDER BY month;
        """

        df = pd.read_sql(query, connection)
        connection.close()
        return df

    @staticmethod
    def monthly_defects():
        connection = get_connection()

        query = """
        SELECT
            DATE_FORMAT(production_date,'%Y-%m') AS month,
            SUM(defective_units) AS total_defects
        FROM production_batches
        GROUP BY month
        ORDER BY month;
        """

        df = pd.read_sql(query, connection)
        connection.close()
        return df