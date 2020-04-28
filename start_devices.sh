#!/bin/bash

# debugging
# set -x

# install necessery libraries
echo "Install libraries"
sudo yum install jq -y
sudo yum install python3 -y

echo "Start device simulator"
# echo "How many device do I need to spin up?"
# read numberOfDevices

################### SETUP ###################
root_folder=$PWD

cd src

# get endpoint
if ! test -f "endpoint.json"; then
    aws iot describe-endpoint --endpoint-type iot:Data-ATS > endpoint.json
fi

endpoint="$(jq -r ".endpointAddress" endpoint.json)"
echo $endpoint

# # create policy 
if ! test -f "iot_policy.json"; then
    echo "Policy file does not exist. First create a iot_policy.json file!"
    exit 1
fi

if ! aws iot get-policy --policy-name iot-sim-policy; then
    aws iot create-policy --policy-name iot-sim-policy --policy-document  file://iot_policy.json
fi

# # get certificates
aws iot create-keys-and-certificate --set-as-active --certificate-pem-outfile "certificate.pem" --private-key-outfile "private.key" > cert_info.json

if ! test -f "AmazonRootCA1.pem"; then
    wget https://www.amazontrust.com/repository/AmazonRootCA1.pem
fi

# # attach policy to certificate
cert_arn="$(jq -r ".certificateArn" cert_info.json)" 
aws iot attach-policy --policy-name iot-sim-policy --target $cert_arn

cd $root_folder

################### CREATE DEVICE ###################

mkdir -p devices
cd devices

for i in 1 2 #3 4 5
do
    # create own folder with files
    device_name="device_$i"
    mkdir -p $device_name
    cd $device_name

    # Copy files
    cp -r $root_folder/src/AWSIoTPythonSDK .
    cp $root_folder/src/private.key .
    cp $root_folder/src/certificate.pem .
    cp $root_folder/src/AmazonRootCA1.pem .
    cp $root_folder/src/device.py .

    aws iot create-thing --thing-name $device_name > thing_info.json

    # Attache certificate to thing
    aws iot attach-thing-principal --thing-name $device_name --principal $cert_arn

    nohup python3 device.py -e $endpoint -r "AmazonRootCA1.pem" -c "certificate.pem" -k "private.key" -id $(jq -r ".thingId" thing_info.json) -t "data" -n $(jq -r ".thingName" thing_info.json) &

    cd ..
done


################### REMOVE ###################

# function cleanup() {
#     for pid in $(ps -ef | grep -v grep | grep "python3 device.py" | awk '{ print $2 }'); do kill $pid; done
# }

# trap "for pid in $(ps -ef | grep -v grep | grep "python3 device.py" | awk '{ print $2 }'); do kill $pid; done" EXIT

# sudo scp -r -i iot-test.pem  iot-device-simulator/ ec2-user@ec2-34-245-59-249.eu-west-1.compute.amazonaws.com:~/
# sudo scp -r -i iot-test.pem iot-device-simulator/ ec2-user@ec2-52-213-41-72.eu-west-1.compute.amazonaws.com