#!/usr/bin/env python3
"""
Test script for Blastify CSV parsing and email validation
"""
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import pandas as pd
from utils import validate_email

def test_csv_parsing():
    """Test CSV parsing functionality"""
    print("🧪 Testing CSV parsing...")
    
    try:
        # Read the CSV file directly
        df = pd.read_csv('NidarTeamSheet - Sheet1.csv')
        print(f"✅ CSV parsing successful!")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        
        return df
    except Exception as e:
        print(f"❌ CSV parsing failed: {e}")
        return None

def test_email_validation(df):
    """Test email validation functionality"""
    print("\n🧪 Testing email validation...")
    
    if df is None:
        print("❌ Cannot test email validation - no data")
        return
    
    try:
        emails = df['Email'].tolist()
        print(f"   Total emails found: {len(emails)}")
        
        valid_emails = []
        invalid_emails = []
        
        for email in emails:
            if validate_email(email):
                valid_emails.append(email)
            else:
                invalid_emails.append(email)
        
        print(f"✅ Email validation completed!")
        print(f"   Valid emails: {len(valid_emails)}")
        print(f"   Invalid emails: {len(invalid_emails)}")
        
        if valid_emails:
            print(f"\n📧 Valid emails:")
            for email in valid_emails:
                print(f"   ✓ {email}")
        
        if invalid_emails:
            print(f"\n⚠️  Invalid emails:")
            for email in invalid_emails:
                print(f"   ✗ {email}")
        
        return valid_emails
        
    except Exception as e:
        print(f"❌ Email validation failed: {e}")
        return []

def main():
    """Main test function"""
    print("🚀 Starting Blastify functionality tests...\n")
    
    # Test CSV parsing
    df = test_csv_parsing()
    
    # Test email validation
    valid_emails = test_email_validation(df)
    
    print(f"\n🎯 Test Summary:")
    print(f"   CSV parsing: {'✅ Success' if df is not None else '❌ Failed'}")
    print(f"   Email validation: {'✅ Success' if valid_emails else '❌ Failed'}")
    print(f"   Ready for use: {'✅ Yes' if df is not None and valid_emails else '❌ No'}")

if __name__ == "__main__":
    main()
