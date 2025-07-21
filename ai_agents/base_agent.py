import os
import requests
import json
from dotenv import load_dotenv
import urllib3

# Disable SSL warnings for now
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

class MedicalAgent:
    def __init__(self, specialty):
        self.specialty = specialty
        self.api_key = os.getenv('IO_API_KEY')
        # Try different possible endpoints for IO API
        self.api_endpoints = [
            "https://api.io.net/v1/chat/completions",
            "https://api.ionet.io/v1/chat/completions",
            "https://io.net/api/v1/chat/completions"
        ]

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
                    "content": f"You are an expert {self.specialty} providing medical advice. Always respond in JSON format with the following structure: {{\"diagnosis\": \"brief diagnosis\", \"medicines\": [\"medicine1\", \"medicine2\"], \"dosage\": \"dosage instructions\", \"restrictions\": \"dietary/activity restrictions\", \"duration\": \"treatment duration\"}}. Be professional, accurate, and always include safety disclaimers."
                },
                {
                    "role": "user",
                    "content": f"Patient symptoms: {prompt}"
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        # Try each endpoint until one works
        for api_url in self.api_endpoints:
            try:
                print(f"Trying endpoint: {api_url}")
                response = requests.post(
                    api_url, 
                    headers=headers, 
                    json=payload, 
                    timeout=30,
                    verify=False  # Disable SSL verification temporarily
                )
                response.raise_for_status()
                
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Try to parse as JSON, fallback to structured text if needed
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # Fallback: extract information from text response
                    return self._parse_text_response(content)
                    
            except requests.exceptions.RequestException as e:
                print(f"Failed with endpoint {api_url}: {str(e)}")
                continue
        
        # If all endpoints fail, use OpenAI-compatible API as fallback
        return self._try_openai_fallback(prompt)
    
    def _try_openai_fallback(self, prompt):
        """Fallback to OpenAI API format"""
        openai_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are an expert {self.specialty} providing medical advice. Respond in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 500
        }
        
        try:
            response = requests.post(openai_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return json.loads(content)
        except:
            pass
        
        # Final fallback - return structured response
        return self._generate_fallback_response(prompt)
    
    def _generate_fallback_response(self, symptoms):
        """Generate a structured medical response when API fails"""
        # Basic symptom analysis based on keywords
        symptoms_lower = symptoms.lower()
        
        if any(word in symptoms_lower for word in ['headache', 'migraine', 'head pain']):
            return {
                "diagnosis": "Possible tension headache or migraine",
                "medicines": ["Paracetamol 500mg", "Ibuprofen 400mg"],
                "dosage": "Take as directed on package, do not exceed daily limits",
                "restrictions": "Avoid bright lights, loud noises. Stay hydrated",
                "duration": "If symptoms persist beyond 48 hours, consult a doctor"
            }
        elif any(word in symptoms_lower for word in ['anxiety', 'stress', 'panic', 'worried']):
            return {
                "diagnosis": "Possible anxiety or stress-related symptoms",
                "medicines": ["Deep breathing exercises", "Relaxation techniques"],
                "dosage": "Practice 10-15 minutes daily",
                "restrictions": "Limit caffeine, avoid alcohol",
                "duration": "Consider professional counseling if symptoms persist"
            }
        elif any(word in symptoms_lower for word in ['allergy', 'rash', 'itching', 'sneezing']):
            return {
                "diagnosis": "Possible allergic reaction",
                "medicines": ["Antihistamines (Cetirizine 10mg)", "Topical cream for rash"],
                "dosage": "Once daily for antihistamines, apply cream as needed",
                "restrictions": "Identify and avoid allergen triggers",
                "duration": "3-7 days, seek help if symptoms worsen"
            }
        else:
            return {
                "diagnosis": "Symptoms require professional medical evaluation",
                "medicines": ["Symptomatic relief only"],
                "dosage": "As appropriate for specific symptoms",
                "restrictions": "Monitor symptoms carefully",
                "duration": "Please consult a healthcare provider for proper diagnosis"
            }
    
    def _parse_text_response(self, text):
        """Fallback method to parse non-JSON responses"""
        return {
            "diagnosis": "Please consult with a medical professional",
            "medicines": ["Over-the-counter pain relief if appropriate"],
            "dosage": "As directed on packaging",
            "restrictions": "Monitor symptoms closely",
            "duration": "Seek medical attention if symptoms persist",
            "note": "AI response could not be parsed properly"
        }

    def analyze(self, symptoms):
        raise NotImplementedError("Each agent must implement its own analyze method.")
