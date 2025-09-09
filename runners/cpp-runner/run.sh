#!/bin/bash

# Set strict error handling
set -euo pipefail

# Timeout for execution (10 seconds)
TIMEOUT=10

# Create temporary directory for execution
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Copy the user code from stdin to a file
cat > solution.cpp

# Create the input file from the first argument
if [ $# -ge 1 ]; then
    echo "$1" > input.txt
else
    echo "" > input.txt
fi

# Compile the C++ code
if ! timeout 30 g++ -o solution solution.cpp -std=c++17 2> compile_error.txt; then
    echo "COMPILATION_ERROR"
    cat compile_error.txt >&2
    exit 1
fi

# Run the compiled program with timeout and capture output
timeout $TIMEOUT ./solution < input.txt > output.txt 2> error.txt

# Check if the program ran successfully
if [ $? -eq 0 ]; then
    # Success - output the result
    cat output.txt
    exit 0
else
    # Runtime error occurred
    echo "RUNTIME_ERROR"
    cat error.txt >&2
    exit 1
fi