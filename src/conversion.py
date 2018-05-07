import csv
from keboola import docker
from inputs import InputFormat
from outputs import FeatureOutputFormat

docker.Config.register_csv_dialect()


def convert(input_file, output_stream,
            input_format: InputFormat,
            feature_output_format: FeatureOutputFormat,
            include_fields=True):
    data_source = input_format.open(input_file)
    field_names = [feature_output_format.field_name]

    if include_fields:
        field_names.extend(data_source.get_non_spatial_field_names())

    field_values_fn = data_source.get_non_spatial_field_values_for_feature_fn()

    writer = csv.DictWriter(output_stream, dialect='kbc',
                            fieldnames=field_names)
    writer.writeheader()
    for f in data_source.get_features():
        v = field_values_fn(f) if include_fields else {}
        v[feature_output_format.field_name] = \
            feature_output_format.feature_to_string(f, field_values_fn)
        writer.writerow(v)
