# Header Mapping Guide

## Overview
The system now uses intelligent fuzzy matching to automatically map headers from your Excel files to the correct column IDs. However, you can customize mappings for unconventional or specific header names.

## How It Works

### 1. Automatic Smart Matching
The system automatically handles common variations:
- **P.O. variations**: "P.O Nº", "P.O. No.", "PON", "Purchase Order" → `col_po`
- **Description variations**: "Description", "Desc", "Commodity", "Name of Commodity" → `col_desc`
- **Quantity variations**: "Quantity", "Qty", "Quantity (SF)", "QTY SF" → `col_qty_sf`
- **Price variations**: "Unit Price", "Price", "Unit Cost", "FCA" → `col_unit_price`
- **Amount variations**: "Amount", "Total Value", "Total Amount" → `col_amount`

### 2. Special Character Handling
The system automatically normalizes special characters:
- `Nº` and `N°` → `No`
- Removes dots, parentheses, and other punctuation
- Handles line breaks (`\n`) in headers
- Case-insensitive matching

### 3. Custom Mappings
You can add custom mappings in `mapping_config.json`:

```json
{
  "header_text_mappings": {
    "mappings": {
      "Your Custom Header": "col_po",
      "Weird Header Name": "col_desc",
      "Name of\nCormodity": "col_desc"
    }
  }
}
```

## Common Issues and Solutions

### Issue: Header not recognized
**Solution**: Add it to `mapping_config.json`
```json
"Your Unrecognized Header": "target_column_id"
```

### Issue: Header mapped to wrong column
**Solution**: Override in `mapping_config.json`
```json
"Problematic Header": "correct_column_id"
```

### Issue: Special characters causing problems
**Solution**: The system handles most special characters automatically, but you can add exact mappings:
```json
"Header with º or ñ": "col_target"
```

## Available Column IDs

| Column ID | Purpose | Common Headers |
|-----------|---------|----------------|
| `col_static` | Mark & Number | "Mark & Nº", "Mark & No" |
| `col_po` | Purchase Order | "P.O. Nº", "P.O No", "Purchase Order" |
| `col_item` | Item Number | "ITEM Nº", "Item No", "HL ITEM" |
| `col_desc` | Description | "Description", "Commodity", "Product" |
| `col_qty_sf` | Quantity (SF) | "Quantity (SF)", "Qty SF", "Square Feet" |
| `col_qty_pcs` | Quantity (PCS) | "PCS", "Pieces", "Quantity (PCS)" |
| `col_unit_price` | Unit Price | "Unit Price", "Price", "FCA" |
| `col_amount` | Amount/Total | "Amount", "Total Value", "Total" |
| `col_no` | Number/Sequence | "No.", "Number", "Seq" |
| `col_net` | Net Weight | "N.W (kgs)", "Net Weight" |
| `col_gross` | Gross Weight | "G.W (kgs)", "Gross Weight" |
| `col_cbm` | Volume | "CBM", "Cubic Meter" |
| `col_pallet` | Pallet Number | "Pallet No", "Pallet" |
| `col_remarks` | Remarks/Notes | "Remarks", "Notes", "Comment" |

## Testing Your Mappings

1. Add your custom mapping to `mapping_config.json`
2. Run the generator: `python generate_config_ascii.py your_data.json`
3. Check the output for any warnings about unrecognized headers
4. Adjust mappings as needed

## Pro Tips

1. **Use exact header text**: Copy the exact header text from the warning messages
2. **Check for hidden characters**: Headers with line breaks need `\n` in the mapping
3. **Test incrementally**: Add one mapping at a time and test
4. **Use descriptive names**: The system is smart enough to match similar meanings

## Example Configuration

```json
{
  "header_text_mappings": {
    "mappings": {
      "P.O. Nº": "col_po",
      "Name of\nCormodity": "col_desc",
      "Custom Product Code": "col_item",
      "Special Price Field": "col_unit_price",
      "Weird Total Column": "col_amount"
    }
  }
}
```

This makes the system much more flexible and user-friendly while maintaining intelligent automatic matching!