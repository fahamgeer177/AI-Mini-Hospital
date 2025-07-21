from .base_agent import MedicalAgent

class NeurologistAgent(MedicalAgent):
    def __init__(self):
        super().__init__('Neurologist')

    def analyze(self, symptoms):
        neurologist_prompt = f"""
        As a Neurologist, analyze these symptoms: {symptoms}
        
        Focus on neurological conditions including but not limited to:
        - Headaches and migraines
        - Seizures and epilepsy
        - Stroke symptoms
        - Memory and cognitive issues
        - Nerve pain and neuropathy
        - Movement disorders
        - Brain and spinal cord conditions
        
        Provide a professional assessment with appropriate treatment recommendations.
        """
        
        return self.call_llm(neurologist_prompt)
