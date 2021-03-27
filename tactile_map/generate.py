from osm_bot_abstraction_layer.overpass_downloader import download_overpass_query
import sys
import subprocess
import os
import jsbeautifier
import json
import shapely
import shapely.ops

def main():
    name = "jubilat"
    center_lat = 50.05525
    center_lon = 19.927575
    r          = 0.000452
    generate(name, center_lat, center_lon, r)

def generate(name, center_lat, center_lon, r):
    bb = bb_from_center_point(center_lat, center_lon, r)
    query = buildings_query(bb)
    print(query)
    filepath_to_osm_input = '/tmp/buildings.osm'
    #download_overpass_query(query, filepath_to_osm_input)

    filepath_to_osm_filtered_tmp_file = '/tmp/temp.osm'
    filepath_to_geojson_output = '/tmp/dump.geojson'
    convert_osm_to_geojson(filepath_to_osm_input, filepath_to_osm_filtered_tmp_file, filepath_to_geojson_output)

    with open(filepath_to_geojson_output) as f:
        geojson_parsed_as_json = json.load(f)
        merged = merge_geojson_features_to_single_multipolygon(geojson_parsed_as_json)
        print(merged)


def feature_collection_to_single_multipolygon(geojson_parsed_as_json):
    """
    input: geojson_parsed_as_json (feature collection)
    output: geojson_parsed_as_json (multipolygon)
    """"
    features = geojson_parsed_as_json["features"]
    shapes = []
    for feature in features:
        geometry = feature['geometry']
        #print(jsbeautifier.beautify(json.dumps(geometry)))
        shp = shapely.geometry.shape(geometry)
        #print(shp)
        shapes.append(shp)
        #print(shp.area)
        #print(shapely_object_to_geojson_text(shp))
    merged = shapely.ops.cascaded_union(shapes)
    #print(shapely_object_to_geojson_text(merged))
    return shapely.geometry.mapping(merged)

def shapely_object_to_geojson_text(shp):
    return jsbeautifier.beautify(json.dumps(shapely.geometry.mapping(shp)))

def bb_from_center_point(center_lat, center_lon, r):
  return str(center_lat - r) + "," + str(center_lon - r) + "," + str(center_lat + r) + "," + str(center_lon + r)

def generic_area_query(selections, bb):
    query = ""
    query += '[out:xml][timeout:50];'
    query += "\n"
    query += "("
    query += "\n"

    for filter in selections:
        query += 'way[' + filter + ']({{bbox}});' + "\n"
        query += 'relation[' + filter + ']({{bbox}});' + "\n"

    query += ');'
    query += "\n"
    query += "(._;>;);"
    query += "\n"
    query += "out meta;"
    query += "\n"

    query = query.replace('({{bbox}})', '(' + bb + ')')
    return query

def buildings_query(bb):
  return generic_area_query(['"building"'], bb)

def area_highway_query(bb, types):
  selections = []
  for type in types:
    selections << '"area:highway"="' + type + '"'
  return generic_area_query(selections, bb)


def convert_osm_to_geojson(filepath_to_osm_input, filepath_to_osm_filtered_tmp_file, filepath_to_geojson_output):
    # convert os.system to things like
    # subprocess.call(["netsh", "interface", "set", "interface", "Wi-Fi", "enable"])
    # escaping for free and other nice stuff 
    # https://stackoverflow.com/a/44731082/4130619 
    # https://stackoverflow.com/a/64341833/4130619

    # get rid of this dependencies or document them! TODO
    # asked on IRC about osmfilter
    # https://webchat.oftc.net/?nick=Mateusz&channels=%23osm
    # Is anyone aware of osmfilter equivalent (drop tags except specified whitelist) available as pip package?
    # It should be fairly easy to reimplement, but maybe it can be avoided?
    # (I can just use osmfilter but I am tying to drop some unusual dependencies and turn it into pure python package)
    # also, for the same reasons - is there osmtogeojson equivalent available in python?

    # https://github.com/osmcode/pyosmium

    # Is anyone aware about pip package that would be equivalent of osmtogeojson? And allowing to generate geojson (or some other standard and human readable format) from .osm files?
    # drop unneded tags to prevent osmtogeojson from generating unneded point geometries
    subprocess.call(["osmfilter", filepath_to_osm_input, "--keep-tags=all area:highway= building= landuse= type=multipolygon", "-o=" + filepath_to_osm_filtered_tmp_file])

    # convert to standard format
    os.system("osmtogeojson '" + filepath_to_osm_filtered_tmp_file + "' >  '" + filepath_to_geojson_output + "'")

main()