  # 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 🎥 Camera Issues

#### Problem: "Cannot open camera"
**Symptoms:** Error message on startup, no preview window

**Solutions:**
1. **Check permissions:**
   ```bash
   # macOS
   # System Preferences → Security & Privacy → Camera
   # Enable for Terminal/your IDE
   
   # Linux
   ls -l /dev/video0
   sudo chmod 666 /dev/video0
   
   # Windows
   # Settings → Privacy → Camera → Allow desktop apps
   ```

2. **Try different camera ID:**
   ```json
   // config.json
   {
       "camera_id": 1  // Try 0, 1, 2, etc.
   }
   ```

3. **Check if camera is in use:**
   ```bash
   # macOS/Linux
   lsof | grep -i camera
   
   # Kill other applications using camera
   ```

4. **Test camera directly:**
   ```bash
   python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
   ```

---

#### Problem: Camera lag or frozen frames
**Symptoms:** Preview shows old frames, slow updates

**Solutions:**
1. **Increase capture interval:**
   ```json
   {"capture_interval": 5.0}
   ```

2. **Reduce FPS:**
   ```json
   {"capture_fps": 15}
   ```

3. **Close other camera apps:**
   - Zoom, Skype, browser tabs using camera

4. **Check system resources:**
   ```bash
   top
   # Look for high CPU/memory usage
   ```

---

### 🧠 Ollama Issues

#### Problem: "Cannot connect to Ollama"
**Symptoms:** LLM not responding, connection errors

**Solutions:**
1. **Check if Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   # Should return JSON with models
   ```

2. **Start Ollama server:**
   ```bash
   # macOS/Linux
   ollama serve
   
   # Or in background
   ollama serve &
   
   # Windows
   # Run in separate PowerShell window
   ollama serve
   ```

3. **Verify Ollama installation:**
   ```bash
   ollama --version
   # Should show version number
   ```

4. **Check port availability:**
   ```bash
   # macOS/Linux
   lsof -i :11434
   
   # Windows
   netstat -ano | findstr :11434
   ```

5. **Try different Ollama URL:**
   ```json
   {
       "ollama_url": "http://127.0.0.1:11434"
   }
   ```

---

#### Problem: "Model not found"
**Symptoms:** Ollama running but model unavailable

**Solutions:**
1. **List available models:**
   ```bash
   ollama list
   ```

2. **Pull required model:**
   ```bash
   ollama pull llama3.1
   # or
   ollama pull phi3
   ```

3. **Check model name in config:**
   ```json
   {
       "llm_model": "llama3.1"  // Must match ollama list
   }
   ```

4. **Try smaller model if download fails:**
   ```bash
   ollama pull phi3  // Smaller than llama3.1
   ```

---

#### Problem: Slow LLM responses
**Symptoms:** Long delays between suggestions

**Solutions:**
1. **Use smaller model:**
   ```bash
   ollama pull phi3
   ```
   ```json
   {"llm_model": "phi3"}
   ```

2. **Reduce context window:**
   ```json
   {"context_window": 3}
   ```

3. **Check system resources:**
   ```bash
   # Monitor CPU usage
   top -p $(pgrep ollama)
   ```

4. **Lower temperature for faster responses:**
   - Edit `intent_engine.py` line ~150:
   ```python
   "temperature": 0.1  # Lower = faster, more deterministic
   ```

---

### 🖼️ Vision Model Issues

#### Problem: "Failed to load vision model"
**Symptoms:** BLIP model not loading, import errors

**Solutions:**
1. **Check internet connection:**
   - First run downloads ~1GB model from HuggingFace

2. **Verify transformers installation:**
   ```bash
   pip install --upgrade transformers torch
   ```

3. **Check disk space:**
   ```bash
   df -h
   # Models cached in ~/.cache/huggingface/
   du -sh ~/.cache/huggingface/
   ```

4. **Manual model download:**
   ```python
   from transformers import BlipProcessor, BlipForConditionalGeneration
   
   processor = BlipProcessor.from_pretrained("Salesforce/blip-base")
   model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-base")
   ```

5. **Use fallback analyzer:**
   - Assistant automatically falls back to simple analyzer if BLIP fails
   - Check logs for fallback message

6. **Clear cache and retry:**
   ```bash
   rm -rf ~/.cache/huggingface/transformers/
   python main.py  # Will re-download
   ```

---

#### Problem: CUDA/GPU errors
**Symptoms:** GPU-related error messages

**Solutions:**
1. **Force CPU usage:**
   - Edit `scene_analyzer.py` line ~45:
   ```python
   # Comment out GPU code
   # if torch.cuda.is_available():
   #     self.model = self.model.to("cuda")
   ```

2. **Install CPU-only PyTorch:**
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

3. **Check CUDA installation:**
   ```python
   import torch
   print(f"CUDA available: {torch.cuda.is_available()}")
   print(f"CUDA version: {torch.version.cuda}")
   ```

---

### 💻 Performance Issues

#### Problem: High CPU usage
**Symptoms:** Laptop fans running, system slow

**Solutions:**
1. **Increase capture interval:**
   ```json
   {"capture_interval": 10.0}  // Every 10 seconds
   ```

2. **Disable preview window:**
   ```json
   {"show_preview": false}
   ```

3. **Use smaller models:**
   ```json
   {
       "vision_model": "blip-base",  // Not blip-large
       "llm_model": "phi3"            // Not llama3.1
   }
   ```

4. **Reduce context window:**
   ```json
   {"context_window": 3}
   ```

5. **Check background processes:**
   ```bash
   ps aux | grep python
   # Kill any orphaned processes
   ```

---

#### Problem: Memory leak / growing memory usage
**Symptoms:** Memory usage increases over time

**Solutions:**
1. **Restart assistant periodically:**
   - Normal for first few minutes as models load
   - If continues to grow, may be a leak

2. **Check frame release:**
   - Verify `frame_capture.py` releases frames properly

3. **Limit context history:**
   ```json
   {"context_window": 5}  // Don't set too high
   ```

4. **Monitor memory:**
   ```bash
   watch -n 1 'ps aux | grep main.py'
   ```

5. **Add memory profiling:**
   ```bash
   pip install memory_profiler
   python -m memory_profiler main.py
   ```

---

### 📝 Output Issues

#### Problem: No suggestions appearing
**Symptoms:** Assistant runs but never provides suggestions

**Solutions:**
1. **Lower confidence threshold:**
   ```json
   {"confidence_threshold": 0.3}  // Lower = more suggestions
   ```

2. **Reduce intervention interval:**
   ```json
   {"min_intervention_interval": 10.0}  // Allow more frequent suggestions
   ```

3. **Check logs:**
   ```bash
   tail -f logs/assistant.log
   # Look for "should_assist": false
   ```

4. **Test with obvious scenario:**
   - Hold a clear object in front of camera
   - Perform obvious action (waving, pointing)

5. **Debug LLM responses:**
   - Add logging in `intent_engine.py`:
   ```python
   logger.info(f"LLM response: {response}")
   ```

---

#### Problem: Text-to-Speech not working
**Symptoms:** TTS enabled but no audio output

**Solutions:**
1. **Check pyttsx3 installation:**
   ```bash
   pip install --upgrade pyttsx3
   ```

2. **Test TTS independently:**
   ```python
   import pyttsx3
   engine = pyttsx3.init()
   engine.say("Test message")
   engine.runAndWait()
   ```

3. **Check audio output:**
   - Verify speakers/headphones connected
   - Check system volume

4. **Try alternative TTS (macOS):**
   ```bash
   say "Test message"
   ```

5. **Platform-specific issues:**
   - **Linux:** Install espeak: `sudo apt-get install espeak`
   - **Windows:** Verify SAPI5 voices installed

---

### 🔧 Installation Issues

#### Problem: "Module not found" errors
**Symptoms:** Import errors when running

**Solutions:**
1. **Verify virtual environment activated:**
   ```bash
   which python
   # Should show path to venv/bin/python
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check Python version:**
   ```bash
   python --version
   # Must be 3.8 or higher
   ```

4. **Install missing packages individually:**
   ```bash
   pip install opencv-python transformers torch requests
   ```

---

#### Problem: pip install fails
**Symptoms:** Errors during dependency installation

**Solutions:**
1. **Upgrade pip:**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

2. **Install system dependencies (Linux):**
   ```bash
   sudo apt-get update
   sudo apt-get install python3-dev python3-pip
   sudo apt-get install libgl1-mesa-glx  # For OpenCV
   ```

3. **Use binary wheels:**
   ```bash
   pip install --only-binary :all: opencv-python
   ```

4. **Check disk space:**
   ```bash
   df -h
   ```

5. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

---

### 🐛 Runtime Errors

#### Problem: Assistant crashes randomly
**Symptoms:** Unexpected exits, error messages

**Solutions:**
1. **Check logs:**
   ```bash
   tail -n 100 logs/assistant.log
   ```

2. **Run with debug logging:**
   - Edit `main.py` line ~15:
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Add error handling:**
   - Wrap main loop in additional try/except

4. **Check for resource exhaustion:**
   ```bash
   # Monitor resources
   htop  # or top
   ```

5. **Test components individually:**
   ```python
   # Test frame capture alone
   from src.vision.frame_capture import FrameCapture
   fc = FrameCapture()
   for i in range(100):
       frame = fc.get_frame()
       print(f"Frame {i}: OK")
   ```

---

#### Problem: "Privacy mode stuck"
**Symptoms:** Cannot re-enable monitoring

**Solutions:**
1. **Remove privacy flag file:**
   ```bash
   rm data/.privacy_mode
   ```

2. **Check file permissions:**
   ```bash
   ls -la data/
   chmod 644 data/.privacy_mode
   ```

3. **Restart assistant:**
   ```bash
   python main.py
   ```

---

### 📊 Getting Help

#### Debug Information to Collect

When reporting issues, include:

```bash
# System info
uname -a  # macOS/Linux
systeminfo  # Windows

# Python version
python --version

# Package versions
pip list | grep -E "opencv|torch|transformers|requests"

# Ollama status
ollama list
curl http://localhost:11434/api/tags

# Camera test
python -c "import cv2; print(f'OpenCV: {cv2.__version__}'); cap = cv2.VideoCapture(0); print(f'Camera: {cap.isOpened()}')"

# Recent logs
tail -n 50 logs/assistant.log

# Configuration
cat config.json
```

#### Useful Log Analysis

```bash
# Find errors in logs
grep -i error logs/assistant.log

# Find warnings
grep -i warning logs/assistant.log

# Check intervention history
grep "Response delivered" logs/assistant.log

# Monitor in real-time
tail -f logs/assistant.log | grep -E "error|warning|Response"
```

---

### 🚀 Still Having Issues?

1. **Review complete logs** - `logs/assistant.log`
2. **Check GitHub Issues** - See if others had similar problems
3. **Verify all prerequisites** - Python, Ollama, camera permissions
4. **Try minimal configuration** - Use default settings first
5. **Test components separately** - Isolate the problem

---

## Quick Diagnostic Script

```bash
#!/bin/bash
# diagnostic.sh - Run system diagnostics

echo "=== System Diagnostics ==="

echo -e "\n1. Python Version:"
python --version

echo -e "\n2. Virtual Environment:"
which python

echo -e "\n3. Key Packages:"
pip list | grep -E "opencv|torch|transformers"

echo -e "\n4. Camera Test:"
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera FAIL'); cap.release()"

echo -e "\n5. Ollama Status:"
curl -s http://localhost:11434/api/tags | python -m json.tool

echo -e "\n6. Disk Space:"
df -h .

echo -e "\n7. Recent Errors:"
grep -i error logs/assistant.log | tail -5

echo -e "\n=== Diagnostics Complete ==="
```

Save and run:
```bash
chmod +x diagnostic.sh
./diagnostic.sh
```