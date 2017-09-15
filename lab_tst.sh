#/bin/sh
#
#Usage: './rm_ipam_data.sh customername vlan'
#customername is same as routing-instance/vrf-name
#
token=`curl -X POST --user username:password http://192.168.112.148/api/api/user/ | grep token | awk -F\" '{print $10}'`

subnetid=`curl -X GET -H "token: $token" http://192.168.112.148/api/api/sections/4/subnets/ | sed 's/{/\n/g' | grep $1 | awk -F\" '{print $4}'`
vrfid=`curl -X GET -H "token: $token" http://192.168.112.148/api/api/vrf/ | sed 's/{/\n/g' | grep $1 | awk -F\" '{print $4}'`
vlanid=`curl -X GET -H "token: $token" http://192.168.112.148/api/api/vlan/ | sed 's/{/\n/g' | grep $2 | grep $1 | awk -F\" '{print $4}'`
#

curl -X DELETE -H "token: $token" http://192.168.112.148/api/api/vrf/ -d "id=$vrfid"
echo ""
curl -X DELETE -H "token: $token" http://192.168.112.148/api/api/subnets/$subnetid/
echo ""
curl -X DELETE -H "token: $token" http://192.168.112.148/api/api/vlan/ -d "id=$vlanid"
echo ""

