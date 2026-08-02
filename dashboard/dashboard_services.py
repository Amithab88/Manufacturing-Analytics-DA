from analytics.production import ProductionAnalytics
from analytics.factories import FactoryAnalytics
from analytics.machines import MachineAnalytics
from analytics.quality import QualityAnalytics
from analytics.employees import EmployeeAnalytics
from analytics.trends import TrendAnalytics


class DashboardService:

    @staticmethod
    def production_summary():
        return ProductionAnalytics.get_summary()

    @staticmethod
    def factory_summary():
        return FactoryAnalytics.factory_production()

    @staticmethod
    def machine_status():
        return MachineAnalytics.machine_status()

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
    def monthly_production():
        return TrendAnalytics.monthly_production()