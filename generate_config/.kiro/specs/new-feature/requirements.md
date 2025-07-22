# Requirements Document

## Introduction

This feature will create a configuration generator that uses sample_config.json as a template and selectively replaces specific data points with values from quantity mode analysis JSON data. The tool will load the template configuration, extract header positions and font information from the analysis data, and update only the dynamic values while preserving all business logic, styling, and complex configurations from the template.

## Requirements

### Requirement 1

**User Story:** As a developer, I want to use sample_config.json as a template and only replace specific values from quantity mode analysis data, so that I can maintain all existing business logic while updating dynamic content.

#### Acceptance Criteria

1. WHEN the system starts THEN it SHALL load sample_config.json as the base template configuration
2. WHEN processing quantity mode analysis data THEN it SHALL extract only header positions, font information, and start row data for replacement
3. WHEN updating the template THEN it SHALL preserve all existing mappings, footer_configurations, styling rules, and business logic
4. WHEN replacing header_to_write sections THEN it SHALL update only the text values and positions while keeping all other attributes
5. WHEN updating font information THEN it SHALL replace only the font name and size values in styling sections

### Requirement 2

**User Story:** As a developer, I want the generated config to maintain the exact sample_config.json structure, so that it can be used seamlessly with existing processing systems without any compatibility issues.

#### Acceptance Criteria

1. WHEN loading the template THEN the system SHALL preserve the complete structure including all sections: sheets_to_process, sheet_data_map, data_mapping
2. WHEN updating configurations THEN the system SHALL maintain all existing sections: mappings, footer_configurations, styling, column_id_styles, number_formats
3. WHEN replacing font information THEN the system SHALL update header_font and default_font values in styling sections using analysis data
4. WHEN updating start_row values THEN the system SHALL replace only the start_row field while keeping all other sheet configuration intact

### Requirement 3

**User Story:** As a developer, I want accurate header text mapping based on actual data patterns, so that header_to_write sections are updated with correct text while maintaining existing column IDs from the template.

#### Acceptance Criteria

1. WHEN encountering "Mark & Nº" headers THEN the system SHALL update the text in col_static entries
2. WHEN encountering "P.O Nº" or "P.O. Nº" patterns THEN the system SHALL update the text in col_po entries
3. WHEN encountering "ITEM Nº" or "HL ITEM" keywords THEN the system SHALL update the text in col_item entries  
4. WHEN encountering "Description" or "Cargo Descprition" keywords THEN the system SHALL map "Cargo Descprition" to col_po and "Description" to col_desc
5. WHEN encountering "Quantity" headers THEN the system SHALL update the text in quantity-related entries (col_qty_sf, col_qty_pcs)
6. WHEN encountering "Unit price", "FCA", or "Amount" headers THEN the system SHALL update text in col_unit_price or col_amount entries respectively
7. WHEN encountering "N.W (kgs)" or "G.W (kgs)" headers THEN the system SHALL update text in col_net and col_gross entries
8. WHEN encountering "CBM" headers THEN the system SHALL update text in col_cbm entries
9. WHEN encountering "PCS" or "SF" sub-headers THEN the system SHALL update text in col_qty_pcs and col_qty_sf entries

### Requirement 4

**User Story:** As a developer, I want to update header positions while preserving the template's multi-row structure and spanning attributes, so that complex header layouts remain intact.

#### Acceptance Criteria

1. WHEN updating header_to_write entries THEN the system SHALL preserve existing row, col, rowspan, and colspan attributes from the template
2. WHEN updating header text THEN the system SHALL replace only the text field while keeping all positioning attributes
3. WHEN processing multi-row headers THEN the system SHALL maintain the template's row structure (row: 0, row: 1) and spanning rules
4. WHEN updating "PCS" and "SF" sub-headers THEN the system SHALL preserve their row: 1 positioning under the Quantity parent
5. WHEN updating column positions THEN the system SHALL adjust col values based on actual header positions from analysis data while preserving spans

### Requirement 5

**User Story:** As a developer, I want to preserve all template sheet configurations while updating only the dynamic values, so that business logic and mappings remain intact.

#### Acceptance Criteria

1. WHEN processing sheets THEN the system SHALL preserve existing sheet_data_map values from the template ("aggregation" for Invoice/Contract, "processed_tables_multi" for Packing list)
2. WHEN updating sheet configurations THEN the system SHALL preserve all existing mappings, footer_configurations, and styling sections from the template
3. WHEN updating start_row values THEN the system SHALL replace the start_row field with values from the analysis data (18 for Contract, 21 for Invoice, 22 for Packing list)
4. WHEN processing sheets THEN the system SHALL maintain all existing column IDs and their associated business logic from the template
5. WHEN updating configurations THEN the system SHALL preserve all template sections including static_content_before_footer, merge_rules, and data_cell_merging_rule

### Requirement 6

**User Story:** As a developer, I want to update font information from analysis data while preserving all other styling rules, so that the visual appearance matches the source document.

#### Acceptance Criteria

1. WHEN updating header fonts THEN the system SHALL replace header_font name and size in styling sections with header_font data from quantity analysis
2. WHEN updating default fonts THEN the system SHALL replace default_font name and size in styling sections with data_font data from quantity analysis
3. WHEN updating footer fonts THEN the system SHALL replace footer font information to match the header font from analysis data
4. WHEN updating font sizes THEN the system SHALL preserve any existing font size relationships and hierarchy rules from the template
5. WHEN updating styling THEN the system SHALL preserve all other styling attributes including alignment, number_formats, column_widths, and row_heights from the template