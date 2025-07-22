# Design Document

## Overview

The Config Generator is a Python-based tool that uses sample_config.json as a template and selectively replaces specific values with data from quantity mode analysis JSON. The system loads the complete template configuration, extracts header positions and font information from the analysis data, and updates only the dynamic values while preserving all business logic, mappings, and styling rules from the template.

## Architecture

The system follows a template-based architecture with selective data replacement:

```
ConfigGenerator
├── TemplateLoader - Loads sample_config.json as base template
├── QuantityDataLoader - Loads and validates quantity mode analysis data
├── HeaderTextUpdater - Updates header text values in header_to_write sections
├── FontUpdater - Updates font information in styling sections
├── PositionUpdater - Updates start_row and column positions
└── ConfigWriter - Outputs the updated configuration JSON
```

## Components and Interfaces

### TemplateLoader
**Purpose:** Load and validate the sample_config.json template
**Interface:**
```python
class TemplateLoader:
    def load_template(self, template_path: str) -> Dict
    def validate_template_structure(self, template: Dict) -> bool
```

### QuantityDataLoader
**Purpose:** Load and validate quantity mode analysis data
**Interface:**
```python
class QuantityDataLoader:
    def load_quantity_data(self, file_path: str) -> Dict
    def validate_structure(self, data: Dict) -> bool
```

### HeaderTextUpdater
**Purpose:** Update header text values in header_to_write sections
**Interface:**
```python
class HeaderTextUpdater:
    def __init__(self):
        self.header_mappings = {
            'Mark & Nº': 'col_static',
            'P.O Nº': 'col_po',
            'P.O. Nº': 'col_po', 
            'ITEM Nº': 'col_item',
            'HL ITEM': 'col_item',
            'Description': 'col_desc',
            'Cargo Descprition': 'col_po',  # Special case mapping
            # ... other mappings
        }
    
    def update_header_texts(self, template: Dict, quantity_data: Dict) -> Dict
    def map_header_to_column_id(self, header_text: str) -> str
```

### FontUpdater
**Purpose:** Update font information in styling sections
**Interface:**
```python
class FontUpdater:
    def update_fonts(self, template: Dict, quantity_data: Dict) -> Dict
    def update_header_fonts(self, styling: Dict, header_font: Dict) -> Dict
    def update_default_fonts(self, styling: Dict, data_font: Dict) -> Dict
```

### PositionUpdater
**Purpose:** Update start_row and column positions
**Interface:**
```python
class PositionUpdater:
    def update_start_rows(self, template: Dict, quantity_data: Dict) -> Dict
    def update_column_positions(self, template: Dict, quantity_data: Dict) -> Dict
```

### ConfigWriter
**Purpose:** Output the updated configuration
**Interface:**
```python
class ConfigWriter:
    def write_config(self, config: Dict, output_path: str) -> None
    def validate_completeness(self, config: Dict) -> bool
```

## Data Models

### QuantityAnalysisData
```python
@dataclass
class QuantityAnalysisData:
    file_path: str
    timestamp: str
    sheets: List[SheetData]

@dataclass 
class SheetData:
    sheet_name: str
    header_font: FontInfo
    data_font: FontInfo
    start_row: int
    header_positions: List[HeaderPosition]

@dataclass
class HeaderPosition:
    keyword: str
    row: int
    column: int

@dataclass
class FontInfo:
    name: str
    size: float
```

### ConfigurationData
```python
@dataclass
class ConfigurationData:
    sheets_to_process: List[str]
    sheet_data_map: Dict[str, str]
    data_mapping: Dict[str, SheetConfig]

@dataclass
class SheetConfig:
    start_row: int
    header_to_write: List[HeaderEntry]
    mappings: Dict
    footer_configurations: Dict
    styling: Dict
```

## Error Handling

### Input Validation
- Validate JSON structure matches expected quantity analysis format
- Check for required fields (sheet_name, header_positions, fonts, start_row)
- Verify header positions have valid row/column values

### Pattern Matching Fallbacks
- If header pattern matching fails, use position-based fallback mapping
- Log unrecognized headers for manual review
- Provide default column IDs for unmapped headers

### Configuration Completeness
- Validate all required configuration sections are present
- Check font size hierarchy rules are followed
- Ensure column ID consistency across mappings

### File Operations
- Handle file not found errors gracefully
- Validate output directory permissions
- Provide clear error messages for JSON parsing failures

## Testing Strategy

### Unit Tests
- Test HeaderMapper pattern matching with various header text variations
- Test FontStyler font hierarchy enforcement
- Test ConfigBuilder section generation
- Test JSONLoader validation logic

### Integration Tests  
- Test complete transformation from quantity JSON to config JSON
- Test with real quantity analysis data samples
- Verify generated configs match sample_config.json structure

### Edge Case Tests
- Test with missing header information
- Test with unusual font size combinations
- Test with multi-row header structures
- Test with sheets containing different header counts

### Validation Tests
- Verify generated configs can be loaded by existing processing systems
- Test configuration completeness validation
- Test pattern matching accuracy with various header naming conventions

## Implementation Details

### Header Text Mapping Strategy
The HeaderTextUpdater will use direct mapping for known header variations:
```python
HEADER_TEXT_MAPPINGS = {
    'Mark & Nº': 'col_static',
    'P.O Nº': 'col_po',
    'P.O. Nº': 'col_po',
    'ITEM Nº': 'col_item', 
    'HL ITEM': 'col_item',
    'Description': 'col_desc',
    'Cargo Descprition': 'col_po',  # Special mapping case
    'Quantity': 'col_qty_sf',
    'Unit price (USD)': 'col_unit_price',
    'FCA\nSVAY RIENG': 'col_unit_price',
    'Amount': 'col_amount',
    'Amount (USD)': 'col_amount',
    'N.W (kgs)': 'col_net',
    'G.W (kgs)': 'col_gross',
    'CBM': 'col_cbm',
    'PCS': 'col_qty_pcs',
    'SF': 'col_qty_sf'
}
```

### Template-Based Update Process
1. Load sample_config.json as complete template
2. Extract header positions and fonts from quantity analysis data
3. Update only specific fields while preserving template structure:
   - Replace header text in header_to_write sections
   - Update start_row values for each sheet
   - Replace font information in styling sections
   - Preserve all mappings, footer_configurations, and business logic

### Font Information Update
Replace font values in styling sections:
```python
def update_font_info(styling_section, header_font, data_font):
    styling_section['header_font']['name'] = header_font['name']
    styling_section['header_font']['size'] = header_font['size']
    styling_section['default_font']['name'] = data_font['name']
    styling_section['default_font']['size'] = data_font['size']
    return styling_section
```

### Selective Data Replacement
The system performs minimal, targeted updates:
- start_row values: Use analysis data (Contract: 18, Invoice: 21, Packing list: 22)
- header_to_write text: Replace with actual header text from analysis
- font information: Replace with analysis font data
- All other sections: Preserve exactly from template