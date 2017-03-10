FTF Geonode (ftf_geonode)
========================

django-admin.py startproject --template=https://github.com/GeoNode/geonode-project/archive/master.zip -epy,rst,yml ftf_geonode


ANSIBLE_ROLES_PATH=~/.ansible/roles ansible-playbook -i inventory --limit all playbook.yml
