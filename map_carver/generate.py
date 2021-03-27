from osm_bot_abstraction_layer.overpass_downloader import download_overpass_query
import sys
import subprocess
import os

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
    download_overpass_query(query, filepath_to_osm_input)

    filepath_to_osm_filtered_tmp_file = '/tmp/temp.osm'
    filepath_to_geojson_output = '/tmp/dump.geojson'
    convert_osm_to_geojson(filepath_to_osm_input, filepath_to_osm_filtered_tmp_file, filepath_to_geojson_output)

    import json
    from shapely.geometry import shape, GeometryCollection
    with open(filepath_to_geojson_output) as f:
        features = json.load(f)["features"]

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

    # drop unneded tags to prevent osmtogeojson from generating unneded point geometries
    subprocess.call(["osmfilter", filepath_to_osm_input, "--keep-tags=all area:highway= building= landuse= type=multipolygon", "-o=" + filepath_to_osm_filtered_tmp_file])

    # convert to standard format
    os.system("osmtogeojson '" + filepath_to_osm_filtered_tmp_file + "' >  '" + filepath_to_geojson_output + "'")

main()