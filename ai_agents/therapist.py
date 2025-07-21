from .base_agent import MedicalAgent

class TherapistAgent(MedicalAgent):
    def __init__(self):
        super().__init__('Mental Health Therapist')

    def analyze(self, symptoms):
        therapist_prompt = f"""
        As a Mental Health Therapist, analyze these symptoms: {symptoms}
        
        Focus on mental health conditions including but not limited to:
        - Anxiety and panic disorders
        - Depression and mood disorders
        - Stress-related conditions
        - Sleep disorders
        - PTSD and trauma responses
        - Behavioral patterns
        - Emotional regulation issues
        
        Provide therapeutic recommendations, coping strategies, and when appropriate, suggest whether medication consultation might be beneficial. Always emphasize the importance of professional therapy sessions.
        """
        
        return self.call_llm(therapist_prompt)
