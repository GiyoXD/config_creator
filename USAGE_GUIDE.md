# Usage Guide - Automated Invoice Config Generator

## Quick Start

Generate a configuration from an Excel file:
```bash
python main.py path/to/your/invoice.xlsx
```

## Basic Commands

### Generate Configuration (Default)
```bash
python main.py invoice.xlsx
```
- Creates: `invoice_config.json`
- Creates: `invoice_headers_found.txt`

### Specify Output File
```bash
python main.py invoice.xlsx -o my_config.json
```

### Use Custom Template
```bash
python main.py invoice.xlsx -t path/to/template.json
```

## Advanced Options

### Interactive Mode
Add missing header mappings interactively:
```bash
python main.py invoice.xlsx --interactive
```

### Generate Processed XLSX
Create a processed Excel file with text replacement and row removal:
```bash
python main.py invoice.xlsx --generate-xlsx
```

### Specify XLSX Output
```bash
python main.py invoice.xlsx --generate-xlsx --xlsx-output processed.xlsx
```

### Verbose Output
See detailed processing information:
```bash
python main.py invoice.xlsx -v
```

### Keep Intermediate Files
Keep the analysis JSON file:
```bash
python main.py invoice.xlsx --keep-intermediate
```

## Complete Example

```bash
python main.py "CT&INV&PL MT2-25005E DAP.xlsx" \
  -o final_config.json \
  --interactive \
  --generate-xlsx \
  --xlsx-output processed.xlsx \
  -v
```

## What It Does

1. **Analyzes** your Excel file to extract structure, fonts, and data positions
2. **Generates** a configuration file based on the analysis and template
3. **Creates** a header log showing which headers were found and mapped
4. **Optionally** processes the Excel file with text replacement and row removal

## Output Files

- `*_config.json` - Final configuration file
- `*_headers_found.txt` - Header analysis and mapping status
- `*_processed.xlsx` - Processed Excel file (if --generate-xlsx used)

## Need Help?

Check the header log file to see which headers need mapping, then use interactive mode or manually add mappings to `mapping_config.json`. 