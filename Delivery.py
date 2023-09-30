import subprocess
import sys
import os
import logging

logging.basicConfig(filename='´Delivery.log', filemode='w',format='%(name)s - %(levelname)s - %(message)s')

# Check if the correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python Delivery.py h1_cleaned filename")
    sys.exit(1)

# Get the arguments
h1_cleaned = sys.argv[1]
filename = sys.argv[2]

# Construct the local file path
local_file_path = os.path.join(filename)

# Construct the AWS CLI command as a list of strings
aws_command = [
    'aws',
    'polly',
    'start-speech-synthesis-task',
    '--engine',
    'standard',
    '--language-code',
    'en-US',
    '--output-format',
    'mp3',
    '--output-s3-bucket-name',
    'reuters-mp3-readout',
    '--output-s3-key-prefix',
    h1_cleaned,  # Use h1_cleaned directly
    '--text-type',
    'text',
    '--voice-id',
    'Joanna',
    '--text',
    f'file://{local_file_path}'  # Use 'file://' to specify a local file
]

# Run the command in CMD.
result = subprocess.run(aws_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Print the output and errors, if any.
print("Output:")
john=result.stdout.decode('utf-8')
logging.info(john)
  # Decode the output as UTF-8

print("Errors:")
logging.warning(result.stderr.decode('utf-8')) # Decode the error messages as UTF-8
