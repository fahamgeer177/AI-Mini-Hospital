# 🏥 AI Mini-Hospital System

## 📋 Table of Contents
- [Problem Statement](#problem-statement)
- [Solution & Goals](#solution--goals)
- [System Architecture](#system-architecture)
- [Key Features](#key-features)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [API Integration](#api-integration)
- [Future Enhancements](#future-enhancements)

## 🚨 Problem Statement

Millions of people in poor and rural communities worldwide lack access to basic healthcare services. The challenges include:

- **Geographic Isolation**: Remote areas with no nearby hospitals or clinics
- **Economic Barriers**: High costs of medical consultations and travel
- **Limited Specialists**: Shortage of specialized doctors in underserved regions
- **Time-Critical Situations**: Delays in getting medical advice can be life-threatening
- **Knowledge Gap**: Lack of basic medical knowledge for common ailments

### Real-World Impact
- Over 3.6 billion people lack access to quality healthcare
- Rural areas often have 1 doctor per 10,000+ people vs. urban 1:300 ratio
- Medical emergencies result in preventable deaths due to delayed care

## 🎯 Solution & Goals

### Primary Goal
Create an **affordable, AI-powered mini-hospital system** accessible via smartphones that provides instant, expert medical guidance to underserved communities.

### Core Objectives
1. **Democratize Healthcare**: Make expert medical advice accessible to everyone
2. **Instant Response**: Provide immediate medical guidance 24/7
3. **Specialist Coverage**: Simulate consultations with various medical specialists
4. **Cost-Effective**: Eliminate travel and consultation costs
5. **Scalable Solution**: Serve unlimited patients simultaneously

### Target Impact
- **Primary**: Rural and economically disadvantaged communities
- **Secondary**: Urban areas needing quick preliminary medical advice
- **Emergency**: First-aid guidance before professional help arrives

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Patient UI    │    │   Orchestrator  │    │   AI Agents     │
│  (Streamlit)    │◄──►│    Router       │◄──►│   Specialists   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Symptom Input  │    │ Route Selection │    │  LLM API Calls  │
│  User Interface │    │ Agent Selection │    │ Medical Analysis│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ✨ Key Features

### 🤖 AI Medical Specialists
- **Neurologist**: Brain, nervous system, headaches, seizures
- **Therapist**: Mental health, anxiety, depression, stress
- **Allergist**: Allergies, immune system, asthma, reactions

### 💻 User Interface
- Clean, intuitive Streamlit web interface
- Mobile-responsive design
- Real-time symptom analysis
- Structured medical advice output

### 🔒 Safety Features
- Comprehensive medical disclaimers
- Emergency contact recommendations
- Professional consultation reminders
- Fallback responses for API failures

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- IO API Key (for LLM integration)
- Internet connection

### Step-by-Step Installation

1. **Clone/Download the Project**
```bash
git clone https://github.com/fahamgeer177/AI-Mini-Hospital.git
cd Virtual-Hospital
```

2. **Set up Python Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**
Create `.env` file in project root:
```
IO_API_KEY=your_io_api_key_here
```

5. **Run the Application**
```bash
streamlit run app.py
```

## 🚀 Usage

### For Patients
1. **Access the System**: Open web browser and navigate to the Streamlit app
2. **Select Specialist**: Choose appropriate medical specialist from sidebar
3. **Describe Symptoms**: Provide detailed symptom description
4. **Get Advice**: Receive structured medical guidance including:
   - Preliminary diagnosis
   - Recommended medicines
   - Dosage instructions
   - Restrictions and precautions
   - Treatment duration

### Example Interaction
```
Specialist: Neurologist
Symptoms: "I've been having severe headaches for 3 days, with nausea and sensitivity to light"

Response:
- Diagnosis: Possible migraine headache
- Medicine: Ibuprofen 400mg, rest in dark room
- Dosage: Every 6 hours, max 3 doses/day
- Restrictions: Avoid bright lights, loud noises
- Duration: 24-48 hours, see doctor if persists
```

## 📁 Code Structure

### Project Organization
```
Virtual-Hospital/
├── ai_agents/              # Medical specialist agents
│   ├── __init__.py
│   ├── base_agent.py       # Base agent class
│   ├── neurologist.py      # Neurologist specialist
│   ├── therapist.py        # Mental health specialist
│   └── allergist.py        # Allergy specialist
├── app.py                  # Streamlit frontend
├── orchestrator.py         # Agent routing system
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md              # This file
```

### 🧠 Core Components Explained

#### 1. Base Agent Class (`base_agent.py`)

```python
class MedicalAgent:
    def __init__(self, specialty):
        self.specialty = specialty
        self.api_key = os.getenv('IO_API_KEY')
        self.api_endpoints = [
            "https://api.io.net/v1/chat/completions",
            "https://api.ionet.io/v1/chat/completions",
            "https://io.net/api/v1/chat/completions"
        ]
```

**Purpose**: Foundation class for all medical specialists
**Key Features**:
- API key management from environment variables
- Multiple endpoint fallbacks for reliability
- Standardized response format
- Error handling and fallback mechanisms

#### 2. LLM Integration Method

```python
def call_llm(self, prompt):
    """Make API call to IO API with multiple endpoint fallbacks"""
    headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json",
        "User-Agent": "VirtualHospital/1.0"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert {self.specialty} providing medical advice..."
            },
            {
                "role": "user", 
                "content": f"Patient symptoms: {prompt}"
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
```

**Purpose**: Handles communication with AI language models
**Key Features**:
- Multiple API endpoint attempts for reliability
- Structured prompting for consistent medical responses
- JSON response parsing with fallbacks
- Professional medical context setting

#### 3. Specialist Agent Example (`neurologist.py`)

```python
class NeurologistAgent(MedicalAgent):
    def __init__(self):
        super().__init__('Neurologist')

    def analyze(self, symptoms):
        neurologist_prompt = f"""
        As a Neurologist, analyze these symptoms: {symptoms}
        
        Focus on neurological conditions including:
        - Headaches and migraines
        - Seizures and epilepsy
        - Stroke symptoms
        - Memory and cognitive issues
        - Nerve pain and neuropathy
        """
        return self.call_llm(neurologist_prompt)
```

**Purpose**: Specialized medical agent for neurological conditions
**Key Features**:
- Domain-specific medical expertise
- Tailored symptom analysis
- Neurological condition focus
- Structured diagnostic approach

#### 4. Orchestrator System (`orchestrator.py`)

```python
class Orchestrator:
    def __init__(self):
        self.agents = {
            'neurologist': NeurologistAgent(),
            'therapist': TherapistAgent(),
            'allergist': AllergistAgent(),
        }

    def route(self, specialty, symptoms):
        agent = self.agents.get(specialty)
        if not agent:
            return {'error': 'Specialist not found'}
        return agent.analyze(symptoms)
```

**Purpose**: Central routing system for patient-specialist matching
**Key Features**:
- Dynamic agent selection
- Centralized specialist management
- Error handling for unknown specialties
- Scalable architecture for adding new specialists

#### 5. Streamlit Frontend (`app.py`)

```python
def main():
    st.set_page_config(
        page_title="AI Mini-Hospital", 
        page_icon="🏥", 
        layout="wide"
    )
    
    st.title("🏥 AI Mini-Hospital")
    st.markdown("**Instant Expert Medical Guidance for Everyone**")
    
    # Specialist selection
    specialty = st.sidebar.selectbox(
        "Select a medical specialist:",
        ["neurologist", "therapist", "allergist"]
    )
    
    # Symptoms input
    symptoms = st.text_area(
        "Describe your symptoms in detail:",
        placeholder="E.g., I have been experiencing headaches...",
        height=150
    )
```

**Purpose**: User-friendly web interface for patient interaction
**Key Features**:
- Responsive design for mobile devices
- Intuitive specialist selection
- Structured symptom input
- Real-time result display
- Professional medical disclaimers

### 🔄 Fallback Mechanisms

#### Smart Response Fallbacks
```python
def _generate_fallback_response(self, symptoms):
    symptoms_lower = symptoms.lower()
    
    if any(word in symptoms_lower for word in ['headache', 'migraine']):
        return {
            "diagnosis": "Possible tension headache or migraine",
            "medicines": ["Paracetamol 500mg", "Ibuprofen 400mg"],
            "dosage": "Take as directed on package",
            "restrictions": "Avoid bright lights, stay hydrated",
            "duration": "If symptoms persist beyond 48 hours, consult a doctor"
        }
```

**Purpose**: Ensures system reliability even when APIs fail
**Features**:
- Keyword-based symptom analysis
- Basic medical guidance
- Safety-first approach
- Professional consultation recommendations

## 🔌 API Integration

### IO API Configuration
```python
# Environment setup
IO_API_KEY=your_io_api_key_here

# Multiple endpoint support
api_endpoints = [
    "https://api.io.net/v1/chat/completions",
    "https://api.ionet.io/v1/chat/completions", 
    "https://io.net/api/v1/chat/completions"
]
```

### Request Structure
```python
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "Expert medical specialist prompt"},
        {"role": "user", "content": "Patient symptoms"}
    ],
    "max_tokens": 500,
    "temperature": 0.7
}
```

### Response Processing
```python
# JSON response parsing
try:
    return json.loads(content)
except json.JSONDecodeError:
    return self._parse_text_response(content)
```

## 🔮 Future Enhancements

### Phase 2: Extended Specialists
- **Cardiologist**: Heart and cardiovascular conditions
- **Pediatrician**: Children's health and development
- **Dermatologist**: Skin conditions and diseases
- **Orthopedist**: Bone and joint problems
- **General Practitioner**: Primary care and general medicine

### Phase 3: Advanced Features
- **Multilingual Support**: Local language interfaces
- **Voice Input**: Speech-to-text symptom description
- **Image Analysis**: Photo-based diagnosis for visible symptoms
- **Treatment Tracking**: Follow-up and progress monitoring
- **Emergency Detection**: Automatic emergency service alerts

### Phase 4: Mobile & Offline
- **Mobile App**: Native iOS/Android applications
- **Offline Mode**: Basic diagnosis without internet
- **SMS Integration**: Text-based consultations
- **Telemedicine**: Video calls with human doctors
- **Health Records**: Personal medical history tracking

### Phase 5: Community & Scale
- **Community Health**: Public health monitoring
- **Epidemic Tracking**: Disease outbreak detection
- **Health Education**: Medical knowledge resources
- **Doctor Integration**: Human specialist oversight
- **Insurance Integration**: Healthcare cost management

## 🚨 Important Disclaimers

⚠️ **CRITICAL**: This AI system provides general medical information only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- Always seek advice from qualified healthcare providers
- In emergencies, contact emergency services immediately
- This system is for preliminary guidance only
- Human medical professionals should validate all recommendations
- Use at your own risk and discretion

## 📞 Emergency Contacts

- **Emergency Services**: Call your local emergency number
- **Poison Control**: Contact your local poison control center
- **Mental Health Crisis**: Contact your local mental health hotline

---

## 🤝 Contributing

We welcome contributions to improve this life-saving technology:

1. Fork the repository
2. Create feature branches
3. Add new medical specialists
4. Improve diagnostic accuracy
5. Enhance user interface
6. Submit pull requests

Together, we can democratize healthcare access worldwide! 🌍💙

---

**Built with ❤️ for global healthcare accessibility**
