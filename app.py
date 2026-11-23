import os
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.styles import get_custom_css
from utils.parser import extract_text_from_file, extract_key_bullets
from utils.ai_engine import (
    get_gemini_client,
    generate_referral_campaign,
    rewrite_message,
    DEFAULT_MODELS
)

# 1. Page Configuration
st.set_page_config(
    page_title="ReferralCraft AI - Next-Gen Referral Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom Design System
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 3. Session State Initialization
if "campaign_result" not in st.session_state:
    st.session_state.campaign_result = None

if "pipeline_records" not in st.session_state:
    st.session_state.pipeline_records = []

# Demo presets
DEMO_PRESETS = {
    "New Grad (Alumni Outreach)": {
        "user_name": "Aarav Sharma",
        "user_role": "CS Senior @ University of Washington",
        "user_url": "linkedin.com/in/aarav-cs",
        "user_background": "Built a distributed cache in Go, 2 internships in full-stack web development, VP of Web3 Student Club.",
        "target_company": "Stripe",
        "target_role": "Associate Software Engineer",
        "target_jd": "Looking for entry-level engineers with strong foundations in API design, Python/Go, and passion for developer infrastructure.",
        "contact_name": "David Chen",
        "contact_headline": "Senior Staff Engineer @ Stripe | UW Alum '18",
        "contact_linkedin": "Leads Core Payments Infrastructure, previously Amazon, UW CS alumnus.",
        "relationship": "🎓 College / University Alumni",
        "tone": "🌱 Enthusiastic & Humble",
        "call_to_action": "☕ 10-minute quick chat or advice on team",
        "common_ground": "Both graduated/studying at UW CS department, passionate about payments infrastructure."
    },
    "Mid-Career (Product Manager)": {
        "user_name": "Elena Rostova",
        "user_role": "Senior Product Manager",
        "user_url": "linkedin.com/in/elena-pm",
        "user_background": "7 years leading B2B SaaS products at ScaleAI. Grew ARR from $4M to $22M, led cross-functional team of 14 engineers.",
        "target_company": "Figma",
        "target_role": "Lead Product Manager, Enterprise Ecosystem",
        "target_jd": "Seeking senior PM to lead enterprise integrations, API platform expansion, and collaboration workflows.",
        "contact_name": "Sarah Jenkins",
        "contact_headline": "Director of Product Management @ Figma",
        "contact_linkedin": "Leading Core Platform product org, ex-Atlassian.",
        "relationship": "🤝 Ex-Colleague or Mutual Connection",
        "tone": "🎯 Confident & Direct",
        "call_to_action": "📄 Quick resume review / feedback on alignment",
        "common_ground": "Mutual connection through Product Leaders Network, both spoke at SaaStr 2024."
    }
}

# 4. Sidebar Controls
with st.sidebar:
    st.markdown("### 🚀 ReferralCraft AI `v2.0`")
    st.caption("Executive Referral Strategy & Multi-Channel Suite")
    
    st.divider()
    st.markdown("#### 🔑 Gemini Configuration")
    
    # API Key Handling (BYOK or environment fallback)
    default_key = os.environ.get("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Gemini API Key",
        value=default_key,
        type="password",
        placeholder="AIzaSy...",
        help="Obtain a free API key at https://aistudio.google.com"
    )
    
    selected_model = st.selectbox(
        "Model Selection",
        options=DEFAULT_MODELS,
        index=0,
        help="Gemini 2.5 Flash is recommended for balanced speed, quality, and low latency."
    )
    
    client = get_gemini_client(api_key_input)
    if client:
        st.success("✓ Gemini Engine Ready", icon="✅")
    else:
        st.warning("⚠️ Enter your Gemini API Key above to generate live referrals.", icon="⚠️")
        st.markdown("[Get free Gemini API Key →](https://aistudio.google.com)")

    st.divider()
    st.markdown("#### ⚡ 1-Click Demo Presets")
    st.caption("Load realistic profiles to test without typing:")
    
    demo_choice = st.selectbox("Select Demo Scenario", ["Custom (Empty)"] + list(DEMO_PRESETS.keys()))
    if st.button("Load Selected Demo", use_container_width=True):
        if demo_choice in DEMO_PRESETS:
            preset = DEMO_PRESETS[demo_choice]
            for k, v in preset.items():
                st.session_state[f"form_{k}"] = v
            st.rerun()

    st.divider()
    st.markdown("#### 📚 Referral Golden Rules")
    st.markdown(
        """
        - **Value First**: Compliment their work before asking.
        - **Keep it Short**: Connection requests must stay under 300 chars.
        - **Make it Easy**: Provide target job ID and 2 bullet points on why you match.
        - **Soft Ask**: Never demand an instant referral; ask for their perspective.
        """
    )

# 5. Hero Header Section
st.markdown(
    """
    <div class="hero-container">
        <span class="hero-badge">ReferralCraft AI 2.0 • Omni-Channel Product Edition</span>
        <h1 class="hero-title">Turn Cold Applications Into Warm Referrals</h1>
        <p class="hero-subtitle">
            Generate tailored LinkedIn connection notes, InMails, cold emails, and follow-ups with 
            an integrated AI Etiquette Audit that eliminates desperate phrasing and maximizes replies.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Metric Highlight Row
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Interview Multiplier</div>
            <div class="metric-value">4.0x</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_m2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">LinkedIn Char Limit</div>
            <div class="metric-value">≤ 300</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_m3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Channels Built</div>
            <div class="metric-value">5 Assets</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_m4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Tone & Etiquette</div>
            <div class="metric-value">Peer-Level</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# 6. Main Navigation Tabs
tab_generator, tab_campaign, tab_audit, tab_tracker = st.tabs([
    "✍️ 1. Referral Suite Generator",
    "📬 2. Multi-Channel Campaign",
    "🛡️ 3. Etiquette & Cringe Audit",
    "📊 4. Outreach Pipeline Tracker"
])

# =========================================================================
# TAB 1: GENERATOR FORM
# =========================================================================
with tab_generator:
    st.subheader("Configure Your Referral Outreach Strategy")
    st.caption("Provide candidate details, target opportunity, and recipient info.")
    
    with st.form("referral_suite_form"):
        # Section 1: Candidate Background
        st.markdown('<div class="section-tag">👤 Section 1: Sender Profile (You)</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            user_name = st.text_input(
                "Your Name",
                value=st.session_state.get("form_user_name", ""),
                placeholder="e.g. Alex Morgan"
            )
        with col2:
            user_role = st.text_input(
                "Your Current Role / Title",
                value=st.session_state.get("form_user_role", ""),
                placeholder="e.g. Senior Frontend Engineer"
            )
        
        user_url = st.text_input(
            "Your LinkedIn Profile URL (Optional)",
            value=st.session_state.get("form_user_url", ""),
            placeholder="e.g. linkedin.com/in/alexmorgan"
        )
        
        # Resume File Uploader + Text Area
        uploaded_resume = st.file_uploader("Upload Resume (PDF / TXT) for Smart Extraction", type=["pdf", "txt"])
        
        parsed_resume_text = ""
        if uploaded_resume is not None:
            extracted = extract_text_from_file(uploaded_resume)
            if extracted:
                parsed_resume_text = extract_key_bullets(extracted, max_chars=1800)
                st.info(f"✓ Extracted {len(parsed_resume_text)} characters of highlights from `{uploaded_resume.name}`")

        initial_background = st.session_state.get("form_user_background", "")
        if parsed_resume_text and not initial_background:
            initial_background = parsed_resume_text

        user_background = st.text_area(
            "Your Top Achievements & Resume Highlights",
            value=initial_background,
            placeholder="Key skills, notable metrics (e.g. reduced latency by 35%, grew sales by $2M), technologies, past companies...",
            height=120
        )
        
        st.divider()
        
        # Section 2: Target Opportunity
        st.markdown('<div class="section-tag">🎯 Section 2: Target Opportunity</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            target_company = st.text_input(
                "Target Company",
                value=st.session_state.get("form_target_company", ""),
                placeholder="e.g. OpenAI, Stripe, Google, Airbnb"
            )
        with col4:
            target_role = st.text_input(
                "Target Role / Job Title",
                value=st.session_state.get("form_target_role", ""),
                placeholder="e.g. Senior Backend Engineer (Job #8921)"
            )
            
        target_jd = st.text_area(
            "Job Description Context / Key Requirements",
            value=st.session_state.get("form_target_jd", ""),
            placeholder="Paste core requirements, preferred technologies, or mission statement from the posting.",
            height=100
        )
        
        st.divider()
        
        # Section 3: Referral Recipient & Strategy
        st.markdown('<div class="section-tag">🤝 Section 3: Referral Contact & Strategy</div>', unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            contact_name = st.text_input(
                "Contact's Full Name",
                value=st.session_state.get("form_contact_name", ""),
                placeholder="e.g. Marcus Vance"
            )
        with col6:
            contact_headline = st.text_input(
                "Contact's Role / Headline",
                value=st.session_state.get("form_contact_headline", ""),
                placeholder="e.g. Engineering Manager, Core Infrastructure"
            )
            
        contact_linkedin = st.text_area(
            "Contact's LinkedIn About / Recent Posts / Background (Optional)",
            value=st.session_state.get("form_contact_linkedin", ""),
            placeholder="e.g. Previously at Apple, writes about distributed consensus, active mentor.",
            height=80
        )
        
        col7, col8, col9 = st.columns(3)
        with col7:
            relationship = st.selectbox(
                "Relationship Context",
                [
                    "🎓 College / University Alumni",
                    "🤝 Ex-Colleague or Mutual Connection",
                    "❄️ Cold Stranger / Industry Peer",
                    "💼 Recruiter or Talent Partner",
                    "👑 Hiring Manager / Department Head"
                ],
                index=0
            )
        with col8:
            tone = st.selectbox(
                "Communication Tone",
                [
                    "🎯 Confident & Direct",
                    "🌱 Enthusiastic & Humble",
                    "☕ Warm & Casual",
                    "👔 Executive & Peer-Level"
                ],
                index=0
            )
        with col9:
            call_to_action = st.selectbox(
                "Primary Call to Action",
                [
                    "☕ 10-minute quick chat or advice on team",
                    "🔗 Direct referral link submission",
                    "📄 Quick resume review / feedback on alignment"
                ],
                index=0
            )
            
        common_ground = st.text_input(
            "Common Ground / Shared Touchpoints (Optional)",
            value=st.session_state.get("form_common_ground", ""),
            placeholder="e.g. Both went to UC Berkeley, both worked in AdTech, shared connection with Jane Doe."
        )
        
        # Submit Button
        generate_clicked = st.form_submit_button("🚀 Generate Full Multi-Channel Referral Campaign", use_container_width=True)

    if generate_clicked:
        if not client:
            st.error("Please enter a valid Gemini API Key in the left sidebar to proceed!")
        elif not user_name or not target_company or not target_role or not contact_name:
            st.warning("Please ensure Your Name, Target Company, Target Role, and Contact Name are filled.")
        else:
            payload = {
                "user_name": user_name,
                "user_role": user_role,
                "user_url": user_url,
                "user_background": user_background,
                "target_company": target_company,
                "target_role": target_role,
                "target_jd": target_jd,
                "contact_name": contact_name,
                "contact_headline": contact_headline,
                "contact_linkedin": contact_linkedin,
                "relationship": relationship,
                "tone": tone,
                "call_to_action": call_to_action,
                "common_ground": common_ground
            }
            
            with st.spinner("Crafting your omni-channel referral campaign and evaluating etiquette..."):
                campaign = generate_referral_campaign(client, payload, model_name=selected_model)
                st.session_state.campaign_result = campaign
                st.session_state.campaign_payload = payload
                st.success("🎉 Campaign Generated Successfully! Switch to Tab 2 to view all drafts.")

# =========================================================================
# TAB 2: MULTI-CHANNEL CAMPAIGN OUTPUTS
# =========================================================================
with tab_campaign:
    res = st.session_state.campaign_result
    
    if not res:
        st.info("No referral campaign generated yet. Fill in the details in **Tab 1** and click **Generate**!")
    else:
        st.subheader("Your Personalized Multi-Channel Outreach Suite")
        st.caption("Each channel is customized for the platform's constraints and recipient psychology.")
        
        channel_tab1, channel_tab2, channel_tab3, channel_tab4, channel_tab5 = st.tabs([
            "🔗 1. LinkedIn Connection Note",
            "💬 2. InMail / Direct Message",
            "📧 3. Cold / Warm Email",
            "⏱️ 4. 5-Day Follow-Up",
            "🎙️ 5. Audio / Voice Script"
        ])
        
        # 1. LinkedIn Connection Note (<300 chars)
        with channel_tab1:
            conn_text = res.get("linkedin_connection", "")
            char_count = len(conn_text)
            
            # Character gauge indicator
            if char_count <= 280:
                badge_html = f'<div class="char-badge-safe">✓ {char_count} / 300 characters (Fits Free LinkedIn Limit)</div>'
            elif char_count <= 300:
                badge_html = f'<div class="char-badge-warning">⚠ {char_count} / 300 characters (Close to Limit)</div>'
            else:
                badge_html = f'<div class="char-badge-danger">✕ {char_count} / 300 characters (Exceeds 300 char limit!)</div>'
                
            st.markdown(badge_html, unsafe_allow_html=True)
            st.write("")
            
            edited_conn = st.text_area(
                "Ready-to-Send Connection Invite Note",
                value=conn_text,
                height=120,
                key="box_linkedin_conn"
            )
            
            col_b1, col_b2, col_b3 = st.columns([1, 1, 2])
            with col_b1:
                if st.button("⚡ Shorten by 15%", key="btn_shorten_conn"):
                    if client:
                        with st.spinner("Rewriting..."):
                            shrunk = rewrite_message(client, edited_conn, "Shorten this connection note by 15% while keeping the core hook. Strictly under 270 characters.")
                            res["linkedin_connection"] = shrunk
                            st.rerun()
            with col_b2:
                if st.button("🔥 Make Punchier", key="btn_punchy_conn"):
                    if client:
                        with st.spinner("Polishing..."):
                            punchy = rewrite_message(client, edited_conn, "Make this note punchier, higher energy, and ultra-compelling. Strictly under 280 characters.")
                            res["linkedin_connection"] = punchy
                            st.rerun()
                            
        # 2. LinkedIn InMail / DM
        with channel_tab2:
            inmail_text = res.get("linkedin_inmail", "")
            st.caption(f"Estimated Word Count: ~{len(inmail_text.split())} words (Ideal range: 100-140 words)")
            
            edited_inmail = st.text_area(
                "Full LinkedIn Message / InMail",
                value=inmail_text,
                height=220,
                key="box_linkedin_inmail"
            )
            
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                if st.button("☕ Make Warmer & More Casual", key="btn_warm_inmail"):
                    if client:
                        with st.spinner("Rewriting..."):
                            warmer = rewrite_message(client, edited_inmail, "Make this InMail warmer, more human and conversational, like chatting with a respected friend.")
                            res["linkedin_inmail"] = warmer
                            st.rerun()
            with col_in2:
                if st.button("👔 Make Executive / Peer-Level", key="btn_exec_inmail"):
                    if client:
                        with st.spinner("Rewriting..."):
                            exec_msg = rewrite_message(client, edited_inmail, "Rewrite this message in an executive peer-to-peer tone focusing on business results and high signal.")
                            res["linkedin_inmail"] = exec_msg
                            st.rerun()
                            
        # 3. Cold / Warm Email
        with channel_tab3:
            cold_email = res.get("cold_email", {})
            subject_lines = cold_email.get("subject_lines", ["Referral Inquiry"])
            email_body = cold_email.get("body", "")
            
            st.markdown("##### High-Converting Subject Line Options:")
            for idx, subj in enumerate(subject_lines):
                st.code(f"Subject Option {idx+1}: {subj}", language="text")
                
            edited_email = st.text_area(
                "Email Body",
                value=email_body,
                height=240,
                key="box_cold_email"
            )
            
        # 4. 5-Day Follow-Up
        with channel_tab4:
            st.info("💡 **Pro-Tip**: 60% of referrals happen on the follow-up note because inboxes are busy. Send this 5–7 days after your initial outreach.")
            followup_text = res.get("follow_up", "")
            
            st.text_area(
                "5-Day Polite Follow-Up Note",
                value=followup_text,
                height=140,
                key="box_followup"
            )
            
        # 5. Audio / Voice Script
        with channel_tab5:
            st.success("🎙️ **Voice Note Strategy**: Sending a 30-second audio note on the LinkedIn mobile app achieves a **3x higher response rate** because it builds instant personal trust.")
            audio_script = res.get("elevator_pitch", "")
            st.text_area(
                "30-Second Audio Note Script",
                value=audio_script,
                height=140,
                key="box_audio_script"
            )
            
        st.divider()
        
        # Download Campaign Bundle
        full_bundle = f"""# ReferralCraft Outreach Campaign for {st.session_state.get('campaign_payload', {}).get('target_company', 'Target Company')}

## 1. LinkedIn Connection Note (<300 chars)
{res.get('linkedin_connection')}

## 2. LinkedIn InMail / DM
{res.get('linkedin_inmail')}

## 3. Email Subject Lines
{chr(10).join(['- ' + s for s in res.get('cold_email', {}).get('subject_lines', [])])}

### Email Body
{res.get('cold_email', {}).get('body')}

## 4. 5-Day Follow-Up
{res.get('follow_up')}

## 5. Audio DM Script
{res.get('elevator_pitch')}
"""
        st.download_button(
            label="💾 Download Full Campaign Bundle (.md)",
            data=full_bundle,
            file_name=f"referral_outreach_{st.session_state.get('campaign_payload', {}).get('target_company', 'company')}.md",
            mime="text/markdown",
            use_container_width=True
        )

# =========================================================================
# TAB 3: ETiquette & CRINGE AUDIT
# =========================================================================
with tab_audit:
    res = st.session_state.campaign_result
    
    if not res:
        st.info("Generate a referral suite in **Tab 1** to view the AI Etiquette and Conversion Audit.")
    else:
        scorecard = res.get("etiquette_scorecard", {})
        
        st.subheader("🛡️ AI Etiquette & Conversion Audit")
        st.caption("Automated evaluation of tone, psychological framing, and likelihood of reply.")
        
        audit_col1, audit_col2, audit_col3, audit_col4 = st.columns(4)
        
        desp = scorecard.get("desperation_score", 2)
        pers = scorecard.get("personalization_score", 9)
        clarity = scorecard.get("clarity_score", 9)
        verdict = scorecard.get("verdict", "Strong Candidate Outreach")
        
        with audit_col1:
            st.metric("Desperation Index (Lower is Better)", f"{desp} / 10", help="1-3 = Confident Peer; 8-10 = Begging/Urgent")
        with audit_col2:
            st.metric("Personalization Score", f"{pers} / 10")
        with audit_col3:
            st.metric("Clarity & Brevity", f"{clarity} / 10")
        with audit_col4:
            st.metric("Overall Verdict", verdict)
            
        st.write("")
        
        st.markdown(
            f"""
            <div class="scorecard-box">
                <h4 style="color: #818cf8; margin-bottom: 0.5rem;">Coach Assessment</h4>
                <p style="color: #cbd5e1; font-size: 1.05rem;">{scorecard.get('coach_critique', 'This message demonstrates solid mutual alignment.')}</p>
                <div class="tip-bullet" style="margin-top: 1rem;">
                    <strong>Recommended Tactical Action:</strong> {scorecard.get('recommended_action', 'Review the contact’s recent LinkedIn activity before hitting send.')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### Why High-Scoring Outreach Works:")
        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown(
                """
                - **Peer-to-Peer Framing**: Framing yourself as a capable peer makes the referrer feel confident that recommending you won't harm their professional reputation.
                - **Low Friction**: Suggesting a 10-minute chat or asking for advice is far easier to say yes to than demanding an instant referral link.
                """
            )
        with c_b:
            st.markdown(
                """
                - **Alumni / Mutual Affinity**: Highlighting shared roots activates in-group psychological reciprocity.
                - **Respect for Character Limits**: Fitting cleanly into connection note limitations ensures non-premium recipients can read the full message immediately.
                """
            )

# =========================================================================
# TAB 4: MINI PIPELINE TRACKER
# =========================================================================
with tab_tracker:
    st.subheader("📊 Referral Outreach Pipeline Tracker")
    st.caption("Keep track of referrers, follow-up dates, and conversion statuses in one place.")
    
    # Quick Add Form
    with st.expander("➕ Log an Outreach Entry into Tracker", expanded=False):
        with st.form("pipeline_add_form"):
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                log_name = st.text_input("Contact Name")
                log_company = st.text_input("Company")
            with t_col2:
                log_role = st.text_input("Role Applied For")
                log_status = st.selectbox("Current Status", [
                    "Drafted",
                    "Connection Request Sent",
                    "InMail Sent",
                    "Email Sent",
                    "Replied - Chat Scheduled",
                    "🎉 Referral Submitted",
                    "Closed / No Reply"
                ])
                
            log_notes = st.text_input("Follow-Up Date / Notes", placeholder="e.g. Follow up on Tuesday if no reply")
            
            submit_log = st.form_submit_button("Add to Pipeline Tracker")
            if submit_log:
                if log_name and log_company:
                    st.session_state.pipeline_records.append({
                        "Date Logged": datetime.now().strftime("%Y-%m-%d"),
                        "Contact Name": log_name,
                        "Company": log_company,
                        "Role": log_role,
                        "Status": log_status,
                        "Notes": log_notes
                    })
                    st.success(f"Added {log_name} at {log_company} to pipeline!")
                    st.rerun()
                else:
                    st.warning("Please provide at least a Contact Name and Company.")
                    
    # Display Pipeline
    if not st.session_state.pipeline_records:
        # Show sample table
        sample_df = pd.DataFrame([
            {"Date Logged": "2026-10-01", "Contact Name": "David Chen", "Company": "Stripe", "Role": "Software Engineer", "Status": "🎉 Referral Submitted", "Notes": "Alumni from UW; referred on Oct 3"},
            {"Date Logged": "2026-10-03", "Contact Name": "Sarah Jenkins", "Company": "Figma", "Role": "Product Manager", "Status": "Connection Request Sent", "Notes": "Follow up next Monday"}
        ])
        st.markdown("##### Current Outreach Activity (Sample Preview):")
        st.dataframe(sample_df, use_container_width=True)
    else:
        df = pd.DataFrame(st.session_state.pipeline_records)
        st.dataframe(df, use_container_width=True)
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Export Pipeline to CSV",
            data=csv_data,
            file_name="referral_pipeline_tracker.csv",
            mime="text/csv"
        )
