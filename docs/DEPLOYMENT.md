# 🚀 Deployment Checklist & Complete Setup Guide

## Pre-Installation Checklist

### System Requirements

- [ ] **Operating System**: macOS, Linux, or Windows 10/11
- [ ] **Python**: Version 3.8 or higher
- [ ] **RAM**: Minimum 8GB (16GB recommended)
- [ ] **Storage**: At least 10GB free space for models
- [ ] **Webcam**: Built-in or USB camera
- [ ] **Internet**: For initial model downloads

### Software Prerequisites

- [ ] Python 3.8+ installed and accessible via command line
- [ ] pip package manager installed
- [ ] Git (optional, for version control)
- [ ] Camera permissions granted to terminal/IDE

---

## 📦 Step 1: Install Ollama

### macOS / Linux

```bash
# Download and install
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### Windows

1. Download installer from <https://ollama.com/download>
2. Run the installer
3. Open PowerShell and verify: `ollama --version`

### Post-Installation

```bash
# Start Ollama server (keep this running)
ollama serve

# In a new terminal, pull a model
ollama pull phi3:latest

# Alternative smaller model
ollama pull phi3:latest

# Verify model is available
ollama list
```

**✅ Checkpoint**: Run `curl http://localhost:11434/api/tags` - should return JSON with models

---

## 📁 Step 2: Create Project Structure

### Option A: Manual Setup

```bash
# Create project directory
mkdir fr-ai
cd fr-ai

# Create directory structure
mkdir -p src/vision src/reasoning src/output src/config src/utils
mkdir -p data/models data/cache logs tests

# Create init files
touch src/__init__.py
touch src/vision/__init__.py
touch src/reasoning/__init__.py
touch src/output/__init__.py
touch src/config/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

### Option B: Automated Setup

```bash
# Run setup script (after creating it)
python setup.py
```

**✅ Checkpoint**: Verify all directories exist with `ls -R`

---

## 📝 Step 3: Create All Required Files

### Core Files Needed

1. **`main.py`** - Main application (see artifact: "Frequent Reasoning AI - Main Application")
2. **`requirements.txt`** - Dependencies (see artifact: "Requirements File")
3. **`.gitignore`** - Git ignore rules (see artifact: ".gitignore File")
4. **`README.md`** - Documentation (see artifact: "README.md")

### Module Files (in `src/` directory)

5. **`src/__init__.py`** - Package init (see artifact: "__init__.py Files")
6. **`src/vision/frame_capture.py`** - Frame capture module
7. **`src/vision/scene_analyzer.py`** - Scene analysis module
8. **`src/reasoning/intent_engine.py`** - Intent inference module
9. **`src/output/response_handler.py`** - Response handling module
10. **`src/config/settings.py`** - Configuration management
11. **`src/utils/privacy.py`** - Privacy controls

### Optional Files

12. **`setup.py`** - Setup automation script
13. **`run.sh`** - Quick launch script (make executable: `chmod +x run.sh`)
14. **`tests/test_*.py`** - Test files

**✅ Checkpoint**: Verify with `find . -name "*.py" | wc -l` - should show all Python files

---

## 🔧 Step 4: Install Python Dependencies

### Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation - prompt should show (venv)
```

### Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# This will install:
# - opencv-python (camera access)
# - transformers (BLIP model)
# - torch (deep learning)
# - requests (Ollama API)
# - pyttsx3 (text-to-speech, optional)
# - pytest (testing)
```

### Verify Installation

```bash
# Test imports
python -c "import cv2; import transformers; import torch; print('All imports OK')"
```

**✅ Checkpoint**: No import errors should appear

---

## 🎥 Step 5: Test Camera Access

```bash
# Quick camera test
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error'); cap.release()"
```

### If Camera Fails

**macOS:**
1. System Preferences → Security & Privacy → Camera
2. Enable for Terminal/iTerm/your IDE

**Linux:**

```bash
# Check camera devices
ls /dev/video*

# Check permissions
sudo chmod 666 /dev/video0
```

**Windows:**

1. Settings → Privacy → Camera
2. Enable for desktop apps

**✅ Checkpoint**: Camera test prints "Camera OK"

---

## 🧠 Step 6: Test Ollama Connection

```bash
# Test Ollama API
curl http://localhost:11434/api/tags

# Should return JSON with models list
```

### If Ollama Not Running

```bash
# Start in background (macOS/Linux)
ollama serve &

# Start in new terminal (Windows)
# Open new PowerShell window
ollama serve
```

**✅ Checkpoint**: API returns valid JSON response

---

## 🚀 Step 7: First Run

### Initial Test Run

```bash
# Make sure you're in project root with venv activated
python main.py
```

### Expected Behavior

1. **Console output**: Setup messages and "Assistant is now running..."
2. **Camera preview**: Window showing webcam feed (if `show_preview: true`)
3. **Model loading**: First run downloads BLIP model (~1GB)
4. **Scene descriptions**: Periodic analysis in console

### First Run Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot open camera" | Check camera permissions, try different `camera_id` |
| "Failed to load vision model" | Check internet, verify disk space for downloads |
| "Cannot connect to Ollama" | Ensure `ollama serve` is running |
| Slow performance | Increase `capture_interval` in config.json |

**✅ Checkpoint**: Assistant runs without errors, displays preview window

---

## ⚙️ Step 8: Configuration

### Create/Edit config.json

```json
{
    "camera_id": 0,
    "capture_interval": 3.0,
    "vision_model": "blip-base",
    "llm_model": "llama3.1",
    "confidence_threshold": 0.6,
    "min_intervention_interval": 30.0,
    "output_mode": "text",
    "enable_tts": false,
    "show_preview": true
}
```

### Recommended Settings for Different Use Cases

**Cooking Assistant:**

```json
{
    "capture_interval": 5.0,
    "confidence_threshold": 0.7,
    "min_intervention_interval": 20.0,
    "enable_tts": true
}
```

**Productivity Monitor:**

```json
{
    "capture_interval": 10.0,
    "confidence_threshold": 0.65,
    "min_intervention_interval": 300.0,
    "output_mode": "text"
}
```

**Exercise Coach:**

```json
{
    "capture_interval": 2.0,
    "confidence_threshold": 0.75,
    "min_intervention_interval": 15.0,
    "enable_tts": true
}
```

**✅ Checkpoint**: Config changes take effect on restart

---

## 🧪 Step 9: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

**✅ Checkpoint**: Tests pass or show expected failures

---

## 🎯 Step 10: Validate Complete System

### System Validation Checklist

- [ ] Camera preview displays correctly
- [ ] Scene descriptions appear in console
- [ ] LLM generates appropriate responses
- [ ] Interventions respect timing settings
- [ ] Privacy mode toggle works (press 'x')
- [ ] Pause/resume works (press 'p')
- [ ] Clean shutdown (press 'q')
- [ ] Logs written to `logs/assistant.log`

### Test Scenarios

1. **Idle Test**: Leave assistant running for 5 minutes
   - Should not crash
   - Should generate occasional descriptions
   - CPU usage should be reasonable

2. **Activity Test**: Perform a simple task (e.g., hold an object)
   - Should detect scene change
   - May generate suggestions if threshold met

3. **Privacy Test**: Toggle privacy mode
   - Should stop monitoring immediately
   - Should restart cleanly

**✅ Final Checkpoint**: All validation items pass

---

## 📊 Performance Optimization

### If Performance is Slow

1. **Increase capture interval**:

   ```json
   "capture_interval": 5.0  // or higher
   ```

2. **Use smaller vision model**:

   ```json
   "vision_model": "blip-base"  // not blip-large
   ```

3. **Disable preview**:

   ```json
   "show_preview": false
   ```

4. **Use smaller LLM**:

   ```bash
   ollama pull phi3  // smaller than llama3.1
   ```

5. **Check GPU usage**:

   ```python
   import torch
   print(f"CUDA available: {torch.cuda.is_available()}")
   ```

---

## 🔒 Security & Privacy Checklist

Before deployment:

- [ ] Inform users about camera usage
- [ ] Provide visible indicator when monitoring
- [ ] Easy access to privacy toggle
- [ ] No frame saving enabled by default
- [ ] Verify no external network calls (except Ollama)
- [ ] Review logs for sensitive data
- [ ] Test privacy mode thoroughly
- [ ] Document data handling in README

---

## 📚 Post-Deployment

### Monitoring

```bash
# Check logs
tail -f logs/assistant.log

# Monitor CPU/memory
top -p $(pgrep -f main.py)

# Check disk usage
du -sh data/
```

### Maintenance

- **Weekly**: Review logs for errors
- **Monthly**: Update dependencies (`pip install --upgrade -r requirements.txt`)
- **Quarterly**: Update models (`ollama pull llama3.1`)

### Backup Important Files

```bash
# Backup configuration
cp config.json config.json.backup

# Backup custom prompts (if modified)
cp -r src/ src_backup/
```

---

## 🆘 Common Issues & Solutions

### Issue: High CPU Usage
**Solution**: Increase `capture_interval`, disable preview, use smaller models

### Issue: Memory Leak
**Solution**: Restart assistant periodically, check for unreleased resources

### Issue: Inconsistent Suggestions
**Solution**: Adjust `confidence_threshold`, improve LLM prompts

### Issue: Camera Lag
**Solution**: Reduce `capture_fps`, check other apps using camera

### Issue: Model Download Fails
**Solution**: Check internet, verify disk space, try manual download

---

## ✅ Deployment Complete!

Your Proactive AI Assistant is now fully set up and ready to use.

**Quick Reference:**
- Start: `python main.py` or `./run.sh`
- Stop: Press `q`
- Pause: Press `p`
- Privacy: Press `x`
- Logs: `logs/assistant.log`
- Config: `config.json`

**Next Steps:**
1. Customize prompts in `intent_engine.py`
2. Add custom intervention logic
3. Integrate with smart home devices
4. Build additional features

Happy coding! 🚀