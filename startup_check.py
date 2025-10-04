#!/usr/bin/env python3
"""
startup_check.py
Pre-flight checks before running the assistant
"""

import sys
import subprocess
import requests

def print_status(message, status):
    """Print colored status message"""
    colors = {
        'success': '\033[92m✓',
        'error': '\033[91m✗',
        'warning': '\033[93m⚠',
        'info': '\033[94mℹ'
    }
    reset = '\033[0m'
    print(f"{colors.get(status, '')} {message}{reset}")


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro}", 'success')
        return True
    else:
        print_status(f"Python {version.major}.{version.minor} - Need 3.8+", 'error')
        return False


def check_camera():
    """Check camera access"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                print_status("Camera accessible", 'success')
                return True
            else:
                print_status("Camera opened but cannot read frames", 'warning')
                return False
        else:
            print_status("Cannot access camera - check permissions", 'error')
            return False
    except Exception as e:
        print_status(f"Camera check failed: {e}", 'error')
        return False


def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                model_names = [m['name'] for m in models]
                print_status(f"Ollama running with {len(models)} model(s)", 'success')
                print(f"   Available: {', '.join(model_names[:3])}")
                return True
            else:
                print_status("Ollama running but no models found", 'warning')
                print("   Run: ollama pull llama3.1")
                return False
        else:
            print_status("Ollama returned unexpected status", 'warning')
            return False
    except requests.exceptions.RequestException:
        print_status("Ollama not running", 'error')
        print("   Start with: ollama serve")
        return False


def check_dependencies():
    """Check key dependencies"""
    packages = {
        'cv2': 'opencv-python',
        'transformers': 'transformers',
        'torch': 'torch',
        'requests': 'requests'
    }
    
    all_good = True
    for module, package in packages.items():
        try:
            __import__(module)
            print_status(f"{package} installed", 'success')
        except ImportError:
            print_status(f"{package} missing", 'error')
            all_good = False
    
    return all_good


def check_config():
    """Check if config.json exists and is valid"""
    import json
    from pathlib import Path
    
    config_file = Path("config.json")
    if config_file.exists():
        try:
            with open(config_file) as f:
                json.load(f)
            print_status("config.json valid", 'success')
            return True
        except json.JSONDecodeError:
            print_status("config.json invalid - will use defaults", 'warning')
            return False
    else:
        print_status("config.json not found - will be created", 'info')
        return True


def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("  Pre-Flight Checks")
    print("="*60 + "\n")
    
    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Camera": check_camera(),
        "Ollama": check_ollama(),
        "Configuration": check_config()
    }
    
    print("\n" + "="*60)
    print("  Summary")
    print("="*60 + "\n")
    
    for check, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {check}")
    
    print("\n")
    
    if all(checks.values()):
        print_status("All checks passed! Ready to run: python main.py", 'success')
        return 0
    else:
        print_status("Some checks failed. Fix issues above before running.", 'warning')
        
        # Provide specific help
        if not checks["Ollama"]:
            print("\nTo start Ollama:")
            print("  Terminal 1: ollama serve")
            print("  Terminal 2: ollama pull llama3.1")
        
        if not checks["Camera"]:
            print("\nTo fix camera:")
            print("  macOS: System Preferences → Security & Privacy → Camera")
            print("  Linux: sudo chmod 666 /dev/video0")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())