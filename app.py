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
        margin: -1rem -5rem 4rem -5rem;
        height: 85vh;
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
        filter: brightness(1.05);
    }
    
    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 55%;
        height: 100%;
        background: linear-gradient(
            90deg,
            rgba(250, 248, 243, 0.98) 0%,
            rgba(250, 248, 243, 0.95) 70%,
            rgba(250, 248, 243, 0.3) 95%,
            rgba(250, 248, 243, 0) 100%
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
        max-width: 55%;
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
    }
    
    .hero-description {
        font-size: 1.15rem;
        color: #666 !important;
        max-width: 600px;
        line-height: 1.7;
        margin-bottom: 2.5rem;
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
            height: 60vh;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 32px 32px;
        }
        
        .hero-overlay {
            width: 100%;
            background: linear-gradient(
                180deg,
                rgba(250, 248, 243, 0.95) 0%,
                rgba(250, 248, 243, 0.85) 100%
            );
        }
        
        .hero-content {
            max-width: 100%;
            padding: 2rem 1.5rem;
        }
        
        .brand-logo {
            font-size: 3.5rem;
        }
        
        .hero-tagline {
            font-size: 1.5rem;
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
    <img src="https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg?auto=compress&cs=tinysrgb&w=1600" 
         class="hero-image" 
         alt="Sustainable Fashion">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="brand-logo">THREDUP</div>
        <div class="brand-subtitle">QuickList</div>
        <div class="hero-tagline">Where Fashion Meets Sustainability</div>
        <div class="hero-description">
            AI-powered product listing generation for thredUP marketplace.
            Advanced image analysis and professional copywriting in seconds.
        </div>
        <div class="eco-badge">
            Sustainable Resale Technology
        </div>
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
            placeholder="e.g., Vintage Silk Dress",
            help="AI will detect if left blank"
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
                st.session_state.show_results = True
                
                st.success("Listing generated successfully")
        
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
