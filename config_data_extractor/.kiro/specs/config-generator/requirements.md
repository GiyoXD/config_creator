# Requirements Document

## Introduction

This feature will create a configuration generator that transforms quantity mode analysis JSON data into sample configuration format. The tool will extract header information, font details, and structural data from the quantity mode JSON and generate a properly formatted configuration file that matches the sample_config.json structure.

## Requirements

### Requirement 1

**User Story:** As a developer, I want to automatically generate configuration files from quantity mode analysis data, so that I can quickly create properly formatted configs without manual transcription.

#### Acceptance Criteria

1. WHEN the system receives a quantity mode analysis JSON file THEN it SHALL extract header positions, font information, and start row data for each sheet
2. WHEN processing header positions THEN the system SHALL use pattern matching to map column keywords to appropriate column IDs regardless of exact text variations
3. WHEN generating the config THEN the system SHALL preserve the original font names and sizes from the analysis data
4. WHEN creating header_to_write sections THEN the system SHALL use the correct row and column positions from the analysis data
5. WHEN encountering header text variations THEN the system SHALL apply flexible pattern matching to identify semantic meaning

### Requirement 2

**User Story:** As a developer, I want the generated config to match the sample_config.json structure, so that it can be used seamlessly with existing processing systems.

#### Acceptance Criteria

1. WHEN generating the configuration THEN the system SHALL create the same top-level structure as sample_config.json (sheets_to_process, sheet_data_map, data_mapping)
2. WHEN creating sheet configurations THEN the system SHALL include all required sections: start_row, header_to_write, mappings, footer_configurations, and styling
3. WHEN setting font information THEN the system SHALL use the header_font data for header styling and data_font for default styling
4. WHEN generating header_to_write arrays THEN the system SHALL create proper row, col, text, and id mappings

### Requirement 3

**User Story:** As a developer, I want intelligent column ID mapping based on header patterns, so that headers with different names but similar meanings are automatically assigned appropriate semantic IDs.

#### Acceptance Criteria

1. WHEN encountering headers containing "Mark" keywords THEN the system SHALL assign "col_static" ID
2. WHEN encountering headers containing "P.O" patterns (with or without periods/spaces) THEN the system SHALL assign "col_po" ID  
3. WHEN encountering headers containing "ITEM" keywords THEN the system SHALL assign "col_item" ID
4. WHEN encountering headers containing "Description" or "Descprition" keywords THEN the system SHALL assign "col_desc" ID
5. WHEN encountering "Quantity" headers THEN the system SHALL assign appropriate quantity IDs based on position and context
6. WHEN encountering price-related headers (containing "price", "Unit", "FCA", "Amount") THEN the system SHALL assign "col_unit_price" or "col_amount" IDs based on context
7. WHEN encountering weight headers (containing "N.W", "G.W", "kgs") THEN the system SHALL assign "col_net" and "col_gross" IDs
8. WHEN encountering "CBM" headers THEN the system SHALL assign "col_cbm" ID
9. WHEN encountering "PCS" or "SQFT" sub-headers THEN the system SHALL assign "col_qty_pcs" and "col_qty_sf" IDs respectively

### Requirement 4

**User Story:** As a developer, I want proper handling of multi-row headers with correct row/column positioning, so that complex header structures are correctly processed.

#### Acceptance Criteria

1. WHEN generating header_to_write entries THEN the system SHALL use relative row positions (row: 0 for first header row, row: 1 for second header row) regardless of the actual start_row value
2. WHEN detecting headers that span multiple columns THEN the system SHALL add colspan attributes appropriately
3. WHEN detecting headers that span multiple rows THEN the system SHALL add rowspan attributes appropriately  
4. WHEN processing "PCS" and "SQFT" sub-headers THEN the system SHALL place them on row: 1 under their parent "Quantity" header
5. WHEN a header has gaps or spans (like "Quantity" covering both PCS and SF) THEN the system SHALL set rowspan: 2 for vertical spanning

### Requirement 5

**User Story:** As a developer, I want the system to handle different sheet types with proper data mapping and styling, so that all sheet configurations are complete and functional.

#### Acceptance Criteria

1. WHEN processing Invoice sheets THEN the system SHALL set sheet_data_map to "aggregation"
2. WHEN processing Contract sheets THEN the system SHALL set sheet_data_map to "aggregation"  
3. WHEN processing Packing list sheets THEN the system SHALL set sheet_data_map to "processed_tables_multi"
4. WHEN generating configurations THEN the system SHALL use the start_row value from the analysis data for the sheet's start_row configuration
5. WHEN creating mappings THEN the system SHALL use only predefined column IDs (col_static, col_po, col_item, col_desc, col_qty_sf, col_qty_pcs, col_unit_price, col_amount, col_net, col_gross, col_cbm, col_remarks, col_pallet, col_no)

### Requirement 6

**User Story:** As a developer, I want consistent font sizing and styling rules, so that the generated config maintains proper visual hierarchy.

#### Acceptance Criteria

1. WHEN setting header fonts THEN the system SHALL use the header_font data from the quantity analysis
2. WHEN setting default/data fonts THEN the system SHALL use the data_font data from the quantity analysis  
3. WHEN setting footer font styles THEN the system SHALL match the header font size and styling
4. WHEN data font size is larger than header font size THEN the system SHALL set data font size equal to or smaller than header font size
5. WHEN generating complete configurations THEN the system SHALL include all required sections: mappings, footer_configurations, styling, column_id_styles, number_formats, alignment settings, and row_heights to prevent configuration errors