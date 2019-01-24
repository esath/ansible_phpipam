
Make subnet, vlan and route-target reservations from phpIPAM.
After that configure Juniper SRX with new vrf and correct route-target.
Add more configuration you need: edit roles/tasks

Python uses API to add new subnet for IPAM.
For comparison, delete script is using curl-commands to clean configuration from IPAM. 


You have to define vrf and mask for new subnet.
-
ansible-playbook lab_tst.yml -e "vrf=lab003" -e "mask=29" -v


Vrf-name and vlan-id are mandatory parameters when removing configuration.
-
ansible-playbook lab_tst.yml -e "vrf=lab003" -e "vlan=4001" -v


Add static route when needed.
-
ansible-playbook lab_tst.yml -e "vrf=lab003" -e "dest_network=x.x.x.x/xx" -e "a_next_hop=x.x.x.x" -v


And full new vrf with static route would be:
-
ansible-playbook lab_tst.yml -v \
-e "vrf=lab003" -e "mask=29" \
-e "dest_network=10.0.0.0/24"


PREREQUISITES:

- phpIPAM access. Version 1.3 needed for API
- Credentials for phpIPAM. Edit lab_tst.py: Add your username/pwd and server-ip
- Add domain and master subnet using IPAM-gui and add domain- and subnet-id to lab_tst.py
- Juniper which is accessible using SSH. I'm using vSRX in Openstack-cloud.
- Ansible and Python!


Need fixes:
- vlan is reserved from domain and it's alway largest number. Should take first available, not largest..
- many more...

