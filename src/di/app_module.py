from logging import Logger
from injector import Module, singleton, provider

from src.core.config import Config
from src.core.logging import get_logger, setup_logging
from src.services.care_planner.generator import CarePlanGenerator
from src.services.care_planner.planner import CarePlannerService
from src.services.spelling.corrector import SpellingCorrectorService
from src.services.schedule.service import ScheduleService


class AppModule(Module):
    @singleton
    @provider
    def provide_config(self) -> Config:
        # Config loads from environment automatically
        return Config()

    @provider
    def provide_class_logger(self, config: Config) -> Logger:
        setup_logging(env=config.environment, log_level=config.log_level)
        return get_logger(self.__class__.__name__)  # inject class-specific loggers


class ServiceModule(Module):
    @singleton
    @provider
    def provide_care_plan_generator(
        self, config: Config, logger: Logger
    ) -> CarePlanGenerator:
        return CarePlanGenerator(logger, config)

    @singleton
    @provider
    def provide_care_planner_service(
        self, care_plan_generator: CarePlanGenerator, logger: Logger
    ) -> CarePlannerService:
        return CarePlannerService(care_plan_generator, logger)

    @singleton
    @provider
    def provide_spelling_corrector_service(
        self, config: Config, logger: Logger
    ) -> SpellingCorrectorService:
        return SpellingCorrectorService(logger, config)

    @singleton
    @provider
    def provide_schedule_service(self, logger: Logger) -> ScheduleService:
        return ScheduleService(logger)
