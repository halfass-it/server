#!/bin/bash

# Function to print colored output
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "\e[32mTest Passed\e[0m"
    else
        echo -e "\e[31mTest Failed\e[0m"
    fi
}

# Debug function to print commands being executed
debug_run() {
    echo -e "\e[34mRunning command:\e[0m $1"
    eval $1
}

# Begin testing
echo -e "\e[1mStarting test script...\e[0m"

# Command to be executed
command='echo "{\"data\": {\"auth\": \"username\", \"command\": \"ping\"}}" | nc localhost 1339'

# Print the command to be run
echo -e "\e[34mCommand to be executed:\e[0m $command"

# Run the command and capture the output
debug_run "$command"
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
