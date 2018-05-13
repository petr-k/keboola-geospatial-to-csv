import pytest
from tests.common import data_file
from inputs import format_geojson


@pytest.fixture
def geojson_file():
    return data_file("geojson/stations.geojson")


def test_open(geojson_file):
    data_source = format_geojson.open(geojson_file)
    assert data_source


def test_get_nonspatial_field_names(geojson_file):
    data_source = format_geojson.open(geojson_file)
    names = list(data_source.get_non_spatial_field_names())
    assert set([
        'name',
        'marker-color',
        'marker-symbol',
        'line']) == set(names)


def test_iterate_features(geojson_file):
    data_source = format_geojson.open(geojson_file)
    assert 86 == len(list(data_source.get_features()))


def test_get_features(geojson_file):
    data_source = format_geojson.open(geojson_file)
    field_names = set(data_source.get_non_spatial_field_names())
    for f in data_source.get_features():
        values = data_source.get_non_spatial_field_values_for_feature(f)
        assert set(values.keys()) == field_names
        assert not f.GetGeometryRef().IsEmpty()
