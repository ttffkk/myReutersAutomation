import subprocess
import sys
import os
import logging

# Configure logging with a more informative format
logging.basicConfig(filename='Delivery.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    logging.error("Usage: python Delivery.py h1_cleaned filename")
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

# Log the output and errors, if any.
logging.info("AWS Command Output:")
logging.info(result.stdout.decode('utf-8'))

logging.warning("AWS Command Error Messages:")
logging.warning(result.stderr.decode('utf-8'))
