"""
Blastify Setup Script

Automated setup for the Blastify bulk email sender application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print the Blastify setup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║               🚀 BLASTIFY SETUP WIZARD 🚀                   ║
    ║                                                              ║
    ║        Your all-in-one bulk email sender with AI            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ is required. You have {version.major}.{version.minor}.{version.micro}")
        print("Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        # Upgrade pip first
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies:")
        print(e.stderr)
        return False

def create_env_file():
    """Create .env file from template"""
    print("\n📝 Setting up environment configuration...")
    
    env_template = Path(__file__).parent / ".env.template"
    env_file = Path(__file__).parent / ".env"
    
    if not env_template.exists():
        print("❌ .env.template not found!")
        return False
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("📝 Keeping existing .env file")
            return True
    
    try:
        shutil.copy(env_template, env_file)
        print("✅ .env file created successfully!")
        print("📝 Please edit .env file with your API keys")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def setup_directories():
    """Ensure all required directories exist"""
    print("\n📁 Setting up directory structure...")
    
    directories = [
        "backend/templates",
        "frontend/templates",
    ]
    
    base_path = Path(__file__).parent
    
    for dir_path in directories:
        full_path = base_path / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {dir_path}")
    
    print("✅ Directory structure ready!")
    return True

def get_api_keys():
    """Interactive API key configuration"""
    print("\n🔑 API Key Configuration")
    print("You'll need API keys from these services:")
    print("1. Google Gemini AI - for content generation")
    print("2. Resend - for email sending")
    
    configure_now = input("\nWould you like to configure API keys now? (y/N): ").strip().lower()
    
    if configure_now != 'y':
        print("⏭️  Skipping API key configuration")
        print("💡 You can configure them later by editing the .env file")
        return True
    
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("❌ .env file not found! Run setup first.")
        return False
    
    # Read current env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Get API keys from user
    print("\n🔑 Enter your API keys (press Enter to skip):")
    
    gemini_key = input("Gemini API Key: ").strip()
    resend_key = input("Resend API Key: ").strip()
    sender_email = input("Sender Email (e.g., 'Your Company <you@domain.com>'): ").strip()
    
    # Update env file
    updated_lines = []
    for line in lines:
        if line.startswith('GEMINI_API_KEY=') and gemini_key:
            updated_lines.append(f'GEMINI_API_KEY={gemini_key}\n')
        elif line.startswith('RESEND_API_KEY=') and resend_key:
            updated_lines.append(f'RESEND_API_KEY={resend_key}\n')
        elif line.startswith('SENDER_EMAIL=') and sender_email:
            updated_lines.append(f'SENDER_EMAIL={sender_email}\n')
        else:
            updated_lines.append(line)
    
    # Write updated env file
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("✅ API keys configured!")
    return True

def run_configuration_check():
    """Run the configuration checker"""
    print("\n🔍 Running configuration check...")
    
    try:
        # Import and run the check
        check_script = Path(__file__).parent / "check_config.py"
        if check_script.exists():
            subprocess.run([sys.executable, str(check_script)], check=True)
        else:
            print("⚠️  Configuration checker not found, skipping...")
        
        return True
        
    except subprocess.CalledProcessError:
        print("⚠️  Configuration check found some issues")
        return False

def show_getting_started():
    """Show getting started information"""
    print("\n" + "="*60)
    print("🎉 BLASTIFY SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. 🔑 Configure your API keys in the .env file:")
    print("   - Get Gemini API key: https://aistudio.google.com/app/apikey")
    print("   - Get Resend API key: https://resend.com")
    
    print("\n2. 🚀 Start the application:")
    print("   python run.py streamlit")
    
    print("\n3. 📚 Access the API documentation:")
    print("   python run.py fastapi")
    print("   Then visit: http://localhost:8000/docs")
    
    print("\n4. 🔍 Check configuration anytime:")
    print("   python check_config.py")
    
    print("\n📖 Documentation:")
    print("   - README.md - Complete setup and usage guide")
    print("   - sample_contacts.csv - Example email list format")
    
    print("\n💡 Tips:")
    print("   - Start with the sample CSV file to test")
    print("   - Use the Streamlit app for easy bulk sending")
    print("   - Check the templates folder to customize emails")
    
    print("\n🆘 Need Help?")
    print("   - Check the README.md file")
    print("   - Create an issue on GitHub")
    
    print("\n" + "="*60)
    print("Happy emailing with Blastify! 📧✨")
    print("="*60)

def main():
    """Main setup function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        return False
    
    # Step 3: Setup directories
    if not setup_directories():
        print("\n❌ Setup failed during directory creation")
        return False
    
    # Step 4: Create environment file
    if not create_env_file():
        print("\n❌ Setup failed during environment configuration")
        return False
    
    # Step 5: Configure API keys (optional)
    get_api_keys()
    
    # Step 6: Run configuration check
    run_configuration_check()
    
    # Step 7: Show getting started info
    show_getting_started()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
