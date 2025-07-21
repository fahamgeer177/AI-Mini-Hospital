import streamlit as st
from orchestrator import Orchestrator

def main():
    st.set_page_config(
        page_title="AI Mini-Hospital", 
        page_icon="🏥", 
        layout="wide"
    )
    
    st.title("🏥 AI Mini-Hospital")
    st.markdown("**Instant Expert Medical Guidance for Everyone**")
    st.markdown("---")
    
    # Initialize orchestrator
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = Orchestrator()
    
    # Sidebar for specialist selection
    st.sidebar.header("Choose Your Specialist")
    specialty = st.sidebar.selectbox(
        "Select a medical specialist:",
        ["neurologist", "therapist", "allergist"],
        index=0
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Consulting with: {specialty.title()}")
        
        # Symptoms input
        symptoms = st.text_area(
            "Describe your symptoms in detail:",
            placeholder="E.g., I have been experiencing headaches for 3 days, feeling nauseous...",
            height=150
        )
        
        # Consult button
        if st.button("Get Medical Advice", type="primary"):
            if symptoms.strip():
                with st.spinner("Analyzing your symptoms..."):
                    result = st.session_state.orchestrator.route(specialty, symptoms)
                
                if 'error' in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.success("Medical advice generated!")
                    
                    # Display results in an organized way
                    st.subheader("📋 Medical Assessment")
                    
                    # Create columns for better layout
                    res_col1, res_col2 = st.columns(2)
                    
                    with res_col1:
                        st.markdown("**🔍 Diagnosis:**")
                        st.info(result.get('diagnosis', 'N/A'))
                        
                        st.markdown("**💊 Recommended Medicine:**")
                        medicines = result.get('medicines', [])
                        if isinstance(medicines, list):
                            for med in medicines:
                                st.write(f"• {med}")
                        else:
                            st.write(f"• {medicines}")
                    
                    with res_col2:
                        st.markdown("**💉 Dosage:**")
                        st.info(result.get('dosage', 'N/A'))
                        
                        st.markdown("**⚠️ Restrictions:**")
                        st.warning(result.get('restrictions', 'None specified'))
                        
                        st.markdown("**⏰ Treatment Duration:**")
                        st.info(result.get('duration', 'N/A'))
            else:
                st.warning("Please describe your symptoms before consulting.")
    
    with col2:
        st.subheader("🩺 Available Specialists")
        specialists = {
            "neurologist": "🧠 Brain & Nervous System",
            "therapist": "🧘 Mental Health & Therapy",
            "allergist": "🤧 Allergies & Immune System"
        }
        
        for spec, desc in specialists.items():
            if spec == specialty:
                st.success(f"**{desc}** ✓")
            else:
                st.write(f"{desc}")
        
        st.markdown("---")
        st.subheader("📱 Quick Tips")
        st.markdown("""
        - Be specific about your symptoms
        - Mention duration and severity
        - Include any relevant medical history
        - Note any current medications
        """)
    
    # Disclaimer
    st.markdown("---")
    st.error("""
    ⚠️ **IMPORTANT DISCLAIMER:** This AI system provides general medical information only. 
    It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
    Always seek the advice of qualified healthcare providers with any questions about your health.
    In case of emergency, contact emergency services immediately.
    """)

if __name__ == '__main__':
    main()
