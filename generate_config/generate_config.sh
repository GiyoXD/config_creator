#!/bin/bash
# Shell script for easy config generation
# Usage: ./generate_config.sh your_quantity_data.json

if [ $# -eq 0 ]; then
    echo "Usage: ./generate_config.sh your_quantity_data.json"
    echo ""
    echo "Example: ./generate_config.sh quantity_mode_analysis.json"
    echo "This will generate a ready-to-use configuration file."
    exit 1
fi

echo "🚀 Generating configuration from $1..."
python3 generate_config.py "$@"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your configuration is ready to use."
else
    echo ""
    echo "❌ Generation failed. Check the error messages above."
fi