import pandas as pd
from io import BytesIO
from typing import BinaryIO

def parse_file(file) -> pd.DataFrame:
    """
    Parse uploaded CSV or Excel file and return DataFrame
    
    Args:
        file: UploadFile object from FastAPI
        
    Returns:
        pd.DataFrame: Parsed data with email validation
        
    Raises:
        ValueError: If file type is unsupported or missing required columns
    """
    try:
        # Read file content
        content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(content))
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(BytesIO(content))
        else:
            raise ValueError(f"Unsupported file type: {file.filename}. Please use CSV or Excel files.")
        
        # Normalize column names to lowercase for consistent handling
        df.columns = df.columns.str.lower().str.strip()
        
        # Validate required columns
        if 'email' not in df.columns:
            raise ValueError("Missing required 'email' column in the uploaded file.")
        
        # Clean and validate email format with strict validation
        df['email'] = df['email'].astype(str).str.strip().str.lower()
        
        # Import the robust email validator
        from utils import validate_email
        
        # Apply strict email validation
        valid_emails = df['email'].apply(validate_email)
        df = df[valid_emails]
        
        if df.empty:
            raise ValueError("No valid email addresses found in the file. Please ensure emails are real and properly formatted with '@' symbol.")
        
        # Ensure we have required columns, fill missing ones
        if 'name' not in df.columns:
            df['name'] = 'Customer'
        
        if 'topic' not in df.columns:
            df['topic'] = 'our services'
            
        if 'message' not in df.columns:
            df['message'] = ''
        
        # Remove duplicates based on email
        df = df.drop_duplicates(keep='first')
        
        return df
        
    except Exception as e:
        raise ValueError(f"Error parsing file: {str(e)}")

def validate_dataframe(df: pd.DataFrame) -> dict:
    """
    Validate DataFrame structure and content
    
    Args:
        df: DataFrame to validate
        
    Returns:
        dict: Validation results
    """
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "stats": {}
    }
    
    # Check required columns
    required_cols = ['email']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        results["valid"] = False
        results["errors"].append(f"Missing required columns: {missing_cols}")
    
    # Statistics
    results["stats"]["total_rows"] = len(df)
    results["stats"]["unique_emails"] = df['email'].nunique() if 'email' in df.columns else 0
    results["stats"]["columns"] = list(df.columns)
    
    # Check for empty emails
    if 'email' in df.columns:
        empty_emails = df['email'].isna().sum() + (df['email'] == '').sum()
        if empty_emails > 0:
            results["warnings"].append(f"{empty_emails} rows have empty email addresses")
    
    return results
