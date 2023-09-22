import subprocess

# Replace 'your_command_here' with the command you want to run in CMD.
command = 'aws polly start-speech-synthesis-task --engine standard --language-code en-US --output-format mp3 --output-s3-bucket-name reuters-mp3-readout --output-s3-key-prefix  --text-type text --voice-id Joanna'

# Run the command in CMD.
result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Print the output and errors, if any.
print("Output:")
print(result.stdout)

print("Errors:")
print(result.stderr)
