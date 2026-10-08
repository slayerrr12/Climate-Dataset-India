try:
    from .climate_pipeline.ingest import discover_files, parse_filename, read_point_file, read_all_points
except ImportError:
    from climate_pipeline.ingest import discover_files, parse_filename, read_point_file, read_all_points
