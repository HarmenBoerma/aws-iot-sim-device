# Get sim app
sudo yum install git -y
git clone https://github.com/HarmenBoerma/aws-iot-sim-device.git
cd aws-iot-sim-device/

# setup AWS credentials
cp -r src/aws_config/ ~/.aws
aws configure

# start sim app
bash start_device.sh