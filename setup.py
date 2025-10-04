#!/usr/bin/env python3
"""
setup.py
Automated setup script for Proactive AI Assistant
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def create_directories():
    """Create necessary directories"""
    print("Creating directory structure...")
    
    directories = [
        "src/vision",
        "src/reasoning",
        "src/output",
        "src/config",
        "src/utils",
        "data/models",
        "data/cache",
        "logs",
        "tests"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  📁 Created: {dir_path}")
    
    print("✅ Directory structure created")


def create_init_files():
    """Create __init__.py files"""
    print("Creating __init__.py files...")
    
    init_files = [
        "src/__init__.py",
        "src/vision/__init__.py",
        "src/reasoning/__init__.py",
        "src/output/__init__.py",
        "src/config/__init__.py",
        "src/utils/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"  ✓ {init_file}")
    
    print("✅ Init files created")


def check_ollama():
    """Check if Ollama is installed and running"""
    print("Checking Ollama installation...")
    
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
            
            # Check if Ollama is running
            try:
                import requests
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    print("✅ Ollama server is running")
                    models = response.json().get('models', [])
                    if models:
                        print("   Available models:")
                        for model in models[:3]:
                            print(f"     - {model['name']}")
                    else:
                        print("⚠️  No models found. Run: ollama pull llama3.1")
                    return True
                else:
                    print("⚠️  Ollama not running. Start with: ollama serve")
                    return False
            except:
                print("⚠️  Ollama not running. Start with: ollama serve")
                return False
        else:
            print("❌ Ollama not found")
            return False
    except FileNotFoundError:
        print("❌ Ollama not installed")
        print("   Install from: https://ollama.com/download")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False


def check_webcam():
    """Check if webcam is accessible"""
    print("Checking webcam access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Webcam accessible")
                return True
            else:
                print("⚠️  Webcam found but cannot read frames")
                return False
        else:
            print("❌ Cannot access webcam")
            print("   Check camera permissions in system settings")
            return False
    except ImportError:
        print("⚠️  OpenCV not installed yet (will be installed with dependencies)")
        return True
    except Exception as e:
        print(f"❌ Error checking webcam: {e}")
        return False


def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    print("This may take several minutes...\n")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True
        )
        
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        
        print("\n✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to install dependencies: {e}")
        return False


def create_sample_config():
    """Create a sample configuration file"""
    print("Creating sample configuration...")
    
    config_content = """{
    "camera_id": 0,
    "capture_fps": 30,
    "capture_interval": 3.0,
    "vision_model": "blip-base",
    "show_preview": true,
    "llm_model": "llama3.1",
    "ollama_url": "http://localhost:11434",
    "context_window": 5,
    "confidence_threshold": 0.6,
    "min_intervention_interval": 30.0,
    "output_mode": "text",
    "enable_tts": false,
    "privacy_mode": false,
    "save_frames": false
}"""
    
    config_path = Path("config.json")
    if not config_path.exists():
        config_path.write_text(config_content)
        print("✅ Created config.json")
    else:
        print("ℹ️  config.json already exists (skipping)")


def run_tests():
    """Run basic tests"""
    print("Running basic tests...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("⚠️  Some tests failed (this is OK for first setup)")
            return True
    except subprocess.CalledProcessError:
        print("⚠️  Could not run tests (pytest may not be installed yet)")
        return True
    except Exception as e:
        print(f"⚠️  Test error: {e}")
        return True


def print_next_steps():
    """Print next steps for user"""
    print_header("Setup Complete!")
    
    print("🎉 Your Proactive AI Assistant is ready!\n")
    print("Next steps:\n")
    print("1. Make sure Ollama is running:")
    print("   $ ollama serve\n")
    print("2. Pull an LLM model (if not already done):")
    print("   $ ollama pull llama3.1")
    print("   or")
    print("   $ ollama pull phi3\n")
    print("3. Run the assistant:")
    print("   $ python main.py\n")
    print("Controls during runtime:")
    print("  - Press 'q' to quit")
    print("  - Press 'p' to pause/resume")
    print("  - Press 'x' for privacy mode\n")
    print("Configuration:")
    print("  - Edit config.json to customize settings\n")
    print("For help and documentation:")
    print("  - See README.md")
    print("  - Check logs/assistant.log for troubleshooting\n")
    print("=" * 60)


def main():
    """Main setup function"""
    print_header("Proactive AI Assistant - Setup")
    
    print("This script will set up your proactive AI assistant.\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create init files
    create_init_files()
    
    # Create sample config
    create_sample_config()
    
    # Check dependencies
    print("\nChecking system requirements...")
    ollama_ok = check_ollama()
    
    # Install Python dependencies
    if Path("requirements.txt").exists():
        response = input("\nInstall Python dependencies? (y/n): ")
        if response.lower() in ['y', 'yes']:
            install_dependencies()
            
            # Now check webcam after OpenCV is installed
            check_webcam()
    else:
        print("⚠️  requirements.txt not found. Please create it first.")
    
    # Summary
    print_header("Setup Summary")
    
    if ollama_ok:
        print("✅ Ollama: Ready")
    else:
        print("⚠️  Ollama: Not ready (install and start it)")
    
    print("\n")
    print_next_steps()


if __name__ == "__main__":
    main()