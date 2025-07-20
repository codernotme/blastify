#!/usr/bin/env python3
"""
Test script for CSV parsing with the NidarTeamSheet file
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import pandas as pd
from backend.utils import validate_email

def test_csv_parsing():
    """Test parsing the NidarTeamSheet CSV file"""
    try:
        # Read the CSV file
        print("Reading CSV file...")
        df = pd.read_csv('NidarTeamSheet - Sheet1.csv')
        
        print(f"Original columns: {list(df.columns)}")
        print(f"Original shape: {df.shape}")
        
        # Normalize column names to lowercase
        df.columns = df.columns.str.lower().str.strip()
        print(f"Normalized columns: {list(df.columns)}")
        
        # Check if email column exists
        if 'email' not in df.columns:
            print("❌ Missing 'email' column!")
            return
        
        # Clean emails
        df['email'] = df['email'].astype(str).str.strip().str.lower()
        
        print(f"\nEmail validation results:")
        print(f"Total emails to validate: {len(df)}")
        
        # Apply email validation
        valid_emails = []
        invalid_emails = []
        
        for idx, email in enumerate(df['email']):
            is_valid = validate_email(email)
            if is_valid:
                valid_emails.append((idx, email))
            else:
                invalid_emails.append((idx, email))
        
        print(f"✅ Valid emails: {len(valid_emails)}")
        print(f"❌ Invalid emails: {len(invalid_emails)}")
        
        if valid_emails:
            print(f"\nValid emails:")
            for idx, email in valid_emails:
                name = df.iloc[idx]['name'] if 'name' in df.columns else 'Unknown'
                print(f"  - {name}: {email}")
        
        if invalid_emails:
            print(f"\nInvalid emails:")
            for idx, email in invalid_emails:
                name = df.iloc[idx]['name'] if 'name' in df.columns else 'Unknown'
                print(f"  - {name}: {email}")
        
        # Filter to valid emails only
        df_valid = df[df['email'].apply(validate_email)]
        print(f"\nFinal dataset shape: {df_valid.shape}")
        
        if not df_valid.empty:
            print("✅ CSV parsing successful!")
            print("Sample data:")
            for col in ['name', 'email']:
                if col in df_valid.columns:
                    print(f"{col}: {list(df_valid[col].head(3))}")
        else:
            print("❌ No valid emails found after filtering!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_csv_parsing()
