import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

# Use Gemini 2.5 Flash for rapid multimodal extraction and reasoning
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def extract_document_info(image_path: str) -> str:
    """
    Uses Gemini Vision to read the PMFBY form.
    """
    try:
        from PIL import Image
        img = Image.open(image_path)
    except Exception as e:
        return f"Error loading image: {str(e)}"
        
    prompt = """
    You are KritiAI's Document Parsing Agent. Extract the following from the PMFBY Crop Loss Form image:
    1. Farmer Name
    2. Aadhaar No
    3. Crop Name
    4. Khasra / Survey No
    5. Cause of Loss
    6. Date of Occurrence
    7. Official Status (Look for verified/rejected stamps)
    8. Handwritten Remarks (if any)
    
    Output strictly as a clear text summary.
    """
    
    try:
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Error during VLM extraction: {str(e)}"

def run_short_audit_firehose(date_str: str, location: str) -> str:
    """
    Simulates fetching live firehose data from X (Twitter) and online local news 
    for the specified date and location to detect disaster chatter.
    """
    if "Kamrup" in location or "26.25" in location:
        return (
            f"X (Twitter) Trending: #AssamFloods, #KamrupWaterlogging (14,200 mentions)\n"
            f"Local News API: 'Severe inundation reported across Kamrup district following unexpected monsoon surge.'\n"
            f"Conclusion: High social/news correlation for flooding."
        )
    else:
        return (
            f"X (Twitter) Trending: Normal regional chatter.\n"
            f"Local News API: No significant disaster events reported.\n"
            f"Conclusion: No social/news correlation for disaster."
        )

def audit_claim(document_text: str, vector_context: str, firehose_context: str = "") -> dict:
    """
    Acts as the Cross-Modal Alignment Brain (Harvey AI inspired reasoning).
    """
    prompt = f"""
    You are KritiAI, a high-level auditing engine for regional governance.
    Analyze the crop loss claim against the satellite vector context.

    --- DOCUMENT CLAIM (PMFBY EXTRACT) ---
    {document_text}

    --- SPATIAL VECTOR CONTEXT (QDRANT/EARTH ENGINE) ---
    {vector_context}
    
    --- LIVE SOCIAL/NEWS FIREHOSE (SHORT AUDIT) ---
    {firehose_context}
    
    --- TASK ---
    Determine if the document claim is scientifically verifiable using the spatial context and firehose corroboration.
    
    Output STRICTLY in JSON format:
    {{
        "audit_decision": "VERIFIABLE" | "DISCREPANCY FOUND" | "FLAGGED",
        "confidence_score": <float 0.0 to 1.0>,
        "reasoning": "Step-by-step reasoning explaining the alignment or discrepancy."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        return {
            "audit_decision": "ERROR",
            "confidence_score": 0.0,
            "reasoning": f"Reasoning failure: {str(e)}"
        }
