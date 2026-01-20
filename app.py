import streamlit as st
import io
import base64
import requests
import urllib.parse
from PIL import Image
import numpy as np
from dataclasses import dataclass
from typing import List, Dict
import time
import json
import os

# Try to import Groq for Gen AI
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

# Get Groq API key from Streamlit secrets (NEVER hardcode in code!)
GROQ_API_KEY = None
if HAS_GROQ:
    try:
        GROQ_API_KEY = st.secrets["groq"]["api_key"]
    except:
        pass  # No key configured - will use templates

# Page configuration
st.set_page_config(
    page_title="QuickList - Professional Product Listings",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Simplified and Fixed
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');
    
    /* Force light theme at root level */
    :root {
        --background-color: #ffffff;
        --text-color: #000000;
    }
    
    /* Main app background - WHITE */
    .stApp {
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Force all Streamlit elements to white background */
    .stApp > div {
        background: #ffffff !important;
    }
    
    .main {
        background: #ffffff !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main header styling */
    .main-header {
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        z-index: 0;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    /* All page text should be black except header */
    body, p, div, span, label, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Force white backgrounds on all interactive elements */
    section, div[class*="st"], div[data-testid] {
        background-color: transparent;
    }
    
    /* Main container white background */
    .main .block-container {
        background: #ffffff !important;
    }
    
    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f8f8f8;
        border-right: 1px solid #e5e5e5;
    }
    
    /* Upload section */
    .upload-section {
        background: #ffffff !important;
        border: 2px solid #e5e5e5;
        border-radius: 16px;
        padding: 3rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .upload-section h2,
    .upload-section p {
        color: #000000 !important;
    }
    
    /* File uploader - FIXED FOR CONTRAST */
    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 3px dashed #0066cc !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* File uploader inner sections - WHITE background */
    [data-testid="stFileUploader"] section {
        background: #ffffff !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        background: #ffffff !important;
    }
    
    /* All divs inside file uploader - WHITE background, BLACK text */
    [data-testid="stFileUploader"] div {
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    /* All text in file uploader - BLACK */
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] label {
        color: #000000 !important;
        background: transparent !important;
    }
    
    /* Drag and drop zone - WHITE background */
    [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
        background: #ffffff !important;
        border: 2px dashed #cccccc !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInput"] {
        background: #ffffff !important;
    }
    
    /* Browse button */
    [data-testid="stFileUploader"] button {
        background: #ffffff !important;
        color: #0066cc !important;
        border: 2px solid #0066cc !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: #0066cc !important;
        color: #ffffff !important;
    }
    
    /* File uploader markdown text */
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {
        color: #000000 !important;
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] * {
        color: #000000 !important;
        background: transparent !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #000000 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.25rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        width: 100%;
        height: 65px !important;
    }
    
    .stButton > button:hover {
        background: #0066cc !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0,102,204,0.3) !important;
    }
    
    /* Force button text to always be white */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #ffffff !important;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 12px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton > button:hover {
        background: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Metric boxes */
    .metric-box {
        background: #ffffff;
        border: 2px solid #e5e5e5;
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        min-height: 140px;
        overflow: hidden;
    }
    
    .metric-box:hover {
        border-color: #0066cc;
        box-shadow: 0 8px 24px rgba(0,102,204,0.1);
        transform: translateY(-4px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #4a5568 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
        font-weight: 700;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif;
        line-height: 1.4;
        padding: 0 0.25rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
    
    /* Description cards */
    .description-card {
        background: #f8f8f8;
        border: 2px solid #e5e5e5;
        border-radius: 16px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .description-card:hover {
        border-color: #000000;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }
    
    .description-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #000000 !important;
        margin-bottom: 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .style-badge {
        background: #000000;
        color: #ffffff !important;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* SEO section */
    .seo-box {
        background: #ffffff;
        border: 2px solid #e5e5e5;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .seo-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #000000 !important;
        margin-bottom: 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .keyword-tag {
        display: inline-block;
        background: #f8f8f8;
        color: #000000 !important;
        border: 1px solid #e5e5e5;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.4rem 0.4rem 0.4rem 0;
    }
    
    /* Image gallery */
    .image-gallery {
        background: #ffffff;
        border: 2px solid #e5e5e5;
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
    }
    
    .gallery-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #000000 !important;
        margin-bottom: 2rem;
        font-family: 'Space Grotesk', sans-serif;
        text-align: center;
    }
    
    /* Uploaded image styling */
    [data-testid="stImage"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    [data-testid="stImage"] img {
        border-radius: 12px;
    }
    
    [data-testid="stImage"] > div {
        text-align: center;
    }
    
    /* Image captions */
    [data-testid="stImage"] + div,
    [data-testid="stImage"] figcaption,
    [data-testid="stImage"] p {
        color: #000000 !important;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #000000 0%, #0066cc 100%);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.6rem 1.5rem;
        border-radius: 24px;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-processing {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: #ffffff !important;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .status-complete {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: #ffffff !important;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
        border-left: 4px solid #0066cc;
        border-radius: 8px;
        padding: 2rem 2.5rem;
        margin: 3rem 0 2rem 0;
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0066cc !important;
        font-family: 'Space Grotesk', sans-serif;
        margin: 0;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: #4a5568 !important;
        margin-top: 0.5rem;
    }
    
    /* Info boxes */
    .info-box {
        background: #f8f8f8;
        border-left: 4px solid #0066cc;
        border-radius: 8px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
    }
    
    .info-box p {
        color: #000000 !important;
        line-height: 1.7;
        margin: 0;
    }
    
    /* Text inputs */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput input,
    .stTextArea textarea {
        background: #ffffff !important;
        border: 2px solid #e5e5e5 !important;
        color: #000000 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 3px rgba(0,102,204,0.1) !important;
    }
    
    /* Code/Pre elements - force white background and black text */
    pre, code {
        background: #f8f8f8 !important;
        color: #000000 !important;
        border: 1px solid #e5e5e5 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stCode, [data-testid="stCode"] {
        background: #f8f8f8 !important;
    }
    
    .stCode pre, [data-testid="stCode"] pre {
        background: #f8f8f8 !important;
        color: #000000 !important;
    }
    
    /* Selectbox */
    .stSelectbox div[data-baseweb="select"] {
        background: #ffffff !important;
        border: 2px solid #e5e5e5 !important;
    }
    
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #0066cc !important;
    }
    
    /* Selectbox dropdown menu */
    .stSelectbox div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Selectbox selected value */
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="input"] {
        color: #000000 !important;
        background: #ffffff !important;
    }
    
    /* Selectbox options in dropdown menu */
    [data-baseweb="menu"] {
        background: #ffffff !important;
        border: 1px solid #e5e5e5 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    [data-baseweb="menu"] ul {
        background: #ffffff !important;
    }
    
    [data-baseweb="menu"] li {
        background: #ffffff !important;
        color: #000000 !important;
        padding: 0.75rem 1rem !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: #f0f0f0 !important;
        color: #000000 !important;
    }
    
    /* Force all text in menu options to be black */
    [data-baseweb="menu"] li div,
    [data-baseweb="menu"] li span,
    [data-baseweb="menu"] li p {
        color: #000000 !important;
        background: transparent !important;
    }
    
    /* Listbox options */
    [role="listbox"] {
        background: #ffffff !important;
    }
    
    [role="option"] {
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    [role="option"]:hover {
        background: #f0f0f0 !important;
        color: #000000 !important;
    }
    
    /* Force all children of options to be black text */
    [role="option"] * {
        color: #000000 !important;
    }
    
    /* Force all selectbox text to be black */
    .stSelectbox div[data-baseweb="select"] div,
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] p {
        color: #000000 !important;
        background: transparent !important;
    }
    
    /* Dropdown arrow */
    .stSelectbox svg {
        fill: #000000 !important;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1.5rem;
            margin: -6rem -1rem 2rem -1rem;
        }
        
        .metric-box {
            padding: 1.5rem 1rem;
            min-height: 120px;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header - Force inline styles to override Streamlit
st.markdown("""
<div class="main-header" style="background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important; text-align: center; padding: 3rem; border-radius: 0 0 24px 24px; margin: -6rem -5rem 3rem -5rem;">
    <div class="header-content">
        <h1 style="color: #ffffff !important; font-size: 3.5rem !important; font-weight: 800 !important; margin: 0 !important; font-family: 'Space Grotesk', sans-serif !important;">QuickList</h1>
        <p style="color: #ffffff !important; font-size: 1.25rem !important; margin-top: 0.75rem !important; font-family: 'Inter', sans-serif !important;">Professional Product Listings in Minutes</p>
        <span style="background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%) !important; color: #ffffff !important; display: inline-block !important; padding: 0.6rem 1.5rem !important; border-radius: 24px !important; font-size: 0.85rem !important; font-weight: 700 !important; margin-top: 1.25rem !important; text-transform: uppercase !important;">AI-Powered</span>
    </div>
</div>
""", unsafe_allow_html=True)


# Data classes
@dataclass
class ProductAnalysis:
    category: str
    materials: List[str]
    colors: List[str]
    style: str
    confidence: float


@dataclass
class ProductDescription:
    title: str
    description: str
    bullet_points: List[str]
    meta_description: str
    style_type: str


class QuickListAI:
    """AI-powered product listing generator"""
    
    @staticmethod
    def analyze_product_with_clip(image: Image.Image) -> ProductAnalysis:
        """Step 1: Quick analysis using CLIP (for metadata)"""
        
        try:
            # Convert image to bytes for API
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            headers = {"Content-Type": "application/octet-stream"}
            API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
            
            # Detect CATEGORY
            broad_categories = [
                "clothing apparel", "electronics device", "furniture", 
                "beauty personal care product", "kitchen cookware",  "sports equipment",
                "toy", "jewelry accessory", "tool", "home decor"
            ]
            
            response1 = requests.post(
                API_URL,
                headers=headers,
                data=img_bytes,
                params={"candidate_labels": ",".join(broad_categories)},
                timeout=20
            )
            
            category = "General Product"
            if response1.status_code == 200:
                result = response1.json()
                if isinstance(result, list) and len(result) > 0:
                    broad_cat = result[0].get('label', 'product')
                    
                    category_map = {
                        "clothing apparel": "Apparel",
                        "electronics device": "Electronics",
                        "furniture": "Furniture",
                        "beauty personal care product": "Beauty & Personal Care",
                        "kitchen cookware": "Kitchen & Home",
                        "sports equipment": "Sports & Fitness",
                        "toy": "Toys & Games",
                        "jewelry accessory": "Accessories",
                        "tool": "Tools & Hardware",
                        "home decor": "Home Decor"
                    }
                    category = category_map.get(broad_cat, "General Product")
            
            # Detect COLOR
            color_labels = [
                "black", "white", "silver", "gray", "red", "blue", 
                "green", "yellow", "pink", "purple", "brown", "gold", 
                "rose gold", "metallic", "transparent", "multicolor", "beige"
            ]
            
            response2 = requests.post(
                API_URL,
                headers=headers,
                data=img_bytes,
                params={"candidate_labels": ",".join(color_labels)},
                timeout=20
            )
            
            detected_color = "neutral"
            if response2.status_code == 200:
                result = response2.json()
                if isinstance(result, list) and len(result) > 0:
                    detected_color = result[0].get('label', 'neutral')
            
            # Detect MATERIAL
            material_labels = [
                "metal", "plastic", "fabric", "leather", "wood", 
                "glass", "ceramic", "silicone", "stainless steel",
                "aluminum", "rubber", "synthetic"
            ]
            
            response3 = requests.post(
                API_URL,
                headers=headers,
                data=img_bytes,
                params={"candidate_labels": ",".join(material_labels)},
                timeout=20
            )
            
            detected_material = "Premium Material"
            material2 = "Quality Construction"
            if response3.status_code == 200:
                result = response3.json()
                if isinstance(result, list) and len(result) >= 2:
                    mat1 = result[0].get('label', 'material')
                    mat2 = result[1].get('label', 'construction')
                    detected_material = mat1.capitalize()
                    material2 = mat2.capitalize()
            
            # Detect STYLE
            style_labels = [
                "modern sleek", "classic traditional", "minimalist", 
                "vintage retro", "elegant luxury", "sporty",
                "professional", "casual", "industrial rugged"
            ]
            
            response4 = requests.post(
                API_URL,
                headers=headers,
                data=img_bytes,
                params={"candidate_labels": ",".join(style_labels)},
                timeout=20
            )
            
            detected_style = "Modern"
            if response4.status_code == 200:
                result = response4.json()
                if isinstance(result, list) and len(result) > 0:
                    style = result[0].get('label', 'modern').split()[0]
                    detected_style = style.capitalize()
            
            # Extract hex color
            img_array = np.array(image.resize((100, 100)))
            pixels = img_array.reshape(-1, 3)
            avg_colors = np.mean(pixels, axis=0).astype(int)
            hex_color = '#{:02x}{:02x}{:02x}'.format(*avg_colors)
            
            # Store for later use
            st.session_state.detected_color = detected_color
            
            return ProductAnalysis(
                category=category,
                materials=[detected_material, material2],
                colors=[detected_color, hex_color],
                style=detected_style,
                confidence=0.88
            )
            
        except Exception as e:
            return ProductAnalysis(
                category="General Product",
                materials=["Premium Material", "Quality Construction"],
                colors=['neutral', '#808080'],
                style='Modern',
                confidence=0.70
            )
    
    @staticmethod
    @staticmethod
    def generate_with_llava(product_name: str, analysis: ProductAnalysis, 
                           style: str, features: str, image: Image.Image) -> ProductDescription:
        """Generate with Groq Gen AI or industry templates"""
        
        # Try Groq if configured
        if GROQ_API_KEY and HAS_GROQ:
            try:
                client = Groq(api_key=GROQ_API_KEY)
                color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
                
                prompts = {
                    "Storytelling (Emotional)": f"""Product: {product_name}, Category: {analysis.category}, Color: {color}, Style: {analysis.style}
Write emotional description (150-200 words) with JSON: {{"title": "...", "description": "...", "bullet_points": [...], "meta_description": "..."}}""",
                    "Feature-Benefit (Practical)": f"""Product: {product_name}, Category: {analysis.category}, Color: {color}
Write practical description (150-200 words) with JSON format""",
                    "Minimalist (Clean)": f"""Product: {product_name}, Color: {color}
Write minimalist (80-100 words) JSON format"""
                }
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompts.get(style, prompts["Feature-Benefit (Practical)"])}],
                    temperature=0.7,
                    max_tokens=500,
                    response_format={"type": "json_object"}
                )
                
                parsed = json.loads(completion.choices[0].message.content)
                return ProductDescription(
                    title=parsed.get('title', product_name),
                    description=parsed.get('description', ''),
                    bullet_points=parsed.get('bullet_points', [])[:5],
                    meta_description=parsed.get('meta_description', '')[:160],
                    style_type=style
                )
            except:
                pass
        
        # Use industry templates
        return QuickListAI._industry_templates(product_name, analysis, style, features)
    @staticmethod
    def _industry_templates(product_name: str, analysis: ProductAnalysis, 
                          style: str, features: str) -> ProductDescription:
        """Industry-specific templates - way better than generic"""
        
        cat_lower = analysis.category.lower()
        prod_lower = product_name.lower()
        
        # Detect industry
        is_clothing = any(word in cat_lower or word in prod_lower for word in ['apparel', 'clothing', 'dress', 'shirt', 'pants', 'jacket', 'sweater', 'coat', 'skirt', 'jeans', 'top', 'blouse'])
        is_electronics = any(word in cat_lower or word in prod_lower for word in ['electronics', 'headphone', 'speaker', 'laptop', 'phone', 'tablet', 'camera', 'device', 'earbuds'])
        is_furniture = any(word in cat_lower or word in prod_lower for word in ['furniture', 'chair', 'table', 'desk', 'sofa', 'bed', 'cabinet', 'shelf', 'couch'])
        
        # Get color
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        color_text = f"{color} " if color else ""
        color_cap = f" in {color}" if color else ""
        
        # CLOTHING - talk about fit, fabric, style, occasions
        if is_clothing:
            if style == "Storytelling (Emotional)":
                title = f"{analysis.style}{color_cap} {product_name} - Effortless Style"
                description = f"""Step into effortless style with this {color_text}{product_name.lower()}.

The soft, breathable fabric drapes beautifully, creating a flattering silhouette that moves with you. Whether heading to the office, meeting friends for brunch, or enjoying an evening out, this {product_name.lower()} adapts to your lifestyle with ease.

{features if features else f'The {analysis.style.lower()} design pairs perfectly with your favorite accessories, giving you endless styling possibilities.'}

More than just another piece in your wardrobe - it's the confidence you feel when you know you look your best."""
                
                bullet_points = [
                    "Soft, breathable fabric for all-day comfort and lasting wear",
                    f"Flattering {analysis.style.lower()} cut that complements any body type",
                    "Versatile styling works for both casual and dressy occasions",
                    "Easy care - maintains shape and color wash after wash",
                    "Pairs effortlessly with wardrobe staples you already own"
                ]
                
            elif style == "Feature-Benefit (Practical)":
                title = f"{color_cap.strip() if color_cap else analysis.style} {product_name} - Comfortable & Versatile"
                description = f"""Experience the perfect balance of style and comfort with this {color_text}{product_name.lower()}.

PREMIUM FABRIC: Soft against your skin while maintaining its shape throughout the day. The breathable construction keeps you comfortable from morning to night.

FLATTERING FIT: The {analysis.style.lower()} cut is designed to flatter - not too tight, not too loose. It skims your silhouette in all the right places while allowing freedom of movement.

{features if features else 'VERSATILE STYLING: Dress it up with heels and jewelry or keep it casual with sneakers and a denim jacket. One piece, countless outfit possibilities.'}

EASY CARE: Machine washable and wrinkle-resistant. Looks fresh wear after wear with minimal effort."""
                
                bullet_points = [
                    "Soft, breathable fabric provides all-day comfort",
                    "Flattering fit designed for real bodies",
                    "Versatile enough for work, weekends, and everything between",
                    "Easy care - machine washable, stays looking new",
                    "Quality construction ensures long-lasting wear"
                ]
                
            else:  # Minimalist
                title = f"{color_cap.strip() if color_cap else ''} {product_name}".strip()
                description = f"""Timeless {analysis.style.lower()} design.{color_cap.capitalize() + '.' if color_cap else ''}

Soft fabric. Flattering fit. All-day comfort.

Pairs with everything in your closet.

{features if features else 'Machine washable. Built to last.'}

Effortless style, simplified."""
                
                bullet_points = [
                    "Soft, comfortable fabric",
                    "Flattering fit",
                    "Versatile styling",
                    "Easy care",
                    "Timeless design"
                ]
        
        # ELECTRONICS - talk about performance, features, reliability
        elif is_electronics:
            if style == "Storytelling (Emotional)":
                title = f"{color_cap.strip() if color_cap else analysis.style} {product_name} - Premium Performance"
                description = f"""Transform your technology experience with this {color_text}{product_name.lower()}.

From the moment you first use it, you'll notice the difference. Crisp, responsive performance. Intuitive controls that feel natural in your hands. The {color_text}finish isn't just sleek - it's built to withstand daily use while looking showroom-new.

{features if features else 'Whether you\'re working, creating, or simply enjoying your favorite content, this device delivers the reliability you need and the quality you deserve.'}

Technology that gets out of your way and lets you focus on what matters."""
                
                bullet_points = [
                    "Durable construction ensures long-lasting reliability",
                    "High-performance components deliver fast, responsive operation",
                    "Intuitive interface - easy to use right out of the box",
                    "Sleek design that looks professional anywhere",
                    "Built to handle daily demands without slowing down"
                ]
                
            elif style == "Feature-Benefit (Practical)":
                title = f"{product_name}{color_cap} - High Performance | Reliable"
                description = f"""Get professional-grade performance with this {color_text}{product_name.lower()}.

POWERFUL PERFORMANCE: Engineered with high-quality components that deliver fast, responsive operation. No lag, no waiting - just smooth, reliable performance when you need it.

DURABLE BUILD: Built to stand up to daily use. The {color_text}finish resists scratches and fingerprints, maintaining that new look longer.

{features if features else 'EASY TO USE: Intuitive controls and clear interface mean you\'ll be productive from day one. No steep learning curve.'}

VERSATILE: Works seamlessly with your existing setup. Plug in and start using immediately."""
                
                bullet_points = [
                    "High-performance components for fast, reliable operation",
                    "Durable construction built for daily use",
                    "Intuitive controls - easy to learn and use",
                    "Broad compatibility with existing devices",
                    "Quality engineering backed by rigorous testing"
                ]
                
            else:  # Minimalist
                title = f"{color_cap.strip() if color_cap else ''} {product_name}".strip()
                description = f"""Performance. Reliability.{color_cap.capitalize() + '.' if color_cap else ''}

Fast response. Intuitive controls.

{features if features else 'Built for daily use.'}

Works when you need it. No complications."""
                
                bullet_points = [
                    "High-performance operation",
                    "Durable construction",
                    "Easy to use",
                    "Reliable daily performance",
                    "Professional quality"
                ]
        
        # FURNITURE - talk about comfort, space, durability
        elif is_furniture:
            if style == "Storytelling (Emotional)":
                title = f"{analysis.style}{color_cap} {product_name} - Transform Your Space"
                description = f"""Reimagine your space with this beautifully crafted {color_text}{product_name.lower()}.

The {color_text}finish adds warmth and character to any room, while the {analysis.style.lower()} design brings everything together with effortless sophistication.

Sink into comfort that lasts - this isn't furniture that looks good but feels mediocre. It's built with solid construction that provides the support and durability you need, day after day.

{features if features else 'Whether you\'re relaxing after a long day, hosting friends, or simply enjoying your morning coffee, this piece becomes the backdrop to your best moments at home.'}"""
                
                bullet_points = [
                    "Solid construction ensures stability and long-lasting comfort",
                    f"{analysis.style} design elevates any room aesthetic",
                    "Ergonomic construction provides excellent support",
                    "Versatile style complements both traditional and contemporary decor",
                    "Built to become a cherished part of your home for years"
                ]
                
            elif style == "Feature-Benefit (Practical)":
                title = f"{color_cap.strip() if color_cap else analysis.style} {product_name} - Durable & Comfortable"
                description = f"""Upgrade your space with this well-crafted {color_text}{product_name.lower()}.

SOLID CONSTRUCTION: Built with quality materials that provide reliable support and exceptional durability. This isn't furniture you'll replace in a year - it's built to last.

ERGONOMIC DESIGN: The {analysis.style.lower()} design isn't just visually appealing - it's engineered for comfort. Proper support where you need it, without sacrificing style.

{features if features else 'VERSATILE STYLING: The clean lines work with any decor style, from traditional to contemporary.'}

QUALITY CRAFTSMANSHIP: Precision assembly and quality materials ensure this piece stays sturdy and attractive through years of daily use."""
                
                bullet_points = [
                    "Solid construction provides excellent durability",
                    "Ergonomic design maximizes comfort during extended use",
                    f"{analysis.style} aesthetic enhances any room",
                    "Quality craftsmanship ensures long-term reliability",
                    "Versatile design adapts to changing decor styles"
                ]
                
            else:  # Minimalist
                title = f"{color_cap.strip() if color_cap else ''} {product_name}".strip()
                description = f"""Solid. Comfortable.{color_cap.capitalize() + '.' if color_cap else ''}

Ergonomic support. Clean lines.

{features if features else 'Quality construction.'}

Furniture that works."""
                
                bullet_points = [
                    "Solid construction",
                    "Ergonomic design",
                    "Durable build",
                    f"{analysis.style} aesthetic",
                    "Built for daily use"
                ]
        
        # GENERAL FALLBACK - still better than before
        else:
            material_text = f"{analysis.materials[0].lower()} and {analysis.materials[1].lower()}"
            if "material" in material_text and "construction" in material_text:
                material_text = "premium materials with quality craftsmanship"
            
            if style == "Storytelling (Emotional)":
                title = f"{analysis.style} {product_name}{color_cap} - Premium Quality"
                description = f"""Discover the perfect harmony of form and function with this exceptional {color_text}{product_name.lower()}.

Crafted from {material_text}, this {product_name.lower()} combines {analysis.style.lower()} aesthetics with uncompromising quality.

{features if features else f'Whether for everyday use or special occasions, this {product_name.lower()} delivers an experience that exceeds expectations.'}

It's more than a product - it's a statement of quality and style."""
                
                bullet_points = [
                    f"{material_text.capitalize()} ensures lasting durability",
                    f"Sophisticated {analysis.style.lower()} design",
                    "Exceptional attention to detail",
                    "Versatile styling for multiple uses",
                    "Makes a thoughtful gift"
                ]
                
            elif style == "Feature-Benefit (Practical)":
                title = f"{product_name}{color_cap} - {analysis.style} Design | Professional Quality"
                description = f"""Experience professional-grade quality with this {color_text}{product_name.lower()}.

SUPERIOR CONSTRUCTION: Built with {material_text}, ensuring exceptional durability and reliable performance.

INTELLIGENT DESIGN: The {analysis.style.lower()} aesthetic is engineered for optimal functionality.

{features if features else 'PROVEN PERFORMANCE: Versatile design adapts to your needs.'}

QUALITY ASSURANCE: Rigorous standards ensure consistent excellence."""
                
                bullet_points = [
                    f"{material_text.capitalize()} provides superior strength",
                    "Intelligent design maximizes functionality",
                    "Premium construction maintains performance",
                    "Versatile use for multiple applications",
                    "Quality craftsmanship guaranteed"
                ]
                
            else:  # Minimalist
                title = f"{product_name}{color_cap} | {analysis.style}"
                description = f"""Clean design. Premium materials.{color_cap.capitalize() + '.' if color_cap else ''}

Crafted from {material_text}. {analysis.style} principles.

{features if features else 'Functional. Reliable. Timeless.'}

Built for those who value substance."""
                
                bullet_points = [
                    f"{material_text.capitalize()}",
                    f"{analysis.style} design aesthetic",
                    "Essential functionality",
                    "Superior craftsmanship",
                    "Timeless quality"
                ]
        
        meta = f"{product_name} - {bullet_points[0]}."[:160]
        
        return ProductDescription(
            title=title,
            description=description,
            bullet_points=bullet_points,
            meta_description=meta,
            style_type=style
        )
    
    @staticmethod
    def extract_keywords(product_name: str, analysis: ProductAnalysis, description: str) -> Dict[str, List[str]]:
        """Generate SEO keywords"""
        
        primary = [
            f"{product_name.lower()}",
            f"{analysis.style.lower()} {product_name.lower()}",
            f"premium {product_name.lower()}",
            f"best {product_name.lower()}",
            f"{analysis.materials[0].lower()} {product_name.lower()}",
            f"professional {product_name.lower()}",
            f"high quality {product_name.lower()}"
        ]
        
        long_tail = [
            f"buy {product_name.lower()} online",
            f"best {product_name.lower()} for sale",
            f"where to buy {product_name.lower()}",
            f"{analysis.style.lower()} {product_name.lower()} reviews",
            f"affordable {product_name.lower()}",
            f"professional grade {product_name.lower()}",
            f"{product_name.lower()} with {analysis.materials[0].lower()}",
            f"durable {product_name.lower()}",
            f"top rated {product_name.lower()}",
            f"{analysis.category.lower()} {product_name.lower()}"
        ]
        
        return {'primary': primary, 'long_tail': long_tail}


def format_for_platform(description: ProductDescription, keywords: Dict, platform: str) -> str:
    """Format listing for platform"""
    
    if platform == "Shopify":
        return f"""PRODUCT TITLE:
{description.title}

DESCRIPTION:
{description.description}

KEY FEATURES:
{chr(10).join(['• ' + bp for bp in description.bullet_points])}

META DESCRIPTION:
{description.meta_description}

PRODUCT TAGS:
{', '.join(keywords['primary'][:10])}

SEO KEYWORDS:
{', '.join(keywords['long_tail'][:8])}"""
    
    elif platform == "Amazon":
        return f"""PRODUCT TITLE (max 200 characters):
{description.title[:200]}

BULLET POINTS (5 maximum):
{chr(10).join(['• ' + bp for bp in description.bullet_points[:5]])}

PRODUCT DESCRIPTION:
{description.description[:2000]}

BACKEND SEARCH TERMS:
{', '.join(keywords['primary'][:7])}

ADDITIONAL KEYWORDS:
{', '.join(keywords['long_tail'][:10])}"""
    
    elif platform == "Etsy":
        return f"""LISTING TITLE (max 140 characters):
{description.title[:140]}

ABOUT THIS ITEM:
{description.description}

ITEM DETAILS:
{chr(10).join(['• ' + bp for bp in description.bullet_points])}

TAGS (max 13 tags):
{', '.join(keywords['primary'][:13])}

SHOP SECTION:
{keywords['primary'][0] if keywords['primary'] else 'Products'}"""
    
    else:  # WooCommerce
        return f"""PRODUCT NAME:
{description.title}

SHORT DESCRIPTION:
{description.meta_description}

FULL DESCRIPTION:
{description.description}

PRODUCT FEATURES:
{chr(10).join(['• ' + bp for bp in description.bullet_points])}

SEO TITLE:
{description.title}

SEO META DESCRIPTION:
{description.meta_description}

FOCUS KEYWORDS:
{', '.join(keywords['primary'][:5])}"""


def main():
    """Main application"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### About QuickList")
        st.markdown("""
        Transform product photos into professional listings in 30 seconds.
        
        **What You Get:**
        
        - Professional product descriptions
        - 3 writing styles to choose from
        - SEO keywords included
        - Ready for your store
        
        **Supported Platforms:**
        - Shopify
        - Amazon
        - Etsy
        - WooCommerce
        """)
        
        st.markdown("---")
        
        st.markdown("### Quick & Easy")
        st.markdown("""
        1. Upload photo
        2. Enter product name
        3. Generate listing
        4. Download
        
        Done in 30 seconds
        """)
        
        st.markdown("---")
        
        st.markdown("""
        **100% Free**  
        No signup required
        """)
    
    # Main content
    st.markdown("""
    <div class="upload-section">
        <h2 style="color: #000000; font-family: 'Space Grotesk', sans-serif; margin-bottom: 1rem;">
            Upload Your Product Photo
        </h2>
        <p style="color: #666666; font-size: 1.1rem;">
            Get professional listings instantly
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Product Image",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear product photo (JPG, JPEG, or PNG)"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Store image in session state for Gen AI
        st.session_state.product_image = image
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption="Your Product", width=500)
        
        st.markdown("""
        <div class="section-header">
            <h2 class="section-title">Product Information</h2>
            <p class="section-subtitle">Tell us about your product</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            product_name = st.text_input(
                "Product Name",
                placeholder="e.g., Wireless Headphones",
                help="Enter product name"
            )
        
        with col2:
            target_platform = st.selectbox(
                "Target Platform",
                ['Shopify', 'Amazon', 'Etsy', 'WooCommerce'],
                help="Choose platform"
            )
        
        product_features = st.text_area(
            "Key Features (Optional)",
            placeholder="e.g., 40-hour battery, noise cancellation...",
            help="Optional features",
            height=100
        )
        
        if product_name:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                if st.button("Generate Listing", use_container_width=True):
                    
                    ai = QuickListAI()
                    
                    st.session_state.show_results = True
                    st.session_state.product_name = product_name
                    st.session_state.target_platform = target_platform
                    
                    # Phase 1: Analysis
                    with st.spinner('Analyzing product...'):
                        progress = st.progress(0)
                        
                        for i in range(40):
                            time.sleep(0.02)
                            progress.progress(i + 1)
                        
                        analysis = ai.analyze_product_with_clip(image)
                        st.session_state.analysis = analysis
                        
                        for i in range(40, 50):
                            time.sleep(0.02)
                            progress.progress(i + 1)
                        
                        progress.empty()
                    
                    # Phase 2: Descriptions
                    with st.spinner('Writing professional descriptions...'):
                        progress = st.progress(0)
                        
                        descriptions = {}
                        styles = ["Storytelling (Emotional)", "Feature-Benefit (Practical)", "Minimalist (Clean)"]
                        
                        for idx, style_name in enumerate(styles):
                            desc = ai.generate_with_llava(
                                product_name, 
                                analysis, 
                                style_name, 
                                product_features,
                                image
                            )
                            descriptions[style_name] = desc
                            
                            prog = int((idx + 1) / len(styles) * 100)
                            progress.progress(prog)
                        
                        progress.empty()
                    
                    st.session_state.descriptions = descriptions
                    
                    # Phase 3: Keywords
                    with st.spinner('Generating keywords...'):
                        progress = st.progress(0)
                        
                        for i in range(100):
                            time.sleep(0.01)
                            progress.progress(i + 1)
                        
                        keywords = ai.extract_keywords(
                            product_name,
                            analysis,
                            descriptions["Feature-Benefit (Practical)"].description
                        )
                        
                        progress.empty()
                    
                    st.session_state.keywords = keywords
                    
                    st.success("Your listing is ready!")
        
        # Display results
        if 'show_results' in st.session_state and st.session_state.show_results:
            analysis = st.session_state.analysis
            descriptions = st.session_state.descriptions
            keywords = st.session_state.keywords
            target_platform = st.session_state.target_platform
            product_name = st.session_state.product_name
            
            # Analysis
            st.markdown("""
            <div class="section-header">
                <h2 class="section-title">Product Analysis</h2>
                <p class="section-subtitle">AI-powered insights from your image</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Category</div>
                    <div class="metric-value">{analysis.category}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Style</div>
                    <div class="metric-value">{analysis.style}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Materials</div>
                    <div class="metric-value" style="font-size: 1.1rem;">{', '.join(analysis.materials)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Descriptions
            st.markdown("""
            <div class="section-header">
                <h2 class="section-title">Your Product Descriptions</h2>
                <p class="section-subtitle">Three professionally written styles - compare side-by-side</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                desc = descriptions["Storytelling (Emotional)"]
                st.markdown(f"""
                <div class="description-card">
                    <div class="description-title">
                        Storytelling
                        <span class="style-badge">Emotional</span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Title:**\n{desc.title}")
                st.markdown(f"**Description:**\n{desc.description}")
                st.markdown("**Features:**")
                for bp in desc.bullet_points:
                    st.markdown(f"• {bp}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                desc = descriptions["Feature-Benefit (Practical)"]
                st.markdown(f"""
                <div class="description-card">
                    <div class="description-title">
                        Feature-Benefit
                        <span class="style-badge">Practical</span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Title:**\n{desc.title}")
                st.markdown(f"**Description:**\n{desc.description}")
                st.markdown("**Features:**")
                for bp in desc.bullet_points:
                    st.markdown(f"• {bp}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                desc = descriptions["Minimalist (Clean)"]
                st.markdown(f"""
                <div class="description-card">
                    <div class="description-title">
                        Minimalist
                        <span class="style-badge">Clean</span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Title:**\n{desc.title}")
                st.markdown(f"**Description:**\n{desc.description}")
                st.markdown("**Features:**")
                for bp in desc.bullet_points:
                    st.markdown(f"• {bp}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Keywords
            st.markdown("""
            <div class="seo-box">
                <div class="seo-title">SEO Keywords</div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Primary:**")
            keywords_html = " ".join([f'<span class="keyword-tag">{kw}</span>' for kw in keywords['primary']])
            st.markdown(keywords_html, unsafe_allow_html=True)
            
            st.markdown("**Long-tail:**")
            longtail_html = " ".join([f'<span class="keyword-tag">{kw}</span>' for kw in keywords['long_tail'][:10]])
            st.markdown(longtail_html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export
            st.markdown("""
            <div class="section-header">
                <h2 class="section-title">Platform Export</h2>
                <p class="section-subtitle">Formatted for {}</p>
            </div>
            """.format(target_platform), unsafe_allow_html=True)
            
            export_style = st.selectbox(
                "Choose Description Style:",
                list(descriptions.keys()),
                help="Select which AI-generated description to use for your platform export",
                key="style_selector"
            )
            
            formatted = format_for_platform(descriptions[export_style], keywords, target_platform)
            
            st.markdown(f"""
            <div style="background: #ffffff; border: 2px solid #e5e5e5; border-radius: 12px; padding: 2rem; margin: 1.5rem 0;">
                <h3 style="color: #0066cc;">Your Listing</h3>
                <pre style="color: #000000; background: #f8f8f8; padding: 1.5rem; border-radius: 8px; white-space: pre-wrap; font-size: 0.9rem;">{formatted}</pre>
            </div>
            """, unsafe_allow_html=True)
            
            # Download
            st.markdown("""
            <div class="section-header">
                <h2 class="section-title">Download Your Listing</h2>
                <p class="section-subtitle">Export and deploy instantly</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.download_button(
                    label=f"Download {target_platform}",
                    data=formatted,
                    file_name=f"{product_name.lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                all_listings = f"=== {product_name.upper()} - ALL STYLES ===\n\n"
                all_listings += f"Created by QuickList AI\n"
                all_listings += f"Platform: {target_platform}\n"
                all_listings += f"Category: {analysis.category}\n\n"
                all_listings += "="*70 + "\n\n"
                
                for style_name, desc in descriptions.items():
                    all_listings += f"\n{'='*70}\n{style_name}\n{'='*70}\n\n"
                    all_listings += format_for_platform(desc, keywords, target_platform) + "\n\n"
                
                st.download_button(
                    label="Download All Styles",
                    data=all_listings,
                    file_name=f"{product_name.lower().replace(' ', '_')}_all.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.markdown(f"""
            <div class="info-box">
                <p style="margin: 0; font-weight: 600;">
                    Your professional listing is ready! Upload to {target_platform} and start selling.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="info-box">
                <p>Enter product name to start</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # How it works
        st.markdown("""
        <div class="section-header">
            <h2 class="section-title">How QuickList Works</h2>
            <p class="section-subtitle">Professional AI-powered listings in seconds</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">1</div>
                <div class="metric-label">Upload Photo</div>
                <div style="color: #666666; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                    Upload your product image
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">2</div>
                <div class="metric-label">Generate Content</div>
                <div style="color: #666666; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                    Get descriptions, keywords, and photos
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">3</div>
                <div class="metric-label">Download & Sell</div>
                <div style="color: #666666; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                    Ready for Shopify, Amazon, Etsy
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 3rem;">
            <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">
                What You Get:
            </p>
            <p style="margin: 0; line-height: 1.8;">
                • Smart product analysis from your image<br>
                • 3 professionally written description styles<br>
                • Search-optimized keywords<br>
                • Platform-ready formatting<br>
                • Complete listing in under 30 seconds
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 2rem; border-left-color: #0066cc;">
            <p style="margin: 0; font-weight: 600;">
                100% Free • No Signup Required • Instant Results
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
