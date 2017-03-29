#!/bin/bash
VENV_PATH=/home/ubuntu/.venvs/ftf_geonode
URL=http://download.geofabrik.de/asia/nepal-latest.osm.pbf
TEMP=/home/ubuntu/ftf_geonode/temp
#==#
# Process point feature types
$VENV_PATH/bin/python /home/ubuntu/ftf_geonode/scripts/import_osm.py \
--clean \
--url=$URL \
--pbf=/home/ubuntu/nepal-latest.osm.pbf \
--temp=$TEMP \
--config=osm.yml \
--regions=Nepal \
--license=ODbL/OSM \
--layer-name-prefix=nepal_ \
--layer-title-prefix="Nepal " \
--geometry-type=POINT
#==#
# Process polygon feature types
$VENV_PATH/bin/python /home/ubuntu/ftf_geonode/scripts/import_osm.py \
--url=$URL \
--pbf=/home/ubuntu/nepal-latest.osm.pbf \
--temp=$TEMP \
--config=osm.yml \
--regions=Nepal \
--license=ODbL/OSM \
--layer-name-prefix=nepal_ \
--layer-title-prefix="Nepal " \
--geometry-type=POLYGON
#==#
# Process line feature types
$VENV_PATH/bin/python /home/ubuntu/ftf_geonode/scripts/import_osm.py \
--url=$URL \
--pbf=/home/ubuntu/nepal-latest.osm.pbf \
--temp=$TEMP \
--config=osm.yml \
--regions=Nepal \
--license=ODbL/OSM \
--layer-name-prefix=nepal_ \
--layer-title-prefix="Nepal " \
--geometry-type=LINE
