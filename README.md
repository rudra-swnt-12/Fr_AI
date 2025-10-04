# 🤖 Frequent Reasoning Artificial Intelligence

A privacy-first, locally-running AI assistant that observes your environment through your webcam and proactively provides helpful suggestions without requiring explicit commands.

## ✨ Features

- 🎥 **Real-time Vision Processing**: Uses BLIP for scene understanding
- 🧠 **Intelligent Intent Inference**: Powered by local LLMs (Llama 3.1/Phi-3) via Ollama
- 🔒 **Privacy-First Design**: All processing happens locally on your machine
- ⚡ **Low-Latency**: Optimized for standard laptop hardware
- 🎤 **Optional TTS**: Text-to-speech output support
- 🛡️ **Privacy Controls**: Easy toggle to disable monitoring anytime

## 🎯 Use Cases

- **Cooking Assistant**: Get timing reminders and cooking tips
- **Productivity Helper**: Break reminders and posture checks
- **Exercise Coach**: Form corrections and workout guidance
- **Study Companion**: Focus tracking and resource suggestions
- **Task Support**: Context-aware suggestions for your activities

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Webcam** connected
3. **Ollama** installed and running

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull phi3:latest

# Start Ollama server
ollama serve
```

### Installation

```bash
# Clone or create project directory
mkdir fr-ai
cd fr-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directory structure
mkdir -p src/{vision,reasoning,output,config,utils} data/{models,cache} logs tests

# Add all the Python files from artifacts to their respective directories
```

### First Run

```bash
python main.py
```

## 🎮 Controls

During runtime:
- **`q`** - Quit the application
- **`p`** - Pause/Resume monitoring
- **`x`** - Toggle privacy mode (stops all monitoring)

## ⚙️ Configuration

Edit `config.json` after first run:

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

### Key Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `capture_interval` | Seconds between frame captures | 3.0 |
| `confidence_threshold` | Minimum confidence to intervene (0-1) | 0.6 |
| `min_intervention_interval` | Min seconds between suggestions | 30.0 |
| `output_mode` | `text`, `tts`, or `both` | text |
| `show_preview` | Display camera preview window | true |

## 🏗️ Architecture

```
User Environment (Camera Feed)
        ↓
Frame Capture (OpenCV)
        ↓
Scene Analyzer (BLIP)
        ↓
Intent Engine (Ollama LLM)
        ↓
Response Handler (Text/TTS)
        ↓
User Output
```

### Components

1. **Frame Capture** (`src/vision/frame_capture.py`)
   - Manages webcam access
   - Provides frame preprocessing

2. **Scene Analyzer** (`src/vision/scene_analyzer.py`)
   - BLIP-based scene captioning
   - Object detection (extensible)
   - Activity recognition (extensible)

3. **Intent Engine** (`src/reasoning/intent_engine.py`)
   - LLM-based intent inference
   - Context-aware reasoning
   - Confidence scoring

4. **Response Handler** (`src/output/response_handler.py`)
   - Formatted output delivery
   - TTS support
   - Intervention timing

5. **Privacy Manager** (`src/utils/privacy.py`)
   - Easy on/off controls
   - No data persistence
   - User consent enforcement

## 📊 Example Interactions

### Cooking Scenario
```
[Camera detects: person stirring pot on stove]

🤖 Assistant Suggestion [14:23:15]
Intent: User cooking, may need timing guidance
Confidence: 78%

💡 The sauce looks like it's simmering. Consider reducing 
   heat to prevent burning. Would you like me to set a 
   timer for 10 minutes?
```

### Work Scenario
```
[Camera detects: person sitting at desk, looking at screen]

🤖 Assistant Suggestion [10:45:30]
Intent: Extended work session detected
Confidence: 82%

💡 You've been working for 50 minutes straight. Taking a 
   5-minute break can help maintain focus and reduce eye 
   strain.
```

## 🔒 Privacy & Security

### What We Do
✅ All processing is **100% local**  
✅ **No cloud uploads** or external data transmission  
✅ **No frame saving** unless explicitly enabled  
✅ Easy **one-button disable** (press 'x')  
✅ Visual indicator when monitoring is active  
✅ Minimal intervention philosophy  

### What We Don't Do
❌ No recording or storing of video  
❌ No facial recognition or biometric data  
❌ No data sharing with third parties  
❌ No persistent logs of visual data  
❌ No background operation when closed  

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_frame_capture.py -v

# Test with coverage
pytest tests/ --cov=src --cov-report=html
```

## 🔧 Troubleshooting

### Camera not working
```bash
# Check camera permissions
# macOS: System Preferences > Security & Privacy > Camera
# Linux: Check camera device
ls /dev/video*

# Test camera directly
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"
```

### Ollama connection failed
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve &
```

### Poor performance
- Increase `capture_interval` to 5-10 seconds
- Use `blip-base` instead of `blip-large`
- Close other heavy applications
- Check if GPU is being utilized

### Models not downloading
```bash
# Check disk space
df -h

# Manually pull model
ollama pull phi3:latest

# Check HuggingFace cache
ls ~/.cache/huggingface/
```

## 🚧 Roadmap

### v0.2 (Planned)
- [ ] Object detection integration (YOLO)
- [ ] Gesture recognition
- [ ] Voice command support
- [ ] Performance optimizations

### v0.3 (Future)
- [ ] Activity recognition models
- [ ] Multi-camera support
- [ ] Smart home integration
- [ ] Mobile app

### v1.0 (Long-term)
- [ ] Advanced context memory
- [ ] Personalized learning
- [ ] Plugin system
- [ ] Cloud sync (optional)

## 📚 Dependencies

### Core Dependencies
- **opencv-python**: Camera capture and image processing
- **transformers**: BLIP vision model
- **torch**: Deep learning backend
- **requests**: Ollama API communication

### Optional Dependencies
- **pyttsx3**: Text-to-speech output
- **pytest**: Testing framework

## 🤝 Contributing

Contributions welcome! Please focus on:
- Performance improvements
- Additional vision models
- Better intent prompts
- Privacy enhancements
- Documentation

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **BLIP** by Salesforce for scene understanding
- **Ollama** for local LLM inference
- **OpenCV** for computer vision capabilities
- **Hugging Face** for model hosting

## 📧 Support

- Open an issue for bugs or feature requests
- Check the documentation in `/docs`
- Review troubleshooting guide above

---

**Note**: This is a prototype focused on local, privacy-first AI assistance. Always ensure you have proper consent before deploying in shared spaces.