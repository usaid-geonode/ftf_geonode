FTF Geonode (ftf_geonode)
========================

django-admin.py startproject --template=https://github.com/GeoNode/geonode-project/archive/master.zip -epy,rst,yml ftf_geonode


ANSIBLE_ROLES_PATH=~/.ansible/roles ansible-playbook -i inventory --limit all playbook.yml


make all NAME=nepal URL=http://download.geofabrik.de/asia/nepal-latest.osm.pbf DB_USER=ftf_geonode DB_PASS=ftf_geonode
CREATE DATABASE osm_nepal WITH TEMPLATE template1 OWNER ftf_geonode;


python scripts/import_osm.py --config osm.yml --pbf /home/ubuntu/nepal-latest.osm.pbf --regions Nepal --geometry-type=POINT
python scripts/update_osm_styles.py --config osm.yml --geometry-type=POLYGON

sudo apt-get install osmctools


sudo apt-get install libgdal-dev libgeos-dev libgeos-c1v5 libpq-dev gdal-bin

ec2-34-205-161-42.compute-1.amazonaws.com ansible_host=ec2-34-205-161-42.compute-1.amazonaws.com ansible_ssh_private_key_file=~/workspaces/ftf-geonode/auth/patrick_ftf_geonode_1
