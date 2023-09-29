cd ..
cd ..
aws s3 cp s3://reuters-mp3-readout . --recursive
aws s3 rm s3://reuters-mp3-readout --recursive