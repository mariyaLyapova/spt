#!/bin/bash

# Unified Parking Data Processor Runner
# This script runs the processor.py with the specified input files

echo "🚀 Running Parking Data Processor..."
echo "=" * 50

# Check if input files exist
if [ ! -f "input/parking_data.xlsx" ]; then
    echo "❌ Error: input/parking_data.xlsx not found"
    exit 1
fi

if [ ! -f "input/Parking table.xlsx" ]; then
    echo "❌ Error: input/Parking table.xlsx not found"
    exit 1
fi

# Run the processor
echo "📊 Processing parking data..."
python3 processor.py "input/parking_data.xlsx" "input/Parking table.xlsx"

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Processing completed successfully!"
    echo "📁 Output file: parking_data.json"
    
    # Show file size if output exists
    if [ -f "parking_data.json" ]; then
        size=$(ls -lh parking_data.json | awk '{print $5}')
        echo "📏 File size: $size"
    fi
else
    echo ""
    echo "❌ Processing failed!"
    exit 1
fi