from pathlib import Path
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

    datadir_path = Path(datadir)
    in_base_path = datadir_path / 'in/files'
    out_base_path = datadir_path / 'out/files'

    params = validate_expand_defaults(cfg.get_parameters())
    print("Datadir: " + str(list(str(d) for d in datadir_path.glob("**"))))

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

        matching_files = list(in_base_path.glob(glob_pattern))
        print(f"Files matching {glob_pattern} in {in_base_path}: "
              f"{[str(f) for f in matching_files]}")

        for full_in_path in matching_files:
            relative_path = Path(full_in_path).relative_to(in_base_path)
            target_relative_path = relative_path.with_suffix(".csv")

            full_out_path = out_base_path / target_relative_path

            print(f"Converting {relative_path} (as {format_name}) "
                  f"to {target_relative_path}")

            full_out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(full_out_path), mode="wt", encoding="utf=8") as out:
                convert(str(full_in_path),
                        out,
                        in_format,
                        feature_format,
                        include_additional_fields)
