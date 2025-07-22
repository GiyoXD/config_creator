# Implementation Plan

- [x] 1. Set up project structure and core data models
  - Create directory structure for the config generator module
  - Define data classes for QuantityAnalysisData, SheetData, HeaderPosition, and FontInfo
  - Create ConfigurationData and SheetConfig data classes
  - Write unit tests for data model validation
  - _Requirements: 1.1, 1.4_

- [x] 2. Implement TemplateLoader component




  - Create TemplateLoader class to load sample_config.json as base template
  - Implement template structure validation
  - Add error handling for template file operations and JSON parsing
  - Write unit tests for TemplateLoader with valid and invalid templates
  - _Requirements: 1.1, 2.1_

- [x] 3. Implement QuantityDataLoader component








  - Create QuantityDataLoader class with load_quantity_data method
  - Implement JSON structure validation for quantity analysis format
  - Add error handling for file operations and JSON parsing
  - Write unit tests for QuantityDataLoader with valid and invalid inputs
  - _Requirements: 1.2, 1.5_

- [x] 4. Implement HeaderTextUpdater component





  - Create HeaderTextUpdater class with header text mapping dictionary
  - Implement update_header_texts method to replace text values in header_to_write sections
  - Add special case handling for "Cargo Descprition" → col_po mapping
  - Write unit tests for header text updates with various header variations
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9_

- [x] 5. Implement FontUpdater component





  - Create FontUpdater class with update_fonts method
  - Implement font replacement in styling sections (header_font and default_font)
  - Add font information extraction from quantity analysis data
  - Write unit tests for font updates in styling sections
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 6. Implement PositionUpdater component





  - Create PositionUpdater class with update_start_rows method
  - Implement start_row replacement using analysis data (Contract: 18, Invoice: 21, Packing list: 22)
  - Add column position updates for header_to_write sections while preserving rowspan/colspan
  - Write unit tests for position updates
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.4_

- [x] 7. Implement ConfigWriter component








  - Create ConfigWriter class with write_config method
  - Add validate_completeness method to ensure all template sections are preserved
  - Implement JSON output formatting and file writing
  - Write unit tests for config writing and validation
  - _Requirements: 2.2, 2.3, 2.4_

- [x] 8. Create main ConfigGenerator orchestrator
















  - Create main ConfigGenerator class that coordinates all components
  - Implement template-based update workflow: load template → load quantity data → update specific fields → write output
  - Add error handling and logging throughout the process
  - Write unit tests for the orchestration logic
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 9. Add comprehensive error handling and validation
















  - Implement input validation for template and quantity data files
  - Add fallback strategies for missing or unrecognized headers
  - Create template preservation validation to ensure no business logic is lost
  - Add file operation error handling
  - Write unit tests for error scenarios
  - _Requirements: All error handling aspects_

- [x] 10. Create integration tests with real data






  - Write integration tests using the provided quantity_mode_analysis.json and sample_config.json
  - Test complete template-based transformation workflow
  - Verify that generated configs preserve all business logic from template
  - Test with different header naming conventions and edge cases
  - Validate that output matches expected structure and content
  - _Requirements: All requirements validation_

- [x] 11. Create CLI interface for easy command-line usage



  - Create command-line interface script with argument parsing
  - Add support for template, quantity data, and output file paths
  - Implement help documentation and usage examples
  - Add verbose/quiet modes for different logging levels
  - Include validation and error reporting for CLI usage
  - Write tests for CLI functionality
  - _Requirements: User-friendly interface for config generation_