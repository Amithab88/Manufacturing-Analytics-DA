import pandas as pd
from database.db_connection import get_connection


class ProductionAnalytics:

    @staticmethod
    def get_summary(
        factory="All",
        shift="All",
        statuses=None,
        start_date=None,
        end_date=None
    ):
        """
        Production summary with optional filters:
        factory, shift, machine status, date range.
        """

        connection = get_connection()

        query = """
        SELECT
            COUNT(pb.production_id) AS total_batches,
            COALESCE(SUM(pb.units_produced), 0) AS total_units_produced,
            COALESCE(SUM(pb.defective_units), 0) AS total_defective_units,
            ROUND(
                COALESCE(
                    (SUM(pb.defective_units) * 100.0) / NULLIF(SUM(pb.units_produced), 0),
                    0
                ), 2
            ) AS defect_rate_percentage,
            ROUND(COALESCE(AVG(pb.units_produced), 0), 2) AS avg_units_per_batch,
            ROUND(COALESCE(AVG(pb.production_hours), 0), 2) AS avg_production_hours
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

        query += ";"

        df = pd.read_sql(query, connection, params=params)
        connection.close()

        return df
