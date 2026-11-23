import os
import json
import re
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

DEFAULT_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

def get_gemini_client(api_key: Optional[str] = None) -> Optional[genai.Client]:
    """Initializes and returns a Gemini client using the given key or environment variable."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    try:
        return genai.Client(api_key=key.strip())
    except Exception:
        return None

def clean_json_text(text: str) -> str:
    """Strips markdown code fences and returns cleaned JSON string."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def build_system_instruction() -> str:
    return """
You are an elite Executive Career Coach, Silicon Valley Talent Advisor, and Master of High-Converting Professional Outreach.
Your mission is to craft exceptional, multi-channel employee referral outreach campaigns that maximize response rates and rapport.

CORE OUTREACH PHILOSOPHY:
1. Never beg or sound desperate. Referrals are mutual wins: companies pay referral bonuses and referrers want to bring in high-caliber peers.
2. Value First: Open with genuine common ground, mutual respect, or deep company knowledge.
3. Frictionless Ask: Never demand an immediate referral submission in the first sentence. Ask for advice, a quick perspective, or whether they would be open to reviewing credentials.
4. Channel Precision:
   - LinkedIn Connection Note: MUST BE STRICTLY UNDER 290 CHARACTERS. Free LinkedIn limits connection notes to 300 characters. If it exceeds 300 characters, the sender physically cannot send it!
   - LinkedIn InMail / DM: 100-140 words. Concise, punchy, conversational.
   - Cold / Warm Email: 3 clickable, high-converting subject lines + readable, well-spaced body.
   - Follow-Up Note: 50-70 words. Polite nudge for 5-7 days later.

RESPONSE FORMAT:
You MUST return ONLY valid JSON matching this schema:
{
  "linkedin_connection": "Message text strictly under 290 characters",
  "linkedin_inmail": "Full LinkedIn InMail/DM text",
  "cold_email": {
    "subject_lines": ["Subject 1", "Subject 2", "Subject 3"],
    "body": "Email body content"
  },
  "follow_up": "Gentle follow-up message text",
  "elevator_pitch": "30-second conversational voice note or audio DM script",
  "etiquette_scorecard": {
    "desperation_score": 1 to 10 (1 = peer-to-peer confident, 10 = sounding like begging),
    "personalization_score": 1 to 10 (10 = deeply tailored),
    "clarity_score": 1 to 10,
    "verdict": "e.g. Exceptional / Ready to Send",
    "coach_critique": "2 sentences explaining why this message works and psychology behind it",
    "recommended_action": "1 tactical tip before sending"
  }
}
"""

def generate_referral_campaign(
    client: genai.Client,
    payload: Dict[str, Any],
    model_name: str = "gemini-2.5-flash"
) -> Dict[str, Any]:
    """Generates the comprehensive referral outreach suite."""
    system_instruction = build_system_instruction()
    
    user_prompt = f"""
Please generate an omni-channel referral campaign with the following context:

SENDER PROFILE:
- Name: {payload.get('user_name', 'The Candidate')}
- Current Role / Title: {payload.get('user_role', 'Professional')}
- LinkedIn: {payload.get('user_url', 'None')}
- Resume Highlights / Background:
{payload.get('user_background', 'Not provided')}

TARGET OPPORTUNITY:
- Target Company: {payload.get('target_company', 'Target Company')}
- Target Role: {payload.get('target_role', 'Target Role')}
- Job Description / Keywords:
{payload.get('target_jd', 'Not provided')}

RECIPIENT (REFERRER):
- Contact Name: {payload.get('contact_name', 'Hiring Colleague')}
- Contact Role / Headline: {payload.get('contact_headline', 'Not specified')}
- Contact LinkedIn / Background: {payload.get('contact_linkedin', 'Not specified')}

RELATIONSHIP & STRATEGY:
- Relationship Context: {payload.get('relationship', 'Cold / Professional Peer')}
- Tone: {payload.get('tone', 'Confident & Direct')}
- Primary Call-to-Action: {payload.get('call_to_action', 'Brief 10-min chat or advice on team')}
- Common Ground / Mutual Touchpoints: {payload.get('common_ground', 'Shared interest in company mission')}

CRITICAL CONSTRAINT: Ensure `linkedin_connection` is under 290 characters count!
Output pure JSON only.
"""

    models_to_try = [model_name]
    for m in DEFAULT_MODELS:
        if m != model_name and m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    for model in models_to_try:
        try:
            response = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.6,
                    response_mime_type="application/json"
                )
            )
            raw_text = clean_json_text(response.text or "")
            parsed = json.loads(raw_text)
            
            # Double check character limit on connection note
            conn_note = parsed.get("linkedin_connection", "")
            if len(conn_note) > 300:
                parsed["linkedin_connection"] = conn_note[:295].rsplit(" ", 1)[0] + "."
                
            return parsed
        except Exception as e:
            last_error = e
            continue

    # Fallback response structure if parsing fails completely
    return {
        "error": f"Failed to generate campaign: {str(last_error)}",
        "linkedin_connection": f"Hi {payload.get('contact_name')}, saw your work at {payload.get('target_company')}. I'm applying for the {payload.get('target_role')} role and would love to connect!",
        "linkedin_inmail": f"Hi {payload.get('contact_name')},\n\nI hope you're having a great week. I noticed the {payload.get('target_role')} position at {payload.get('target_company')} and given your experience there, I would appreciate any quick perspective on the team.",
        "cold_email": {
            "subject_lines": [f"Quick question re: {payload.get('target_role')} at {payload.get('target_company')}"],
            "body": f"Hi {payload.get('contact_name')},\n\nHope this finds you well..."
        },
        "follow_up": f"Hi {payload.get('contact_name')}, just bubbling this up in case it got buried. Hope you're having a productive week!",
        "elevator_pitch": "Hi there, I noticed your team is building great products...",
        "etiquette_scorecard": {
            "desperation_score": 3,
            "personalization_score": 5,
            "clarity_score": 7,
            "verdict": "Basic Fallback",
            "coach_critique": "Generation encountered an issue with the AI engine.",
            "recommended_action": "Verify your API Key in the sidebar."
        }
    }

def rewrite_message(
    client: genai.Client,
    original_text: str,
    instruction: str,
    model_name: str = "gemini-2.5-flash"
) -> str:
    """Adjusts or rewrites a message according to quick user feedback."""
    prompt = f"""
You are an expert career editor.
Please rewrite the following outreach message according to this instruction:
"{instruction}"

ORIGINAL MESSAGE:
{original_text}

Rules:
- If this is a LinkedIn Connection note, keep it strictly under 285 characters!
- Maintain professional polish and high conversion etiquette.
- Return ONLY the revised message text with no conversational preamble.
"""
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )
        return (response.text or "").strip()
    except Exception as e:
        return f"Error during rewrite: {str(e)}"
