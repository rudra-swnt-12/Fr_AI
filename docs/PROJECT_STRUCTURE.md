# Proactive Multimodal AI Assistant - Project Structure

## 📁 Complete Directory Structure

```
proactive-ai-assistant/
│
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── config.json                      # Configuration file (auto-generated)
├── README.md                        # Project documentation
├── .gitignore                       # Git ignore file
│
├── src/                             # Source code modules
│   ├── __init__.py
│   │
│   ├── vision/                      # Computer vision components
│   │   ├── __init__.py
│   │   ├── frame_capture.py        # Webcam frame capture
│   │   └── scene_analyzer.py       # Scene understanding (BLIP)
│   │
│   ├── reasoning/                   # Intent inference
│   │   ├── __init__.py
│   │   └── intent_engine.py        # LLM-based intent inference
│   │
│   ├── output/                      # Response delivery
│   │   ├── __init__.py
│   │   └── response_handler.py     # Text/TTS output
│   │
│   ├── config/                      # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py             # Settings loader
│   │
│   └── utils/                       # Utility modules
│       ├── __init__.py
│       └── privacy.py              # Privacy controls
│
├── data/                            # Data directory
│   ├── models/                      # Cached models
│   ├── cache/                       # Temporary cache
│   └── .privacy_mode               # Privacy flag file
│
├── logs/                            # Application logs
│   └── assistant.log
│
└── tests/                           # Unit tests
    ├── __init__.py
    ├── test_frame_capture.py
    ├── test_scene_analyzer.py
    └── test_intent_engine.py
```

## 🚀 Setup Instructions

### 1. Prerequisites

**Install Ollama** (for local LLM):
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com/download
```

**Pull LLM model**:
```bash
ollama pull llama3.1
# or
ollama pull phi3
```

**Start Ollama server**:
```bash
ollama serve
```

### 2. Project Setup

**Create project directory**:
```bash
mkdir proactive-ai-assistant
cd proactive-ai-assistant
```

**Create virtual environment**:
```bash
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**Install dependencies**:
```bash
pip install -r requirements.txt
```

**Create directory structure**:
```bash
mkdir -p src/vision src/reasoning src/output src/config src/utils
mkdir -p data/models data/cache logs tests
touch src/__init__.py src/vision/__init__.py src/reasoning/__init__.py
touch src/output/__init__.py src/config/__init__.py src/utils/__init__.py
```

### 3. First Run

**Run the assistant**:
```bash
python main.py
```

**Controls during runtime**:
- Press `q` to quit
- Press `p` to pause/resume
- Press `x` to toggle privacy mode

## ⚙️ Configuration

Edit `config.json` to customize settings:

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

### Key Settings Explained

- **capture_interval**: Seconds between frame captures (default: 3.0)
- **confidence_threshold**: Minimum confidence (0-1) to trigger intervention (default: 0.6)
- **min_intervention_interval**: Minimum seconds between suggestions (default: 30)
- **output_mode**: `text`, `tts`, or `both`
- **vision_model**: `blip-base` (faster) or `blip-large` (more accurate)

## 🔧 Component Overview

### Frame Capture (`src/vision/frame_capture.py`)
- Captures webcam frames using OpenCV
- Handles camera initialization and resource management
- Provides frames in BGR or RGB format

### Scene Analyzer (`src/vision/scene_analyzer.py`)
- Uses BLIP model for scene captioning
- Generates natural language descriptions
- Placeholder for object detection and activity recognition

### Intent Engine (`src/reasoning/intent_engine.py`)
- Interfaces with Ollama for LLM inference
- Analyzes scene context and history
- Determines when and how to intervene
- Returns structured intent with confidence scores

### Response Handler (`src/output/response_handler.py`)
- Formats and delivers suggestions
- Supports text and TTS output
- Manages intervention timing

### Privacy Manager (`src/utils/privacy.py`)
- Controls monitoring on/off state
- File-based privacy flag
- Easy toggle mechanism

## 🧪 Testing

**Run tests**:
```bash
pytest tests/
```

**Test individual components**:
```bash
# Test webcam capture
python -c "from src.vision.frame_capture import FrameCapture; fc = FrameCapture(); print('Camera OK' if fc.get_frame() is not None else 'Camera Error')"

# Test Ollama connection
curl http://localhost:11434/api/tags
```

## 📝 Usage Examples

### Scenario 1: Cooking Assistant
- User is cooking and reading a recipe
- Assistant detects: "person looking at pan on stove"
- Intent: User might need timing help
- Suggestion: "Would you like me to set a timer?"

### Scenario 2: Work Productivity
- User staring at screen for extended period
- Assistant detects: "person sitting at desk"
- Intent: Possible fatigue or need for break
- Suggestion: "You've been working for 45 minutes. Consider a short break?"

### Scenario 3: Exercise Support
- User doing workout with equipment
- Assistant detects: "person with exercise mat"
- Intent: Exercise routine in progress
- Suggestion: "Keep your core engaged during planks!"

## 🔒 Privacy & Ethics

**Built-in Privacy Features**:
- No cloud uploads - all processing is local
- Privacy mode toggle (press 'x')
- No frame saving by default
- Minimal intervention philosophy
- User consent-first design

**Best Practices**:
- Inform users about camera usage
- Provide easy disable mechanism
- Log all interventions
- Respect user autonomy
- Minimize false positives

## 🚧 Future Enhancements

1. **Object Detection**: Integrate YOLO for precise object recognition
2. **Action Recognition**: Add activity classification models
3. **Voice Input**: Enable voice commands for interaction
4. **Gesture Control**: Recognize hand gestures for commands
5. **Multi-camera**: Support multiple camera feeds
6. **Smart Home Integration**: Control IoT devices
7. **Context Memory**: Long-term user preference learning
8. **Mobile App**: Extend to mobile platforms

## 🐛 Troubleshooting

**Camera not accessible**:
```bash
# Check camera permissions
# On macOS: System Preferences > Security & Privacy > Camera
# On Linux: Check /dev/video0 exists
ls /dev/video*
```

**Ollama not connecting**:
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve
```

**Model download slow**:
```bash
# Models are downloaded on first use
# BLIP models: ~1GB (base) or ~2GB (large)
# Check ~/.cache/huggingface/ for downloaded models
```

**Low FPS/Performance**:
- Increase `capture_interval` in config.json
- Use smaller vision model (blip-base)
- Close other applications
- Consider GPU acceleration if available

## 📚 Dependencies

**Core**:
- OpenCV: Camera capture and image processing
- Transformers/PyTorch: BLIP vision model
- Requests: Ollama API communication

**Optional**:
- pyttsx3: Text-to-speech output
- pytest: Testing framework

## 📄 License

MIT License - Feel free to modify and extend!

## 🤝 Contributing

Contributions welcome! Focus areas:
- Additional vision models
- Better intent inference prompts
- Performance optimizations
- Privacy enhancements
- Documentation improvements