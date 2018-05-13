from osgeo import ogr


class Field:
    _supported_field_types = {
        ogr.OFTInteger: lambda f, i: f.GetFieldAsInteger(i),
        ogr.OFTInteger64: lambda f, i: f.GetFieldAsInteger64(i),
        ogr.OFTReal: lambda f, i: f.GetFieldAsDouble(i),
        ogr.OFTString: lambda f, i: f.GetFieldAsString(i),
        # TODO: need to figure out how date/datetime values are encoded
        # ogr.OFTDate: lambda f, i: f.GetFieldAsDateTime(i),
        # ogr.OFTDateTime: lambda f, i: f.GetFieldAsDateTime(i),
    }

    def __init__(self, name, type, index):
        if not Field.is_supported_type(type):
            raise ValueError(f"Unsupported field type {type}, "
                             f"field name is {name}")
        self.name = name
        self.type = type
        self.index = index
        self._get_value_fn = Field._supported_field_types[type]

    def get_value(self, feature):
        if self.index == -1:
            return feature.GetFID()
        if feature.IsFieldNull(self.index):
            return None
        return self._get_value_fn(feature, self.index)

    @staticmethod
    def is_supported_type(field_type):
        return field_type in Field._supported_field_types


class InputDataSource:
    def __init__(self, ogr_data_source, ogr_layer: ogr.Layer):
        self.ogr_layer = ogr_layer
        self.ogr_data_source = ogr_data_source
        ogr_layer.thisown = 0
        ogr_data_source.thisown = 0

        self.fid_column_name = ogr_layer.GetFIDColumn()
        self.fields = list(self._get_fields())

    def get_features(self):
        self.ogr_layer.ResetReading()
        for feature in self.ogr_layer:
            yield feature

    def get_non_spatial_field_names(self):
        return [f.name for f in self.fields]

    def get_non_spatial_field_values_for_feature(self, feature):
        values = {f.name: f.get_value(feature) for f in self.fields}
        return values

    def get_non_spatial_field_values_for_feature_fn(self):
        def fn(feature):
            return self.get_non_spatial_field_values_for_feature(feature)
        return fn

    def _get_fields(self):
        layer_def = self.ogr_layer.GetLayerDefn()
        if self.fid_column_name:
            yield Field(self.fid_column_name, ogr.OFTInteger64,
                        -1)
        for i in range(layer_def.GetFieldCount()):
            field_def = layer_def.GetFieldDefn(i)
            if Field.is_supported_type(field_def.GetType()):
                yield Field(field_def.GetName(), field_def.GetType(), i)


class InputFormat:
    def __init__(self, name: str):
        self.name = name

    def open(path: str) -> InputDataSource:
        pass


class _GenericOgrFormat(InputFormat):
    def __init__(self, name, ogr_driver_name):
        super().__init__(name)
        self.ogr_driver = ogr.GetDriverByName(ogr_driver_name)
        if not self.ogr_driver:
            raise ValueError(f"OGR driver {ogr_driver_name} not found.")
        self.ogr_driver.thisown = 0

    def open(self, path):
        data_source = self.ogr_driver.Open(path, 0)  # 0 = open
        if not data_source:
            raise ValueError(f"Could not open {path}")
        layer = data_source.GetLayer()
        return InputDataSource(data_source, layer)


format_kml = _GenericOgrFormat("kml", "LIBKML")
format_shapefile = _GenericOgrFormat("shapefile", "ESRI Shapefile")
format_geojson = _GenericOgrFormat("geojson", "GeoJSON")

input_formats = {f.name: f for f in [format_kml, format_shapefile,
                                     format_geojson]}
