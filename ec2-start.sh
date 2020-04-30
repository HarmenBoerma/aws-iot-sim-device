Content-Type: multipart/mixed; boundary='//'
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset='us-ascii'
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename='cloud-config.txt'

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset='us-ascii'
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename='userdata.txt'

#!/bin/bash
# Get sim app
sudo apt install git -y
git clone https://github.com/HarmenBoerma/aws-iot-sim-device.git
cd aws-iot-sim-device/

# setup AWS credentials
cp -r src/aws_config/ ~/.aws

# start sim app
bash start_devices.sh