try:
    from .climate_pipeline.pipeline import run_pipeline
except ImportError:
    from climate_pipeline.pipeline import run_pipeline
