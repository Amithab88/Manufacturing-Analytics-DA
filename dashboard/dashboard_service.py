import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from analytics.production import ProductionAnalytics
from analytics.factories import FactoryAnalytics
from analytics.machines import MachineAnalytics
from analytics.quality import QualityAnalytics
from analytics.employees import EmployeeAnalytics
from analytics.trends import TrendAnalytics


class DashboardService:

    @staticmethod
    def production_summary(
        factory="All",
        shift="All",
        statuses=None,
        start_date=None,
        end_date=None
    ):
        return ProductionAnalytics.get_summary(
            factory,
            shift,
            statuses,
            start_date,
            end_date
        )


    @staticmethod
    def factory_summary(
        factory="All", 
        shift="All", 
        start_date=None,
        end_date=None
    ):
        return FactoryAnalytics.factory_production(
            factory,
            shift,
            start_date,
            end_date
        )

    @staticmethod
    def machine_status(factory="All", statuses=None):
        return MachineAnalytics.machine_status(
            factory,
            statuses
        )


    @staticmethod
    def machine_count():
        return MachineAnalytics.factory_machine_count()


    @staticmethod
    def quality_summary():
        return QualityAnalytics.quality_summary()


    @staticmethod
    def employee_summary():
        return EmployeeAnalytics.employee_production()


    @staticmethod
    def monthly_production(
        factory="All",
        shift="All",
        statuses=None
    ):
        return TrendAnalytics.monthly_production(
            factory,
            shift,
            statuses
        )


    @staticmethod
    def monthly_defects(
        factory="All",
        shift="All",
        statuses=None
    ):
        return TrendAnalytics.monthly_defects(
            factory,
            shift,
            statuses
        )


    @staticmethod
    def top_employees(
        limit=10,
        factory="All",
        shift="All",
        statuses=None
    ):
        return EmployeeAnalytics.top_employees(
            limit,
            factory,
            shift,
            statuses
        )


    @staticmethod
    def shift_performance(shift="All", factory="All"):
        return EmployeeAnalytics.shift_performance(
            shift,
            factory
        )


    @staticmethod
    def get_factory_names():
        return FactoryAnalytics.get_factory_names()