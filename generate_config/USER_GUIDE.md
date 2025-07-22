# Config Generator - User Guide

This comprehensive guide will walk you through using the Config Generator system to create Excel configuration files from your quantity analysis data.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Understanding the System](#understanding-the-system)
4. [Working with Mappings](#working-with-mappings)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)
8. [Examples](#examples)

## Getting Started

### Prerequisites

- Python 3.7 or higher installed
- Windows OS (for batch script) or any OS (for Python scripts)
- Your quantity analysis data in JSON format

### First Run

1. **Place your quantity data file** in the same directory as `generate_config.bat`
2. **Double-click** `generate_config.bat` or run from command line:
   ```bash
   .\generate_config.bat your_quantity_data.json
   ```
3. **Check the output** - you'll see either success or warnings about missing mappings

## Basic Usage

### Command Line Interface

The main interface is through `generate_config_ascii.py`:

```bash
# Basic usage
python generate_config_ascii.py quantity_data.json

# Specify custom output file
python generate_config_ascii.py quantity_data.json -o my_config.json

# Use custom template
python generate_config_ascii.py quantity_data.json -t my_template.json

# Verbose output (see detailed processing)
python generate_config_ascii.py quantity_data.json -v

# Quiet mode (only show errors)
python generate_config_ascii.py quantity_data.json -q

# Validate files only (don't generate output)
python generate_config_ascii.py quantity_data.json --validate-only

# Show information about quantity data
python generate_config_ascii.py quantity_data.json --show-info
```

### Windows Batch Script

For convenience, use the batch script:

```bash
# Basic usage
.\generate_config.bat quantity_data.json

# The batch script automatically passes all arguments to the Python script
.\generate_config.bat quantity_data.json -o custom_output.json -v
```

## Understanding the System

### What the System Does

The Config Generator performs a **template-based update workflow**:

1. **Loads** your template configuration (`sample_config.json`)
2. **Loads** your quantity analysis data
3. **Updates** specific fields while preserving business logic:
   - Start row positions
   - Font information (names and sizes)
   - Header texts
4. **Writes** the complete, ready-to-use configuration

### Input Files

#### Quantity Analysis Data
Your JSON file should contain:
```json
{
  "file_path": "path/to/your/excel/file.xlsx",
  "timestamp": "2025-01-01T12:00:00",
  "sheets": [
    {
      "sheet_name": "INV",
      "header_font": {"name": "Times New Roman", "size": 16.0},
      "data_font": {"name": "Times New Roman", "size": 15.0},
      "start_row": 21,
      "header_positions": [
        {"keyword": "P.O.", "row": 20, "column": 1},
        {"keyword": "ITEM", "row": 20, "column": 3}
      ]
    }
  ]
}
```

#### Template Configuration
The `sample_config.json` contains your business logic and should not be modified directly.

### Output Files

- **Main config**: `{input_name}_config.json` - Your generated configuration
- **Mapping report**: `{input_name}_config_mapping_report.txt` - Items needing attention

## Working with Mappings

### Understanding Mappings

The system uses two types of mappings:

1. **Sheet Name Mappings**: Map quantity data sheet names to template sheet names
   - `"INV"` → `"Invoice"`
   - `"PAK"` → `"Packing list"`

2. **Header Text Mappings**: Map header texts to column IDs
   - `"P.O. Nº"` → `"col_po"`
   - `"ITEM Nº"` → `"col_item"`

### Managing Mappings

#### View Current Mappings
```bash
python add_mapping.py --list-mappings
```

#### Add Sheet Name Mapping
```bash
python add_mapping.py --add-sheet "ACTUAL_SHEET_NAME:Template Sheet Name"

# Examples:
python add_mapping.py --add-sheet "INVOICE_2024:Invoice"
python add_mapping.py --add-sheet "PACKING_LIST:Packing list"
```

#### Add Header Text Mapping
```bash
python add_mapping.py --add-header "ACTUAL_HEADER:col_id"

# Examples:
python add_mapping.py --add-header "TOTAL AMOUNT:col_amount"
python add_mapping.py --add-header "ITEM CODE:col_item"
python add_mapping.py --add-header "NET WEIGHT KG:col_net"
```

### Standard Column IDs

| Column ID | Purpose | Common Headers |
|-----------|---------|----------------|
| `col_static` | Mark & Number | "Mark & Nº", "MARK & NOTE" |
| `col_po` | Purchase Order | "P.O Nº", "P.O. NO." |
| `col_item` | Item Number | "ITEM Nº", "HL ITEM" |
| `col_desc` | Description | "Description", "DESCRIPTION" |
| `col_qty_sf` | Quantity (SF) | "Quantity", "QUANTITY  (SQFT)" |
| `col_qty_pcs` | Quantity (PCS) | "PCS" |
| `col_unit_price` | Unit Price | "Unit price (USD)", "FCA" |
| `col_amount` | Total Amount | "Amount(USD)", "Total value(USD)" |
| `col_net` | Net Weight | "N.W (kgs)", "NW(KGS)" |
| `col_gross` | Gross Weight | "G.W (kgs)", "GW(KGS)" |
| `col_cbm` | Cubic Meters | "CBM", "(CBM)" |
| `col_pallet` | Pallet Number | "Pallet NO." |
| `col_remarks` | Remarks | "REMARKS" |
| `col_no` | Sequential Number | "No." |

## Advanced Usage

### Custom Configuration Files

You can use custom mapping configurations:

```bash
# Create custom mapping config
cp mapping_config.json my_custom_mappings.json

# Edit my_custom_mappings.json with your specific mappings

# Use with the helper tool
python add_mapping.py --config my_custom_mappings.json --list-mappings
```

### Batch Processing

Process multiple files:

```bash
# Process multiple files in sequence
for file in *.json; do
    echo "Processing $file..."
    .\generate_config.bat "$file"
done
```

### Integration with Other Tools

The system can be integrated into larger workflows:

```python
# Python integration example
from config_generator.config_generator import ConfigGenerator

generator = ConfigGenerator()
generator.generate_config(
    template_path="sample_config.json",
    quantity_data_path="data.json",
    output_path="output.json"
)
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Sheet not found" warnings
```
Warning: Missing start row data for sheets: ['ACTUAL_SHEET -> MAPPED_SHEET']
```

**Solution**: Add sheet name mapping
```bash
python add_mapping.py --add-sheet "ACTUAL_SHEET:Template Sheet"
```

#### Issue: Headers not updating
```
Warning: Unrecognized headers found: ['Sheet:HEADER_NAME']
```

**Solution**: Add header text mappings
```bash
python add_mapping.py --add-header "HEADER_NAME:col_appropriate_id"
```

#### Issue: Font information not updating
```
Warning: Missing font data for sheets: ['Sheet Name']
```

**Cause**: The quantity data doesn't contain font information for that sheet, or sheet name mapping is missing.

**Solution**: 
1. Check sheet name mapping
2. Verify quantity data contains font information

#### Issue: Start row not updating

**Cause**: Sheet name mapping is missing or quantity data doesn't contain start_row.

**Solution**: Add sheet name mapping and verify data structure.

### Debugging Steps

1. **Run with verbose output**:
   ```bash
   python generate_config_ascii.py data.json -v
   ```

2. **Check the mapping report** (automatically generated)

3. **Validate input files**:
   ```bash
   python generate_config_ascii.py data.json --validate-only
   ```

4. **Show quantity data info**:
   ```bash
   python generate_config_ascii.py data.json --show-info
   ```

## Best Practices

### File Organization
- Keep quantity data files in a dedicated folder
- Use descriptive names for output files
- Backup your `mapping_config.json` file

### Mapping Management
- **Start with common mappings**: Add frequently used variations first
- **Use consistent naming**: Follow the `col_*` convention for column IDs
- **Document patterns**: Keep notes on common variations you encounter
- **Test incrementally**: Add a few mappings, test, then add more

### Quality Control
- **Review mapping reports**: Check for suggestions and unrecognized items
- **Validate outputs**: Ensure generated configs work as expected
- **Keep templates updated**: Maintain your `sample_config.json`

### Workflow Optimization
1. **Process similar files together**: Group files with similar formats
2. **Build mapping libraries**: Create comprehensive mappings for each client/format
3. **Automate repetitive tasks**: Use batch scripts for common operations

## Examples

### Example 1: New Client with Different Format

**Scenario**: New client uses sheet "FACTURE" instead of "Invoice" and headers in French.

**Steps**:
1. Run initial generation:
   ```bash
   .\generate_config.bat client_data.json
   ```

2. Review warnings and mapping report

3. Add mappings:
   ```bash
   python add_mapping.py --add-sheet "FACTURE:Invoice"
   python add_mapping.py --add-header "Numéro P.O:col_po"
   python add_mapping.py --add-header "Quantité:col_qty_sf"
   python add_mapping.py --add-header "Prix unitaire:col_unit_price"
   ```

4. Re-run generation:
   ```bash
   .\generate_config.bat client_data.json
   ```

### Example 2: Multiple File Processing

**Scenario**: Process multiple files with similar format.

**Steps**:
1. Process first file and set up mappings
2. Create batch script:
   ```bash
   @echo off
   for %%f in (*.json) do (
       echo Processing %%f...
       .\generate_config.bat "%%f"
   )
   ```

### Example 3: Custom Template

**Scenario**: Use a custom template for specific client.

**Steps**:
1. Create custom template: `client_template.json`
2. Generate with custom template:
   ```bash
   python generate_config_ascii.py data.json -t client_template.json -o client_config.json
   ```

### Example 4: Validation Workflow

**Scenario**: Validate files before processing.

**Steps**:
1. Validate input:
   ```bash
   python generate_config_ascii.py data.json --validate-only
   ```

2. Show data info:
   ```bash
   python generate_config_ascii.py data.json --show-info
   ```

3. Generate if validation passes:
   ```bash
   python generate_config_ascii.py data.json -v
   ```

## Getting Help

### Resources
- **README.md**: Quick start and overview
- **MAPPING_GUIDE.md**: Detailed mapping configuration
- **Mapping reports**: Automatically generated guidance
- **Verbose output**: Detailed processing information

### Support Workflow
1. **Check the documentation** first
2. **Review error messages** and mapping reports
3. **Test with verbose output** to understand the process
4. **Try incremental changes** rather than large modifications

---

**Happy configuring!** 🎉

The Config Generator is designed to handle the complexity of Excel file variations while keeping the user experience simple. With proper mapping configuration, it can handle virtually any Excel format you encounter.