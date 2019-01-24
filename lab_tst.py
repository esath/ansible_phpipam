#!/usr/bin/python
import requests, json, sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--name", action="store", dest="customer_name",
 help="This will be used as description and vrf-name")

parser.add_argument("-m", "--mask", action="store", dest="mask_length",
 help="Bit Mask")

results = parser.parse_args()

customer_name = results.customer_name
mask_length = results.mask_length



### Variables:
#
test_network_id = '40'
domain_id = "4"


ServerAddr = "http://192.168.112.148"

#Authenticate to IPAM:
user = 'your_username'
passw = 'your_password'

###############



#Request token for API-calls
r = requests.post(ServerAddr+'/api/api/user/', auth=(user, passw))
token = (r.json()['data']['token'])
headers = {'token': token}


#GET list of vlans and vrfs/rd
xvrf = requests.get(ServerAddr+'/api/api/vrf/', headers=headers)
vrf = xvrf.json()[u'data']

xvlan = requests.get(ServerAddr+'/api/api/l2domains/'+domain_id+'/vlans/', headers=headers)
#xvlan = requests.get(ServerAddr+'/api/api/vlan/', headers=headers)
vlan = xvlan.json()[u'data']


#Get next available VLAN-value
#
lastVlan = 0
for item in vlan:
    number=int(item['number'])
    if number > lastVlan:
        lastVlan = number

nextVlan = int(lastVlan)+1


# Get next available RD-value
#
lastVRF = 0
for item in vrf:
    number=int(item['vrfId'])
    if number > lastVRF:
        lastVRF = number

nextVRF = int(lastVRF)+1

#
# Create VRF and save RD-value for later use
vrf_data = [
  ('name', customer_name),
  ('rd', nextVRF),
]
vrf = requests.post(ServerAddr+'/api/api/vrf/', headers=headers, data=vrf_data)
print vrf.json()
rd = vrf.json()['id']


#
# Create new VLAN to IPAM-server:
vlan_data = [
  ('name', customer_name),
  ('domainId', domain_id),
  ('number', nextVlan),
]
vlan = requests.post(ServerAddr+'/api/api/vlan/', headers=headers, data=vlan_data)
print vlan.json()
vlanid = vlan.json()['id']

# Create variable used in subnet description field.
# Read-only user can't see RT-value otherwise.
customer_name_rt = "%s - RouteTarget: 65202:%d" % (customer_name, nextVRF)

#
# Create /29 Subnet to new VRF and VLAN
#
subnet_data = [
  ('description', customer_name_rt),
  ('vrfId', rd),
  ('vlanId', vlanid),
]
subnet = requests.post(ServerAddr+'/api/api/subnets/'+test_network_id+'/first_subnet/'+mask_length+'/', headers=headers, data=subnet_data)
print subnet.json()

subip = subnet.json()['data']
subid = subnet.json()['id']

#Request next available ip from subnet and reserve from IPAM
cust_data = [
  ('description', customer_name),
]
vipip = requests.post(ServerAddr+'/api/api/addresses/first_free/'+subid+'/', headers=headers, data=cust_data)
r1 = requests.post(ServerAddr+'/api/api/addresses/first_free/'+subid+'/', headers=headers, data=cust_data)
r2 = requests.post(ServerAddr+'/api/api/addresses/first_free/'+subid+'/', headers=headers, data=cust_data)
nsg = requests.post(ServerAddr+'/api/api/addresses/first_free/'+subid+'/', headers=headers, data=cust_data)

vipipx = vipip.json()['data']
r1_ip = r1.json()['data']
r1_ip = r1.json()['data']
r2_ip = r2.json()['data']
next_hop_ip = nsg.json()['data']

#VRRP-group id is just RD-value incremented by 100 or 50 in this test
vrrpgrp = int(rd)+100


#Create vars for ansible
sys.stdout=open("lab_vars.yml","w")

print 'a_vlan: %s' % (nextVlan)
print 'a_vrf: %s' % (customer_name)
print 'a_vip: %s' % (vipipx)
print 'a_primary: %s' % (r1_ip)
print 'a_secondary: %s' % (r2_ip)
print 'a_netmask: /%s' % (mask_length)
print 'a_vrrp_grp: %s' % (vrrpgrp)
print 'a_rd: %s' % (nextVRF)
print 'a_target: %s' % (nextVRF)
print 'a_next_hop: %s' % (next_hop_ip)

sys.stdout.close()

