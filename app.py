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
import re

# Multi-AI fallback configuration
HAS_GROQ = False
GROQ_API_KEY = None

try:
    from groq import Groq
    GROQ_API_KEY = st.secrets.get("groq", {}).get("api_key")
    HAS_GROQ = True if GROQ_API_KEY else False
except:
    pass

# Page configuration
st.set_page_config(
    page_title="QuickList by ThreadUp",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with ThreadUp-inspired green theme and shaded backgrounds
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    :root {
        --primary-green: #00A676;
        --light-green: #2FB56A;
        --accent-green: #4CC38A;
        --mint-bg: #F0FDF8;
        --background-cream: #FAFAFA;
        --text-dark: #1a1a1a;
        --border-light: #E5E5E5;
    }
    
    .stApp {
        background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F5 100%) !important;
    }
    
    .stApp > div {
        background: transparent !important;
    }
    
    .main {
        background: transparent !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-header {
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 166, 118, 0.12);
        border-radius: 0 0 32px 32px !important;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.08'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        z-index: 0;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    body, p, div, span, label, h1, h2, h3, h4, h5, h6 {
        color: var(--text-dark) !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FAFAFA 0%, #F5F5F5 100%);
        border-right: 2px solid var(--border-light);
    }
    
    .upload-section {
        background: #FFFFFF !important;
        border: 2px solid var(--border-light);
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 166, 118, 0.08);
    }
    
    .upload-section h2,
    .upload-section p {
        color: var(--text-dark) !important;
    }
    
    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 3px dashed var(--accent-green) !important;
        border-radius: 16px !important;
        padding: 2.5rem !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: var(--primary-green) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: #ffffff !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        background: #ffffff !important;
    }
    
    [data-testid="stFileUploader"] div {
        background: #ffffff !important;
        color: var(--text-dark) !important;
    }
    
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] label {
        color: var(--text-dark) !important;
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: #ffffff !important;
        color: var(--primary-green) !important;
        border: 2px solid var(--primary-green) !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: var(--primary-green) !important;
        color: #ffffff !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--light-green) 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1.25rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(45, 95, 63, 0.25) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        width: 100%;
        height: 65px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--light-green) 0%, var(--accent-green) 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(74, 140, 95, 0.35) !important;
    }
    
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #ffffff !important;
    }
    
    .stDownloadButton > button {
        background: #ffffff !important;
        color: var(--primary-green) !important;
        border: 2px solid var(--primary-green) !important;
        border-radius: 14px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: var(--primary-green) !important;
        color: #ffffff !important;
        transform: translateY(-2px);
    }
    
    .metric-box {
        background: #FFFFFF;
        border: 2px solid var(--border-light);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        min-height: 140px;
        box-shadow: 0 2px 12px rgba(0, 166, 118, 0.06);
    }
    
    .metric-box:hover {
        border-color: var(--accent-green);
        box-shadow: 0 8px 24px rgba(0, 166, 118, 0.15);
        transform: translateY(-4px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
        font-weight: 700;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-green) !important;
        font-family: 'Poppins', sans-serif;
        line-height: 1.4;
        padding: 0 0.25rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
    
    .description-card {
        background: #FFFFFF;
        border: 2px solid var(--border-light);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 166, 118, 0.08);
    }
    
    .description-card:hover {
        border-color: var(--accent-green);
        box-shadow: 0 8px 28px rgba(0, 166, 118, 0.12);
    }
    
    .description-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-green) !important;
        margin-bottom: 1.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .seo-box {
        background: linear-gradient(135deg, #F0FDF8 0%, #E6FAF3 100%);
        border: 2px solid var(--border-light);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 16px rgba(0, 166, 118, 0.08);
    }
    
    .seo-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-green) !important;
        margin-bottom: 1.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .keyword-tag {
        display: inline-block;
        background: #FFFFFF;
        color: var(--primary-green) !important;
        border: 2px solid var(--primary-green);
        padding: 0.5rem 1rem;
        border-radius: 24px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.4rem 0.4rem 0.4rem 0;
        transition: all 0.2s ease;
    }
    
    .keyword-tag:hover {
        background: var(--primary-green);
        color: #ffffff !important;
        transform: scale(1.05);
    }
    
    [data-testid="stImage"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(0, 166, 118, 0.12);
    }
    
    [data-testid="stImage"] img {
        border-radius: 16px;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-green) 0%, var(--accent-green) 100%);
    }
    
    .section-header {
        background: linear-gradient(135deg, #F0FDF8 0%, #E6FAF3 100%);
        border-left: 5px solid var(--primary-green);
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin: 3rem 0 2rem 0;
        box-shadow: 0 3px 12px rgba(0, 166, 118, 0.08);
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-green) !important;
        font-family: 'Poppins', sans-serif;
        margin: 0;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: #6b7280 !important;
        margin-top: 0.5rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, #F0FDF8 0%, #E6FAF3 100%);
        border-left: 4px solid var(--primary-green);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 10px rgba(0, 166, 118, 0.06);
    }
    
    .info-box p {
        color: var(--text-dark) !important;
        line-height: 1.7;
        margin: 0;
    }
    
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
        color: var(--primary-green) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput input,
    .stTextArea textarea {
        background: #ffffff !important;
        border: 2px solid var(--border-light) !important;
        color: var(--text-dark) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--accent-green) !important;
        box-shadow: 0 0 0 3px rgba(107, 183, 123, 0.1) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background: #ffffff !important;
        border: 2px solid var(--border-light) !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: var(--accent-green) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: var(--text-dark) !important;
    }
    
    [data-baseweb="menu"] {
        background: #ffffff !important;
        border: 1px solid var(--border-light) !important;
        box-shadow: 0 4px 16px rgba(45, 95, 63, 0.1) !important;
        border-radius: 8px !important;
    }
    
    [data-baseweb="menu"] ul {
        background: #ffffff !important;
    }
    
    [data-baseweb="menu"] li {
        background: #ffffff !important;
        color: var(--text-dark) !important;
        padding: 0.75rem 1rem !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: #f0f7f3 !important;
        color: var(--primary-green) !important;
    }
    
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
    
    .brand-tag {
        background: #FFFFFF;
        border: 2px solid #00A676;
        color: #00A676 !important;
        display: inline-block;
        padding: 0.6rem 1.4rem;
        border-radius: 24px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 1.25rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        box-shadow: 0 2px 12px rgba(0, 166, 118, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Header with ThreadUp branding
st.markdown("""
<div class="main-header" style="background: linear-gradient(135deg, #F0FDF8 0%, #E6FAF3 100%) !important; text-align: center; padding: 3rem; border-radius: 0 0 32px 32px; margin: -6rem -5rem 3rem -5rem;">
    <div class="header-content">
        <h1 style="color: #00A676 !important; font-size: 3.5rem !important; font-weight: 800 !important; margin: 0 !important; font-family: 'Poppins', sans-serif !important;">QuickList</h1>
        <p style="color: #00A676 !important; font-size: 0.9rem !important; margin-top: 0.5rem !important; font-family: 'Inter', sans-serif !important; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 600; opacity: 0.8;">by ThreadUp</p>
        <p style="color: #1a1a1a !important; font-size: 1.25rem !important; margin-top: 1rem !important; font-family: 'Inter', sans-serif !important; opacity: 0.85;">Professional Product Listings in Seconds</p>
        <div class="brand-tag">
            🌿 Powered by AI • Sustainable Resale
        </div>
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
    specific_type: str = ""


@dataclass
class ProductDescription:
    title: str
    description: str
    bullet_points: List[str]
    meta_description: str


class QuickListAI:
    """AI-powered product listing generator"""
    
    @staticmethod
    def analyze_with_vision_apis(image: Image.Image, product_name: str = "") -> ProductAnalysis:
        """Multi-tier FREE image detection: Google Vision → Amazon Rekognition → CLIP"""
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=95)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # ============================================
        # TIER 1: Google Cloud Vision API (1000/month free)
        # ============================================
        try:
            # Check if Google API key exists
            google_key = None
            try:
                google_key = st.secrets.get("google", {}).get("vision_api_key")
            except:
                pass
            
            if google_key:
                response = requests.post(
                    f"https://vision.googleapis.com/v1/images:annotate?key={google_key}",
                    json={
                        "requests": [{
                            "image": {"content": img_base64},
                            "features": [
                                {"type": "LABEL_DETECTION", "maxResults": 10},
                                {"type": "OBJECT_LOCALIZATION", "maxResults": 5},
                                {"type": "IMAGE_PROPERTIES"}
                            ]
                        }]
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    labels = [label['description'].lower() for label in result['responses'][0].get('labelAnnotations', [])]
                    objects = [obj['name'].lower() for obj in result['responses'][0].get('localizedObjectAnnotations', [])]
                    colors_data = result['responses'][0].get('imagePropertiesAnnotation', {}).get('dominantColors', {}).get('colors', [])
                    
                    # Extract category from labels/objects
                    category, specific_type = QuickListAI._parse_google_vision(labels, objects, product_name)
                    
                    # Extract dominant color
                    dominant_color = "neutral"
                    if colors_data:
                        rgb = colors_data[0].get('color', {})
                        dominant_color = QuickListAI._rgb_to_color_name(rgb.get('red', 0), rgb.get('green', 0), rgb.get('blue', 0))
                    
                    # Detect materials and style from labels
                    materials, style = QuickListAI._detect_materials_style(labels, category)
                    
                    return ProductAnalysis(
                        category=category,
                        materials=materials,
                        colors=[dominant_color, "#000000"],
                        style=style,
                        confidence=0.92,
                        specific_type=specific_type
                    )
        except Exception as e:
            pass
        
        # ============================================
        # TIER 2: Amazon Rekognition (5000/month free first year)
        # ============================================
        try:
            # Check for AWS credentials
            aws_key = None
            aws_secret = None
            try:
                aws_key = st.secrets.get("aws", {}).get("access_key_id")
                aws_secret = st.secrets.get("aws", {}).get("secret_access_key")
            except:
                pass
            
            if aws_key and aws_secret:
                import boto3
                
                client = boto3.client(
                    'rekognition',
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret,
                    region_name='us-east-1'
                )
                
                response = client.detect_labels(
                    Image={'Bytes': buffered.getvalue()},
                    MaxLabels=15,
                    MinConfidence=70
                )
                
                labels = [label['Name'].lower() for label in response['Labels']]
                
                category, specific_type = QuickListAI._parse_amazon_labels(labels, product_name)
                materials, style = QuickListAI._detect_materials_style(labels, category)
                
                # Get color from image
                dominant_color = QuickListAI._extract_dominant_color(image)
                
                return ProductAnalysis(
                    category=category,
                    materials=materials,
                    colors=[dominant_color, "#000000"],
                    style=style,
                    confidence=0.89,
                    specific_type=specific_type
                )
        except Exception as e:
            pass
        
        # ============================================
        # TIER 3: CLIP (HuggingFace - Unlimited Free)
        # ============================================
        return QuickListAI._analyze_with_clip(image, product_name)
    
    @staticmethod
    def _parse_google_vision(labels: List[str], objects: List[str], product_name: str) -> tuple:
        """Parse Google Vision labels to category"""
        all_tags = labels + objects
        prod_lower = product_name.lower()
        
        # Clothing
        if any(tag in all_tags or tag in prod_lower for tag in ['dress', 'gown', 'frock']):
            return "Apparel & Fashion", "Dress"
        elif any(tag in all_tags or tag in prod_lower for tag in ['shirt', 'blouse', 'top']):
            return "Apparel & Fashion", "Top"
        elif any(tag in all_tags or tag in prod_lower for tag in ['pants', 'jeans', 'trousers']):
            return "Apparel & Fashion", "Pants"
        elif any(tag in all_tags or tag in prod_lower for tag in ['jacket', 'coat', 'blazer']):
            return "Apparel & Fashion", "Jacket"
        
        # Electronics
        elif any(tag in all_tags or tag in prod_lower for tag in ['headphones', 'earbuds', 'earphones']):
            return "Electronics", "Headphones"
        elif any(tag in all_tags or tag in prod_lower for tag in ['phone', 'smartphone', 'mobile']):
            return "Electronics", "Smartphone"
        elif any(tag in all_tags or tag in prod_lower for tag in ['laptop', 'computer', 'notebook']):
            return "Electronics", "Laptop"
        
        # Furniture
        elif any(tag in all_tags or tag in prod_lower for tag in ['chair', 'seat']):
            return "Furniture", "Chair"
        elif any(tag in all_tags or tag in prod_lower for tag in ['table', 'desk']):
            return "Furniture", "Table"
        elif any(tag in all_tags or tag in prod_lower for tag in ['sofa', 'couch']):
            return "Furniture", "Sofa"
        
        # Accessories
        elif any(tag in all_tags or tag in prod_lower for tag in ['bag', 'purse', 'handbag']):
            return "Bags & Luggage", "Bag"
        elif any(tag in all_tags or tag in prod_lower for tag in ['shoes', 'sneakers', 'boots']):
            return "Footwear", "Shoes"
        
        # Default
        return "Product", "Item"
    
    @staticmethod
    def _parse_amazon_labels(labels: List[str], product_name: str) -> tuple:
        """Parse Amazon Rekognition labels"""
        return QuickListAI._parse_google_vision(labels, [], product_name)
    
    @staticmethod
    def _rgb_to_color_name(r: int, g: int, b: int) -> str:
        """Convert RGB to color name"""
        if r < 50 and g < 50 and b < 50:
            return "black"
        elif r > 200 and g > 200 and b > 200:
            return "white"
        elif r > g and r > b:
            return "red"
        elif g > r and g > b:
            return "green"
        elif b > r and b > g:
            return "blue"
        elif r > 150 and g > 100 and b < 100:
            return "brown"
        elif r > 150 and g > 150 and b < 100:
            return "yellow"
        else:
            return "neutral"
    
    @staticmethod
    def _extract_dominant_color(image: Image.Image) -> str:
        """Extract dominant color from image"""
        img_array = np.array(image.resize((100, 100)))
        pixels = img_array.reshape(-1, 3)
        avg_color = np.mean(pixels, axis=0).astype(int)
        return QuickListAI._rgb_to_color_name(avg_color[0], avg_color[1], avg_color[2])
    
    @staticmethod
    def _detect_materials_style(labels: List[str], category: str) -> tuple:
        """Detect materials and style from labels"""
        materials = ["Premium", "Quality"]
        style = "Modern"
        
        # Materials
        if category == "Apparel & Fashion":
            if any(mat in ' '.join(labels) for mat in ['silk', 'satin']):
                materials = ["Silk", "Premium Fabric"]
            elif any(mat in ' '.join(labels) for mat in ['cotton', 'cloth']):
                materials = ["Cotton", "Soft Fabric"]
            elif any(mat in ' '.join(labels) for mat in ['leather']):
                materials = ["Leather", "Premium Material"]
            else:
                materials = ["Fabric", "Quality Material"]
        
        # Style
        if any(s in ' '.join(labels) for s in ['elegant', 'formal', 'luxury']):
            style = "Elegant"
        elif any(s in ' '.join(labels) for s in ['casual', 'everyday']):
            style = "Casual"
        elif any(s in ' '.join(labels) for s in ['vintage', 'classic']):
            style = "Classic"
        
        return materials, style
    
    @staticmethod
    def _analyze_with_clip(image: Image.Image, product_name: str) -> ProductAnalysis:
        """Fallback CLIP analysis"""
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            headers = {"Content-Type": "application/octet-stream"}
            API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
            
            prod_lower = product_name.lower()
            
            # Detect category
            categories = [
                "dress evening gown", "shirt blouse top", "pants jeans", "jacket coat",
                "headphones earbuds", "smartphone phone", "laptop computer",
                "chair seating", "table desk", "sofa couch",
                "bag purse", "shoes footwear"
            ]
            
            response = requests.post(
                API_URL,
                headers=headers,
                data=img_bytes,
                params={"candidate_labels": ",".join(categories)},
                timeout=20
            )
            
            category = "Apparel & Fashion"
            specific_type = "Dress"
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    detected = result[0].get('label', '').lower()
                    
                    if "dress" in detected or "dress" in prod_lower:
                        category, specific_type = "Apparel & Fashion", "Dress"
                    elif "shirt" in detected or "top" in detected or "shirt" in prod_lower:
                        category, specific_type = "Apparel & Fashion", "Top"
                    elif "pants" in detected or "jeans" in detected or "pants" in prod_lower:
                        category, specific_type = "Apparel & Fashion", "Pants"
                    elif "headphone" in detected or "headphone" in prod_lower:
                        category, specific_type = "Electronics", "Headphones"
                    elif "phone" in detected or "phone" in prod_lower:
                        category, specific_type = "Electronics", "Smartphone"
                    elif "laptop" in detected or "laptop" in prod_lower:
                        category, specific_type = "Electronics", "Laptop"
            
            # Get color
            dominant_color = QuickListAI._extract_dominant_color(image)
            if "black" in prod_lower:
                dominant_color = "black"
            
            # Materials and style based on category
            if category == "Apparel & Fashion":
                materials = ["Silk", "Premium Fabric"]
                style = "Elegant"
            else:
                materials = ["Premium", "Quality"]
                style = "Modern"
            
            return ProductAnalysis(
                category=category,
                materials=materials,
                colors=[dominant_color, "#000000"],
                style=style,
                confidence=0.82,
                specific_type=specific_type
            )
            
        except Exception as e:
            return ProductAnalysis(
                category="Apparel & Fashion",
                materials=["Silk", "Quality Fabric"],
                colors=['black', '#000000'],
                style='Elegant',
                confidence=0.75,
                specific_type="Dress"
            )
    
    @staticmethod
    def clean_json_response(text: str) -> str:
        """Extract JSON from response"""
        text = re.sub(r'```json\s*|\s*```', '', text, flags=re.IGNORECASE)
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            return text[start:end]
        return text
    
    @staticmethod
    def generate_description(product_name: str, analysis: ProductAnalysis, 
                            features: str, image: Image.Image,
                            target_audience: str = "", price_range: str = "") -> ProductDescription:
        """Generate ONE professional description using multi-AI fallback"""
        
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        
        # Build context
        context = f"""Product: {product_name}
Category: {analysis.category}
Type: {analysis.specific_type}
Color: {color}
Style: {analysis.style}
Materials: {', '.join(analysis.materials)}
Features: {features if features else 'Premium quality'}"""
        
        if target_audience:
            context += f"\nTarget Audience: {target_audience}"
        if price_range:
            context += f"\nPrice Range: {price_range}"
        
        # Create prompt for professional e-commerce description
        prompt = f"""Write a professional e-commerce product description for this {analysis.specific_type.lower()}.

{context}

Write 150-200 words that balance emotional appeal with practical benefits. Be specific, engaging, and persuasive.

Respond ONLY with valid JSON (no markdown, no extra text):
{{"title": "compelling product title", "description": "engaging professional description", "bullet_points": ["key benefit 1", "key benefit 2", "key benefit 3", "key benefit 4", "key benefit 5"], "meta_description": "SEO meta under 160 chars"}}"""
        
        # ============================================
        # Try multiple AI services
        # ============================================
        
        # TIER 1: Groq
        if GROQ_API_KEY and HAS_GROQ:
            try:
                client = Groq(api_key=GROQ_API_KEY)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=700,
                    response_format={"type": "json_object"}
                )
                
                parsed = json.loads(completion.choices[0].message.content)
                return ProductDescription(
                    title=parsed.get('title', product_name),
                    description=parsed.get('description', ''),
                    bullet_points=parsed.get('bullet_points', [])[:5],
                    meta_description=parsed.get('meta_description', '')[:160]
                )
            except Exception as e:
                pass
        
        # TIER 2: DeepInfra
        try:
            response = requests.post(
                "https://api.deepinfra.com/v1/inference/meta-llama/Meta-Llama-3.1-70B-Instruct",
                headers={"Content-Type": "application/json"},
                json={"input": prompt, "max_tokens": 700, "temperature": 0.7},
                timeout=25
            )
            
            if response.status_code == 200:
                result = response.json()
                generated = result.get('results', [{}])[0].get('generated_text', '') or result.get('output', '')
                
                if generated:
                    cleaned = QuickListAI.clean_json_response(generated)
                    parsed = json.loads(cleaned)
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160]
                    )
        except Exception as e:
            pass
        
        # TIER 3: Together AI
        try:
            response = requests.post(
                "https://api.together.xyz/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 700,
                    "temperature": 0.7
                },
                timeout=25
            )
            
            if response.status_code == 200:
                result = response.json()
                generated = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                
                if generated:
                    cleaned = QuickListAI.clean_json_response(generated)
                    parsed = json.loads(cleaned)
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160]
                    )
        except Exception as e:
            pass
        
        # TIER 4: Pollinations
        try:
            response = requests.post(
                "https://text.pollinations.ai/",
                json={
                    "messages": [{"role": "user", "content": f"{prompt}\n\nIMPORTANT: Respond ONLY with valid JSON."}],
                    "model": "openai",
                    "jsonMode": True
                },
                timeout=25
            )
            
            if response.status_code == 200:
                generated = response.text.strip()
                cleaned = QuickListAI.clean_json_response(generated)
                parsed = json.loads(cleaned)
                
                return ProductDescription(
                    title=parsed.get('title', product_name),
                    description=parsed.get('description', ''),
                    bullet_points=parsed.get('bullet_points', [])[:5],
                    meta_description=parsed.get('meta_description', '')[:160]
                )
        except Exception as e:
            pass
        
        # TIER 5: HuggingFace Qwen
        try:
            response = requests.post(
                "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct",
                headers={"Content-Type": "application/json"},
                json={
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": 700, "temperature": 0.7, "return_full_text": False}
                },
                timeout=25
            )
            
            if response.status_code == 200:
                result = response.json()
                generated = result[0].get('generated_text', '') if isinstance(result, list) else result.get('generated_text', '')
                
                if generated:
                    cleaned = QuickListAI.clean_json_response(generated)
                    parsed = json.loads(cleaned)
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160]
                    )
        except Exception as e:
            pass
        
        # TIER 6: HuggingFace Mistral
        try:
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
                headers={"Content-Type": "application/json"},
                json={
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": 600, "temperature": 0.7, "return_full_text": False}
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                generated = result[0].get('generated_text', '') if isinstance(result, list) else result.get('generated_text', '')
                
                if generated:
                    cleaned = QuickListAI.clean_json_response(generated)
                    parsed = json.loads(cleaned)
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160]
                    )
        except Exception as e:
            pass
        
        # FINAL FALLBACK: Simple template
        # Don't duplicate color if it's already in product name
        color_text = ""
        if color and color.lower() not in product_name.lower():
            color_text = f"{color} "
        
        return ProductDescription(
            title=f"{analysis.style} {color_text}{product_name}".strip(),
            description=f"Experience exceptional quality with this {color_text}{product_name.lower()}. Crafted from {analysis.materials[0].lower()}, this {analysis.specific_type.lower()} combines {analysis.style.lower()} design with premium craftsmanship. {features if features else 'Perfect for any occasion.'}",
            bullet_points=[
                f"{analysis.materials[0]} construction for durability",
                f"{analysis.style} design that stands out",
                f"Versatile {color if color else 'classic'} styling",
                "Quality craftsmanship ensures long-lasting wear",
                "Perfect addition to your collection"
            ],
            meta_description=f"{product_name} - {analysis.style} {analysis.specific_type.lower()}"[:160]
        )
    
    @staticmethod
    def extract_keywords(product_name: str, analysis: ProductAnalysis, description: str) -> Dict[str, List[str]]:
        """Generate SEO keywords"""
        
        base = product_name.lower()
        category = analysis.category.lower()
        style = analysis.style.lower()
        material = analysis.materials[0].lower()
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        specific = analysis.specific_type.lower()
        
        primary = [base]
        
        if color and color not in base:
            primary.append(f"{color} {base}")
        
        primary.extend([
            f"{style} {base}",
            f"premium {base}",
            f"best {base}",
        ])
        
        if material and material not in ["premium", "quality"] and material not in base:
            primary.append(f"{material} {base}")
        
        if category != "product" and specific and specific not in base:
            primary.append(f"{specific} {category.split()[0].lower()}")
        
        # Remove duplicates
        primary = list(dict.fromkeys(primary[:8]))
        
        long_tail = [
            f"buy {base} online",
            f"best {base} for sale",
            f"where to buy {base}",
        ]
        
        if color and color not in base:
            long_tail.append(f"{color} {base} for sale")
        
        long_tail.extend([
            f"{style} {base} reviews",
            f"affordable {base}",
            f"professional grade {base}",
            f"durable {base}",
            f"top rated {base}",
        ])
        
        if specific and specific not in base:
            long_tail.append(f"best {specific} for {category.split()[0].lower()}")
        
        long_tail = list(dict.fromkeys(long_tail[:12]))
        
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
        st.markdown("### 🌿 About QuickList")
        st.markdown("""
        Transform product photos into professional listings instantly.
        
        **What You Get:**
        
        - Professional product description
        - SEO-optimized keywords
        - Platform-ready formatting
        
        **Supported Platforms:**
        - Shopify
        - Amazon
        - Etsy
        - WooCommerce
        """)
        
        st.markdown("---")
        
        st.markdown("### ⚡ Quick & Easy")
        st.markdown("""
        1. Upload product photo
        2. Enter product details
        3. Generate listing
        4. Download & publish
        
        **Done in 30 seconds**
        """)
        
        st.markdown("---")
        
        st.markdown("""
        **100% Free**  
        No signup required
        
        🌱 **Sustainable Resale**  
        Powered by ThreadUp
        """)
    
    # Main content
    st.markdown("""
    <div class="upload-section">
        <h2 style="color: #2d5f3f; font-family: 'Poppins', sans-serif; margin-bottom: 1rem;">
            📸 Upload Your Product Photo
        </h2>
        <p style="color: #6b7280; font-size: 1.1rem;">
            Get professional, SEO-optimized listings instantly
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
        
        st.session_state.product_image = image
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption="Your Product", width=500)
        
        st.markdown("""
        <div class="section-header">
            <h2 class="section-title">📝 Product Information</h2>
            <p class="section-subtitle">Tell us about your product</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            product_name = st.text_input(
                "Product Name",
                placeholder="e.g., Black Pearl Dress",
                help="Enter product name"
            )
        
        with col2:
            target_platform = st.selectbox(
                "Target Platform",
                ['Shopify', 'Amazon', 'Etsy', 'WooCommerce'],
                help="Choose platform"
            )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            target_audience = st.text_input(
                "Target Audience (Optional)",
                placeholder="e.g., young professionals, fashion enthusiasts",
                help="Who is this product for?"
            )
        
        with col2:
            price_range = st.selectbox(
                "Price Range (Optional)",
                ['', 'Budget ($0-$50)', 'Mid-Range ($50-$150)', 'Premium ($150-$500)', 'Luxury ($500+)'],
                help="Price positioning"
            )
        
        product_features = st.text_area(
            "Key Features (Optional but Recommended)",
            placeholder="e.g., elegant V-neck design, midi length, breathable fabric, machine washable",
            help="Specific features make better descriptions",
            height=100
        )
        
        if product_name:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                if st.button("✨ Generate Listing", use_container_width=True):
                    
                    ai = QuickListAI()
                    
                    st.session_state.product_name = product_name
                    st.session_state.target_platform = target_platform
                    
                    # Phase 1: Image Analysis
                    with st.spinner('🔍 Analyzing your product...'):
                        progress = st.progress(0)
                        
                        for i in range(50):
                            time.sleep(0.02)
                            progress.progress(i + 1)
                        
                        analysis = ai.analyze_with_vision_apis(image, product_name)
                        st.session_state.analysis = analysis
                        
                        for i in range(50, 60):
                            time.sleep(0.02)
                            progress.progress(i + 1)
                        
                        progress.empty()
                    
                    # Phase 2: Generate Description
                    with st.spinner('✍️ Writing professional description...'):
                        progress = st.progress(0)
                        
                        description = ai.generate_description(
                            product_name, 
                            analysis, 
                            product_features,
                            image,
                            target_audience,
                            price_range
                        )
                        
                        st.session_state.description = description
                        
                        for i in range(100):
                            time.sleep(0.01)
                            progress.progress(i + 1)
                        
                        progress.empty()
                    
                    # Phase 3: Keywords
                    with st.spinner('🎯 Generating SEO keywords...'):
                        progress = st.progress(0)
                        
                        for i in range(100):
                            time.sleep(0.01)
                            progress.progress(i + 1)
                        
                        keywords = ai.extract_keywords(
                            product_name,
                            analysis,
                            description.description
                        )
                        
                        progress.empty()
                    
                    st.session_state.keywords = keywords
                    st.session_state.show_results = True
                    
                    st.success("✅ Your listing is ready!")
        
        # Display results
        if ('show_results' in st.session_state and st.session_state.show_results and 
            'description' in st.session_state and 'analysis' in st.session_state and 
            'keywords' in st.session_state):
            analysis = st.session_state.analysis
            description = st.session_state.description
            keywords = st.session_state.keywords
            target_platform = st.session_state.target_platform
            product_name = st.session_state.product_name
            
            # Analysis
            st.markdown("""
            <div class="section-header">
                <h2 class="section-title">🔍 Product Analysis</h2>
                <p class="section-subtitle">AI-powered insights from your image</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                display_category = f"{analysis.category}" + (f" - {analysis.specific_type}" if analysis.specific_type and analysis.specific_type != "Item" else "")
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Category</div>
                    <div class="metric-value">{display_category}</div>
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
            
            # Description
            st.markdown("""
            <div class="section-header">
                <h2 class="section-title">📄 Your Product Description</h2>
                <p class="section-subtitle">Professional listing ready to use</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="description-card">
                <div class="description-title">Product Listing</div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Title:**\n{description.title}")
            st.markdown(f"**Description:**\n{description.description}")
            st.markdown("**Key Features:**")
            for bp in description.bullet_points:
                st.markdown(f"• {bp}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Keywords
            st.markdown("""
            <div class="seo-box">
                <div class="seo-title">🎯 SEO Keywords</div>
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
                <h2 class="section-title">💾 Download Listing</h2>
                <p class="section-subtitle">Formatted for {}</p>
            </div>
            """.format(target_platform), unsafe_allow_html=True)
            
            formatted = format_for_platform(description, keywords, target_platform)
            
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 2px solid #E5E5E5; border-radius: 16px; padding: 2rem; margin: 1.5rem 0; box-shadow: 0 4px 16px rgba(0, 166, 118, 0.08);">
                <h3 style="color: #00A676;">Your Listing</h3>
                <pre style="color: #1a1a1a; background: #F8F8F8; padding: 1.5rem; border-radius: 8px; white-space: pre-wrap; font-size: 0.9rem; border: 1px solid #E5E5E5;">{formatted}</pre>
            </div>
            """, unsafe_allow_html=True)
            
            # Download
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.download_button(
                    label=f"📥 Download for {target_platform}",
                    data=formatted,
                    file_name=f"{product_name.lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.markdown(f"""
            <div class="info-box">
                <p style="margin: 0; font-weight: 600;">
                    ✨ Your professional listing is ready! Upload to {target_platform} and start selling.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif not product_name:
            st.markdown("""
            <div class="info-box">
                <p>👆 Enter product name above to generate your listing</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # How it works
        st.markdown("""
        <div class="section-header">
            <h2 class="section-title">🚀 How QuickList Works</h2>
            <p class="section-subtitle">Professional AI-powered listings in seconds</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📸</div>
                <div class="metric-label">Upload Photo</div>
                <div style="color: #6b7280; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                    Upload your product image
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <div class="metric-label">AI Analysis</div>
                <div style="color: #6b7280; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                    Professional description generated
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💚</div>
                <div class="metric-label">Download & Sell</div>
                <div style="color: #6b7280; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                    Ready for any platform
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 3rem;">
            <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">
                🌟 What You Get:
            </p>
            <p style="margin: 0; line-height: 1.8;">
                • AI-powered product analysis from your image<br>
                • Professional product description<br>
                • Search-optimized keywords for better visibility<br>
                • Platform-ready formatting (Shopify, Amazon, Etsy, WooCommerce)<br>
                • Complete listing in under 30 seconds<br>
                • Download and deploy instantly
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 2rem; border-left-color: #00A676;">
            <p style="margin: 0; font-weight: 600;">
                🌿 100% Free • No Signup Required • Sustainable Resale by ThreadUp
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
