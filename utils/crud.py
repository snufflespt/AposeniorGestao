"""Unified CRUD Operations for Streamlit App

This module provides standardized database operations and utility functions
for consistent data management across all sections of the application.
"""

import streamlit as st
import pandas as pd
from typing import Any, Dict, List, Optional, Callable, Union
from utils.sheets import get_worksheet


# ===== DATA TYPE DEFINITIONS =====

class SheetConfig:
    """Configuration for a specific Google Sheet worksheet.

    Attributes:
        name (str): Name of the worksheet
        id_column (str): Column name for unique identifiers
        id_prefix (str): Prefix for generating new IDs (e.g., 'P', 'U')
        required_columns (List[str]): Columns that must have values
        unique_columns (List[str]): Columns that must have unique values
        conflict_rules (Optional[Dict[str, Any]]): Rules for checking conflicts
    """

    def __init__(self,
                 name: str,
                 id_column: str = 'ID',
                 id_prefix: str = '',
                 required_columns: Optional[List[str]] = None,
                 unique_columns: Optional[List[str]] = None,
                 conflict_rules: Optional[Dict[str, Any]] = None):
        self.name = name
        self.id_column = id_column
        self.id_prefix = id_prefix
        self.required_columns = required_columns or []
        self.unique_columns = unique_columns or []
        self.conflict_rules = conflict_rules or {}


# ===== CRUD OPERATIONS =====

@st.cache_data(ttl=300)
def get_sheet_data(sheet_name: str) -> pd.DataFrame:
    """Retrieve all data from a Google Sheet as a DataFrame with caching.

    Args:
        sheet_name (str): Name of the worksheet

    Returns:
        pandas.DataFrame: Data from the worksheet
    """
    try:
        sheet = get_worksheet(sheet_name)
        records = sheet.get_all_records()
        return pd.DataFrame(records)
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha {sheet_name}: {str(e)}")
        return pd.DataFrame()


def generate_unique_id(sheet_df: pd.DataFrame,
                       column_name: str,
                       prefix: str = '',
                       start_num: int = 1) -> str:
    """Generate a unique sequential ID for a new record.

    Args:
        sheet_df (pd.DataFrame): Existing data to check for uniqueness
        column_name (str): Name of the ID column
        prefix (str): Prefix to add to the ID (e.g., 'P', 'U')
        start_num (int): Starting number if no records exist

    Returns:
        str: Generated unique ID
    """
    if sheet_df.empty or column_name not in sheet_df.columns:
        return f"{prefix}{start_num:04d}"

    # Extract existing IDs with the same prefix
    existing_ids = []
    for idx in sheet_df[column_name]:
        if isinstance(idx, str) and idx.startswith(prefix):
            try:
                num_part = int(idx.replace(prefix, ''))
                existing_ids.append(num_part)
            except ValueError:
                continue

    # Find next available number
    if existing_ids:
        return f"{prefix}{max(existing_ids) + 1:04d}"
    else:
        return f"{prefix}{start_num:04d}"


def validate_required_fields(data: Dict[str, Any],
                             required_fields: List[str],
                             field_names: Optional[Dict[str, str]] = None) -> List[str]:
    """Validate that required fields have values.

    Args:
        data (Dict[str, Any]): Data to validate
        required_fields (List[str]): List of required field keys
        field_names (Optional[Dict[str, str]]): Display names for fields

    Returns:
        List[str]: List of validation error messages
    """
    errors = []
    field_names = field_names or {}

    for field in required_fields:
        field_name = field_names.get(field, field)
        value = data.get(field)

        # Check if field exists and is not empty
        if field not in data:
            errors.append(f"Campo '{field_name}' é obrigatório")
        elif isinstance(value, (str, list)) and not str(value).strip():
            errors.append(f"Campo '{field_name}' é obrigatório")
        elif isinstance(value, pd.Series):
            continue  # Skip pandas series used in DataFrame operations
        elif value is None:
            errors.append(f"Campo '{field_name}' é obrigatório")

    return errors


def validate_unique_fields(sheet_df: pd.DataFrame,
                          data: Dict[str, Any],
                          unique_fields: List[str],
                          exclude_index: Optional[int] = None,
                          field_names: Optional[Dict[str, str]] = None) -> List[str]:
    """Validate that fields have unique values (not already in sheet).

    Args:
        sheet_df (pd.DataFrame): Existing sheet data
        data (Dict[str, Any]): New data to validate
        unique_fields (List[str]): Fields that must be unique
        exclude_index (Optional[int]): Index to exclude (for updates)
        field_names (Optional[Dict[str, str]]): Display names for fields

    Returns:
        List[str]: List of validation error messages
    """
    errors = []
    field_names = field_names or {}

    for field in unique_fields:
        if field not in data:
            continue

        field_name = field_names.get(field, field)
        new_value = str(data[field]).strip().lower()

        # Check against existing records
        for idx, row in sheet_df.iterrows():
            if exclude_index is not None and idx == exclude_index:
                continue

            existing_value = str(row.get(field, '')).strip().lower()
            if existing_value == new_value:
                errors.append(f"O valor '{data[field]}' já está em uso para o campo '{field_name}'")
                break

    return errors


def validate_custom_rules(sheet_df: pd.DataFrame,
                         data: Dict[str, Any],
                         rules: Dict[str, Any],
                         exclude_index: Optional[int] = None) -> List[str]:
    """Validate custom business rules.

    Args:
        sheet_df (pd.DataFrame): Existing sheet data
        data (Dict[str, Any]): New data to validate
        rules (Dict[str, Any]): Custom validation rules
        exclude_index (Optional[int]): Index to exclude (for updates)

    Returns:
        List[str]: List of validation error messages
    """
    errors = []

    # Example: Schedule conflict validation
    if 'schedule_conflict_check' in rules:
        conflict_config = rules['schedule_conflict_check']
        day_field = conflict_config.get('day_field')
        start_field = conflict_config.get('start_field')
        end_field = conflict_config.get('end_field')
        resource_fields = conflict_config.get('resource_fields', [])
        overlap_message = conflict_config.get('message', 'Conflito de horário detectado')

        if all(field in data for field in [day_field, start_field, end_field]):
            new_day = data[day_field]
            new_start = data[start_field]
            new_end = data[end_field]

            # Check for time overlaps on same day
            for idx, row in sheet_df.iterrows():
                if exclude_index is not None and idx == exclude_index:
                    continue

                if row.get(day_field) == new_day:
                    existing_start = row.get(start_field)
                    existing_end = row.get(end_field)

                    # Check time overlap
                    if (new_start < existing_end and new_end > existing_start):
                        # Check resource conflicts
                        for resource_field in resource_fields:
                            if (resource_field in data and
                                data[resource_field] == row.get(resource_field)):
                                field_name = resource_field.replace('_', ' ').title()
                                errors.append(f"{overlap_message}: {field_name} já está ocupado")

    return errors


def validate_data(sheet_config: SheetConfig,
                  data: Dict[str, Any],
                  sheet_df: pd.DataFrame,
                  exclude_index: Optional[int] = None) -> List[str]:
    """Comprehensive validation for new/edit operations.

    Args:
        sheet_config (SheetConfig): Configuration for the sheet
        data (Dict[str, Any]): Data to validate
        sheet_df (pd.DataFrame): Existing sheet data
        exclude_index (Optional[int]): Index to exclude (for updates)

    Returns:
        List[str]: List of all validation error messages
    """
    all_errors = []

    # Required fields validation
    required_errors = validate_required_fields(data, sheet_config.required_columns)
    all_errors.extend(required_errors)

    # Unique fields validation
    unique_errors = validate_unique_fields(
        sheet_df, data, sheet_config.unique_columns,
        exclude_index=exclude_index
    )
    all_errors.extend(unique_errors)

    # Custom business rule validation
    custom_errors = validate_custom_rules(
        sheet_df, data, sheet_config.conflict_rules,
        exclude_index=exclude_index
    )
    all_errors.extend(custom_errors)

    return all_errors


def create_record(sheet_config: SheetConfig,
                  data: Dict[str, Any],
                  success_message: Optional[str] = None,
                  field_names: Optional[Dict[str, str]] = None) -> bool:
    """Create a new record in the Google Sheet.

    Args:
        sheet_config (SheetConfig): Configuration for the sheet
        data (Dict[str, Any]): Data to create the record with
        success_message (Optional[str]): Custom success message
        field_names (Optional[Dict[str, str]]): Display names for fields

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        sheet_df = get_sheet_data(sheet_config.name)

        # Validate data
        validation_errors = validate_data(sheet_config, data, sheet_df)
        if validation_errors:
            for error in validation_errors:
                st.error(error)
            return False

        # Generate new ID if not provided
        if sheet_config.id_column not in data or not data[sheet_config.id_column]:
            data[sheet_config.id_column] = generate_unique_id(
                sheet_df, sheet_config.id_column, sheet_config.id_prefix
            )

        # Create record
        sheet = get_worksheet(sheet_config.name)
        row_data = [data.get(col, '') for col in sheet_df.columns.tolist()]

        sheet.append_row(row_data)

        # Success feedback
        if success_message:
            st.success(success_message)
        elif 'Nome' in data:
            st.success("Registado adicionado com sucesso!")
        else:
            st.success("Registado criado com sucesso!")

        # Clear cache to refresh data
        get_sheet_data.clear()

        return True

    except Exception as e:
        st.error(f"Ocorreu um erro ao criar o registado: {str(e)}")
        return False


def update_record(sheet_config: SheetConfig,
                  index: int,
                  data: Dict[str, Any],
                  success_message: Optional[str] = None) -> bool:
    """Update an existing record in the Google Sheet.

    Args:
        sheet_config (SheetConfig): Configuration for the sheet
        index (int): Index of the record to update (DataFrame index)
        data (Dict[str, Any]): Updated data
        success_message (Optional[str]): Custom success message

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        sheet_df = get_sheet_data(sheet_config.name)

        # Validate data (exclude current record from uniqueness checks)
        validation_errors = validate_data(sheet_config, data, sheet_df, exclude_index=index)
        if validation_errors:
            for error in validation_errors:
                st.error(error)
            return False

        # Update record
        sheet = get_worksheet(sheet_config.name)
        row_data = []
        columns = sheet_df.columns.tolist()

        for col in columns:
            if col in data:
                # Handle date objects
                value = data[col]
                if hasattr(value, 'strftime'):
                    value = value.strftime('%d/%m/%Y')
                row_data.append(value)
            else:
                row_data.append(sheet_df.loc[index, col])

        # Update the row (add 2 to index to account for header row)
        sheet.update(f'A{index + 2}', [row_data])

        # Success feedback
        if success_message:
            st.success(success_message)
        else:
            st.success("Registo atualizado com sucesso!")

        # Clear cache to refresh data
        get_sheet_data.clear()

        return True

    except Exception as e:
        st.error(f"Ocorreu um erro ao atualizar o registado: {str(e)}")
        return False


def delete_record(sheet_config: SheetConfig,
                  index: int,
                  confirm_message: str = "Esta ação não pode ser desfeita.",
                  success_message: Optional[str] = None) -> bool:
    """Delete a record from the Google Sheet with confirmation.

    Args:
        sheet_config (SheetConfig): Configuration for the sheet
        index (int): Index of the record to delete (DataFrame index)
        confirm_message (str): Custom confirmation message
        success_message (Optional[str]): Custom success message

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        sheet_df = get_sheet_data(sheet_config.name)

        # Show confirmation dialog
        if 'confirm_delete' not in st.session_state or st.session_state.confirm_delete != index:
            st.session_state.confirm_delete = index
            st.warning(confirm_message)

            col1, col2, _ = st.columns([1, 1, 5])
            with col1:
                if st.button("✅ Sim, eliminar"):
                    st.session_state.confirm_delete = index
                    st.rerun()
            with col2:
                if st.button("❌ Cancelar"):
                    del st.session_state.confirm_delete
                    st.rerun()
            return False

        # Delete the record
        sheet = get_worksheet(sheet_config.name)
        sheet.delete_rows(index + 2)  # +2 for header and array offset

        # Success feedback
        if success_message:
            st.success(success_message)
        else:
            st.success("Registo eliminado com sucesso!")

        # Clear session state and cache
        if hasattr(st.session_state, 'confirm_delete'):
            del st.session_state.confirm_delete
        get_sheet_data.clear()

        return True

    except Exception as e:
        st.error(f"Ocorreu um erro ao eliminar o registado: {str(e)}")
        return False


# ===== UTILITY FUNCTIONS =====

def search_and_filter_dataframe(df: pd.DataFrame,
                                search_text: str,
                                search_columns: Optional[List[str]] = None,
                                filters: Optional[Dict[str, Any]] = None,
                                limit: int = 50,
                                offset: int = 0) -> pd.DataFrame:
    """Filter DataFrame based on search text and additional filters with pagination.

    Args:
        df (pd.DataFrame): DataFrame to filter
        search_text (str): Text to search for
        search_columns (Optional[List[str]]): Columns to search in
        filters (Optional[Dict[str, Any]]): Additional filters
        limit (int): Maximum number of records to return
        offset (int): Number of records to skip

    Returns:
        pd.DataFrame: Filtered and paginated DataFrame
    """
    if df.empty:
        return df

    # Text search
    if search_text and search_columns:
        df_filtered = df.copy()
        search_lower = search_text.lower()

        search_mask = False
        for col in search_columns:
            if col in df_filtered.columns:
                search_mask = search_mask | df_filtered[col].astype(str).str.lower().str.contains(search_lower, na=False)

        df_filtered = df_filtered[search_mask]

    else:
        df_filtered = df

    # Additional filters
    if filters:
        for col, value in filters.items():
            if col in df_filtered.columns and value is not None:
                df_filtered = df_filtered[df_filtered[col] == value]

    # Apply pagination
    start_idx = offset * limit
    end_idx = start_idx + limit

    return df_filtered.iloc[start_idx:end_idx]


def format_datetime_for_display(value: Any) -> str:
    """Format datetime/date values for display.

    Args:
        value (Any): Value to format

    Returns:
        str: Formatted string
    """
    if hasattr(value, 'strftime'):
        return value.strftime('%d/%m/%Y %H:%M')
    elif isinstance(value, str) and value:
        return value
    else:
        return str(value)


def safe_get_column_value(row: pd.Series, column: str, default: Any = '') -> Any:
    """Safely get a value from a DataFrame row.

    Args:
        row (pd.Series): Row from DataFrame
        column (str): Column name
        default (Any): Default value if column doesn't exist

    Returns:
        Any: Value from the column or default
    """
    try:
        return row.get(column, default)
    except (KeyError, AttributeError):
        return default


def create_pagination_controls(num_items: int,
                               items_per_page: int = 10,
                               session_key_prefix: str = "pagination") -> tuple[int, int]:
    """Create pagination controls for displaying large datasets.

    Args:
        num_items (int): Total number of items
        items_per_page (int): Number of items per page
        session_key_prefix (str): Prefix for session state keys

    Returns:
        tuple: (current_page, items_per_page)
    """
    total_pages = max(1, (num_items + items_per_page - 1) // items_per_page)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Anterior", disabled=st.session_state.get(f"{session_key_prefix}_current_page", 1) <= 1):
            st.session_state[f"{session_key_prefix}_current_page"] = st.session_state.get(f"{session_key_prefix}_current_page", 1) - 1
            st.rerun()

    with col2:
        current_page = st.session_state.get(f"{session_key_prefix}_current_page", 1)

        # Ensure current page is within bounds
        if current_page > total_pages:
            current_page = total_pages
            st.session_state[f"{session_key_prefix}_current_page"] = current_page

        if total_pages > 1:
            cols = st.columns(5)
            show_pages = min(5, total_pages)

            if total_pages <= 5:
                start_page = 1
            else:
                start_page = max(1, current_page - 2)
                end_page = min(total_pages, current_page + 2)
                if end_page - start_page + 1 < 5:
                    start_page = max(1, end_page - 4)

            for i, page in enumerate(range(start_page, min(start_page + 5, total_pages + 1))):
                if i < len(cols):
                    with cols[i]:
                        if st.button(str(page), disabled=current_page == page):
                            st.session_state[f"{session_key_prefix}_current_page"] = page
                            st.rerun()
        else:
            st.write("Página 1 de 1")

    with col3:
        if st.button("Próximo ➡️", disabled=current_page >= total_pages):
            st.session_state[f"{session_key_prefix}_current_page"] = st.session_state.get(f"{session_key_prefix}_current_page", 1) + 1
            st.rerun()

    start_index = (current_page - 1) * items_per_page
    end_index = min(start_index + items_per_page, num_items)

    st.write(f"**Mostrando {start_index + 1}-{end_index} de {num_items} registos**")

    return current_page, items_per_page
