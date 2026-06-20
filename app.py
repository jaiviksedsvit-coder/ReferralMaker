import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Initialize the Gemini Client
try:
    client = genai.Client()
except Exception as e:
    st.error("Could not find your Gemini API Key. Make sure your Streamlit Secrets are set!")

# 2. Configure the Streamlit Page Layout
st.set_page_config(page_title="ReferralCraft AI", page_icon="✉️", layout="wide")

st.title("✉️ ReferralCraft AI")
st.write("Generate a hyper-personalized referral request. Provide URLs, background notes, or both!")
st.divider()

# 3. The Form UI
with st.form("outreach_form"):
    
    # --- SECTION 1: ABOUT YOU ---
    st.subheader("Section 1: About You")
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Your Name")
    with col2:
        user_role = st.text_input("Current Role")
    
    user_url = st.text_input("Your LinkedIn URL (Optional)", placeholder="e.g., linkedin.com/in/your-profile")
    user_linkedin = st.text_area(
        "Your Background / Resume Notes (Optional)", 
        placeholder="Paste a few bullet points from your resume here if you want extra precision."
    )
    
    st.divider()
    
    # --- SECTION 2: TARGET JOB ---
    st.subheader("Section 2: Target Job")
    col3, col4 = st.columns(2)
    with col3:
        target_company = st.text_input("Target Company")
    with col4:
        target_role = st.text_input("Target Role")
        
    target_jd = st.text_area(
        "Job Description Context", 
        placeholder="Paste the core requirements or a summary of the job description."
    )
    
    st.divider()
    
    # --- SECTION 3: REFERRAL CONTACT ---
    st.subheader("Section 3: Referral Contact")
    contact_name = st.text_input("Contact's Name")
    
    contact_url = st.text_input("Contact's LinkedIn URL (Optional)", placeholder="e.g., linkedin.com/in/their-profile")    
    contact_linkedin = st.text_area(
        "Contact's Background Notes (Optional)", 
        placeholder="Paste their LinkedIn Headline or 'About' section here."
    )
    
    common_ground = st.text_input(
        "Anything Common? (Optional)", 
        placeholder="e.g., We both went to the same university, or both love AI products."
    )
    
    # Submit button
    submit_button = st.form_submit_button("Generate Referral Draft")

# 4. Logic Execution
if submit_button:
    if not target_company or not target_role or not contact_name or not user_name:
        st.warning("Please fill in at least Your Name, Target Company, Target Role, and Contact Name.")
    else:
        with st.spinner("Analyzing inputs and crafting your personalized note..."):
            
            # Instructing the AI to attempt URL analysis alongside the text
            system_instruction = """
            You are an expert Executive Career Coach and Technical Recruiter. 
            Your goal is to write a highly compelling, personalized LinkedIn referral request (under 150 words).
            Analyze all provided context. If LinkedIn URLs are provided, try to extract or infer details from the URL slugs to draw parallels between the user and the contact.
            Do not use generic placeholders. Make sure the text sounds human, warm, and confident.
            """
            
            user_prompt = f"""
            Write a referral request from {user_name} to {contact_name}.
            
            ABOUT THE SENDER ({user_name}):
            - Current Role: {user_role}
            - LinkedIn URL: {user_url if user_url else 'None provided'}
            - Background Data: {user_linkedin if user_linkedin else 'None provided'}
            
            ABOUT THE TARGET ROLE:
            - Company: {target_company}
            - Role: {target_role}
            - Job Description Details: {target_jd}
            
            ABOUT THE RECIPIENT ({contact_name}):
            - LinkedIn URL: {contact_url if contact_url else 'None provided'}
            - Background Data: {contact_linkedin if contact_linkedin else 'None provided'}
            
            COMMON GROUND TO MENTION:
            - {common_ground if common_ground else 'None specified'}
            
            Provide exactly ONE highly optimized message ready to be sent.
            """
            
            try:
                # Assuming gemini-2.0-flash as the current standard
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7 
                    )
                )
                
                st.success("Draft Generated Successfully!")
                st.text_area("Your Ready-to-Use Message:", value=response.text, height=250)
                
            except Exception as e:
                st.error(f"An error occurred while talking to the AI engine: {e}")
