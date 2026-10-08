try:
    from .climate_pipeline.validation import validate_city_monthly, validate_daily_schema
except ImportError:
    from climate_pipeline.validation import validate_city_monthly, validate_daily_schema
