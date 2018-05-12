import glob
from os import path, makedirs
from keboola import docker as kbc_py
from osgeo import gdal, ogr
from config_schema import validate_expand_defaults
from conversion import convert
from inputs import input_formats
from outputs import feature_output_formats


gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()
ogr.UseExceptions()


def run(datadir):
    cfg = kbc_py.Config(datadir)

    in_base_path = path.join(datadir, 'in/files')
    out_base_path = path.join(datadir, 'out/files')

    params = validate_expand_defaults(cfg.get_parameters())

    output_params = params["output"]
    feature_format = feature_output_formats[output_params["featureFormat"]]
    include_additional_fields = output_params["includeAdditionalColumns"]

    input_format_params = params["input"]["format"]
    for format_name, format_params in input_format_params.items():
        in_format = input_formats[format_name]
        enabled = format_params["enabled"]
        glob_pattern = format_params["glob"]
        if not enabled:
            continue

        for full_in_path in glob.iglob(path.join(in_base_path, glob_pattern)):
            relative_path = path.relpath(full_in_path, start=in_base_path)
            target_relative_path = relative_path + ".csv"
            full_out_path = path.join(out_base_path, target_relative_path)
            print(f"Converting {relative_path} (as {format_name}) "
                  f"to {target_relative_path}")
            makedirs(path.dirname(full_out_path), exist_ok=True)
            with open(full_out_path, mode="wt", encoding="utf=8") as out_file:
                convert(full_in_path,
                        out_file,
                        in_format,
                        feature_format,
                        include_additional_fields)
