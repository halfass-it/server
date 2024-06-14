#!/bin/bash

# Function to print colored output
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "\e[32mTest Passed\e[0m"
    else
        echo -e "\e[31mTest Failed\e[0m"
    fi
}

# Begin testing
echo -e "\e[1mStarting test script...\e[0m"

# Set the URL to test, adjust as per your Nginx configuration
url="https://localhost/r0"

# Data to send in the request
data='{"auth": "username", "command": "ping"}'

# Command to be executed with curl
command="curl -sS -X POST -d '$data' -H 'Content-Type: application/json' --insecure $url"

# Print the command to be run
echo -e "\e[34mCommand to be executed:\e[0m $command"

# Run the command and capture the output
output=$(eval "$command")

# Check if the output matches the expected result
expected_output='{"data": {"auth": true, "command": "pong"}}'

echo -e "\e[1m\nComparing output:\e[0m"
echo "Expected output: $expected_output"
echo "Actual output  : $output"

if [ "$output" == "$expected_output" ]; then
    print_result 0
else
    print_result 1
    echo -e "\e[31mTest Failed\e[0m"
    echo "Expected output: $expected_output"
    echo "Actual output  : $output"
fi
