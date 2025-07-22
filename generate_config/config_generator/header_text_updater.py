"""
HeaderTextUpdater component for updating header text values in configuration templates.

This module provides functionality to update header_to_write sections in configuration
templates with actual header text from quantity analysis data while preserving all
other attributes like positioning, spanning, and IDs.
"""

from typing import Dict, List, Any, Optional
import copy
from .models import QuantityAnalysisData, SheetData, HeaderPosition
from .mapping_manager import MappingManager, MappingManagerError


class HeaderTextUpdaterError(Exception):
    """Custom exception for HeaderTextUpdater errors."""
    pass


class HeaderTextUpdater:
    """Updates header text values in header_to_write sections of configuration templates."""
    
    def __init__(self, mapping_config_path: str = "mapping_config.json"):
        """Initialize HeaderTextUpdater with mapping manager."""
        # Initialize mapping manager
        try:
            self.mapping_manager = MappingManager(mapping_config_path)
        except MappingManagerError as e:
            print(f"Warning: Could not load mapping config: {e}")
            # Fallback to default mappings
            self.mapping_manager = None
        
        # Fallback header text mapping for when mapping manager is not available
        self.fallback_header_mappings = {
            # Mark & Nº variations
            'Mark & Nº': 'col_static',
            'Mark & N°': 'col_static',
            
            # P.O Nº variations  
            'P.O Nº': 'col_po',
            'P.O. Nº': 'col_po',
            'P.O N°': 'col_po',
            'P.O. N°': 'col_po',
            
            # ITEM Nº variations
            'ITEM Nº': 'col_item',
            'ITEM N°': 'col_item',
            'HL ITEM': 'col_item',
            
            # Description variations - special case handling
            'Description': 'col_desc',
            'Cargo Descprition': 'col_po',  # Special mapping per requirement 3.4
            
            # Quantity variations
            'Quantity': 'col_qty_sf',
            'Quantity\n(SF)': 'col_qty_sf',
            
            # Unit price variations
            'Unit price': 'col_unit_price',
            'Unit price (USD)': 'col_unit_price',
            'Unit price\n(USD)': 'col_unit_price',
            'Unit Price(USD)': 'col_unit_price',
            'FCA': 'col_unit_price',
            'FCA\nSVAY RIENG': 'col_unit_price',
            
            # Amount variations
            'Amount': 'col_amount',
            'Amount (USD)': 'col_amount',
            'Amount(USD)': 'col_amount',
            'Total value(USD)': 'col_amount',
            
            # Weight variations
            'N.W (kgs)': 'col_net',
            'G.W (kgs)': 'col_gross',
            
            # CBM variations
            'CBM': 'col_cbm',
            
            # Sub-header variations for quantity
            'PCS': 'col_qty_pcs',
            'SF': 'col_qty_sf',
            
            # Other common headers
            'No.': 'col_no',
            'Pallet\nNO.': 'col_pallet',
            'REMARKS': 'col_remarks'
        }
    
    def update_header_texts(self, template: Dict[str, Any], quantity_data: QuantityAnalysisData) -> Dict[str, Any]:
        """
        Update header text values in header_to_write sections using quantity analysis data.
        
        Args:
            template: Configuration template dictionary
            quantity_data: Quantity analysis data containing header positions
            
        Returns:
            Updated template with header texts replaced
            
        Raises:
            HeaderTextUpdaterError: If template structure is invalid or update fails
        """
        try:
            if not isinstance(template, dict):
                raise HeaderTextUpdaterError("Template must be a dictionary")
            
            if not isinstance(quantity_data, QuantityAnalysisData):
                raise HeaderTextUpdaterError("Quantity data must be QuantityAnalysisData instance")
            
            # Validate template structure
            self._validate_template_structure(template)
            
            # Create deep copy to avoid modifying original template
            updated_template = copy.deepcopy(template)
            
            # Process each sheet in the template
            data_mapping = updated_template.get('data_mapping', {})
            
            # Track unrecognized headers for fallback strategies
            unrecognized_headers = []
            
            for sheet_data in quantity_data.sheets:
                quantity_sheet_name = sheet_data.sheet_name
                mapped_sheet_name = self._map_sheet_name(quantity_sheet_name)
                
                if mapped_sheet_name not in data_mapping:
                    # Log missing sheet but continue processing
                    continue
                    
                sheet_config = data_mapping[mapped_sheet_name]
                header_to_write = sheet_config.get('header_to_write', [])
                
                # Update header texts for this sheet with fallback handling
                sheet_unrecognized = self._update_sheet_headers_with_fallback(
                    header_to_write, sheet_data.header_positions, mapped_sheet_name
                )
                unrecognized_headers.extend(sheet_unrecognized)
            
            # Apply fallback strategies for unrecognized headers
            if unrecognized_headers:
                self._apply_fallback_strategies(updated_template, unrecognized_headers)
            
            return updated_template
            
        except Exception as e:
            if isinstance(e, HeaderTextUpdaterError):
                raise
            raise HeaderTextUpdaterError(f"Header text update failed: {str(e)}") from e
    
    def _map_sheet_name(self, quantity_sheet_name: str) -> str:
        """
        Map quantity data sheet name to template config sheet name.
        
        Args:
            quantity_sheet_name: Sheet name from quantity data
            
        Returns:
            Mapped sheet name for template config, or original name if no mapping found
        """
        if self.mapping_manager:
            return self.mapping_manager.map_sheet_name(quantity_sheet_name)
        
        # Fallback to hardcoded mappings if mapping manager is not available
        fallback_mappings = {
            'INV': 'Invoice',
            'PAK': 'Packing list',
            'CON': 'Contract',
            'CONTRACT': 'Contract',
            'INVOICE': 'Invoice',
            'PACKING': 'Packing list',
            'PACKING LIST': 'Packing list'
        }
        
        return fallback_mappings.get(quantity_sheet_name.upper(), quantity_sheet_name)
    
    def _update_sheet_headers_with_fallback(self, header_to_write: List[Dict[str, Any]], 
                                           header_positions: List[HeaderPosition], sheet_name: str) -> List[str]:
        """
        Update header texts for a single sheet with fallback handling.
        
        Args:
            header_to_write: List of header entries to update
            header_positions: Header positions from quantity analysis
            sheet_name: Name of the sheet being processed
            
        Returns:
            List of unrecognized header keywords
        """
        try:
            # Validate inputs
            if not isinstance(header_to_write, list):
                raise HeaderTextUpdaterError(f"header_to_write for sheet '{sheet_name}' must be a list")
            
            if not isinstance(header_positions, list):
                raise HeaderTextUpdaterError(f"header_positions for sheet '{sheet_name}' must be a list")
            
            # Create mapping of column IDs to actual header texts from analysis data
            column_id_to_text = {}
            unrecognized_headers = []
            
            for i, header_pos in enumerate(header_positions):
                if not isinstance(header_pos, HeaderPosition):
                    raise HeaderTextUpdaterError(f"header_position {i} for sheet '{sheet_name}' must be HeaderPosition instance")
                
                keyword = header_pos.keyword
                if not keyword or not isinstance(keyword, str):
                    continue  # Skip invalid keywords
                
                column_id = self.map_header_to_column_id(keyword)
                
                if column_id:
                    column_id_to_text[column_id] = keyword
                else:
                    unrecognized_headers.append(f"{sheet_name}:{keyword}")
            
            # Update header_to_write entries with actual header texts
            for i, header_entry in enumerate(header_to_write):
                if not isinstance(header_entry, dict):
                    raise HeaderTextUpdaterError(f"header_entry {i} for sheet '{sheet_name}' must be a dictionary")
                
                if 'id' in header_entry and header_entry['id'] in column_id_to_text:
                    # Validate that text field exists and is modifiable
                    if 'text' not in header_entry:
                        raise HeaderTextUpdaterError(f"header_entry {i} for sheet '{sheet_name}' missing 'text' field")
                    
                    # Update text while preserving all other attributes
                    header_entry['text'] = column_id_to_text[header_entry['id']]
            
            return unrecognized_headers
            
        except Exception as e:
            if isinstance(e, HeaderTextUpdaterError):
                raise
            raise HeaderTextUpdaterError(f"Failed to update headers for sheet '{sheet_name}': {str(e)}") from e
    
    def _update_sheet_headers(self, header_to_write: List[Dict[str, Any]], header_positions: List[HeaderPosition]) -> None:
        """
        Update header texts for a single sheet (legacy method for backward compatibility).
        
        Args:
            header_to_write: List of header entries to update
            header_positions: Header positions from quantity analysis
        """
        self._update_sheet_headers_with_fallback(header_to_write, header_positions, "unknown")
    
    def map_header_to_column_id(self, header_text: str) -> Optional[str]:
        """
        Map header text to column ID using the mapping manager or fallback mappings.
        
        Args:
            header_text: Header text from quantity analysis
            
        Returns:
            Column ID string or None if no mapping found
        """
        if not isinstance(header_text, str):
            return None
        
        # Use mapping manager if available
        if self.mapping_manager:
            return self.mapping_manager.map_header_to_column_id(header_text)
        
        # Fallback to hardcoded mappings
        if header_text in self.fallback_header_mappings:
            return self.fallback_header_mappings[header_text]
        
        # Fallback: try case-insensitive matching for common variations
        header_lower = header_text.lower().strip()
        
        for mapped_header, column_id in self.fallback_header_mappings.items():
            if mapped_header.lower().strip() == header_lower:
                return column_id
        
        # Additional pattern matching for common cases
        if 'mark' in header_lower and ('nº' in header_lower or 'n°' in header_lower):
            return 'col_static'
        elif 'p.o' in header_lower and ('nº' in header_lower or 'n°' in header_lower):
            return 'col_po'
        elif 'item' in header_lower and ('nº' in header_lower or 'n°' in header_lower):
            return 'col_item'
        elif 'description' in header_lower:
            return 'col_desc'
        elif 'quantity' in header_lower:
            return 'col_qty_sf'
        elif 'unit price' in header_lower or 'unit_price' in header_lower:
            return 'col_unit_price'
        elif 'amount' in header_lower:
            return 'col_amount'
        elif 'n.w' in header_lower and 'kg' in header_lower:
            return 'col_net'
        elif 'g.w' in header_lower and 'kg' in header_lower:
            return 'col_gross'
        elif header_lower == 'cbm':
            return 'col_cbm'
        elif header_lower == 'pcs':
            return 'col_qty_pcs'
        elif header_lower == 'sf':
            return 'col_qty_sf'
        
        return None
    
    def _validate_template_structure(self, template: Dict[str, Any]) -> None:
        """
        Validate template structure for header text updates.
        
        Args:
            template: Template dictionary to validate
            
        Raises:
            HeaderTextUpdaterError: If template structure is invalid
        """
        if 'data_mapping' not in template:
            raise HeaderTextUpdaterError("Template missing 'data_mapping' section")
        
        data_mapping = template['data_mapping']
        if not isinstance(data_mapping, dict):
            raise HeaderTextUpdaterError("Template 'data_mapping' must be a dictionary")
        
        # Validate each sheet configuration has header_to_write
        for sheet_name, sheet_config in data_mapping.items():
            if not isinstance(sheet_config, dict):
                raise HeaderTextUpdaterError(f"Sheet config for '{sheet_name}' must be a dictionary")
            
            if 'header_to_write' not in sheet_config:
                raise HeaderTextUpdaterError(f"Sheet '{sheet_name}' missing 'header_to_write' section")
            
            header_to_write = sheet_config['header_to_write']
            if not isinstance(header_to_write, list):
                raise HeaderTextUpdaterError(f"'header_to_write' for sheet '{sheet_name}' must be a list")
    
    def _apply_fallback_strategies(self, template: Dict[str, Any], unrecognized_headers: List[str]) -> None:
        """
        Apply fallback strategies for unrecognized headers.
        
        Args:
            template: Template dictionary to update
            unrecognized_headers: List of unrecognized header strings in format "sheet:header"
        """
        if not unrecognized_headers:
            return
        
        # Log unrecognized headers for manual review
        # In a production system, this could write to a log file or send alerts
        print(f"Warning: Unrecognized headers found: {unrecognized_headers}")
        
        # Apply position-based fallback mapping
        data_mapping = template.get('data_mapping', {})
        
        for unrecognized in unrecognized_headers:
            if ':' not in unrecognized:
                continue
                
            sheet_name, header_text = unrecognized.split(':', 1)
            
            if sheet_name not in data_mapping:
                continue
            
            # Try position-based fallback
            self._apply_position_based_fallback(data_mapping[sheet_name], header_text)
    
    def _apply_position_based_fallback(self, sheet_config: Dict[str, Any], header_text: str) -> None:
        """
        Apply position-based fallback for unrecognized headers.
        
        Args:
            sheet_config: Sheet configuration dictionary
            header_text: Unrecognized header text
        """
        header_to_write = sheet_config.get('header_to_write', [])
        
        # Find headers without IDs (parent headers) and try to match by position
        for header_entry in header_to_write:
            if 'id' not in header_entry and 'text' in header_entry:
                # For parent headers, we can update text if it's similar
                existing_text = header_entry['text']
                if self._is_similar_header(existing_text, header_text):
                    header_entry['text'] = header_text
                    break
    
    def _is_similar_header(self, existing_text: str, new_text: str) -> bool:
        """
        Check if two header texts are similar enough to be considered the same.
        
        Args:
            existing_text: Existing header text
            new_text: New header text to compare
            
        Returns:
            True if headers are similar enough to match
        """
        if not isinstance(existing_text, str) or not isinstance(new_text, str):
            return False
        
        # Normalize both texts for comparison
        existing_norm = existing_text.lower().strip().replace(' ', '').replace('\n', '')
        new_norm = new_text.lower().strip().replace(' ', '').replace('\n', '')
        
        # Check for exact match after normalization
        if existing_norm == new_norm:
            return True
        
        # Check for partial matches (at least 70% similarity)
        if len(existing_norm) > 0 and len(new_norm) > 0:
            # Simple similarity check based on common characters
            common_chars = sum(1 for c in existing_norm if c in new_norm)
            similarity = common_chars / max(len(existing_norm), len(new_norm))
            return similarity >= 0.7
        
        return False