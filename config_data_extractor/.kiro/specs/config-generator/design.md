# Design Document

## Overview

The Config Generator is a Python-based tool that transforms quantity mode analysis JSON data into sample configuration format. The system uses pattern matching to intelligently map header keywords to semantic column IDs, preserves font styling information, and generates complete configuration files that match the sample_config.json structure.

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
ConfigGenerator
├── JSONLoader - Loads and validates quantity mode analysis data
├── HeaderMapper - Maps header keywords to column IDs using pattern matching
├── ConfigBuilder - Constructs the configuration structure
├── FontStyler - Handles font and styling configurations
└── ConfigWriter - Outputs the final configuration JSON
```

## Components and Interfaces

### JSONLoader
**Purpose:** Load and validate input JSON data
**Interface:**
```python
class JSONLoader:
    def load_quantity_data(self, file_path: str) -> Dict
    def validate_structure(self, data: Dict) -> bool
```

### HeaderMapper
**Purpose:** Map header keywords to semantic column IDs using pattern matching
**Interface:**
```python
class HeaderMapper:
    def __init__(self):
        self.pattern_mappings = {
            'mark': 'col_static',
            'p\.?o\.?': 'col_po', 
            'item': 'col_item',
            'desc': 'col_desc',
            # ... other patterns
        }
    
    def map_header_to_id(self, header_text: str, position: int) -> str
    def detect_multi_row_structure(self, headers: List[Dict]) -> Dict
```

### ConfigBuilder
**Purpose:** Build the main configuration structure
**Interface:**
```python
class ConfigBuilder:
    def build_config(self, quantity_data: Dict) -> Dict
    def create_sheet_config(self, sheet_data: Dict) -> Dict
    def generate_header_to_write(self, headers: List[Dict]) -> List[Dict]
    def create_mappings_section(self, headers: List[Dict]) -> Dict
```

### FontStyler
**Purpose:** Handle font and styling configurations
**Interface:**
```python
class FontStyler:
    def extract_font_info(self, sheet_data: Dict) -> Tuple[Dict, Dict]
    def create_styling_config(self, header_font: Dict, data_font: Dict) -> Dict
    def ensure_font_hierarchy(self, header_font: Dict, data_font: Dict) -> Tuple[Dict, Dict]
```

### ConfigWriter
**Purpose:** Output the final configuration
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

### Pattern Matching Strategy
The HeaderMapper will use regex patterns to identify header types:
```python
HEADER_PATTERNS = {
    r'mark.*n[oº°]?': 'col_static',
    r'p\.?o\.?\s*n[oº°]?': 'col_po',
    r'item.*n[oº°]?': 'col_item',
    r'desc': 'col_desc',
    r'quantity': 'col_qty_sf',  # default, context-dependent
    r'unit.*price|fca': 'col_unit_price',
    r'amount': 'col_amount',
    r'n\.?w.*kg': 'col_net',
    r'g\.?w.*kg': 'col_gross',
    r'cbm': 'col_cbm',
    r'pcs': 'col_qty_pcs',
    r'sqft|sf': 'col_qty_sf'
}
```

### Multi-Row Header Handling
For complex headers like Packing list:
1. Identify parent headers (row 0) and child headers (row 1)
2. Calculate rowspan/colspan based on child header positions
3. Generate proper header_to_write entries with correct row/col values

### Font Size Hierarchy
Enforce font size rules:
```python
def ensure_font_hierarchy(header_font, data_font):
    if data_font.size > header_font.size:
        data_font.size = header_font.size
    return header_font, data_font
```

### Configuration Template
Use the sample_config.json as a template, replacing dynamic values:
- start_row from analysis data
- header_to_write from mapped headers  
- font information from analysis data
- Keep all other sections (mappings, footer_configurations, styling) as complete copies