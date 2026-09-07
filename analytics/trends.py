import pandas as pd
from database.db_connection import get_connection


class TrendAnalytics:

    @staticmethod
    def monthly_production(
        factory="All",
        shift="All",
        statuses=None,
        start_date=None,
        end_date=None
    ):
        """
        Monthly production trend. Returns (month, total_units).
        """

        connection = get_connection()

        query = """
        SELECT
            DATE_FORMAT(pb.production_date, '%Y-%m') AS month,
            SUM(pb.units_produced) AS total_units
        FROM production_batches pb
        JOIN machines m ON pb.machine_id = m.machine_id
        JOIN factories f ON m.factory_id = f.factory_id
        JOIN shifts s ON pb.shift_id = s.shift_id
        """

        conditions = []
        params = []

        if factory != "All":
            conditions.append(
                "REPLACE(f.factory_name, ' Manufacturing Plant', '') = %s"
            )
            params.append(factory)

        if shift != "All":
            conditions.append("s.shift_name = %s")
            params.append(shift)

        if statuses:
            placeholders = ", ".join(["%s"] * len(statuses))
            conditions.append(f"m.status IN ({placeholders})")
            params.extend(statuses)

        if start_date is not None:
            conditions.append("pb.production_date >= %s")
            params.append(start_date)

        if end_date is not None:
            conditions.append("pb.production_date <= %s")
            params.append(end_date)

        if conditions:
            query += "\nWHERE " + " AND ".join(conditions)

        query += """
        GROUP BY month
        ORDER BY month;
        """

        df = pd.read_sql(query, connection, params=params)
        connection.close()

        return df

    @staticmethod
    def monthly_defects(
        factory="All",
        shift="All",
        statuses=None,
        start_date=None,
        end_date=None
    ):
        """
        Monthly defective-units trend. Returns (month, total_defects).
        """

        connection = get_connection()

        query = """
        SELECT
            DATE_FORMAT(pb.production_date, '%Y-%m') AS month,
            SUM(pb.defective_units) AS total_defects
        FROM production_batches pb
        JOIN machines m ON pb.machine_id = m.machine_id
        JOIN factories f ON m.factory_id = f.factory_id
        JOIN shifts s ON pb.shift_id = s.shift_id
        """

        conditions = []
        params = []

        if factory != "All":
            conditions.append(
                "REPLACE(f.factory_name, ' Manufacturing Plant', '') = %s"
            )
            params.append(factory)

        if shift != "All":
            conditions.append("s.shift_name = %s")
            params.append(shift)

        if statuses:
            placeholders = ", ".join(["%s"] * len(statuses))
            conditions.append(f"m.status IN ({placeholders})")
            params.extend(statuses)

        if start_date is not None:
            conditions.append("pb.production_date >= %s")
            params.append(start_date)

        if end_date is not None:
            conditions.append("pb.production_date <= %s")
            params.append(end_date)

        if conditions:
            query += "\nWHERE " + " AND ".join(conditions)

        query += """
        GROUP BY month
        ORDER BY month;
        """

        df = pd.read_sql(query, connection, params=params)
        connection.close()

        return df
