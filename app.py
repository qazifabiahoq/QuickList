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
    page_title="QuickList - thredUP Product Tagging",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Premium Fashion Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #C8E6C9;
        --secondary: #C8E6C9;
        --accent: #D4EDE0;
        --cream: #FAF8F3;
        --ivory: #FFFEF9;
        --charcoal: #1A1A1A;
        --sage: #B8C5B4;
        --gold: #D4AF37;
    }
    
    /* Remove default padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    .stApp {
        background: linear-gradient(180deg, var(--ivory) 0%, var(--cream) 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: var(--charcoal) !important;
    }
    
    body, p, div, span, label {
        font-family: 'Inter', sans-serif;
        color: var(--charcoal) !important;
    }
    
    /* Premium Hero Section */
    .hero-container {
        position: relative;
        margin: -1rem -5rem 3rem -5rem;
        height: 50vh;
        overflow: hidden;
        border-radius: 0 0 48px 48px;
        box-shadow: 0 20px 60px rgba(45, 95, 63, 0.15);
    }
    
    .hero-image {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: right center;
        filter: brightness(1.05);
        opacity: 0.75;
    }
    
    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            rgba(250, 248, 243, 0.95) 0%,
            rgba(250, 248, 243, 0.85) 50%,
            rgba(250, 248, 243, 0.3) 100%
        );
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 4rem 2rem;
    }
    
    .brand-logo {
        font-family: 'Playfair Display', serif;
        font-size: 7rem;
        font-weight: 900;
        color: #1A1A1A !important;
        letter-spacing: 0.15em;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        line-height: 1.1;
    }
    
    .brand-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #1A1A1A !important;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    
    .hero-tagline {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: var(--charcoal) !important;
        font-weight: 500;
        margin-bottom: 1.5rem;
        font-style: italic;
        max-width: 700px;
        text-align: center;
    }
    
    .hero-description {
        font-size: 1.15rem;
        color: #666 !important;
        max-width: 600px;
        line-height: 1.7;
        margin-bottom: 2.5rem;
        text-align: center;
    }
    
    .eco-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        background: #C8E6C9;
        border: 2px solid #C8E6C9;
        padding: 1rem 2rem;
        border-radius: 50px;
        color: #1A1A1A !important;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.05em;
    }
    
    /* Photo Showcase Cards */
    .photo-showcase {
        display: flex;
        gap: 2rem;
        justify-content: center;
        margin: 4rem auto;
        max-width: 1200px;
        padding: 0 2rem;
    }
    
    .photo-card {
        flex: 1;
        max-width: 350px;
        background: white;
        border: 3px solid #C8E6C9;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(45, 95, 63, 0.1);
        transition: all 0.3s ease;
    }
    
    .photo-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(45, 95, 63, 0.2);
        border-color: #B8C5B4;
    }
    
    .photo-card img {
        width: 100%;
        height: 400px;
        object-fit: cover;
        display: block;
    }
    
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--ivory) 0%, var(--cream) 100%);
        border-right: 1px solid rgba(45, 95, 63, 0.1);
    }
    
    [data-testid="stSidebar"] h3 {
        color: #1A1A1A !important;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--secondary);
        padding-bottom: 0.5rem;
    }
    
    /* Upload Section */
    .upload-zone {
        background: white;
        border: 3px dashed var(--secondary);
        border-radius: 32px;
        padding: 4rem 3rem;
        text-align: center;
        margin: 3rem 0;
        transition: all 0.4s ease;
        box-shadow: 0 10px 40px rgba(45, 95, 63, 0.08);
    }
    
    .upload-zone:hover {
        border-color: var(--primary);
        box-shadow: 0 15px 50px rgba(45, 95, 63, 0.15);
        transform: translateY(-4px);
    }
    
    .upload-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: #1A1A1A !important;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .upload-subtitle {
        font-size: 1.1rem;
        color: #666 !important;
        margin-bottom: 2rem;
    }
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] {
        background: white !important;
        border: 3px dashed var(--secondary) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] > div {
        background: white !important;
        border: none !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #1A1A1A !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: white !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        background: white !important;
    }
    
    [data-testid="stFileUploader"] div {
        background: white !important;
        color: var(--charcoal) !important;
    }
    
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small {
        color: var(--charcoal) !important;
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: #C8E6C9 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: #D4EDE0 !important;
        color: white !important;
    }
    
    /* Primary Button */
    .stButton > button {
        background: #C8E6C9 !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1.5rem 4rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(200, 230, 201, 0.25) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        background: #D4EDE0 !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(200, 230, 201, 0.30) !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: white !important;
        color: #C8E6C9 !important;
        border: 2px solid #C8E6C9 !important;
        border-radius: 16px !important;
        padding: 1.25rem 3rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: #C8E6C9 !important;
        color: white !important;
        transform: translateY(-2px);
    }
    
    /* Section Headers */
    .section-divider {
        margin: 4rem 0 2.5rem 0;
        text-align: center;
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        color: #1A1A1A !important;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .section-subtitle {
        font-size: 1.15rem;
        color: #666 !important;
        font-style: italic;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border: 1px solid rgba(45, 95, 63, 0.1);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        transition: all 0.4s ease;
        height: 100%;
        min-height: 180px;
        box-shadow: 0 5px 20px rgba(45, 95, 63, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .metric-card:hover {
        border-color: var(--secondary);
        box-shadow: 0 12px 40px rgba(108, 191, 0, 0.15);
        transform: translateY(-6px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #888 !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: #1A1A1A !important;
        font-weight: 700;
        line-height: 1.4;
        word-wrap: break-word;
        overflow-wrap: break-word;
        hyphens: auto;
        max-width: 100%;
        padding: 0 0.5rem;
    }
    
    /* Description Card */
    .content-card {
        background: white;
        border-left: 5px solid var(--secondary);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 8px 30px rgba(45, 95, 63, 0.08);
        transition: all 0.3s ease;
        min-height: 240px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .content-card:hover {
        box-shadow: 0 12px 40px rgba(45, 95, 63, 0.12);
        transform: translateY(-3px);
    }
    
    .content-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: #1A1A1A !important;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    /* SEO Box */
    .seo-container {
        background: #C8E6C9;
        border-radius: 24px;
        padding: 3rem;
        margin: 2.5rem 0;
        box-shadow: 0 8px 30px rgba(45, 95, 63, 0.08);
    }
    
    .seo-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        color: #1A1A1A !important;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    .keyword-badge {
        display: inline-block;
        background: white;
        color: #1A1A1A !important;
        border: 2px solid var(--secondary);
        padding: 0.6rem 1.3rem;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.4rem;
        transition: all 0.3s ease;
    }
    
    .keyword-badge:hover {
        background: var(--secondary);
        color: white !important;
        transform: scale(1.05);
    }
    
    /* Image Styling */
    [data-testid="stImage"] {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 35px rgba(45, 95, 63, 0.15);
    }
    
    /* Input Fields */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
        color: #1A1A1A !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput input,
    .stTextArea textarea {
        background: white !important;
        border: 2px solid rgba(45, 95, 63, 0.15) !important;
        border-radius: 12px !important;
        color: var(--charcoal) !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--secondary) !important;
        box-shadow: 0 0 0 3px rgba(108, 191, 0, 0.1) !important;
    }
    
    /* Review Panel */
    .review-panel {
        background: linear-gradient(135deg, #F0F7F3 0%, #E8F5ED 100%);
        border: 3px solid #C8E6C9;
        border-radius: 24px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background: white !important;
        border: 2px solid rgba(45, 95, 63, 0.15) !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: var(--secondary) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background: white !important;
        color: var(--charcoal) !important;
    }
    
    .stSelectbox [data-baseweb="select"] span {
        color: var(--charcoal) !important;
    }
    
    .stSelectbox [data-baseweb="select"] svg {
        color: var(--charcoal) !important;
    }
    
    [data-baseweb="menu"] {
        background: white !important;
        border: 1px solid rgba(45, 95, 63, 0.15) !important;
        box-shadow: 0 4px 16px rgba(45, 95, 63, 0.1) !important;
        border-radius: 8px !important;
    }
    
    [data-baseweb="menu"] ul {
        background: white !important;
    }
    
    [data-baseweb="menu"] li {
        background: white !important;
        color: var(--charcoal) !important;
        padding: 0.75rem 1rem !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: #f0f7f3 !important;
        color: var(--primary) !important;
    }
    
    /* Info Box */
    .info-banner {
        background: linear-gradient(135deg, #F0F7F3 0%, #E8F5ED 100%);
        border-left: 4px solid var(--secondary);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin: 2rem 0;
    }
    
    .info-banner p {
        margin: 0;
        line-height: 1.7;
        color: var(--charcoal) !important;
    }
    
    /* Feature Grid */
    .feature-step {
        text-align: center;
        padding: 2rem;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    
    .step-number {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        color: #1A1A1A !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .step-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1A1A1A !important;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .step-description {
        color: #1A1A1A !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: #C8E6C9;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-container {
            height: 45vh;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 32px 32px;
        }
        
        .hero-content {
            padding: 2rem 1.5rem;
        }
        
        .brand-logo {
            font-size: 3.5rem;
        }
        
        .hero-tagline {
            font-size: 1.5rem;
        }
        
        .photo-showcase {
            flex-direction: column;
            gap: 1.5rem;
            padding: 0 1rem;
            margin: 2rem auto;
        }
        
        .photo-card {
            max-width: 100%;
        }
        
        .photo-card img {
            height: 350px;
        }
        
        .metric-card {
            padding: 2rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section with Premium Fashion Image
st.markdown("""
<div class="hero-container">
    <div class="hero-overlay" style="background: linear-gradient(180deg, rgba(250, 248, 243, 0.98) 0%, rgba(250, 248, 243, 0.95) 100%);"></div>
    <div class="hero-content">
        <div class="brand-logo">THREDUP</div>
        <div class="brand-subtitle">QuickList</div>
        <div class="hero-tagline">Where Fashion Meets Sustainability</div>
        <div class="hero-description">
            AI-powered product listing generation
        </div>
    </div>
</div>

<div class="photo-showcase">
    <div class="photo-card">
        <img src="https://images.pexels.com/photos/925402/pexels-photo-925402.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Fashion showcase">
    </div>
    <div class="photo-card">
        <img src="https://images.pexels.com/photos/18108804/pexels-photo-18108804.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Fashion showcase">
    </div>
    <div class="photo-card">
        <img src="https://images.pexels.com/photos/32007386/pexels-photo-32007386.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Fashion showcase">
    </div>
</div>
""", unsafe_allow_html=True)


# Data classes (UNCHANGED)
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
        """Parse Google Vision labels with comprehensive fashion detection"""
        all_tags = ' '.join(labels + objects).lower()
        prod_lower = product_name.lower()
        combined = all_tags + ' ' + prod_lower
        
        # COMPREHENSIVE CLOTHING DETECTION - Check specific items FIRST
        
        # TOPS
        if any(term in combined for term in [
            'blouse', 'shirt', 'top', 'tee', 't-shirt', 'tank', 'cami', 'camisole',
            'crop top', 'tube top', 'halter', 'bodysuit', 'bustier', 'corset',
            'tunic', 'henley', 'polo', 'button-up', 'peplum'
        ]):
            return "Apparel & Fashion", "Top"
        
        # DRESSES
        elif any(term in combined for term in [
            'dress', 'gown', 'frock', 'maxi', 'midi', 'mini', 'sundress',
            'wrap dress', 'bodycon', 'shift', 'a-line', 'sheath', 'cocktail'
        ]):
            return "Apparel & Fashion", "Dress"
        
        # SKIRTS
        elif any(term in combined for term in [
            'skirt', 'mini skirt', 'midi skirt', 'maxi skirt', 'pencil skirt',
            'pleated skirt', 'tennis skirt', 'skort'
        ]):
            return "Apparel & Fashion", "Skirt"
        
        # PANTS
        elif any(term in combined for term in [
            'pants', 'jeans', 'trousers', 'slacks', 'chinos', 'leggings',
            'joggers', 'sweatpants', 'cargo', 'palazzo', 'culottes', 'wide leg',
            'skinny', 'mom jeans', 'boyfriend jeans'
        ]):
            return "Apparel & Fashion", "Pants"
        
        # SHORTS
        elif any(term in combined for term in [
            'shorts', 'bermuda', 'cutoffs', 'bike shorts'
        ]):
            return "Apparel & Fashion", "Shorts"
        
        # OUTERWEAR
        elif any(term in combined for term in [
            'jacket', 'coat', 'blazer', 'cardigan', 'sweater', 'pullover',
            'hoodie', 'sweatshirt', 'bomber', 'denim jacket', 'leather jacket',
            'parka', 'puffer', 'peacoat', 'trench', 'windbreaker', 'cape',
            'vest', 'kimono', 'fleece', 'teddy coat'
        ]):
            return "Apparel & Fashion", "Jacket"
        
        # JUMPSUITS
        elif any(term in combined for term in [
            'jumpsuit', 'romper', 'playsuit', 'overall', 'coverall'
        ]):
            return "Apparel & Fashion", "Jumpsuit"
        
        # BAGS
        elif any(term in combined for term in [
            'bag', 'purse', 'handbag', 'tote', 'clutch', 'satchel', 'crossbody',
            'messenger', 'backpack', 'duffel', 'bucket bag', 'fanny pack'
        ]):
            return "Bags & Accessories", "Bag"
        
        # SHOES
        elif any(term in combined for term in [
            'shoes', 'sneakers', 'boots', 'heels', 'sandals', 'pumps', 'stilettos',
            'platforms', 'wedges', 'ankle boots', 'combat boots', 'trainers',
            'loafers', 'oxfords', 'flats', 'espadrilles', 'mules'
        ]):
            return "Footwear", "Shoes"
        
        # Generic clothing fallback
        elif any(term in combined for term in ['clothing', 'apparel', 'fashion', 'wear', 'garment']):
            return "Apparel & Fashion", "Clothing"
        
        # Default
        return "Product", "Item"
    
    @staticmethod
    def _parse_amazon_labels(labels: List[str], product_name: str) -> tuple:
        """Parse Amazon Rekognition labels"""
        return QuickListAI._parse_google_vision(labels, [], product_name)
    
    @staticmethod
    def _rgb_to_color_name(r: int, g: int, b: int) -> str:
        """Convert RGB to color name with comprehensive accuracy"""
        # Check for black/very dark
        if r < 50 and g < 50 and b < 50:
            return "black"
        
        # Check for white/off-white
        if min(r, g, b) > 200 and max(r, g, b) - min(r, g, b) < 25:
            return "white"
        
        # Check for cream/ivory (warm whites)
        if r > 220 and g > 215 and b > 200 and r > b:
            return "white"
        
        # Check for gray (RGB values close to each other)
        if max(r, g, b) - min(r, g, b) < 30 and min(r, g, b) > 50 and max(r, g, b) < 200:
            return "gray"
        
        # Calculate dominance for color detection
        values = sorted([r, g, b], reverse=True)
        dominance = values[0] - values[1]
        
        # Need at least 25 point difference for specific colors
        if dominance < 25:
            return "neutral"
        
        # RED family
        if r > g and r > b:
            if r > 180 and g < 100 and b < 100:
                return "red"
            elif r > 150 and g > 100 and b < 80:
                return "brown"
            elif r > 200 and g > 150 and b > 150:
                return "pink"
            elif r > 180 and g > 120 and b < 120:
                return "orange"
            else:
                return "pink"
        
        # GREEN family
        elif g > r and g > b:
            if g > 150 and r < 100 and b < 100:
                return "green"
            elif g > 180 and r > 150 and b < 100:
                return "yellow"
            elif g > r and b > r and abs(g - b) < 40:
                return "teal"
            else:
                return "green"
        
        # BLUE family
        elif b > r and b > g:
            if b > 180 and r < 100 and g < 100:
                return "blue"
            elif b > 150 and r > 100 and g < b - 30:
                return "purple"
            elif b > 200 and g > 180:
                return "light blue"
            else:
                return "blue"
        
        # YELLOW/ORANGE
        elif r > 150 and g > 150 and b < 100:
            if r > g:
                return "orange"
            else:
                return "yellow"
        
        # Fallback
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
        """Comprehensive material and style detection from labels"""
        materials = ["Quality", "Fabric"]
        style = "Classic"
        
        all_labels = ' '.join(labels).lower()
        
        # COMPREHENSIVE MATERIAL DETECTION
        if any(mat in all_labels for mat in ['silk', 'satin', 'charmeuse']):
            materials = ["Silk", "Luxurious"]
        elif any(mat in all_labels for mat in ['cotton', 'organic']):
            materials = ["Cotton", "Breathable"]
        elif any(mat in all_labels for mat in ['linen', 'flax']):
            materials = ["Linen", "Natural"]
        elif any(mat in all_labels for mat in ['wool', 'cashmere', 'merino']):
            materials = ["Wool", "Warm"]
        elif any(mat in all_labels for mat in ['leather', 'suede', 'nubuck']):
            materials = ["Leather", "Premium"]
        elif any(mat in all_labels for mat in ['denim', 'chambray']):
            materials = ["Denim", "Durable"]
        elif any(mat in all_labels for mat in ['velvet', 'velour', 'plush']):
            materials = ["Velvet", "Plush"]
        elif any(mat in all_labels for mat in ['chiffon', 'georgette', 'sheer']):
            materials = ["Chiffon", "Lightweight"]
        elif any(mat in all_labels for mat in ['knit', 'sweater', 'cable']):
            materials = ["Knit", "Cozy"]
        elif any(mat in all_labels for mat in ['polyester', 'poly']):
            materials = ["Polyester", "Wrinkle-resistant"]
        elif any(mat in all_labels for mat in ['stretch', 'spandex', 'lycra']):
            materials = ["Stretch", "Comfortable"]
        elif any(mat in all_labels for mat in ['sequin', 'glitter', 'sparkle']):
            materials = ["Sequin", "Sparkling"]
        elif any(mat in all_labels for mat in ['lace', 'crochet', 'eyelet']):
            materials = ["Lace", "Delicate"]
        elif any(mat in all_labels for mat in ['mesh', 'net', 'tulle']):
            materials = ["Mesh", "Sheer"]
        elif any(mat in all_labels for mat in ['fleece', 'sherpa', 'teddy']):
            materials = ["Fleece", "Warm"]
        elif category == "Apparel & Fashion":
            materials = ["Fabric", "Quality Material"]
        
        # COMPREHENSIVE STYLE DETECTION
        if any(s in all_labels for s in ['elegant', 'formal', 'evening', 'sophisticated', 'luxury', 'cocktail']):
            style = "Elegant"
        elif any(s in all_labels for s in ['casual', 'everyday', 'comfortable', 'relaxed']):
            style = "Casual"
        elif any(s in all_labels for s in ['vintage', 'retro', 'classic', 'antique', 'throwback']):
            style = "Vintage"
        elif any(s in all_labels for s in ['modern', 'contemporary', 'trendy', 'fashion-forward', 'chic']):
            style = "Modern"
        elif any(s in all_labels for s in ['boho', 'bohemian', 'hippie', 'festival', 'free spirit']):
            style = "Boho"
        elif any(s in all_labels for s in ['romantic', 'feminine', 'delicate', 'soft', 'dreamy']):
            style = "Romantic"
        elif any(s in all_labels for s in ['edgy', 'bold', 'statement', 'punk', 'grunge']):
            style = "Edgy"
        elif any(s in all_labels for s in ['preppy', 'classic', 'collegiate', 'ivy league']):
            style = "Preppy"
        elif any(s in all_labels for s in ['athletic', 'sporty', 'activewear', 'performance']):
            style = "Athletic"
        elif any(s in all_labels for s in ['minimalist', 'minimal', 'simple', 'clean']):
            style = "Minimalist"
        elif any(s in all_labels for s in ['glamorous', 'glam', 'sparkle', 'luxe']):
            style = "Glamorous"
        
        return materials, style
    
    @staticmethod
    def _analyze_with_clip(image: Image.Image, product_name: str) -> ProductAnalysis:
        """Fallback CLIP analysis with comprehensive fashion detection"""
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            headers = {"Content-Type": "application/octet-stream"}
            API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
            
            prod_lower = product_name.lower()
            
            # COMPREHENSIVE GARMENT DETECTION
            category = "Apparel & Fashion"
            specific_type = "Clothing"
            
            if prod_lower:
                # TOPS
                if any(term in prod_lower for term in [
                    'blouse', 'shirt', 'top', 'tee', 't-shirt', 'tank', 'cami', 'camisole', 
                    'crop top', 'tube top', 'halter', 'bodysuit', 'bustier', 'corset',
                    'tunic', 'henley', 'polo', 'button-up', 'button-down', 'peplum'
                ]):
                    specific_type = "Top"
                
                # DRESSES
                elif any(term in prod_lower for term in [
                    'dress', 'gown', 'frock', 'maxi', 'midi', 'mini', 'slip dress',
                    'sundress', 'shift dress', 'wrap dress', 'bodycon', 'fit and flare',
                    'a-line', 'sheath', 'smock dress', 'pinafore', 'kaftan', 'muumuu',
                    'ball gown', 'cocktail dress', 'evening gown', 'tea dress'
                ]):
                    specific_type = "Dress"
                
                # BOTTOMS
                elif any(term in prod_lower for term in [
                    'pants', 'jeans', 'trousers', 'slacks', 'chinos', 'khakis',
                    'leggings', 'joggers', 'sweatpants', 'cargo pants', 'palazzo',
                    'culottes', 'capris', 'wide leg', 'straight leg', 'skinny',
                    'flare', 'bootcut', 'boyfriend jeans', 'mom jeans', 'baggy',
                    'skirt', 'mini skirt', 'midi skirt', 'maxi skirt', 'pencil skirt',
                    'pleated skirt', 'circle skirt', 'tennis skirt', 'skort', 'sarong',
                    'shorts', 'bermuda', 'cutoffs', 'hot pants', 'bike shorts'
                ]):
                    if 'skirt' in prod_lower or 'skort' in prod_lower or 'sarong' in prod_lower:
                        specific_type = "Skirt"
                    elif 'short' in prod_lower:
                        specific_type = "Shorts"
                    else:
                        specific_type = "Pants"
                
                # OUTERWEAR
                elif any(term in prod_lower for term in [
                    'jacket', 'coat', 'blazer', 'cardigan', 'sweater', 'pullover',
                    'hoodie', 'sweatshirt', 'bomber', 'denim jacket', 'jean jacket',
                    'leather jacket', 'moto jacket', 'parka', 'puffer', 'peacoat',
                    'trench', 'raincoat', 'windbreaker', 'anorak', 'cape', 'poncho',
                    'shrug', 'bolero', 'vest', 'gilet', 'kimono', 'duster',
                    'overcoat', 'topcoat', 'car coat', 'barn jacket', 'varsity jacket',
                    'track jacket', 'fleece', 'teddy coat', 'shearling', 'fur coat'
                ]):
                    specific_type = "Jacket"
                
                # JUMPSUITS & ROMPERS
                elif any(term in prod_lower for term in [
                    'jumpsuit', 'romper', 'playsuit', 'overall', 'coverall', 'onesie'
                ]):
                    specific_type = "Jumpsuit"
                
                # BAGS
                elif any(term in prod_lower for term in [
                    'bag', 'purse', 'handbag', 'tote', 'clutch', 'satchel', 'hobo',
                    'crossbody', 'messenger', 'shoulder bag', 'backpack', 'rucksack',
                    'duffel', 'weekender', 'bucket bag', 'saddle bag', 'baguette',
                    'pouch', 'wristlet', 'wallet', 'coin purse', 'fanny pack', 'belt bag'
                ]):
                    category = "Bags & Accessories"
                    specific_type = "Bag"
                
                # SHOES
                elif any(term in prod_lower for term in [
                    'shoes', 'heels', 'pumps', 'stilettos', 'platforms', 'wedges',
                    'boots', 'ankle boots', 'knee boots', 'combat boots', 'chelsea boots',
                    'sneakers', 'trainers', 'athletic shoes', 'running shoes',
                    'sandals', 'slides', 'flip flops', 'thongs', 'mules', 'clogs',
                    'loafers', 'oxfords', 'brogues', 'flats', 'ballet flats',
                    'espadrilles', 'mary janes', 'slingbacks', 'kitten heels'
                ]):
                    category = "Footwear"
                    specific_type = "Shoes"
            
            # Detect category using CLIP
            categories = [
                "blouse shirt top camisole tank", "dress gown maxi midi", "pants jeans trousers leggings", 
                "skirt mini midi pleated", "jacket coat blazer cardigan sweater", "jumpsuit romper overall",
                "bag purse handbag tote clutch", "shoes heels boots sneakers sandals",
                "shorts bermuda cutoffs", "hoodie sweatshirt pullover"
            ]
            
            response = requests.post(
                API_URL,
                headers=headers,
                data=img_bytes,
                params={"candidate_labels": ",".join(categories)},
                timeout=20
            )
            
            # Only override user input if CLIP is very confident AND user didn't specify
            if response.status_code == 200 and not prod_lower:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    detected = result[0].get('label', '').lower()
                    
                    if "shirt" in detected or "top" in detected or "blouse" in detected or "camisole" in detected or "tank" in detected:
                        specific_type = "Top"
                    elif "jacket" in detected or "coat" in detected or "blazer" in detected or "sweater" in detected or "cardigan" in detected:
                        specific_type = "Jacket"
                    elif "hoodie" in detected or "sweatshirt" in detected or "pullover" in detected:
                        specific_type = "Sweater"
                    elif "dress" in detected or "gown" in detected:
                        specific_type = "Dress"
                    elif "skirt" in detected:
                        specific_type = "Skirt"
                    elif "pants" in detected or "jeans" in detected or "trousers" in detected or "leggings" in detected:
                        specific_type = "Pants"
                    elif "shorts" in detected:
                        specific_type = "Shorts"
                    elif "jumpsuit" in detected or "romper" in detected or "overall" in detected:
                        specific_type = "Jumpsuit"
                    elif "bag" in detected or "purse" in detected or "handbag" in detected or "tote" in detected or "clutch" in detected:
                        category, specific_type = "Bags & Accessories", "Bag"
                    elif "shoes" in detected or "heels" in detected or "boots" in detected or "sneakers" in detected or "sandals" in detected:
                        category, specific_type = "Footwear", "Shoes"
            
            # Get color - check product name first for color keywords
            dominant_color = QuickListAI._extract_dominant_color(image)
            
            # COMPREHENSIVE COLOR DETECTION from product name
            color_keywords = {
                'black': ['black', 'noir', 'ebony', 'jet', 'onyx'],
                'white': ['white', 'ivory', 'cream', 'off-white', 'ecru', 'pearl', 'snow'],
                'gray': ['gray', 'grey', 'charcoal', 'slate', 'ash', 'silver', 'dove'],
                'red': ['red', 'crimson', 'scarlet', 'ruby', 'burgundy', 'wine', 'maroon', 'cherry'],
                'pink': ['pink', 'rose', 'blush', 'coral', 'salmon', 'fuchsia', 'magenta', 'hot pink'],
                'orange': ['orange', 'tangerine', 'peach', 'apricot', 'rust', 'terracotta'],
                'yellow': ['yellow', 'gold', 'mustard', 'canary', 'lemon', 'butter', 'saffron'],
                'green': ['green', 'olive', 'sage', 'mint', 'emerald', 'forest', 'lime', 'jade', 'teal'],
                'blue': ['blue', 'navy', 'cobalt', 'royal', 'sky', 'azure', 'turquoise', 'cerulean', 'sapphire', 'indigo'],
                'purple': ['purple', 'violet', 'lavender', 'lilac', 'plum', 'mauve', 'orchid', 'amethyst'],
                'brown': ['brown', 'tan', 'beige', 'camel', 'chocolate', 'mocha', 'taupe', 'khaki', 'cognac'],
                'multicolor': ['multicolor', 'rainbow', 'tie-dye', 'ombre', 'color block', 'print', 'floral', 'striped']
            }
            
            for color_name, keywords in color_keywords.items():
                if any(keyword in prod_lower for keyword in keywords):
                    dominant_color = color_name
                    break
            
            # COMPREHENSIVE STYLE & AESTHETIC DETECTION
            style = "Classic"
            style_keywords = {
                'Cottagecore': ['cottagecore', 'prairie', 'cottage', 'floral', 'romantic', 'whimsical', 'pastoral'],
                'Dark Academia': ['dark academia', 'academic', 'preppy', 'scholarly', 'vintage', 'tweed'],
                'Y2K': ['y2k', 'early 2000s', '2000s', 'low rise', 'butterfly', 'velour', 'juicy'],
                'Streetwear': ['streetwear', 'urban', 'oversized', 'graphic', 'hypebeast', 'skate'],
                'Minimalist': ['minimalist', 'minimal', 'simple', 'clean', 'monochrome', 'sleek'],
                'Boho': ['boho', 'bohemian', 'hippie', 'free spirit', 'ethnic', 'festival', 'fringe'],
                'Grunge': ['grunge', 'edgy', 'distressed', 'ripped', 'punk', 'rock', 'alternative'],
                'Preppy': ['preppy', 'classic', 'ivy league', 'nautical', 'collegiate', 'country club'],
                'Glamorous': ['glamorous', 'glam', 'sequin', 'sparkle', 'metallic', 'luxe', 'statement'],
                'Athleisure': ['athleisure', 'sporty', 'athletic', 'activewear', 'gym', 'performance'],
                'Vintage': ['vintage', 'retro', 'throwback', '70s', '80s', '90s', 'antique'],
                'Modern': ['modern', 'contemporary', 'trendy', 'fashion-forward', 'chic'],
                'Elegant': ['elegant', 'sophisticated', 'formal', 'evening', 'cocktail', 'classy'],
                'Casual': ['casual', 'everyday', 'comfortable', 'relaxed', 'effortless'],
                'Edgy': ['edgy', 'bold', 'statement', 'daring', 'unconventional'],
                'Romantic': ['romantic', 'feminine', 'delicate', 'soft', 'dreamy', 'lace'],
                'Western': ['western', 'cowboy', 'cowgirl', 'rodeo', 'ranch', 'denim'],
                'Coastal': ['coastal', 'beach', 'nautical', 'resort', 'vacation', 'summer'],
                'Goth': ['goth', 'gothic', 'dark', 'black', 'victorian', 'alternative'],
                'Mod': ['mod', 'retro', '60s', 'geometric', 'bold'],
                'Artsy': ['artsy', 'artistic', 'creative', 'avant-garde', 'unique', 'quirky']
            }
            
            for style_name, keywords in style_keywords.items():
                if any(keyword in prod_lower for keyword in keywords):
                    style = style_name
                    break
            
            # COMPREHENSIVE MATERIAL & TEXTURE DETECTION
            materials = ["Quality", "Fabric"]
            
            material_keywords = {
                ('Silk', 'Luxurious'): ['silk', 'satin', 'charmeuse'],
                ('Cotton', 'Breathable'): ['cotton', 'organic cotton', 'supima'],
                ('Linen', 'Natural'): ['linen', 'flax'],
                ('Wool', 'Warm'): ['wool', 'cashmere', 'merino', 'angora', 'mohair'],
                ('Leather', 'Premium'): ['leather', 'genuine leather', 'suede', 'nubuck'],
                ('Denim', 'Durable'): ['denim', 'chambray'],
                ('Velvet', 'Plush'): ['velvet', 'velour', 'crushed velvet'],
                ('Chiffon', 'Lightweight'): ['chiffon', 'georgette', 'organza'],
                ('Knit', 'Cozy'): ['knit', 'sweater knit', 'cable knit', 'ribbed'],
                ('Polyester', 'Wrinkle-resistant'): ['polyester', 'poly blend'],
                ('Spandex', 'Stretch'): ['spandex', 'lycra', 'elastane', 'stretch'],
                ('Rayon', 'Soft'): ['rayon', 'viscose', 'modal', 'tencel'],
                ('Sequin', 'Sparkling'): ['sequin', 'glitter', 'sparkle'],
                ('Lace', 'Delicate'): ['lace', 'crochet', 'eyelet'],
                ('Mesh', 'Sheer'): ['mesh', 'net', 'tulle'],
                ('Corduroy', 'Textured'): ['corduroy', 'cord'],
                ('Tweed', 'Sophisticated'): ['tweed', 'boucle'],
                ('Fleece', 'Warm'): ['fleece', 'sherpa', 'teddy'],
                ('Faux Fur', 'Cozy'): ['faux fur', 'fur', 'shearling', 'fuzzy']
            }
            
            for (material, descriptor), keywords in material_keywords.items():
                if any(keyword in prod_lower for keyword in keywords):
                    materials = [material, descriptor]
                    break
            
            # TEXTURE & DETAIL DETECTION (for style enhancement)
            texture_keywords = [
                'ruffled', 'ruffle', 'pleated', 'smocked', 'gathered', 'embroidered',
                'beaded', 'studded', 'distressed', 'frayed', 'raw hem', 'puff sleeve',
                'bishop sleeve', 'bell sleeve', 'off shoulder', 'one shoulder', 'halter',
                'v-neck', 'scoop neck', 'crew neck', 'turtleneck', 'cowl neck',
                'wrap', 'tie front', 'button front', 'zip front', 'asymmetric',
                'high waist', 'low rise', 'mid rise', 'cropped', 'ankle length',
                'floor length', 'backless', 'cutout', 'slit', 'tiered',
                'quilted', 'padded', 'structured', 'oversized', 'fitted', 'relaxed'
            ]
            
            # Enhance style if texture keywords found
            if any(keyword in prod_lower for keyword in texture_keywords):
                if style == "Classic":
                    style = "Detailed"
            
            return ProductAnalysis(
                category=category,
                materials=materials,
                colors=[dominant_color, "#000000"],
                style=style,
                confidence=0.82,
                specific_type=specific_type
            )
            
        except Exception as e:
            # Fallback with comprehensive detection based on product name
            prod_lower = product_name.lower()
            specific_type = "Clothing"
            category = "Apparel & Fashion"
            materials = ["Quality", "Fabric"]
            style = "Classic"
            color = "neutral"
            
            # Garment detection
            if any(term in prod_lower for term in ['blouse', 'shirt', 'top', 'tee', 'tank', 'cami']):
                specific_type = "Top"
            elif any(term in prod_lower for term in ['jacket', 'coat', 'blazer', 'sweater', 'cardigan', 'hoodie']):
                specific_type = "Jacket"
            elif any(term in prod_lower for term in ['dress', 'gown', 'maxi', 'midi']):
                specific_type = "Dress"
            elif any(term in prod_lower for term in ['pants', 'jeans', 'leggings', 'trousers']):
                specific_type = "Pants"
            elif any(term in prod_lower for term in ['skirt']):
                specific_type = "Skirt"
            elif any(term in prod_lower for term in ['shorts']):
                specific_type = "Shorts"
            elif any(term in prod_lower for term in ['bag', 'purse', 'tote', 'clutch']):
                category, specific_type = "Bags & Accessories", "Bag"
            elif any(term in prod_lower for term in ['shoes', 'heels', 'boots', 'sneakers']):
                category, specific_type = "Footwear", "Shoes"
            
            # Color detection
            if any(c in prod_lower for c in ['black', 'noir']):
                color = "black"
            elif any(c in prod_lower for c in ['white', 'ivory', 'cream']):
                color = "white"
            elif any(c in prod_lower for c in ['gray', 'grey', 'silver']):
                color = "gray"
            elif any(c in prod_lower for c in ['red', 'burgundy', 'wine']):
                color = "red"
            elif any(c in prod_lower for c in ['blue', 'navy', 'cobalt']):
                color = "blue"
            
            # Material detection
            if any(m in prod_lower for m in ['silk', 'satin']):
                materials = ["Silk", "Luxurious"]
            elif any(m in prod_lower for m in ['cotton']):
                materials = ["Cotton", "Breathable"]
            elif any(m in prod_lower for m in ['leather', 'suede']):
                materials = ["Leather", "Premium"]
            elif any(m in prod_lower for m in ['denim']):
                materials = ["Denim", "Durable"]
            
            return ProductAnalysis(
                category=category,
                materials=materials,
                colors=[color, '#000000'],
                style=style,
                confidence=0.65,
                specific_type=specific_type
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
                            target_audience: str = "", price: str = "") -> ProductDescription:
        """Generate ONE professional description using multi-AI fallback"""
        
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        
        # Build context with STRICT instructions
        context = f"""Product: {product_name}
Category: {analysis.category}
Type: {analysis.specific_type}
DETECTED COLOR: {color if color else 'NOT SPECIFIED'}
Style: {analysis.style}
Materials: {', '.join(analysis.materials)}
Features: {features if features else 'Premium quality'}"""
        
        if target_audience:
            context += f"\nTarget Audience: {target_audience}"
        if price:
            context += f"\nPrice: {price}"
        
        # STRICT VALIDATION: Build list of FORBIDDEN colors (all colors except detected one)
        all_colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'white', 'black', 'gray', 'grey', 'beige', 'navy', 'maroon', 'burgundy', 'crimson', 'scarlet']
        forbidden_colors = [c for c in all_colors if c != color.lower()] if color else []
        
        # Create EXTREMELY strict prompt
        prompt = f"""Write a professional e-commerce product description for this {analysis.specific_type.lower()}.

{context}

CRITICAL RULES - FOLLOW EXACTLY:
1. COLOR: {"Use ONLY '" + color + "' as the color. DO NOT mention: " + ", ".join(forbidden_colors) if color else "Do NOT mention any specific color"}
2. MATERIALS: Use ONLY these materials: {', '.join(analysis.materials)}
3. STYLE: Use ONLY this style: {analysis.style}
4. Write 150-200 words that balance emotional appeal with practical benefits
5. DO NOT use em dashes (—) - use regular hyphens (-) or periods instead
6. {"Consider the price point of " + price + " in your tone" if price else ""}

DO NOT invent colors, materials, or attributes not listed above.

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
                
                # VALIDATION: Check for forbidden colors in output
                generated_text = (parsed.get('title', '') + ' ' + parsed.get('description', '')).lower()
                if color and any(forbidden in generated_text for forbidden in forbidden_colors):
                    # Color hallucination detected - use fallback
                    print(f"⚠️ COLOR HALLUCINATION DETECTED! Generated text contains forbidden colors.")
                    raise ValueError("Color validation failed")
                
                return ProductDescription(
                    title=parsed.get('title', product_name),
                    description=parsed.get('description', ''),
                    bullet_points=parsed.get('bullet_points', [])[:5],
                    meta_description=parsed.get('meta_description', '')[:160]
                )
            except Exception as e:
                print(f"Groq failed: {e}")
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
                    
                    # VALIDATION: Check for forbidden colors
                    generated_text = (parsed.get('title', '') + ' ' + parsed.get('description', '')).lower()
                    if color and any(forbidden in generated_text for forbidden in forbidden_colors):
                        print(f"⚠️ DeepInfra COLOR HALLUCINATION DETECTED!")
                        raise ValueError("Color validation failed")
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160]
                    )
        except Exception as e:
            print(f"DeepInfra failed: {e}")
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
                    
                    # VALIDATION: Check for forbidden colors
                    generated_text = (parsed.get('title', '') + ' ' + parsed.get('description', '')).lower()
                    if color and any(forbidden in generated_text for forbidden in forbidden_colors):
                        print(f"⚠️ Together AI COLOR HALLUCINATION DETECTED!")
                        raise ValueError("Color validation failed")
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160]
                    )
        except Exception as e:
            print(f"Together AI failed: {e}")
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
                
                # VALIDATION: Check for forbidden colors
                generated_text = (parsed.get('title', '') + ' ' + parsed.get('description', '')).lower()
                if color and any(forbidden in generated_text for forbidden in forbidden_colors):
                    print(f"⚠️ Pollinations COLOR HALLUCINATION DETECTED!")
                    raise ValueError("Color validation failed")
                
                return ProductDescription(
                    title=parsed.get('title', product_name),
                    description=parsed.get('description', ''),
                    bullet_points=parsed.get('bullet_points', [])[:5],
                    meta_description=parsed.get('meta_description', '')[:160]
                )
        except Exception as e:
            print(f"Pollinations failed: {e}")
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
                    
                    # VALIDATION: Check for forbidden colors
                    generated_text = (parsed.get('title', '') + ' ' + parsed.get('description', '')).lower()
                    if color and any(forbidden in generated_text for forbidden in forbidden_colors):
                        print(f"⚠️ Qwen COLOR HALLUCINATION DETECTED!")
                        raise ValueError("Color validation failed")
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160]
                    )
        except Exception as e:
            print(f"Qwen failed: {e}")
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
                    
                    # VALIDATION: Check for forbidden colors
                    generated_text = (parsed.get('title', '') + ' ' + parsed.get('description', '')).lower()
                    if color and any(forbidden in generated_text for forbidden in forbidden_colors):
                        print(f"⚠️ Mistral COLOR HALLUCINATION DETECTED!")
                        raise ValueError("Color validation failed")
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160]
                    )
        except Exception as e:
            print(f"Mistral failed: {e}")
            pass
        
        # FINAL FALLBACK: Simple template using ONLY detected attributes
        # Don't duplicate color if it's already in product name
        color_text = ""
        if color and color.lower() not in product_name.lower():
            color_text = f"{color} "
        
        # Build description using ONLY detected attributes
        desc_parts = []
        desc_parts.append(f"Experience exceptional quality with this {color_text}{product_name.lower()}.")
        
        if analysis.materials and analysis.materials[0] not in ["Premium", "Quality"]:
            desc_parts.append(f"Crafted from {analysis.materials[0].lower()}, this {analysis.specific_type.lower()} combines durability with comfort.")
        
        if analysis.style:
            desc_parts.append(f"Features {analysis.style.lower()} design that stands out.")
        
        if features:
            desc_parts.append(features)
        else:
            desc_parts.append("Perfect for any occasion.")
        
        final_description = " ".join(desc_parts)
        
        # Build bullet points using ONLY detected attributes
        bullet_points = []
        
        if analysis.materials and analysis.materials[0] not in ["Premium", "Quality"]:
            bullet_points.append(f"{analysis.materials[0]} construction for durability")
        else:
            bullet_points.append("Premium quality construction")
        
        if analysis.style:
            bullet_points.append(f"{analysis.style} design that stands out")
        
        if color:
            bullet_points.append(f"Beautiful {color} styling")
        else:
            bullet_points.append("Classic styling")
        
        bullet_points.append("Quality craftsmanship ensures long-lasting wear")
        bullet_points.append("Perfect addition to your collection")
        
        return ProductDescription(
            title=f"{analysis.style} {color_text}{product_name}".strip(),
            description=final_description,
            bullet_points=bullet_points,
            meta_description=f"{product_name} - {analysis.style} {analysis.specific_type.lower()}"[:160]
        )
    
    @staticmethod
    def extract_keywords(product_name: str, analysis: ProductAnalysis, description: str) -> Dict[str, List[str]]:
        """Generate SEO keywords using AI for better specificity"""
        
        base = product_name.lower()
        category = analysis.category.lower()
        style = analysis.style.lower()
        material = analysis.materials[0].lower()
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        specific = analysis.specific_type.lower()
        
        # Try AI-powered keyword generation first
        try:
            if GROQ_API_KEY and HAS_GROQ:
                client = Groq(api_key=GROQ_API_KEY)
                
                prompt = f"""Generate SEO keywords for this product:
Product: {product_name}
Category: {category}
Type: {specific}
Color: {color if color else 'not specified'}
Style: {style}
Material: {material}
Description: {description[:200]}

Generate 2 lists:
1. Primary keywords (8 keywords): Specific product identifiers, brand-style terms, material+product combos
2. Long-tail keywords (12 keywords): Detailed search phrases people actually use when shopping

Focus on:
- Actual shopping search terms (not generic)
- Specific attributes (color, material, style)
- Purchase intent phrases
- Resale/secondhand market terms where relevant

Respond ONLY with JSON:
{{"primary": ["keyword1", "keyword2", ...], "long_tail": ["long phrase 1", "long phrase 2", ...]}}"""
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                    max_tokens=400,
                    response_format={"type": "json_object"}
                )
                
                result = json.loads(completion.choices[0].message.content)
                
                # Validate and clean keywords
                primary_kw = [kw.lower().strip() for kw in result.get('primary', [])[:8] if kw.strip()]
                long_tail_kw = [kw.lower().strip() for kw in result.get('long_tail', [])[:12] if kw.strip()]
                
                if len(primary_kw) >= 5 and len(long_tail_kw) >= 8:
                    return {'primary': primary_kw, 'long_tail': long_tail_kw}
        except Exception as e:
            print(f"AI keyword generation failed: {e}")
            pass
        
        # Fallback: Enhanced template-based generation
        primary = [base]
        
        # Add specific color+product combinations
        if color and color not in base:
            primary.append(f"{color} {base}")
            if specific and specific != base:
                primary.append(f"{color} {specific}")
        
        # Add style combinations
        if style and style not in ["modern", "premium"]:
            primary.append(f"{style} {base}")
            if color:
                primary.append(f"{style} {color} {specific}")
        
        # Add material combinations if meaningful
        if material and material not in ["premium", "quality", "fabric"] and material not in base:
            primary.append(f"{material} {base}")
            if color:
                primary.append(f"{color} {material} {base}")
        
        # Add category-specific terms
        if category != "product" and specific and specific not in base:
            primary.append(f"{specific} {category.split()[0].lower()}")
        
        # Add resale-specific terms
        primary.extend([
            f"pre-owned {base}",
            f"secondhand {base}"
        ])
        
        # Remove duplicates, keep first 8
        primary = list(dict.fromkeys(primary[:8]))
        
        # Long-tail: More specific shopping intent
        long_tail = []
        
        # Purchase intent
        long_tail.extend([
            f"buy {base} online",
            f"where to buy {base}",
            f"{base} for sale near me"
        ])
        
        # Color-specific
        if color and color not in base:
            long_tail.extend([
                f"{color} {base} for sale",
                f"best {color} {specific} online",
                f"buy {color} {base} secondhand"
            ])
        
        # Style-specific
        if style and style not in ["modern", "premium"]:
            long_tail.extend([
                f"{style} {base} reviews",
                f"best {style} {specific}",
                f"affordable {style} {base}"
            ])
        
        # Material-specific
        if material and material not in ["premium", "quality", "fabric"]:
            long_tail.extend([
                f"{material} {base} online",
                f"buy {material} {specific}"
            ])
        
        # Resale/sustainable
        long_tail.extend([
            f"sustainable {base}",
            f"eco-friendly {specific}",
            f"thrift {base} online"
        ])
        
        # Quality/condition
        long_tail.extend([
            f"high quality {base}",
            f"gently used {base}",
            f"like new {specific}"
        ])
        
        # Remove duplicates, keep first 12
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
        st.markdown("### About QuickList")
        st.markdown("""
        Professional AI-powered product listings for thredUP.
        
        **Features:**
        - AI-analyzed product attributes
        - Professional SEO descriptions
        - Optimized keywords & tags
        - Ready-to-use listings
        """)
        
        st.markdown("---")
        
        st.markdown("### Process")
        st.markdown("""
        1. Upload product photo
        2. AI analyzes attributes
        3. Generate professional listing
        4. Download & publish
        
        *Typical completion: 30 seconds*
        """)
        
        st.markdown("---")
        
        st.markdown("""
        **Internal Tool**  
        thredUP Product Tagging
        """)
    
    # Main content
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-title">Upload Product Photo</div>
        <div class="upload-subtitle">
            Generate professional listing with AI analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose product image",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear product photo"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        st.session_state.product_image = image
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption="Your Product", width=500)
        
        st.markdown("""
        <div class="section-divider">
            <div class="section-title">Product Details</div>
            <div class="section-subtitle">Help us create the perfect listing</div>
        </div>
        """, unsafe_allow_html=True)
        
        product_name = st.text_input(
            "Product Name (Optional)",
            placeholder="e.g., white silk blouse, grey teddy coat, burgundy midi dress",
            help="AI will detect type, color, material & style if left blank"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            target_audience = st.text_input(
                "Target Audience (Optional)",
                placeholder="e.g., sustainable fashion enthusiasts",
                help="Who will love this product?"
            )
        
        with col2:
            price = st.text_input(
                "Price (Optional)",
                placeholder="e.g., $45",
                help="Product price"
            )
        
        product_features = st.text_area(
            "Key Features (Optional)",
            placeholder="e.g., elegant V-neck, midi length, breathable fabric",
            help="Specific features improve quality",
            height=100
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("Generate Listing", use_container_width=True):
                
                ai = QuickListAI()
                
                detected_product_name = product_name.strip() if product_name else ""
                
                st.session_state.product_name = detected_product_name
                
                # Phase 1: Image Analysis
                with st.spinner('Analyzing product image...'):
                    progress = st.progress(0)
                    
                    for i in range(50):
                        time.sleep(0.02)
                        progress.progress(i + 1)
                    
                    analysis = ai.analyze_with_vision_apis(image, detected_product_name)
                    st.session_state.analysis = analysis
                    
                    detected_color = analysis.colors[0] if analysis.colors[0] != "neutral" else "Not detected"
                    st.info(f"AI Detection: Color: {detected_color} | Category: {analysis.category} | Type: {analysis.specific_type} | Style: {analysis.style}")
                    
                    if not detected_product_name:
                        detected_product_name = f"{analysis.specific_type}" if analysis.specific_type != "Item" else analysis.category
                        st.session_state.product_name = detected_product_name
                    
                    for i in range(50, 60):
                        time.sleep(0.02)
                        progress.progress(i + 1)
                    
                    progress.empty()
                
                # Phase 2: Generate Description
                with st.spinner('Generating product description...'):
                    progress = st.progress(0)
                    
                    description = ai.generate_description(
                        detected_product_name, 
                        analysis, 
                        product_features,
                        image,
                        target_audience,
                        price
                    )
                    
                    st.session_state.description = description
                    
                    for i in range(100):
                        time.sleep(0.01)
                        progress.progress(i + 1)
                    
                    progress.empty()
                
                # Phase 3: Keywords
                with st.spinner('Generating SEO keywords...'):
                    progress = st.progress(0)
                    
                    for i in range(100):
                        time.sleep(0.01)
                        progress.progress(i + 1)
                    
                    keywords = ai.extract_keywords(
                        detected_product_name,
                        analysis,
                        description.description
                    )
                    
                    progress.empty()
                
                st.session_state.keywords = keywords
                st.session_state.needs_review = True
                st.session_state.show_results = False
                
                st.success("Listing generated successfully")
        
        # Edit/Review Panel
        if ('needs_review' in st.session_state and st.session_state.needs_review and 
            'description' in st.session_state and 'analysis' in st.session_state and 
            'keywords' in st.session_state):
            
            description = st.session_state.description
            keywords = st.session_state.keywords
            product_name = st.session_state.product_name
            
            st.markdown("""
            <div class="section-divider">
                <div class="section-title">✨ Review & Edit Your Listing</div>
                <div class="section-subtitle">Make any changes before finalizing</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="review-panel">', unsafe_allow_html=True)
            
            # Editable fields
            edited_title = st.text_input(
                "Product Title",
                value=description.title,
                help="Edit the AI-generated title",
                key="edit_title"
            )
            
            edited_description = st.text_area(
                "Description",
                value=description.description,
                height=200,
                help="Edit the AI-generated description",
                key="edit_description"
            )
            
            edited_features = st.text_area(
                "Key Features",
                value='\n'.join([f"• {point}" for point in description.bullet_points]),
                height=150,
                help="Edit the key features (one per line with •)",
                key="edit_features"
            )
            
            edited_primary_keywords = st.text_input(
                "Primary Keywords",
                value=', '.join(keywords['primary']),
                help="Edit primary SEO keywords (comma-separated)",
                key="edit_primary_keywords"
            )
            
            edited_longtail_keywords = st.text_input(
                "Long-tail Keywords",
                value=', '.join(keywords['long_tail']),
                help="Edit long-tail SEO keywords (comma-separated)",
                key="edit_longtail_keywords"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("↺ Regenerate", use_container_width=True):
                    st.session_state.needs_review = False
                    st.session_state.show_results = False
                    st.rerun()
            
            with col3:
                if st.button("✓ Approve & Finalize", use_container_width=True, type="primary"):
                    # Update session state with edited values
                    st.session_state.description = ProductDescription(
                        title=edited_title,
                        description=edited_description,
                        bullet_points=[line.strip().lstrip('• ').strip() for line in edited_features.split('\n') if line.strip()],
                        meta_description=description.meta_description
                    )
                    
                    st.session_state.keywords = {
                        'primary': [kw.strip() for kw in edited_primary_keywords.split(',') if kw.strip()],
                        'long_tail': [kw.strip() for kw in edited_longtail_keywords.split(',') if kw.strip()]
                    }
                    
                    st.session_state.needs_review = False
                    st.session_state.show_results = True
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display results
        if ('show_results' in st.session_state and st.session_state.show_results and 
            'description' in st.session_state and 'analysis' in st.session_state and 
            'keywords' in st.session_state):
            analysis = st.session_state.analysis
            description = st.session_state.description
            keywords = st.session_state.keywords
            product_name = st.session_state.product_name
            
            # Analysis
            st.markdown("""
            <div class="section-divider">
                <div class="section-title">AI Analysis</div>
                <div class="section-subtitle">Detected from your image</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                display_category = f"{analysis.category}" + (f" - {analysis.specific_type}" if analysis.specific_type and analysis.specific_type != "Item" else "")
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Category</div>
                    <div class="metric-value">{display_category}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Style</div>
                    <div class="metric-value">{analysis.style}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Materials</div>
                    <div class="metric-value" style="font-size: 1.4rem;">{', '.join(analysis.materials)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Description
            st.markdown("""
            <div class="section-divider">
                <div class="section-title">Your Listing</div>
                <div class="section-subtitle">Professional & SEO-optimized</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="content-card">
                <div class="content-title">Product Description</div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<span style='color: #1A1A1A; font-weight: 600;'>Title:</span><br>{description.title}", unsafe_allow_html=True)
            st.markdown(f"<br><span style='color: #1A1A1A; font-weight: 600;'>Description:</span><br>{description.description}", unsafe_allow_html=True)
            st.markdown("<br><span style='color: #1A1A1A; font-weight: 600;'>Key Features:</span>", unsafe_allow_html=True)
            for bp in description.bullet_points:
                st.markdown(f"<span style='color: #1A1A1A;'>• {bp}</span>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Keywords
            st.markdown("""
            <div class="seo-container">
                <div class="seo-title">SEO Keywords</div>
            """, unsafe_allow_html=True)
            
            st.markdown("<span style='color: #1A1A1A; font-weight: 600; font-size: 1.05rem;'>Primary Keywords:</span>", unsafe_allow_html=True)
            keywords_html = " ".join([f'<span class="keyword-badge">{kw}</span>' for kw in keywords['primary']])
            st.markdown(keywords_html, unsafe_allow_html=True)
            
            st.markdown("<br><span style='color: #1A1A1A; font-weight: 600; font-size: 1.05rem;'>Long-tail Keywords:</span>", unsafe_allow_html=True)
            longtail_html = " ".join([f'<span class="keyword-badge">{kw}</span>' for kw in keywords['long_tail'][:10]])
            st.markdown(longtail_html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export
            st.markdown(f"""
            <div class="section-divider">
                <div class="section-title">Download Listing</div>
                <div class="section-subtitle">Ready for thredUP</div>
            </div>
            """, unsafe_allow_html=True)
            
            formatted = format_for_platform(description, keywords, "Shopify")  # Use Shopify format as default
            
            st.markdown(f"""
            <div class="content-card">
                <h3 style="color: var(--primary);">Your thredUP Listing</h3>
                <pre style="background: #F8F8F8; padding: 2rem; border-radius: 12px; white-space: pre-wrap; font-size: 0.9rem; color: var(--charcoal);">{formatted}</pre>
            </div>
            """, unsafe_allow_html=True)
            
            # Download
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.download_button(
                    label="Download Listing",
                    data=formatted,
                    file_name=f"{product_name.lower().replace(' ', '_')}_listing.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.markdown(f"""
            <div class="info-banner">
                <p style="font-weight: 600;">
                    Listing ready for thredUP platform
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # How it works
        st.markdown("""
        <div class="section-divider">
            <div class="section-title">Process Overview</div>
            <div class="section-subtitle">Three-step listing generation</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card feature-step">
                <div class="step-number">1</div>
                <div class="step-title">Upload Photo</div>
                <div class="step-description">
                    Upload your product image - any angle, any lighting
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card feature-step">
                <div class="step-number">2</div>
                <div class="step-title">AI Analysis</div>
                <div class="step-description">
                    Our AI detects attributes and generates professional copy
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card feature-step">
                <div class="step-number">3</div>
                <div class="step-title">Download & Sell</div>
                <div class="step-description">
                    Get platform-ready listings instantly
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-banner" style="margin-top: 3rem;">
            <p style="font-size: 1.15rem; font-weight: 600; margin-bottom: 1rem;">
                Output Includes:
            </p>
            <p style="margin: 0; line-height: 1.9;">
                • AI-powered visual analysis<br>
                • Professional product descriptions<br>
                • SEO-optimized keywords & tags<br>
                • Complete listing generation in ~30 seconds<br>
                • Downloadable text format
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-banner" style="margin-top: 2rem; background: linear-gradient(135deg, #E8F5ED 0%, #D4EDE0 100%); border-left-color: var(--secondary);">
            <p style="margin: 0; font-weight: 600; font-size: 1.1rem;">
                Internal Product Tagging Tool • thredUP
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
