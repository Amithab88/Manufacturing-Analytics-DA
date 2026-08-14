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
    def production_summary(factory="All"):
        return ProductionAnalytics.get_summary(factory)


    @staticmethod
    def factory_summary(factory="All", shift="All"):
        return FactoryAnalytics.factory_production(
            factory,
            shift
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
    def monthly_production(factory="All"):
        return TrendAnalytics.monthly_production(factory)


    @staticmethod
    def monthly_defects(factory="All"):
        return TrendAnalytics.monthly_defects(factory)


    @staticmethod
    def top_employees(factory="All"):
        return EmployeeAnalytics.top_employees(
            factory=factory
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