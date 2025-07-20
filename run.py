#!/usr/bin/env python3
"""
Blastify Runner Script

This script provides easy commands to run different parts of the Blastify application.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_streamlit():
    """Run the Streamlit frontend application"""
    frontend_path = Path(__file__).parent / "frontend" / "app.py"
    
    if not frontend_path.exists():
        print("❌ Frontend app.py not found!")
        return False
    
    print("🚀 Starting Blastify Streamlit App...")
    print("📍 Access the app at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(frontend_path),
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Blastify app stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit app: {e}")
        return False
    
    return True

def run_fastapi():
    """Run the FastAPI backend server"""
    backend_path = Path(__file__).parent / "backend"
    
    if not (backend_path / "main.py").exists():
        print("❌ Backend main.py not found!")
        return False
    
    print("🚀 Starting Blastify FastAPI Server...")
    print("📍 API docs available at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Change to backend directory
    original_cwd = os.getcwd()
    os.chdir(backend_path)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 FastAPI server stopped.")
    except Exception as e:
        print(f"❌ Error running FastAPI server: {e}")
        return False
    finally:
        os.chdir(original_cwd)
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit', 'pandas', 'jinja2', 'resend', 
        'httpx', 'python-dotenv', 'openpyxl', 
        'fastapi', 'uvicorn', 'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed!")
    return True

def check_environment():
    """Check environment configuration"""
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("💡 Create a .env file with your API keys:")
        print("   GEMINI_API_KEY=your-gemini-api-key")
        print("   RESEND_API_KEY=your-resend-api-key")
        print("   SENDER_EMAIL=Your Company <you@domain.com>")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['GEMINI_API_KEY', 'RESEND_API_KEY', 'SENDER_EMAIL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Add these to your .env file")
        return False
    
    print("✅ Environment configuration is complete!")
    return True

def install_dependencies():
    """Install required dependencies"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup():
    """Setup the Blastify application"""
    print("🔧 Setting up Blastify...")
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check environment
    env_template = Path(__file__).parent / ".env.template"
    env_file = Path(__file__).parent / ".env"
    
    if env_template.exists() and not env_file.exists():
        print("📝 Creating .env file from template...")
        import shutil
        shutil.copy(env_template, env_file)
        print("✅ .env file created! Please edit it with your API keys.")
    
    print("✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your API keys")
    print("2. Run: python run.py streamlit")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Blastify Application Runner")
    parser.add_argument(
        'command',
        choices=['streamlit', 'fastapi', 'check', 'setup', 'install'],
        help='Command to run'
    )
    
    args = parser.parse_args()
    
    if args.command == 'setup':
        setup()
    elif args.command == 'install':
        install_dependencies()
    elif args.command == 'check':
        print("🔍 Checking Blastify configuration...")
        deps_ok = check_dependencies()
        env_ok = check_environment()
        
        if deps_ok and env_ok:
            print("\n✅ Blastify is ready to run!")
            print("🚀 Start with: python run.py streamlit")
        else:
            print("\n❌ Please fix the issues above before running Blastify")
    elif args.command == 'streamlit':
        if check_dependencies():
            run_streamlit()
    elif args.command == 'fastapi':
        if check_dependencies():
            run_fastapi()

if __name__ == "__main__":
    main()
