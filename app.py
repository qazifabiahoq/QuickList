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

# Multi-AI fallback configuration
HAS_GROQ = False
GROQ_API_KEY = None

# Try to import and configure Groq
try:
    from groq import Groq
    GROQ_API_KEY = st.secrets.get("groq", {}).get("api_key")
    HAS_GROQ = True if GROQ_API_KEY else False
except:
    pass

# Page configuration
st.set_page_config(
    page_title="QuickList - Professional Product Listings",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Same as before
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');
    
    :root {
        --background-color: #ffffff;
        --text-color: #000000;
    }
    
    .stApp {
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    .stApp > div {
        background: #ffffff !important;
    }
    
    .main {
        background: #ffffff !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    
    body, p, div, span, label, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }
    
    section, div[class*="st"], div[data-testid] {
        background-color: transparent;
    }
    
    .main .block-container {
        background: #ffffff !important;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] {
        background: #f8f8f8;
        border-right: 1px solid #e5e5e5;
    }
    
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
    
    [data-testid="stFileUploader"] section {
        background: #ffffff !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        background: #ffffff !important;
    }
    
    [data-testid="stFileUploader"] div {
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] label {
        color: #000000 !important;
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
        background: #ffffff !important;
        border: 2px dashed #cccccc !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInput"] {
        background: #ffffff !important;
    }
    
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
    
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #ffffff !important;
    }
    
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
    
    [data-testid="stImage"] + div,
    [data-testid="stImage"] figcaption,
    [data-testid="stImage"] p {
        color: #000000 !important;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #000000 0%, #0066cc 100%);
    }
    
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
    
    .stSelectbox div[data-baseweb="select"] {
        background: #ffffff !important;
        border: 2px solid #e5e5e5 !important;
    }
    
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #0066cc !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="input"] {
        color: #000000 !important;
        background: #ffffff !important;
    }
    
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
    
    [data-baseweb="menu"] li div,
    [data-baseweb="menu"] li span,
    [data-baseweb="menu"] li p {
        color: #000000 !important;
        background: transparent !important;
    }
    
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
    
    [role="option"] * {
        color: #000000 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] div,
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] p {
        color: #000000 !important;
        background: transparent !important;
    }
    
    .stSelectbox svg {
        fill: #000000 !important;
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header" style="background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important; text-align: center; padding: 3rem; border-radius: 0 0 24px 24px; margin: -6rem -5rem 3rem -5rem;">
    <div class="header-content">
        <h1 style="color: #ffffff !important; font-size: 3.5rem !important; font-weight: 800 !important; margin: 0 !important; font-family: 'Space Grotesk', sans-serif !important;">QuickList</h1>
        <p style="color: #ffffff !important; font-size: 1.25rem !important; margin-top: 0.75rem !important; font-family: 'Inter', sans-serif !important;">Professional Product Listings in Minutes</p>
        <span style="background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%) !important; color: #ffffff !important; display: inline-block !important; padding: 0.6rem 1.5rem !important; border-radius: 24px !important; font-size: 0.85rem !important; font-weight: 700 !important; margin-top: 1.25rem !important; text-transform: uppercase !important;">Multi-AI Powered</span>
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
    style_type: str
    ai_source: str = "template"  # Track which AI generated this


class QuickListAI:
    """AI-powered product listing generator with multi-AI fallback"""
    
    @staticmethod
    def analyze_product_with_clip(image: Image.Image, product_name: str = "") -> ProductAnalysis:
        """IMPROVED: Better CLIP analysis with more specific categories"""
        
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            headers = {"Content-Type": "application/octet-stream"}
            API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
            
            clothing_categories = [
                "dress evening formal", "dress casual day", "shirt top blouse",
                "pants jeans trousers", "jacket coat outerwear", "sweater cardigan",
                "skirt", "activewear sportswear", "lingerie sleepwear", "suit blazer"
            ]
            
            electronics_categories = [
                "headphones earbuds audio", "smartphone mobile phone", "laptop computer",
                "tablet device", "camera photography", "speaker bluetooth", 
                "smartwatch wearable", "gaming console", "television screen"
            ]
            
            furniture_categories = [
                "chair seating", "table desk workspace", "sofa couch",
                "bed mattress", "cabinet storage", "shelf bookcase",
                "lamp lighting", "rug carpet"
            ]
            
            other_categories = [
                "jewelry watch accessory", "bag purse luggage", "shoes footwear",
                "beauty cosmetics skincare", "kitchen cookware utensils",
                "toy game", "book stationery", "tool hardware equipment",
                "home decor decorative"
            ]
            
            all_categories = clothing_categories + electronics_categories + furniture_categories + other_categories
            
            response1 = requests.post(
                API_URL,
                headers=headers,
                data=img_bytes,
                params={"candidate_labels": ",".join(all_categories)},
                timeout=20
            )
            
            category = "Product"
            specific_type = ""
            
            if response1.status_code == 200:
                result = response1.json()
                if isinstance(result, list) and len(result) > 0:
                    detected = result[0].get('label', '').strip()
                    
                    if any(c in detected for c in ["dress", "shirt", "pants", "jacket", "sweater", "skirt", "suit"]):
                        category = "Apparel & Fashion"
                        specific_type = detected.split()[0].capitalize()
                    elif any(c in detected for c in ["headphone", "phone", "laptop", "camera", "speaker", "watch"]):
                        category = "Electronics"
                        specific_type = detected.split()[0].capitalize()
                    elif any(c in detected for c in ["chair", "table", "sofa", "bed", "cabinet", "shelf"]):
                        category = "Furniture"
                        specific_type = detected.split()[0].capitalize()
                    elif "jewelry" in detected or "watch" in detected:
                        category = "Jewelry & Accessories"
                        specific_type = "Jewelry"
                    elif "bag" in detected or "purse" in detected:
                        category = "Bags & Luggage"
                        specific_type = "Bag"
                    elif "shoes" in detected or "footwear" in detected:
                        category = "Footwear"
                        specific_type = "Shoes"
                    elif "beauty" in detected or "cosmetics" in detected:
                        category = "Beauty & Personal Care"
                        specific_type = "Beauty Product"
                    elif "kitchen" in detected or "cookware" in detected:
                        category = "Kitchen & Home"
                        specific_type = "Kitchen Item"
                    elif "toy" in detected or "game" in detected:
                        category = "Toys & Games"
                        specific_type = "Toy"
                    else:
                        category = "Product"
                        specific_type = detected.split()[0].capitalize() if detected else "Item"
            
            color_labels = [
                "black dark", "white light", "silver metallic", "gray grey", 
                "red crimson", "blue navy", "green emerald", "yellow gold",
                "pink rose", "purple violet", "brown tan", "beige cream",
                "orange coral", "multicolor rainbow", "transparent clear"
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
                    color_full = result[0].get('label', 'neutral')
                    detected_color = color_full.split()[0]
            
            if category in ["Apparel & Fashion", "Bags & Luggage"]:
                material_labels = [
                    "cotton fabric textile", "silk satin", "wool knit",
                    "leather genuine", "synthetic polyester", "denim",
                    "linen natural", "velvet luxe", "lace delicate"
                ]
            elif category == "Electronics":
                material_labels = [
                    "metal aluminum", "plastic polymer", "glass screen",
                    "stainless steel", "carbon fiber", "silicone rubber"
                ]
            elif category == "Furniture":
                material_labels = [
                    "wood oak walnut", "metal steel", "upholstered fabric",
                    "leather genuine", "plastic modern", "glass transparent",
                    "marble stone", "rattan wicker"
                ]
            else:
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
            material2 = "Quality Craftsmanship"
            if response3.status_code == 200:
                result = response3.json()
                if isinstance(result, list) and len(result) >= 2:
                    mat1_full = result[0].get('label', 'material')
                    mat2_full = result[1].get('label', 'construction')
                    
                    detected_material = mat1_full.split()[0].capitalize()
                    material2 = mat2_full.split()[0].capitalize() if len(mat2_full.split()) > 0 else "Quality"
            
            style_labels = [
                "elegant sophisticated luxury", "modern contemporary sleek",
                "casual everyday comfortable", "vintage retro classic",
                "minimalist clean simple", "sporty athletic active",
                "bohemian artistic creative", "professional business formal",
                "trendy fashionable stylish", "traditional timeless"
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
                    style_full = result[0].get('label', 'modern')
                    detected_style = style_full.split()[0].capitalize()
            
            img_array = np.array(image.resize((100, 100)))
            pixels = img_array.reshape(-1, 3)
            avg_colors = np.mean(pixels, axis=0).astype(int)
            hex_color = '#{:02x}{:02x}{:02x}'.format(*avg_colors)
            
            return ProductAnalysis(
                category=category,
                materials=[detected_material, material2],
                colors=[detected_color, hex_color],
                style=detected_style,
                confidence=0.85,
                specific_type=specific_type
            )
            
        except Exception as e:
            return ProductAnalysis(
                category="Product",
                materials=["Premium Material", "Quality Construction"],
                colors=['neutral', '#808080'],
                style='Modern',
                confidence=0.70,
                specific_type="Item"
            )
    
    @staticmethod
    def generate_with_multi_ai(product_name: str, analysis: ProductAnalysis, 
                               style: str, features: str, image: Image.Image,
                               target_audience: str = "", price_range: str = "") -> ProductDescription:
        """MULTI-AI FALLBACK CHAIN: Try multiple AI services before falling back to templates"""
        
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        
        # Enhanced context
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
        
        # Build prompt based on style
        if style == "Storytelling (Emotional)":
            prompt = f"""Write an emotional, storytelling e-commerce product description.

{context}

Write 150-200 words that:
- Create emotional connection with the customer
- Use vivid, sensory language
- Focus on lifestyle benefits and how it makes them FEEL
- Tell a mini-story about using the product
- Make it personal and relatable

Respond with JSON:
{{"title": "emotional compelling title", "description": "storytelling description with sensory details", "bullet_points": ["emotional benefit 1", "emotional benefit 2", "emotional benefit 3", "emotional benefit 4", "emotional benefit 5"], "meta_description": "SEO meta under 160 chars"}}"""

        elif style == "Feature-Benefit (Practical)":
            prompt = f"""Write a practical feature-benefit product description.

{context}

Write 150-200 words that:
- Lead with SPECIFIC features (not generic)
- Translate each feature into a clear benefit
- Use professional, authoritative language
- Include technical details where relevant
- Make it scannable with clear sections

Respond with JSON:
{{"title": "professional descriptive title with key feature", "description": "feature-benefit description with specifics", "bullet_points": ["specific feature + benefit 1", "specific feature + benefit 2", "specific feature + benefit 3", "specific feature + benefit 4", "specific feature + benefit 5"], "meta_description": "SEO meta under 160 chars"}}"""

        else:  # Minimalist
            prompt = f"""Write a minimalist product description.

{context}

Write 80-100 words:
- Short, punchy sentences
- Essential details only
- No fluff or filler
- Clean and direct
- Modern tone

Respond with JSON:
{{"title": "simple clean title", "description": "minimalist description, short sentences only", "bullet_points": ["essential detail 1", "essential detail 2", "essential detail 3", "essential detail 4", "essential detail 5"], "meta_description": "meta under 160"}}"""
        
        # ============================================
        # TIER 1: Groq (Best quality, fastest - needs API key)
        # ============================================
        if GROQ_API_KEY and HAS_GROQ:
            try:
                client = Groq(api_key=GROQ_API_KEY)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=600,
                    response_format={"type": "json_object"}
                )
                
                parsed = json.loads(completion.choices[0].message.content)
                return ProductDescription(
                    title=parsed.get('title', product_name),
                    description=parsed.get('description', ''),
                    bullet_points=parsed.get('bullet_points', [])[:5],
                    meta_description=parsed.get('meta_description', '')[:160],
                    style_type=style,
                    ai_source="Groq Llama 3.3"
                )
            except Exception as e:
                pass  # Continue to next tier
        
        # ============================================
        # TIER 2: Pollinations AI (100% Free, no API key needed!)
        # ============================================
        try:
            pollinations_url = "https://text.pollinations.ai/"
            
            # Format prompt for Pollinations
            pollinations_prompt = f"{prompt}\n\nIMPORTANT: Respond ONLY with valid JSON, no other text."
            
            response = requests.post(
                pollinations_url,
                json={
                    "messages": [
                        {"role": "user", "content": pollinations_prompt}
                    ],
                    "model": "openai",
                    "jsonMode": True
                },
                timeout=30
            )
            
            if response.status_code == 200:
                generated = response.text.strip()
                
                # Clean response
                generated = generated.replace('```json', '').replace('```', '').strip()
                start = generated.find('{')
                end = generated.rfind('}') + 1
                
                if start != -1 and end > start:
                    json_str = generated[start:end]
                    parsed = json.loads(json_str)
                    
                    return ProductDescription(
                        title=parsed.get('title', product_name),
                        description=parsed.get('description', ''),
                        bullet_points=parsed.get('bullet_points', [])[:5],
                        meta_description=parsed.get('meta_description', '')[:160],
                        style_type=style,
                        ai_source="Pollinations AI"
                    )
        except Exception as e:
            pass  # Continue to next tier
        
        # ============================================
        # TIER 3: HuggingFace Mistral (Free)
        # ============================================
        try:
            API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
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
                        
                        return ProductDescription(
                            title=parsed.get('title', product_name),
                            description=parsed.get('description', ''),
                            bullet_points=parsed.get('bullet_points', [])[:5],
                            meta_description=parsed.get('meta_description', '')[:160],
                            style_type=style,
                            ai_source="HuggingFace Mistral"
                        )
        except Exception as e:
            pass  # Continue to next tier
        
        # ============================================
        # TIER 4: HuggingFace Llama (Alternative model)
        # ============================================
        try:
            API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "inputs": f"<s>[INST] {prompt} [/INST]",
                "parameters": {
                    "max_new_tokens": 500,
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
                        
                        return ProductDescription(
                            title=parsed.get('title', product_name),
                            description=parsed.get('description', ''),
                            bullet_points=parsed.get('bullet_points', [])[:5],
                            meta_description=parsed.get('meta_description', '')[:160],
                            style_type=style,
                            ai_source="HuggingFace Llama"
                        )
        except Exception as e:
            pass  # Continue to final fallback
        
        # ============================================
        # TIER 5: IMPROVED Templates (Final fallback - always works)
        # ============================================
        return QuickListAI._industry_templates(product_name, analysis, style, features, target_audience, price_range)
    
    @staticmethod
    def _industry_templates(product_name: str, analysis: ProductAnalysis, 
                          style: str, features: str, target_audience: str = "", 
                          price_range: str = "") -> ProductDescription:
        """Industry-specific templates - same as before but marked with source"""
        
        # [Same template code as in previous version - truncated for brevity]
        # This is identical to the improved templates from the previous file
        
        cat_lower = analysis.category.lower()
        prod_lower = product_name.lower()
        specific = analysis.specific_type.lower() if analysis.specific_type else ""
        
        material1 = analysis.materials[0].lower()
        material2 = analysis.materials[1].lower()
        
        if "material" in material1 and "construction" in material2:
            material_desc = "premium materials with expert craftsmanship"
        elif material1 == material2:
            material_desc = f"high-quality {material1}"
        else:
            material_desc = f"{material1} with {material2} accents"
        
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        color_text = f"{color} " if color else ""
        color_mention = f" in {color}" if color else ""
        
        audience_context = f" designed for {target_audience}" if target_audience else ""
        
        # APPAREL
        if "apparel" in cat_lower or "fashion" in cat_lower or any(word in specific for word in ["dress", "shirt", "pants", "jacket"]):
            
            if "dress" in prod_lower or "dress" in specific:
                garment = "dress"
                occasion_desc = "whether it's a special evening out, office presentation, or weekend brunch"
            elif "shirt" in prod_lower or "shirt" in specific or "blouse" in prod_lower:
                garment = "top"
                occasion_desc = "from professional meetings to casual coffee dates"
            elif "pants" in prod_lower or "jeans" in prod_lower or "pants" in specific:
                garment = "pants"
                occasion_desc = "whether you're at work, running errands, or meeting friends"
            elif "jacket" in prod_lower or "coat" in prod_lower or "jacket" in specific:
                garment = "outerwear"
                occasion_desc = "in any weather and every season"
            else:
                garment = "piece"
                occasion_desc = "wherever your day takes you"
            
            if style == "Storytelling (Emotional)":
                title = f"{analysis.style}{color_mention} {product_name} - Effortless Style"
                
                description = f"""Step into confidence with this {color_text}{product_name.lower()}.

The moment you slip it on, you'll feel the difference. Crafted from {material_desc}, it drapes beautifully against your body, creating a silhouette that's both flattering and comfortable. The {color_text}shade catches the light perfectly, adding subtle sophistication to your look.

{features if features else f'The {analysis.style.lower()} design is timeless yet contemporary - it works seamlessly with pieces you already own while elevating your entire outfit.'}

Perfect for {occasion_desc}, this {garment} becomes your go-to choice when you want to look polished without overthinking it. It's the piece you'll reach for again and again, the one that makes getting dressed feel effortless."""
                
                bullet_points = [
                    f"Luxurious {material_desc} feels incredible against your skin",
                    f"{analysis.style} cut designed to flatter your natural shape",
                    f"Versatile {color_text}design works for multiple occasions and seasons",
                    "Maintains its beauty wash after wash - looks new for years",
                    "Pairs effortlessly with your existing wardrobe favorites"
                ]
                
            elif style == "Feature-Benefit (Practical)":
                title = f"{product_name}{color_mention} - {analysis.style} Design | Premium {material1.capitalize()}"
                
                description = f"""Elevate your wardrobe with this expertly crafted {color_text}{product_name.lower()}.

PREMIUM CONSTRUCTION: Made from {material_desc}, ensuring exceptional comfort and durability. The fabric breathes naturally while maintaining its shape through repeated wear and washing.

FLATTERING FIT: The {analysis.style.lower()} cut is precision-designed to complement various body types. It provides the right amount of structure without feeling restrictive - you'll forget you're wearing it.

{features if features else f'VERSATILE STYLING: The clean lines and {color_text}finish make this incredibly adaptable. Dress it up or down depending on your needs.'}

EASY MAINTENANCE: Machine washable and wrinkle-resistant. The color stays vibrant and the fabric maintains its integrity even with frequent use."""
                
                bullet_points = [
                    f"Premium {material_desc} provides superior comfort and longevity",
                    f"{analysis.style} silhouette flatters without restricting movement",
                    f"Versatile {color_text}design adapts to professional and casual settings",
                    "Low-maintenance care - machine washable, stays looking fresh",
                    "Quality stitching and construction built for years of wear"
                ]
                
            else:  # Minimalist
                title = f"{color_text.strip()}{product_name}".strip()
                
                description = f"""{analysis.style} design.{color_mention.capitalize() + '.' if color_mention else ''}

{material1.capitalize()} construction. Clean lines.

{features if features else 'Timeless silhouette.'}

Wears well. Lasts longer."""
                
                bullet_points = [
                    f"{material1.capitalize()} fabric",
                    f"{analysis.style} fit",
                    "Versatile styling",
                    "Easy care",
                    "Built to last"
                ]
        
        # ELECTRONICS
        elif "electronic" in cat_lower or any(word in specific for word in ["headphone", "speaker", "phone", "laptop"]):
            
            if "headphone" in prod_lower or "earbuds" in prod_lower or "headphone" in specific:
                device_type = "audio device"
                use_case = "whether you're working, commuting, or just unwinding with your favorite playlist"
            elif "speaker" in prod_lower or "speaker" in specific:
                device_type = "speaker"
                use_case = "from intimate gatherings to larger celebrations"
            elif "phone" in prod_lower or "phone" in specific:
                device_type = "smartphone"
                use_case = "throughout your busiest days"
            else:
                device_type = "device"
                use_case = "in your daily workflow"
            
            if style == "Storytelling (Emotional)":
                title = f"{product_name}{color_mention} - Premium Performance"
                
                description = f"""Experience technology the way it should be with this {color_text}{product_name.lower()}.

From the first moment you use it, you'll notice the quality. Built with {material_desc}, it feels solid and reliable in your hands. The {color_text}finish isn't just attractive - it's designed to resist fingerprints and everyday wear, keeping it looking pristine.

{features if features else 'The performance is where this truly shines. Responsive, intuitive, and powerful enough to handle whatever you throw at it.'}

Perfect {use_case}, this {device_type} becomes the reliable companion you didn't know you needed. No frustration, no compromises - just technology that works."""
                
                bullet_points = [
                    f"Premium {material_desc} construction ensures long-lasting durability",
                    "High-performance components deliver consistently responsive operation",
                    f"Intuitive interface makes complex tasks feel effortless{audience_context}",
                    f"Sleek {color_text}design looks professional in any setting",
                    "Built to handle intensive daily use without performance degradation"
                ]
                
            elif style == "Feature-Benefit (Practical)":
                title = f"{product_name}{color_mention} - High Performance | {material1.capitalize()} Build"
                
                description = f"""Get professional-grade performance with this {color_text}{product_name.lower()}.

POWERFUL PERFORMANCE: Engineered with premium components that deliver fast, reliable operation. Whether you're multitasking or running demanding applications, it handles everything smoothly.

DURABLE CONSTRUCTION: Built with {material_desc} that stands up to daily use. The {color_text}finish resists scratches and maintains its appearance over time.

{features if features else 'USER-FRIENDLY DESIGN: Intuitive controls and clear interface mean minimal learning curve. You\'ll be productive from day one.'}

BROAD COMPATIBILITY: Works seamlessly with your existing devices and accessories. No complicated setup required."""
                
                bullet_points = [
                    "High-performance components provide reliable, lag-free operation",
                    f"Durable {material_desc} withstands intensive daily use",
                    "Intuitive interface requires minimal learning time",
                    "Wide compatibility with standard devices and platforms",
                    "Quality engineering backed by rigorous testing standards"
                ]
                
            else:  # Minimalist
                title = f"{color_text.strip()}{product_name}".strip()
                
                description = f"""Performance.{color_mention.capitalize() + '.' if color_mention else ''}

{material1.capitalize()} build. Fast response.

{features if features else 'Built for daily use.'}

Works reliably. No complications."""
                
                bullet_points = [
                    "High performance",
                    f"{material1.capitalize()} construction",
                    "Easy to use",
                    "Reliable operation",
                    "Professional quality"
                ]
        
        # FURNITURE
        elif "furniture" in cat_lower or any(word in specific for word in ["chair", "table", "sofa", "bed"]):
            
            if "chair" in prod_lower or "chair" in specific:
                furniture_type = "seating"
                comfort_note = "ergonomic support that keeps you comfortable during extended sitting"
            elif "table" in prod_lower or "desk" in prod_lower or "table" in specific:
                furniture_type = "surface"
                comfort_note = "spacious, stable surface that handles your daily needs"
            elif "sofa" in prod_lower or "couch" in prod_lower or "sofa" in specific:
                furniture_type = "seating"
                comfort_note = "plush comfort that invites you to relax for hours"
            elif "bed" in prod_lower or "bed" in specific:
                furniture_type = "sleeping"
                comfort_note = "supportive comfort for restorative sleep night after night"
            else:
                furniture_type = "piece"
                comfort_note = "quality construction that lasts for years"
            
            if style == "Storytelling (Emotional)":
                title = f"{analysis.style}{color_mention} {product_name} - Transform Your Space"
                
                description = f"""Reimagine your space with this beautifully crafted {color_text}{product_name.lower()}.

The moment you bring it home, you'll see the difference quality makes. Built from {material_desc}, it provides {comfort_note}. The {color_text}finish adds warmth and character to your room, while the {analysis.style.lower()} design brings everything together with effortless sophistication.

{features if features else f'This isn\'t furniture that looks good but disappoints in use. It\'s built with solid construction that you can feel the first time you sit down.'}

Whether you're relaxing after a long day, working from home, or hosting friends, this {furniture_type} becomes the backdrop to your best moments at home."""
                
                bullet_points = [
                    f"Solid {material_desc} ensures exceptional stability and longevity",
                    f"{analysis.style} design elevates any room's aesthetic instantly",
                    f"Ergonomic construction provides genuine comfort{audience_context}",
                    f"Versatile {color_text}finish complements multiple decor styles",
                    "Quality craftsmanship built to become a cherished part of your home"
                ]
                
            elif style == "Feature-Benefit (Practical)":
                title = f"{product_name}{color_mention} - {analysis.style} Design | {material1.capitalize()}"
                
                description = f"""Upgrade your space with this expertly crafted {color_text}{product_name.lower()}.

SOLID CONSTRUCTION: Built with {material_desc} that provides exceptional durability and stability. This furniture is designed for real life - it handles daily use without showing wear.

ERGONOMIC DESIGN: The {analysis.style.lower()} design isn't just attractive - it's engineered for comfort. Proper support where you need it, generous proportions that don't cramp your space.

{features if features else f'VERSATILE STYLING: Clean lines and {color_text}finish work with any decor style, from traditional to contemporary.'}

QUALITY CRAFTSMANSHIP: Precision assembly and premium materials ensure this piece stays sturdy and beautiful through years of use."""
                
                bullet_points = [
                    f"Robust {material_desc} provides superior structural integrity",
                    "Ergonomic proportions maximize comfort during extended use",
                    f"{analysis.style} aesthetic enhances both modern and classic interiors",
                    "Quality construction maintains stability and appearance over time",
                    f"Versatile {color_text}design adapts as your style evolves"
                ]
                
            else:  # Minimalist
                title = f"{color_text.strip()}{product_name}".strip()
                
                description = f"""Solid.{color_mention.capitalize() + '.' if color_mention else ''}

{material1.capitalize()} construction. Clean design.

{features if features else 'Built to last.'}

Furniture that works."""
                
                bullet_points = [
                    f"{material1.capitalize()} build",
                    "Ergonomic design",
                    "Durable construction",
                    f"{analysis.style} aesthetic",
                    "Quality craftsmanship"
                ]
        
        # GENERAL FALLBACK
        else:
            if style == "Storytelling (Emotional)":
                title = f"{analysis.style} {product_name}{color_mention} - Premium Quality"
                
                description = f"""Discover exceptional quality with this {color_text}{product_name.lower()}.

Crafted from {material_desc}, this piece combines {analysis.style.lower()} aesthetics with uncompromising quality. The attention to detail is evident the moment you see it - from the {color_text}finish to the precise construction.

{features if features else f'Designed {audience_context if audience_context else "for those who appreciate quality"}, it delivers an experience that exceeds expectations.'}

More than just a {analysis.category.lower()} - it's a statement of your standards."""
                
                bullet_points = [
                    f"Premium {material_desc} ensures lasting durability and performance",
                    f"Sophisticated {analysis.style.lower()} design stands out from ordinary alternatives",
                    "Exceptional attention to detail in every aspect of construction",
                    f"Versatile {color_text}design adapts to multiple uses and settings",
                    "Quality that makes it perfect for gifting or personal use"
                ]
                
            elif style == "Feature-Benefit (Practical)":
                title = f"{product_name}{color_mention} - {analysis.style} | Premium {material1.capitalize()}"
                
                description = f"""Experience professional-grade quality with this {color_text}{product_name.lower()}.

SUPERIOR CONSTRUCTION: Built with {material_desc}, ensuring exceptional durability and reliable performance. This is designed to handle real-world use, not just look good on a shelf.

INTELLIGENT DESIGN: The {analysis.style.lower()} aesthetic is engineered for optimal functionality. Form and function work together seamlessly.

{features if features else f'PROVEN PERFORMANCE: {audience_context.capitalize() if audience_context else "Versatile design"} adapts to your specific needs.'}

QUALITY ASSURANCE: Rigorous standards ensure consistent excellence in every detail."""
                
                bullet_points = [
                    f"Premium {material_desc} provides superior strength and longevity",
                    "Intelligent design maximizes both functionality and aesthetics",
                    "Quality construction maintains performance through intensive use",
                    f"Versatile {color_text}design suits multiple applications and environments",
                    "Backed by rigorous quality control standards"
                ]
                
            else:  # Minimalist
                title = f"{product_name}{color_mention}"
                
                description = f"""{analysis.style} design.{color_mention.capitalize() + '.' if color_mention else ''}

{material1.capitalize()} construction.

{features if features else 'Built for those who value quality.'}

Functional. Reliable."""
                
                bullet_points = [
                    f"{material1.capitalize()} build",
                    f"{analysis.style} design",
                    "Quality construction",
                    "Versatile use",
                    "Built to last"
                ]
        
        meta = f"{product_name} - {bullet_points[0]}"[:160]
        
        return ProductDescription(
            title=title,
            description=description,
            bullet_points=bullet_points,
            meta_description=meta,
            style_type=style,
            ai_source="Smart Templates"
        )
    
    @staticmethod
    def extract_keywords(product_name: str, analysis: ProductAnalysis, description: str) -> Dict[str, List[str]]:
        """Generate SEO keywords"""
        
        base = product_name.lower()
        category = analysis.category.lower()
        style = analysis.style.lower()
        material = analysis.materials[0].lower()
        color = analysis.colors[0] if analysis.colors[0] != "neutral" else ""
        
        primary = [
            base,
            f"{style} {base}",
            f"premium {base}",
            f"best {base}",
            f"{material} {base}",
        ]
        
        if color:
            primary.extend([
                f"{color} {base}",
                f"{color} {style} {base}",
            ])
        
        if category != "product":
            primary.extend([
                f"{category.lower()} {base}",
                f"professional {base}",
            ])
        
        primary = list(dict.fromkeys(primary[:8]))
        
        long_tail = [
            f"buy {base} online",
            f"best {base} for sale",
            f"where to buy {base}",
            f"{style} {base} reviews",
            f"affordable {base}",
            f"professional grade {base}",
        ]
        
        if color:
            long_tail.extend([
                f"{color} {base} for sale",
                f"best {color} {base}",
            ])
        
        if material != "premium material":
            long_tail.append(f"{material} {base}")
        
        long_tail.extend([
            f"durable {base}",
            f"top rated {base}",
            f"{category.lower()} {base}" if category != "product" else f"quality {base}",
        ])
        
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
        
        # Show Multi-AI status
        st.markdown("### AI Status")
        if GROQ_API_KEY and HAS_GROQ:
            st.success("✅ Groq (Tier 1)")
        st.info("✅ Pollinations AI (Tier 2)")
        st.info("✅ HuggingFace Mistral (Tier 3)")
        st.info("✅ HuggingFace Llama (Tier 4)")
        st.info("✅ Smart Templates (Tier 5)")
        
        st.caption("**Multi-AI Fallback:** Tries multiple AI services for best quality!")
        
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
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            target_audience = st.text_input(
                "Target Audience (Optional)",
                placeholder="e.g., professionals, fitness enthusiasts",
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
            placeholder="e.g., 40-hour battery, active noise cancellation, wireless charging",
            help="Specific features make better descriptions",
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
                    with st.spinner('Analyzing product with AI...'):
                        progress = st.progress(0)
                        
                        for i in range(40):
                            time.sleep(0.02)
                            progress.progress(i + 1)
                        
                        analysis = ai.analyze_product_with_clip(image, product_name)
                        st.session_state.analysis = analysis
                        
                        for i in range(40, 50):
                            time.sleep(0.02)
                            progress.progress(i + 1)
                        
                        progress.empty()
                    
                    # Phase 2: Multi-AI Descriptions
                    with st.spinner('Generating descriptions with Multi-AI (trying Pollinations, Mistral, Llama...)'):
                        progress = st.progress(0)
                        
                        descriptions = {}
                        styles = ["Storytelling (Emotional)", "Feature-Benefit (Practical)", "Minimalist (Clean)"]
                        
                        for idx, style_name in enumerate(styles):
                            desc = ai.generate_with_multi_ai(
                                product_name, 
                                analysis, 
                                style_name, 
                                product_features,
                                image,
                                target_audience,
                                price_range
                            )
                            descriptions[style_name] = desc
                            
                            prog = int((idx + 1) / len(styles) * 100)
                            progress.progress(prog)
                        
                        progress.empty()
                    
                    st.session_state.descriptions = descriptions
                    
                    # Phase 3: Keywords
                    with st.spinner('Generating SEO keywords...'):
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
                    
                    # Show which AI was used
                    ai_sources = list(set([desc.ai_source for desc in descriptions.values()]))
                    if len(ai_sources) == 1:
                        st.success(f"✅ Listing ready! Generated by: **{ai_sources[0]}**")
                    else:
                        st.success(f"✅ Listing ready! Generated by: **{', '.join(ai_sources)}**")
        
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
            
            # Descriptions
            st.markdown("""
            <div class="section-header">
                <h2 class="section-title">Your Product Descriptions</h2>
                <p class="section-subtitle">Three professionally written styles</p>
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
                
                st.caption(f"Generated by: {desc.ai_source}")
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
                
                st.caption(f"Generated by: {desc.ai_source}")
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
                
                st.caption(f"Generated by: {desc.ai_source}")
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
                help="Select which description to use",
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
                all_listings += f"Created by QuickList Multi-AI\n"
                all_listings += f"Platform: {target_platform}\n"
                all_listings += f"Category: {analysis.category}\n\n"
                all_listings += "="*70 + "\n\n"
                
                for style_name, desc in descriptions.items():
                    all_listings += f"\n{'='*70}\n{style_name} (Generated by: {desc.ai_source})\n{'='*70}\n\n"
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
            <p class="section-subtitle">Multi-AI powered listings in seconds</p>
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
                <div class="metric-label">Multi-AI Generation</div>
                <div style="color: #666666; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                    5 AI services work together for best results
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">3</div>
                <div class="metric-label">Download & Sell</div>
                <div style="color: #666666; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">
                    Ready for any platform
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 3rem;">
            <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">
                Multi-AI Fallback System:
            </p>
            <p style="margin: 0; line-height: 1.8;">
                • <strong>Tier 1:</strong> Groq Llama 3.3 (if API key provided)<br>
                • <strong>Tier 2:</strong> Pollinations AI (100% free, no key needed!)<br>
                • <strong>Tier 3:</strong> HuggingFace Mistral<br>
                • <strong>Tier 4:</strong> HuggingFace Llama<br>
                • <strong>Tier 5:</strong> Smart Industry Templates<br><br>
                <strong>Result:</strong> Almost always get Gen AI responses instead of templates!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 2rem; border-left-color: #0066cc;">
            <p style="margin: 0; font-weight: 600;">
                100% Free • No Signup Required • Multiple AI Services • Instant Results
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
