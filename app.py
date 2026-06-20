import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Initialize the Gemini Client
try:
    client = genai.Client()
except Exception as e:
    st.error("Could not find your Gemini API Key. Make sure your environment variable is set!")

# 2. Configure the Streamlit Page Layout
st.set_page_config(page_title="ReferralCraft AI", page_icon="✉️", layout="wide")

st.title("✉️ ReferralCraft AI")
st.write("Generate a hyper-personalized referral request by providing context about yourself, the role, and your connection.")

st.divider()

# 3. The New Form UI Component Layout
with st.form("outreach_form"):
    
    # --- SECTION 1: ABOUT YOU ---
    st.subheader("Section 1: About You")
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Your Name")
    with col2:
        user_role = st.text_input("Current Role")
    
    user_bg = st.text_area("Short Background", placeholder="e.g., 3 years in fintech building scalable APIs...")
    user_resume = st.text_area("Resume Summary", placeholder="Paste a few bullet points from your resume here.")
    
    st.divider()
    
    # --- SECTION 2: TARGET JOB ---
    st.subheader("Section 2: Target Job")
    col3, col4 = st.columns(2)
    with col3:
        target_company = st.text_input("Target Company")
    with col4:
        target_role = st.text_input("Target Role")
        
    target_jd = st.text_area("Job Description", placeholder="Paste the core requirements or description of the job.")
    
    st.divider()
    
    # --- SECTION 3: REFERRAL CONTACT ---
    st.subheader("Section 3: Referral Contact")
    col5, col6 = st.columns(2)
    with col5:
        contact_name = st.text_input("Contact's Name")
    with col6:
        contact_headline = st.text_input("Contact's LinkedIn Headline")
        
    contact_about = st.text_area("Contact's LinkedIn About Section", placeholder="Paste their about section here.")
    common_ground = st.text_area("Anything Common?", placeholder="e.g., We both went to the same university, or both love AI products.")
    
    # Submit button
    submit_button = st.form_submit_button("Generate Referral Draft")

# 4. Logic Execution upon submission
if submit_button:
    if not target_company or not target_role or not contact_name:
        st.warning("Please provide at least the Target Company, Target Role, and Contact's Name.")
    else:
        with st.spinner("Crafting your personalized referral note..."):
            
            # The PM Prompt Engineering - Now highly contextual
            system_instruction = """
            You are an expert Executive Career Coach, Technical Recruiter and expert writer. 
            Your goal is to write a highly compelling, personalized LinkedIn referral request and I should get the referral.
            Keep the message concise (under ~150 words). 
            Do not use generic placeholders. 
            Make sure the text is completely ready to copy and paste.
            Focus on drawing a subtle but clear line between the User's background and the Job Description, while warmly acknowledging the Contact's background. Write as a linkedin message not as an email.
            """
            
            user_prompt = f"""
            Write a referral request message from {user_name} to {contact_name}.
            
            ABOUT THE SENDER ({user_name}):
            - Current Role: {user_role}
            - Background: {user_bg}
            - Resume Summary: {user_resume}
            
            ABOUT THE TARGET ROLE:
            - Company: {target_company}
            - Role: {target_role}
            - Job Description Details: {target_jd}
            
            ABOUT THE RECIPIENT ({contact_name}):
            - Headline: {contact_headline}
            - About Section: {contact_about}
            
            COMMON GROUND TO MENTION:
            - {common_ground if common_ground else 'None specified'}
            
            Write exactly ONE highly optimized output option that sounds human, professional, and confident.
            """
            
            try:
                # Using the lightweight model you configured
                response = client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7 
                    )
                )
                
                st.success("Draft Generated Successfully!")
                st.text_area("Your Ready-to-Use Message:", value=response.text, height=300)
                
            except Exception as e:
                st.error(f"An error occurred while talking to the AI engine: {e}")