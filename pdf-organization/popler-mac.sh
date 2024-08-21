#!/bin/bash

# Check if qpdf is installed
if ! command -v qpdf &> /dev/null; then
    echo "Error: qpdf is required. Please install it using Homebrew:"
    echo "brew install qpdf"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p output

# Process each PDF file in the current directory
for file in *.pdf; do
    # Check if there are actually PDF files
    if [ ! -f "$file" ]; then
        echo "No PDF files found in the current directory."
        exit 0
    fi

    # Extract first 4 pages
    qpdf --empty --pages "$file" 1-4 -- "output/${file%.pdf}_temp.pdf"

    # Move the processed file to the output directory
    mv "output/${file%.pdf}_temp.pdf" "output/$file"

    echo "Processed: $file"
done

echo "All files processed. Results are in the 'output' directory."