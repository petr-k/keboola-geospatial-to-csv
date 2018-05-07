import json


class FeatureOutputFormat:
    def __init__(self, name, field_name):
        self.name = name
        self.field_name = field_name

    def feature_to_string(self, feature, get_feature_field_values_fn):
        pass


class WktOutputFormat(FeatureOutputFormat):
    def __init__(self):
        super().__init__("wkt", "wkt_geometry")

    def feature_to_string(self, feature, _):
        geometry = feature.GetGeometryRef()
        if geometry is None or geometry.IsEmpty():
            return ""
        else:
            return geometry.ExportToWkt()


class GeoJsonGeometryOutputFormat(FeatureOutputFormat):
    def __init__(self):
        super().__init__("geojson-geometry", "geojson_geometry")

    def feature_to_string(self, feature, _):
        geometry = feature.GetGeometryRef()
        if geometry is None or geometry.IsEmpty():
            return ""
        else:
            return geometry.ExportToJson()


class GeoJsonFeatureOutputFormat(FeatureOutputFormat):
    def __init__(self):
        super().__init__("geojson-feature", "geojson_feature")

    def feature_to_string(self, feature, get_feature_field_values_fn):
        geojson_feature = {
            "type": "Feature",
            "geometry": self._get_geometry_json(feature),
            "properties": get_feature_field_values_fn(feature)
        }
        return json.dumps(geojson_feature)

    @staticmethod
    def _get_geometry_json(feature):
        geometry = feature.GetGeometryRef()
        if geometry is None or geometry.IsEmpty():
            return None
        else:
            return json.loads(geometry.ExportToJson())


feature_output_formats = {f.name: f for f in
                          [WktOutputFormat(),
                           GeoJsonFeatureOutputFormat(),
                           GeoJsonGeometryOutputFormat()
                           ]}
