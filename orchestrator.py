from ai_agents.neurologist import NeurologistAgent
from ai_agents.therapist import TherapistAgent
from ai_agents.allergist import AllergistAgent

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
