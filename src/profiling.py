try:
    from .climate_pipeline.profiling import profile_frame, profile_files
except ImportError:
    from climate_pipeline.profiling import profile_frame, profile_files
