try:
    from .climate_pipeline.aggregation import aggregate_city_month
except ImportError:
    from climate_pipeline.aggregation import aggregate_city_month
