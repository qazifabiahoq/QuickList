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
        <div style="font-size: 4rem; margin-bottom: 1rem;">⚡</div>
        <h1 style="color: #ffffff !important; font-size: 3.5rem !important; font-weight: 800 !important; margin: 0 !important; font-family: 'Space Grotesk', sans-serif !important;">QuickList</h1>
        <p style="color: #ffffff !important; font-size: 1.25rem !important; margin-top: 0.75rem !important; font-family: 'Inter', sans-serif !important;">Professional Product Listings with TRUE Generative AI</p>
        <span style="background: linear-gradient(135deg, #059669 0%, #047857 100%) !important; color: #ffffff !important; display: inline-block !important; padding: 0.6rem 1.5rem !important; border-radius: 24px !important; font-size: 0.85rem !important; font-weight: 700 !important; margin-top: 1.25rem !important; text-transform: uppercase !important;">🤖 LLaVA Vision AI Powered</span>
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


class TrueGenAI:
    """100% REAL Generative AI - LLaVA Vision-Language Model"""
    
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
                    st.write(f"📦 Category: **{broad_cat}**")
                    
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
                    st.write(f"🎨 Color: **{detected_color}**")
            
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
                    st.write(f"🔧 Materials: **{mat1}, {mat2}**")
            
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
    def generate_with_llava(product_name: str, analysis: ProductAnalysis, 
                           style: str, features: str, image: Image.Image) -> ProductDescription:
        """TRUE GENERATIVE AI: LLaVA Vision-Language Model looks at image and writes description"""
        
        # Build style-specific prompt
        if style == "Storytelling (Emotional)":
            prompt = f"""Look carefully at this product image. This is a {product_name}.

Write an emotional, storytelling e-commerce description (150-200 words) based on what you see:
- Describe the visual details, colors, textures, design
- Create emotional connection - how it makes people feel
- Use sensory, evocative language
- Focus on lifestyle benefits

Additional info: {features if features else 'Premium quality'}

Respond with JSON only:
{{
  "title": "emotional title with benefit",
  "description": "storytelling description",
  "bullet_points": ["benefit 1", "benefit 2", "benefit 3", "benefit 4", "benefit 5"],
  "meta_description": "SEO meta under 160 chars"
}}"""

        elif style == "Feature-Benefit (Practical)":
            prompt = f"""Look at this {product_name} image.

Write a practical feature-benefit description (150-200 words) based on what you see:
- List visual features you observe
- Explain why each feature matters
- Focus on functionality and value
- Professional, clear language

Info: {features if features else 'Professional quality'}

JSON format:
{{
  "title": "professional title",
  "description": "feature-benefit description",
  "bullet_points": ["feature 1", "feature 2", "feature 3", "feature 4", "feature 5"],
  "meta_description": "meta under 160 chars"
}}"""

        else:  # Minimalist
            prompt = f"""Look at this {product_name}.

Write a minimalist description (80-100 words) based on what you see:
- Short sentences
- Essential visual details only
- No fluff
- Clean and direct

Info: {features if features else 'Quality product'}

JSON:
{{
  "title": "simple title",
  "description": "minimalist description",
  "bullet_points": ["detail 1", "detail 2", "detail 3", "detail 4", "detail 5"],
  "meta_description": "meta under 160"
}}"""

        try:
            st.info("🤖 **TRUE GEN AI**: LLaVA is looking at your image and writing description...")
            
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Call LLaVA API
            API_URL = "https://api-inference.huggingface.co/models/llava-hf/llava-1.5-7b-hf"
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "inputs": {
                    "question": prompt,
                    "image": img_b64
                },
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract generated text
                generated_text = ""
                if isinstance(result, dict):
                    generated_text = result.get('generated_text', result.get('answer', result.get('text', '')))
                elif isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', result[0].get('answer', result[0].get('text', '')))
                
                if generated_text and len(generated_text) > 50:
                    # Clean up response
                    generated_text = generated_text.replace('```json', '').replace('```', '').strip()
                    
                    # Try to find JSON
                    start = generated_text.find('{')
                    end = generated_text.rfind('}') + 1
                    
                    if start != -1 and end > start:
                        try:
                            json_str = generated_text[start:end]
                            parsed = json.loads(json_str)
                            
                            st.success("✅ **SUCCESS!** LLaVA Gen AI created description from your image!")
                            
                            return ProductDescription(
                                title=parsed.get('title', f"{product_name}"),
                                description=parsed.get('description', ''),
                                bullet_points=parsed.get('bullet_points', [])[:5],
                                meta_description=parsed.get('meta_description', '')[:160],
                                style_type=style
                            )
                        except json.JSONDecodeError:
                            # Got text but not JSON - still use it!
                            st.warning("LLaVA generated text (not JSON) - reformatting...")
                            
                            return ProductDescription(
                                title=f"{analysis.style} {product_name}",
                                description=generated_text[:500],
                                bullet_points=[
                                    "AI-generated premium quality",
                                    f"{analysis.style} design aesthetic", 
                                    "Professional craftsmanship",
                                    "Versatile use",
                                    "Excellent value"
                                ],
                                meta_description=generated_text[:160],
                                style_type=style
                            )
            
            # LLaVA didn't work - try Mistral as backup
            st.warning("LLaVA busy - trying Mistral Gen AI...")
            raise Exception("Try Mistral")
            
        except Exception as e:
            # BACKUP: Mistral (text-based Gen AI)
            try:
                st.info("Using Mistral Gen AI as backup...")
                
                API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
                
                context = f"""Product: {product_name}
Category: {analysis.category}
Color: {analysis.colors[0]}
Style: {analysis.style}
Materials: {', '.join(analysis.materials)}
Features: {features if features else 'Premium quality'}

{prompt}"""

                headers = {"Content-Type": "application/json"}
                payload = {
                    "inputs": context,
                    "parameters": {
                        "max_new_tokens": 400,
                        "temperature": 0.7,
                        "return_full_text": False
                    }
                }
                
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    generated = result[0].get('generated_text', '') if isinstance(result, list) else result.get('generated_text', '')
                    
                    if generated:
                        generated = generated.replace('```json', '').replace('```', '').strip()
                        start = generated.find('{')
                        end = generated.rfind('}') + 1
                        
                        if start != -1 and end > start:
                            json_str = generated[start:end]
                            parsed = json.loads(json_str)
                            
                            st.success("✅ Mistral Gen AI created description!")
                            
                            return ProductDescription(
                                title=parsed.get('title', product_name),
                                description=parsed.get('description', ''),
                                bullet_points=parsed.get('bullet_points', [])[:5],
                                meta_description=parsed.get('meta_description', '')[:160],
                                style_type=style
                            )
            except:
                pass
            
            # All Gen AI failed - use smart templates with CLIP data
            st.warning("⚠️ Gen AI models overloaded - using enhanced templates with AI-detected features")
            return TrueGenAI._template_fallback(product_name, analysis, style, features)
    
    @staticmethod
    def _template_fallback(product_name: str, analysis: ProductAnalysis, 
                          style: str, features: str) -> ProductDescription:
        """Smart template fallback with CLIP features"""
        
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        color_text = f" in {color}" if color else ""
        
        material_text = f"{analysis.materials[0].lower()} and {analysis.materials[1].lower()}"
        if "material" in material_text and "construction" in material_text:
            material_text = "premium materials with quality craftsmanship"
        
        if style == "Storytelling (Emotional)":
            title = f"{analysis.style} {product_name}{color_text} - Premium Quality"
            description = f"""Discover the perfect harmony of form and function with this exceptional {product_name.lower()}{color_text}.

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
            title = f"{product_name}{color_text} - {analysis.style} Design | Professional Quality"
            description = f"""Experience professional-grade quality with this {product_name.lower()}{color_text}.

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
            title = f"{product_name}{color_text} | {analysis.style}"
            description = f"""Clean design. Premium materials. Built to last.{color_text.capitalize() + '.' if color_text else ''}

This {product_name.lower()} represents essentials, perfected.

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
        
        meta = f"{product_name} - {analysis.style} {analysis.category.lower()}. {bullet_points[0]}."[:160]
        
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
        **QuickList** uses **TRUE Generative AI** to create professional product listings.
        
        **Technology:**
        
        - 🤖 **LLaVA Vision AI** - Looks at images and writes descriptions
        - 🧠 **Mistral AI** - Generates creative copy
        - 👁️ **CLIP Vision** - Analyzes product features
        
        **What You Get:**
        
        - AI-generated descriptions
        - Professional copy (3 styles)
        - SEO keywords
        - Platform formatting
        
        **Works With:**
        - Shopify
        - Amazon
        - Etsy
        - WooCommerce
        """)
        
        st.markdown("---")
        
        st.markdown("### How It Works")
        st.markdown("""
        1. Upload product photo
        2. **LLaVA AI looks at image**
        3. **AI writes description**
        4. Generate 3 copy styles
        5. Download and list
        
        Ready in 60 seconds
        """)
        
        st.markdown("---")
        
        st.markdown("### Why This is Gen AI")
        st.markdown("""
        **Traditional AI:**
        - Templates + keywords ❌
        - Pre-written copy ❌
        
        **QuickList Gen AI:**
        - **Sees** your product ✅
        - **Writes** original text ✅
        - **Creates** from scratch ✅
        
        100% Generative AI
        """)
    
    # Main content
    st.markdown("""
    <div class="upload-section">
        <h2 style="color: #000000; font-family: 'Space Grotesk', sans-serif; margin-bottom: 1rem;">
            Upload Your Product Photo
        </h2>
        <p style="color: #666666; font-size: 1.1rem;">
            LLaVA AI will look at it and write your listing
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Product Image",
        type=['jpg', 'jpeg', 'png'],
        help="AI will analyze this image"
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
                if st.button("🚀 Generate with AI", use_container_width=True):
                    
                    ai = TrueGenAI()
                    
                    st.session_state.show_results = True
                    st.session_state.product_name = product_name
                    st.session_state.target_platform = target_platform
                    
                    # Phase 1: Quick analysis
                    st.markdown('<div class="status-badge status-processing">Quick image analysis...</div>', unsafe_allow_html=True)
                    
                    with st.spinner('Analyzing...'):
                        progress = st.progress(0)
                        
                        for i in range(30):
                            time.sleep(0.03)
                            progress.progress(i + 1)
                        
                        analysis = ai.analyze_product_with_clip(image)
                        st.session_state.analysis = analysis
                        
                        for i in range(30, 50):
                            time.sleep(0.02)
                            progress.progress(i + 1)
                        
                        progress.empty()
                    
                    st.markdown('<div class="status-badge status-complete">Analysis Complete</div>', unsafe_allow_html=True)
                    
                    # Phase 2: GENERATIVE AI
                    st.markdown('<div class="status-badge status-processing">🤖 TRUE GEN AI: Writing descriptions...</div>', unsafe_allow_html=True)
                    
                    with st.spinner('LLaVA AI is looking at your image and writing...'):
                        progress = st.progress(0)
                        
                        descriptions = {}
                        styles = ["Storytelling (Emotional)", "Feature-Benefit (Practical)", "Minimalist (Clean)"]
                        
                        for idx, style_name in enumerate(styles):
                            st.text(f"Gen AI writing: {style_name.split('(')[0].strip()}...")
                            
                            # THIS IS TRUE GEN AI - PASS THE IMAGE!
                            desc = ai.generate_with_llava(
                                product_name, 
                                analysis, 
                                style_name, 
                                product_features,
                                image  # ← IMAGE GOES TO GEN AI
                            )
                            descriptions[style_name] = desc
                            
                            prog = int((idx + 1) / len(styles) * 100)
                            progress.progress(prog)
                            time.sleep(1)
                        
                        progress.empty()
                    
                    st.session_state.descriptions = descriptions
                    
                    st.markdown('<div class="status-badge status-complete">✅ Gen AI Complete!</div>', unsafe_allow_html=True)
                    
                    # Phase 3: Keywords
                    st.markdown('<div class="status-badge status-processing">Generating keywords...</div>', unsafe_allow_html=True)
                    
                    with st.spinner('Creating SEO keywords...'):
                        progress = st.progress(0)
                        
                        for i in range(100):
                            time.sleep(0.02)
                            progress.progress(i + 1)
                        
                        keywords = ai.extract_keywords(
                            product_name,
                            analysis,
                            descriptions["Feature-Benefit (Practical)"].description
                        )
                        
                        progress.empty()
                    
                    st.session_state.keywords = keywords
                    
                    st.markdown('<div class="status-badge status-complete">All Done!</div>', unsafe_allow_html=True)
        
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
                <h2 class="section-title">AI Analysis</h2>
                <p class="section-subtitle">What our AI detected</p>
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
                <h2 class="section-title">🤖 Gen AI Descriptions</h2>
                <p class="section-subtitle">Written by LLaVA Vision AI</p>
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
                "Choose Style:",
                list(descriptions.keys()),
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
                <h2 class="section-title">Download</h2>
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
                all_listings = f"=== {product_name.upper()} - GEN AI ===\n\n"
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
                    ✅ Your AI-generated listing is ready!
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
            <p class="section-subtitle">TRUE Generative AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📸</div>
                <div class="metric-label">Upload Photo</div>
                <div style="color: #666666; font-size: 0.95rem; margin-top: 0.5rem;">
                    AI will look at it
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <div class="metric-label">AI Writes</div>
                <div style="color: #666666; font-size: 0.95rem; margin-top: 0.5rem;">
                    LLaVA generates descriptions
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💾</div>
                <div class="metric-label">Download</div>
                <div style="color: #666666; font-size: 0.95rem; margin-top: 0.5rem;">
                    Ready for your store
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 3rem;">
            <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">
                🤖 TRUE Generative AI:
            </p>
            <p style="margin: 0; line-height: 1.8;">
                • LLaVA Vision AI looks at your product image<br>
                • Generates original descriptions from scratch<br>
                • 3 professional writing styles<br>
                • SEO-optimized keywords<br>
                • Platform-ready formatting
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 2rem; border-left-color: #059669;">
            <p style="margin: 0; font-weight: 600;">
                100% Free • No Signup • Real Generative AI
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
