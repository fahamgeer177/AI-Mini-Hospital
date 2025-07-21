from .base_agent import MedicalAgent

class AllergistAgent(MedicalAgent):
    def __init__(self):
        super().__init__('Allergist and Immunologist')

    def analyze(self, symptoms):
        allergist_prompt = f"""
        As an Allergist and Immunologist, analyze these symptoms: {symptoms}
        
        Focus on allergic and immune system conditions including but not limited to:
        - Seasonal and environmental allergies
        - Food allergies and intolerances
        - Skin allergies and eczema
        - Asthma and respiratory allergies
        - Drug allergies
        - Anaphylaxis risk assessment
        - Immune system disorders
        - Allergy testing recommendations
        
        Provide assessment of potential allergens, treatment options, and prevention strategies. Include emergency action plans if severe allergic reactions are suspected.
        """
        
        return self.call_llm(allergist_prompt)
