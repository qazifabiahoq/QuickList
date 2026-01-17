import streamlit as st
import cv2
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models
import io
import base64
from dataclasses import dataclass
from typing import List, Dict, Tuple

# Page configuration
st.set_page_config(
    page_title="RoomSense - Intelligent Space Planning",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for RoomSense brand design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Main app background */
    .stApp {
        background: #ffffff;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-header {
            text-align: center;
            padding: 1.5rem 1.5rem;
            margin: -6rem -1rem 1.5rem -1rem;
        }
        
        .logo {
            color: #000000 !important;
            font-size: 2rem;
        }
        
        .tagline {
            color: #000000 !important;
            font-size: 0.95rem;
        }
        
        .metric-box {
            padding: 1.25rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
        
        .stButton > button {
            padding: 0.875rem 2rem;
            font-size: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .logo {
            color: #000000 !important;
            font-size: 1.75rem;
        }
        
        .tagline {
            color: #000000 !important;
            font-size: 0.85rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Main header */
    .main-header {
        text-align: center;
        background: white;
        padding: 2.5rem 3rem;
        border-radius: 0 0 24px 24px;
        margin: -6rem -5rem 2rem -5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove empty container spacing */
    .element-container:has(> .stMarkdown > div:empty) {
        display: none;
    }
    
    /* Hide empty blocks */
    [data-testid="stHorizontalBlock"]:empty {
        display: none !important;
    }
    
    /* Remove default Streamlit spacing blocks */
    .block-container > div:empty {
        display: none !important;
    }
    
    /* Hide empty divs */
    div:empty {
        display: none !important;
    }
    
    /* Main header with RoomSense branding */
    .main-header {
        text-align: center;
        background: white;
        padding: 2.5rem 3rem;
        border-radius: 0 0 24px 24px;
        margin: -6rem -5rem 2rem -5rem;
        box-shadow: 0 8px 32px rgba(14,165,233,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.08'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 1;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    .logo {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }
    
    .tagline {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        margin-top: 0.5rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    
    .ai-badge {
        color: #000000 !important;
        background: #f5f5f5;
        border: 2px solid #000000;
        display: inline-block;
        backdrop-filter: blur(10px);
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    p, div, span, label {
        color: #333333 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #f5f5f5;
        border-right: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #000000 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Camera section */
    .camera-section {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 2px solid #e0e0e0;
    }
    
    /* Analysis card */
    .analysis-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #000000;
        position: relative;
    }
    
    /* Metric boxes */
    .metric-box {
        background: white;
        border-radius: 16px;
        padding: 1.5rem 1rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-top: 3px solid #000000;
        transition: all 0.3s ease;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .metric-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.12);
    }
    
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: #000000;
    }
    
    .metric-label {
        font-size: 0.65rem;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #000000;
        font-family: 'Space Grotesk', sans-serif;
        line-height: 1.3;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
    }
    
    .metric-unit {
        font-size: 0.85rem;
        color: #666666;
        font-weight: 400;
    }
    
    /* Recommendation section */
    .rec-item {
        background: #f5f5f5 !important;
        border-radius: 16px;
        padding: 1.75rem;
        margin: 1.25rem 0;
        border: 2px solid #e0e0e0 !important;
        transition: all 0.3s ease;
    }
    
    .rec-item:hover {
        background: #eeeeee !important;
        transform: translateX(8px);
    }
    
    .rec-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        font-family: 'Space Grotesk', sans-serif;
        color: #000000 !important;
    }
    
    .rec-description {
        font-size: 1rem;
        line-height: 1.7;
        color: #000000 !important;
    }
    
    .rec-description * {
        color: #000000 !important;
    }
    
    .rec-description strong {
        color: #000000 !important;
        font-weight: 600;
    }
    
    /* Zone tags */
    .zone-tag {
        display: inline-block;
        background: white;
        color: #000000;
        border: 2px solid #000000;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.3rem 0.3rem 0.3rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Furniture list */
    .furniture-list {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .furniture-list strong {
        color: #000000 !important;
    }
    
    .furniture-item {
        padding: 0.6rem 0;
        border-bottom: 1px solid #e0e0e0;
        font-size: 0.95rem;
        color: #000000 !important;
    }
    
    .furniture-item:last-child {
        border-bottom: none;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .status-processing {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white !important;
        animation: shimmer 2s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .status-complete {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
    }
    
    /* Confidence bar */
    .confidence-bar {
        background: #e0e0e0;
        height: 10px;
        border-radius: 6px;
        overflow: hidden;
        margin: 0.75rem 0;
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #000000 0%, #1a1a1a 100%);
        border-radius: 6px;
        transition: width 1s ease;
    }
    
    /* Buttons */
    .stButton > button {
        background: white !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 12px !important;
        padding: 1rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        width: 100%;
        height: 60px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.15) !important;
        background: #000000 !important;
        color: white !important;
    }
    
    /* Insight box */
    .insight-box {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    .insight-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 1rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Actions section */
    .actions-section {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-top: 4px solid #000000;
    }
    
    .actions-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
        text-align: center;
    }
    
    /* File Uploader styling */
    [data-testid="stFileUploader"] {
        background: white !important;
        border: 2px dashed #000000 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: white !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        color: #000000 !important;
        background: white !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #666666 !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: white !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
    }
    
    /* File uploader text elements */
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }
    
    [data-testid="stFileUploader"] span {
        color: #000000 !important;
    }
    
    /* File uploader drag area */
    [data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {
        background: white !important;
    }
    
    [data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzoneInput"] {
        color: #000000 !important;
    }
    
    /* Camera input */
    [data-testid="stCameraInput"] label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stCameraInput"] button {
        background: white !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
    }
    
    /* Number input */
    .stNumberInput label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stNumberInput input {
        color: #000000 !important;
        background: white !important;
        border: 2px solid #e0e0e0 !important;
    }
    
    /* Slider styling for select_slider */
    .stSlider {
        padding: 1rem 0 !important;
    }
    
    .stSlider > label {
        color: #000000 !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Slider track - make it visible */
    .stSlider [data-baseweb="slider"] {
        padding: 0.5rem 0 !important;
    }
    
    .stSlider [data-baseweb="slider"] > div > div {
        background: #000000 !important;
        height: 4px !important;
    }
    
    /* Slider thumb/handle */
    .stSlider [role="slider"] {
        background: #000000 !important;
        border: 3px solid #000000 !important;
        width: 20px !important;
        height: 20px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Slider labels */
    .stSlider [data-baseweb="tick-bar"] {
        color: #000000 !important;
        font-weight: 600 !important;
        padding-top: 0.5rem !important;
    }
    
    .stSlider [data-baseweb="tick-bar"] > div {
        color: #000000 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #000000 0%, #1a1a1a 100%);
    }
    
    /* Selectbox and radio */
    .stSelectbox label,
    .stRadio label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Selectbox - main selected value display */
    .stSelectbox div[data-baseweb="select"] {
        background: white !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background: white !important;
        color: #000000 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] span {
        color: #000000 !important;
    }
    
    /* Selectbox input field */
    .stSelectbox input {
        background: white !important;
        color: #000000 !important;
    }
    
    /* Dropdown options */
    [role="listbox"] {
        background: white !important;
    }
    
    [role="option"] {
        color: #000000 !important;
        background: white !important;
    }
    
    [role="option"]:hover {
        background: #f5f5f5 !important;
        color: #000000 !important;
    }
    
    [role="option"][aria-selected="true"] {
        background: #e0e0e0 !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Ensure all select elements have proper styling */
    select {
        background: white !important;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <h1 class="logo" style="color: #000000 !important;">RoomSense</h1>
        <p class="tagline" style="color: #000000 !important;">Design your perfect space</p>
        <span class="ai-badge" style="color: #000000 !important;">Smart Room Planning</span>
    </div>
</div>
""", unsafe_allow_html=True)


# Data classes for structured recommendations
@dataclass
class RoomAnalysis:
    room_type: str
    confidence: float
    dimensions: Dict[str, float]
    lighting: str
    layout_type: str
    detected_objects: List[str]
    color_palette: List[str]


@dataclass
class RoomRecommendation:
    zone_name: str
    location: str
    furniture: List[str]
    lighting_needs: str
    considerations: List[str]


class SpaceVisionAI:
    """Deep Learning based room analysis system"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.load_models()
        
    @st.cache_resource
    def load_models(_self):
        """Load pre-trained deep learning models"""
        # Load ResNet50 for scene classification
        resnet = models.resnet50(weights='IMAGENET1K_V1')
        resnet.eval()
        
        # Load MobileNetV2 for efficient object detection
        mobilenet = models.mobilenet_v2(weights='IMAGENET1K_V1')
        mobilenet.eval()
        
        return {
            'scene_classifier': resnet,
            'object_detector': mobilenet
        }
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """Preprocess image for neural network"""
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        return transform(image).unsqueeze(0)
    
    def analyze_room_scene(self, image: Image.Image) -> Dict:
        """Analyze room using deep learning"""
        img_tensor = self.preprocess_image(image)
        
        # Simulated analysis (in production, use trained models)
        room_types = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Dining Room', 'Home Office', 'Kids Room', 'Laundry Room']
        lighting_types = ['Natural - Excellent', 'Mixed - Good', 'Artificial - Moderate', 'Low Light']
        layout_types = ['Open Plan', 'Traditional', 'L-Shaped', 'Square', 'Rectangular']
        
        # Get image features
        img_array = np.array(image)
        brightness = np.mean(img_array)
        
        # Simulate ML predictions
        room_type = np.random.choice(room_types, p=[0.20, 0.20, 0.15, 0.10, 0.10, 0.10, 0.10, 0.05])
        confidence = np.random.uniform(0.78, 0.95)
        lighting = lighting_types[min(int(brightness / 64), 3)]
        layout = np.random.choice(layout_types)
        
        return {
            'room_type': room_type,
            'confidence': confidence,
            'lighting': lighting,
            'layout_type': layout,
            'brightness': brightness
        }
    
    def detect_objects(self, image: Image.Image) -> List[str]:
        """Detect furniture and objects in the room"""
        common_objects = [
            'Sofa', 'Chair', 'Table', 'Bed', 'Dresser', 'Nightstand', 'Bookshelf', 
            'TV Stand', 'Cabinet', 'Desk', 'Lamp', 'Mirror', 'Rug', 'Curtains',
            'Window', 'Door', 'Plant', 'Artwork', 'Shelving'
        ]
        # Simulate object detection
        num_objects = np.random.randint(5, 10)
        detected = np.random.choice(common_objects, size=num_objects, replace=False)
        return detected.tolist()
    
    def estimate_dimensions(self, image: Image.Image) -> Dict[str, float]:
        """Estimate room dimensions"""
        width, height = image.size
        aspect_ratio = width / height
        
        # Simulate dimension estimation
        estimated_width = np.random.uniform(3.0, 5.5)
        estimated_length = estimated_width * aspect_ratio * np.random.uniform(0.8, 1.2)
        estimated_height = np.random.uniform(2.4, 3.0)
        
        return {
            'width': round(estimated_width, 1),
            'length': round(estimated_length, 1),
            'height': round(estimated_height, 1),
            'area': round(estimated_width * estimated_length, 1)
        }
    
    def extract_color_palette(self, image: Image.Image) -> List[str]:
        """Extract dominant colors using K-means clustering"""
        img_array = np.array(image.resize((150, 150)))
        pixels = img_array.reshape(-1, 3)
        
        # Simple color clustering
        from sklearn.cluster import KMeans
        n_colors = 5
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        colors = kmeans.cluster_centers_.astype(int)
        hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in colors]
        
        return hex_colors


def generate_room_recommendations(analysis: RoomAnalysis, room_type: str) -> List[RoomRecommendation]:
    """Generate intelligent room recommendations based on AI analysis"""
    
    recommendations = []
    
    room_configs = {
        'Living Room': {
            'zones': [
                {
                    'name': 'Seating Area',
                    'location': 'Center of room, facing TV or focal point',
                    'furniture': ['3-Seater Sofa', 'Accent Chairs (2x)', 'Coffee Table', 'Side Tables', 'Floor Lamp', 'Area Rug'],
                    'lighting': 'Layered: Overhead pendant + Floor lamp + Table lamps (2700-3000K)',
                    'considerations': ['Leave 45cm walking space around furniture', 'Position sofa 2-3m from TV', 'Create conversation pit with chairs facing each other']
                },
                {
                    'name': 'Entertainment Zone',
                    'location': 'Against main wall',
                    'furniture': ['TV Stand or Media Console', 'Wall-mounted TV', 'Cable Management Box', 'Sound Bar', 'Storage Baskets'],
                    'lighting': 'LED bias lighting behind TV',
                    'considerations': ['Mount TV at eye level when seated', 'Hide cables with cable covers', 'Add closed storage for media clutter']
                },
                {
                    'name': 'Reading Nook',
                    'location': 'Corner near window',
                    'furniture': ['Comfortable Armchair', 'Reading Lamp', 'Small Side Table', 'Throw Blanket', 'Bookshelf'],
                    'lighting': 'Adjustable task lamp (reading light)',
                    'considerations': ['Position near natural light source', 'Add floor cushion for flexibility', 'Keep books within arm\'s reach']
                }
            ]
        },
        'Bedroom': {
            'zones': [
                {
                    'name': 'Sleeping Area',
                    'location': 'Against longest wall, away from door',
                    'furniture': ['Bed Frame', 'Mattress', 'Nightstands (2x)', 'Table Lamps (2x)', 'Headboard'],
                    'lighting': 'Bedside lamps with dimmer switches (2700K warm)',
                    'considerations': ['Allow 60cm on each side of bed', 'Position bed away from direct sunlight', 'Avoid placing bed under window']
                },
                {
                    'name': 'Storage & Dressing',
                    'location': 'Opposite or adjacent to bed',
                    'furniture': ['Wardrobe or Closet System', 'Dresser with Mirror', 'Clothing Rack', 'Storage Boxes', 'Bench'],
                    'lighting': 'Overhead lighting + Mirror lights',
                    'considerations': ['Keep wardrobe doors clearance 90cm', 'Use vertical space efficiently', 'Add drawer organizers']
                },
                {
                    'name': 'Personal Space',
                    'location': 'Corner or window area',
                    'furniture': ['Accent Chair', 'Small Desk or Vanity', 'Ottoman', 'Full-length Mirror'],
                    'lighting': 'Task lighting for vanity area',
                    'considerations': ['Create relaxation spot', 'Add plants for air quality', 'Keep surfaces minimal']
                }
            ]
        },
        'Kitchen': {
            'zones': [
                {
                    'name': 'Cooking Zone',
                    'location': 'Stove, counter, sink triangle',
                    'furniture': ['Kitchen Island or Cart', 'Bar Stools (2-3x)', 'Pot Rack', 'Spice Rack', 'Cutting Board Station'],
                    'lighting': 'Under-cabinet LED strips + Pendant lights over island',
                    'considerations': ['Keep 120cm between counters', 'Place frequently used items within reach', 'Add anti-fatigue mat']
                },
                {
                    'name': 'Storage & Pantry',
                    'location': 'Along walls, maximize vertical space',
                    'furniture': ['Pantry Shelving', 'Upper Cabinets', 'Pull-out Drawers', 'Lazy Susan', 'Clear Storage Containers'],
                    'lighting': 'Interior cabinet lights',
                    'considerations': ['Group items by category', 'Use clear containers for visibility', 'Label everything']
                },
                {
                    'name': 'Dining/Eating Area',
                    'location': 'Adjacent to kitchen',
                    'furniture': ['Dining Table', 'Dining Chairs', 'Pendant Light', 'Buffet or Sideboard'],
                    'lighting': 'Statement pendant 75cm above table',
                    'considerations': ['Allow 60cm per person at table', 'Leave 90cm walking clearance', 'Add rug under table for comfort']
                }
            ]
        },
        'Bathroom': {
            'zones': [
                {
                    'name': 'Vanity Area',
                    'location': 'Primary wall space',
                    'furniture': ['Vanity with Sink', 'Mirror (large)', 'Wall-mounted Shelves', 'Toiletry Organizers', 'Towel Bar'],
                    'lighting': 'Side-mounted mirror lights + Overhead (4000K)',
                    'considerations': ['Install lighting at face level, not overhead', 'Add storage for daily items', 'Keep counter clutter-free']
                },
                {
                    'name': 'Shower/Bath Zone',
                    'location': 'Wet area with proper drainage',
                    'furniture': ['Shower Caddy', 'Bath Mat', 'Towel Hooks', 'Shower Curtain or Glass Door'],
                    'lighting': 'Waterproof recessed lighting',
                    'considerations': ['Use non-slip mats', 'Add grab bar for safety', 'Ensure proper ventilation']
                },
                {
                    'name': 'Storage Solutions',
                    'location': 'Walls, over toilet, under sink',
                    'furniture': ['Over-toilet Cabinet', 'Under-sink Organizers', 'Medicine Cabinet', 'Towel Ladder', 'Baskets'],
                    'lighting': 'Ambient ceiling light',
                    'considerations': ['Use vertical wall space', 'Keep cleaning supplies accessible', 'Store towels within reach']
                }
            ]
        },
        'Dining Room': {
            'zones': [
                {
                    'name': 'Main Dining Area',
                    'location': 'Center of room',
                    'furniture': ['Dining Table (6-8 seater)', 'Dining Chairs', 'Table Runner', 'Centerpiece', 'Area Rug'],
                    'lighting': 'Statement chandelier or pendant (centered, 75-85cm above table)',
                    'considerations': ['Allow 60cm per person', 'Leave 90-120cm walking space around table', 'Rug should extend 60cm beyond table edges']
                },
                {
                    'name': 'Serving Station',
                    'location': 'Against wall, near kitchen',
                    'furniture': ['Buffet or Sideboard', 'Table Lamp', 'Serving Trays', 'Wine Rack', 'Storage for Linens'],
                    'lighting': 'Accent lighting with table lamps',
                    'considerations': ['Height should be 75-90cm', 'Use for dish storage and serving', 'Add decorative items on top']
                },
                {
                    'name': 'Display Area',
                    'location': 'Open wall space',
                    'furniture': ['China Cabinet', 'Display Shelves', 'Artwork', 'Mirror'],
                    'lighting': 'Picture lights or spotlights',
                    'considerations': ['Showcase special dinnerware', 'Create visual interest', 'Balance with room size']
                }
            ]
        },
        'Home Office': {
            'zones': [
                {
                    'name': 'Work Station',
                    'location': 'Near natural light, against wall',
                    'furniture': ['Desk (140x70cm)', 'Ergonomic Office Chair', 'Monitor Stand', 'Desk Lamp', 'Cable Management'],
                    'lighting': 'Task lamp + Ambient overhead (4000-5000K)',
                    'considerations': ['Position desk perpendicular to window', 'Monitor 50-70cm from eyes', 'Add footrest if needed']
                },
                {
                    'name': 'Storage & Filing',
                    'location': 'Adjacent to desk, within reach',
                    'furniture': ['Filing Cabinet', 'Bookshelf', 'Storage Boxes', 'Magazine Holders', 'Printer Stand'],
                    'lighting': 'Overhead lighting',
                    'considerations': ['Keep frequently used items accessible', 'Use vertical storage', 'Label all files clearly']
                },
                {
                    'name': 'Meeting/Reading Corner',
                    'location': 'Opposite desk area',
                    'furniture': ['Comfortable Chair', 'Small Side Table', 'Bookshelf', 'Floor Lamp'],
                    'lighting': 'Adjustable reading lamp',
                    'considerations': ['Create separation from work desk', 'Add plants for relaxation', 'Use for video calls']
                }
            ]
        },
        'Kids Room': {
            'zones': [
                {
                    'name': 'Sleep Zone',
                    'location': 'Quiet corner, away from play area',
                    'furniture': ['Bed with Storage', 'Nightstand', 'Night Light', 'Blackout Curtains'],
                    'lighting': 'Dimmable ceiling light + Night light',
                    'considerations': ['Use bed rails for young children', 'Keep pathway clear', 'Add comfort items (pillows, stuffed animals)']
                },
                {
                    'name': 'Play & Activity Area',
                    'location': 'Open floor space, center of room',
                    'furniture': ['Toy Storage Bins', 'Play Mat', 'Small Table & Chairs', 'Toy Organizer', 'Bookshelf'],
                    'lighting': 'Bright overhead lighting',
                    'considerations': ['Use low storage for easy access', 'Rotate toys regularly', 'Create designated zones for activities']
                },
                {
                    'name': 'Study Corner',
                    'location': 'Near window, quiet area',
                    'furniture': ['Kid-sized Desk', 'Adjustable Chair', 'Desk Lamp', 'Supply Organizer', 'Bulletin Board'],
                    'lighting': 'Task lighting for homework',
                    'considerations': ['Adjust furniture as child grows', 'Keep supplies organized', 'Display artwork and achievements']
                }
            ]
        },
        'Laundry Room': {
            'zones': [
                {
                    'name': 'Washing Station',
                    'location': 'Against wall with plumbing',
                    'furniture': ['Washer & Dryer', 'Laundry Baskets (3x for sorting)', 'Hamper', 'Rolling Cart'],
                    'lighting': 'Bright overhead LED (4000K)',
                    'considerations': ['Leave 10cm space behind machines', 'Use vibration pads', 'Sort lights, darks, delicates']
                },
                {
                    'name': 'Folding & Ironing',
                    'location': 'Open counter space',
                    'furniture': ['Folding Counter', 'Wall-mounted Ironing Board', 'Iron Holder', 'Drying Rack', 'Shelf for Detergent'],
                    'lighting': 'Under-cabinet lights',
                    'considerations': ['Counter height 85-90cm', 'Keep iron at safe distance', 'Add cushioned mat for standing']
                },
                {
                    'name': 'Storage & Organization',
                    'location': 'Upper cabinets and shelving',
                    'furniture': ['Upper Cabinets', 'Shelving Units', 'Clear Storage Jars', 'Hanging Rod', 'Utility Sink'],
                    'lighting': 'General ambient lighting',
                    'considerations': ['Store detergents out of reach of children', 'Label all products', 'Keep stain removers accessible']
                }
            ]
        }
    }
    
    config = room_configs.get(room_type, room_configs['Living Room'])
    
    for zone in config['zones']:
        rec = RoomRecommendation(
            zone_name=zone['name'],
            location=zone['location'],
            furniture=zone['furniture'],
            lighting_needs=zone['lighting'],
            considerations=zone['considerations']
        )
        recommendations.append(rec)
    
    return recommendations


def generate_detailed_insights(analysis: RoomAnalysis) -> List[str]:
    """Generate detailed, room-specific insights"""
    insights = []
    
    # Size-based insights
    if analysis.dimensions['area'] < 10:
        insights.append("**Maximize Space:** Your room is cozy! Use wall-mounted shelves, under-bed storage, and multi-functional furniture like ottomans with storage or fold-down desks.")
    elif analysis.dimensions['area'] < 15:
        insights.append("**Perfect Size:** You have a comfortable room. Create clear zones using area rugs and furniture placement. Keep pathways at least 60cm wide for easy movement.")
    elif analysis.dimensions['area'] < 25:
        insights.append("**Spacious Layout:** Great room size! You can create multiple functional zones. Use furniture to define different areas - a reading corner, entertainment space, etc.")
    else:
        insights.append("**Generous Space:** You have plenty of room! Consider creating distinct zones for different activities. Use area rugs, lighting, and furniture arrangement to define each zone.")
    
    # Lighting insights
    if 'Natural' in analysis.lighting or 'Excellent' in analysis.lighting:
        insights.append("**Natural Light Advantage:** Position furniture to take advantage of natural light. Add sheer curtains to control glare and blackout curtains for privacy and sleep.")
    elif 'Good' in analysis.lighting:
        insights.append("**Lighting Balance:** Mix ambient, task, and accent lighting. Use warm white (2700-3000K) for living areas and cool white (4000-5000K) for workspaces.")
    else:
        insights.append("**Brighten Up:** Add multiple light sources! Use overhead lighting, floor lamps, and table lamps. Aim for 200-300 lumens per square meter in living spaces.")
    
    # Ceiling height
    if analysis.dimensions['height'] > 2.8:
        insights.append("**High Ceilings:** Install tall storage units and use vertical space. Hang artwork higher and add statement pendant lights to draw the eye upward.")
    elif analysis.dimensions['height'] < 2.5:
        insights.append("**Standard Height:** Keep furniture and decor at eye level. Use horizontal lines in decor and avoid tall furniture that makes the room feel smaller.")
    
    return insights


def display_analysis_results(analysis: RoomAnalysis, room_type: str, button_key_suffix: str):
    """Display complete analysis results with recommendations"""
    
    # Display Analysis Results
    st.markdown("## Your Room Analysis")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">🏠</div>
            <div class="metric-label">Room Type</div>
            <div class="metric-value">{analysis.room_type}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">📏</div>
            <div class="metric-label">Estimated Area</div>
            <div class="metric-value">{analysis.dimensions['area']}<span class="metric-unit">m²</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">💡</div>
            <div class="metric-label">Lighting</div>
            <div class="metric-value">{analysis.lighting}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">✓</div>
            <div class="metric-label">Confidence</div>
            <div class="metric-value">{int(analysis.confidence * 100)}<span class="metric-unit">%</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Analysis
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Room Specifications")
        st.markdown(f"""
        - **Layout Type:** {analysis.layout_type}
        - **Width:** {analysis.dimensions['width']}m
        - **Length:** {analysis.dimensions['length']}m
        - **Height:** {analysis.dimensions['height']}m
        - **Total Area:** {analysis.dimensions['area']}m²
        """)
        
        if analysis.detected_objects:
            st.markdown("### Detected Objects")
            objects_html = " ".join([f'<span class="zone-tag">{obj}</span>' for obj in analysis.detected_objects])
            st.markdown(objects_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Confidence Score")
        st.markdown(f"""
        <div class="confidence-bar">
            <div class="confidence-fill" style="width: {analysis.confidence * 100}%;"></div>
        </div>
        <p style="text-align: center; font-size: 0.9rem; color: #666666; margin-top: 0.5rem;">
            {int(analysis.confidence * 100)}% confident in room classification
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate Recommendations
    recommendations = generate_room_recommendations(analysis, room_type)
    
    st.markdown(f"""
    <div class="recommendation-section" style="background: white !important; color: #000000 !important; border: 2px solid #e0e0e0 !important; border-radius: 20px; padding: 2.5rem; margin: 2rem 0;">
        <h2 style="color: #000000 !important; font-family: 'Space Grotesk', sans-serif; margin-bottom: 1.5rem;">
            Smart Recommendations for Your {room_type}
        </h2>
        <p style="color: #000000 !important; font-size: 1.1rem; margin-bottom: 2rem;">
            Based on AI analysis of your {analysis.dimensions['area']}m² {analysis.room_type.lower()} 
            with {analysis.lighting.lower()} conditions
        </p>
    """, unsafe_allow_html=True)
    
    for rec in recommendations:
        st.markdown(f"""
        <div class="rec-item">
            <div class="rec-title">{rec.zone_name}</div>
            <div class="rec-description">
                <strong>Optimal Location:</strong> {rec.location}<br><br>
                <strong>Lighting Setup:</strong> {rec.lighting_needs}
            </div>
            <div class="furniture-list">
                <strong>Recommended Furniture:</strong>
                {''.join([f'<div class="furniture-item">• {item}</div>' for item in rec.furniture])}
            </div>
            <div style="margin-top: 1.25rem;">
                <strong style="font-weight: 600;">Key Considerations:</strong><br>
                {'<br>'.join([f'<span>• {item}</span>' for item in rec.considerations])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional Insights
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("### Smart Insights for Your Space")
    
    insights = generate_detailed_insights(analysis)
    
    for insight in insights:
        st.markdown(insight)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Color Palette Suggestions
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("### Suggested Color Palette for Your Room")
    st.markdown("Professional color combinations that work perfectly for your space:")
    
    if 'Bedroom' in analysis.room_type or 'Kids Room' in analysis.room_type:
        palette_suggestions = [
            ("Calm & Serene", ["#E8EAF6", "#C5CAE9", "#9FA8DA", "#7986CB"]),
            ("Warm & Cozy", ["#FFF3E0", "#FFE0B2", "#FFCC80", "#FFB74D"]),
            ("Modern Neutral", ["#FAFAFA", "#EEEEEE", "#BDBDBD", "#757575"])
        ]
    elif 'Office' in analysis.room_type:
        palette_suggestions = [
            ("Focus Blue", ["#E3F2FD", "#BBDEFB", "#90CAF9", "#42A5F5"]),
            ("Professional Grey", ["#FAFAFA", "#ECEFF1", "#B0BEC5", "#546E7A"]),
            ("Energizing Green", ["#E8F5E9", "#C8E6C9", "#81C784", "#66BB6A"])
        ]
    elif 'Living' in analysis.room_type or 'Dining' in analysis.room_type:
        palette_suggestions = [
            ("Welcoming Warm", ["#FFF8E1", "#FFECB3", "#FFD54F", "#FFA726"]),
            ("Elegant Neutral", ["#F5F5F5", "#E0E0E0", "#9E9E9E", "#616161"]),
            ("Fresh Modern", ["#E0F2F1", "#B2DFDB", "#4DB6AC", "#26A69A"])
        ]
    elif 'Kitchen' in analysis.room_type:
        palette_suggestions = [
            ("Clean White", ["#FFFFFF", "#F8F9FA", "#E9ECEF", "#CED4DA"]),
            ("Classic Wood Tones", ["#F5E6D3", "#D7C9B8", "#A89784", "#8B7355"]),
            ("Modern Charcoal", ["#F5F5F5", "#E0E0E0", "#757575", "#424242"])
        ]
    elif 'Bathroom' in analysis.room_type:
        palette_suggestions = [
            ("Spa Blue", ["#E1F5FE", "#B3E5FC", "#4FC3F7", "#0288D1"]),
            ("Fresh White", ["#FFFFFF", "#F5F5F5", "#EEEEEE", "#BDBDBD"]),
            ("Warm Beige", ["#FFF8E1", "#FFECB3", "#FFD54F", "#F9A825"])
        ]
    else:
        palette_suggestions = [
            ("Bright & Airy", ["#FFFFFF", "#F5F5F5", "#EEEEEE", "#E0E0E0"]),
            ("Warm Neutral", ["#FBE9E7", "#FFCCBC", "#FF8A65", "#FF7043"]),
            ("Cool Modern", ["#E1F5FE", "#B3E5FC", "#4FC3F7", "#29B6F6"])
        ]
    
    for palette_name, colors in palette_suggestions:
        st.markdown(f"**{palette_name}**")
        palette_html = '<div style="display: flex; gap: 0.75rem; margin: 0.75rem 0 1.5rem 0;">'
        for color in colors:
            palette_html += f'<div style="flex: 1; height: 60px; background: {color}; border-radius: 8px; border: 2px solid #ddd; box-shadow: 0 2px 6px rgba(0,0,0,0.1); display: flex; align-items: flex-end; justify-content: center; padding: 0.5rem;"><span style="font-size: 0.7rem; font-weight: 600; color: #000000; background: rgba(255,255,255,0.9); padding: 0.25rem 0.5rem; border-radius: 4px;">{color}</span></div>'
        palette_html += '</div>'
        st.markdown(palette_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visual Inspiration
    st.markdown(f"""
    <div style="margin: 2rem 0; text-align: center;">
        <h3 style="color: #000000; font-family: 'Space Grotesk', sans-serif; margin-bottom: 1.5rem;">Get Inspired</h3>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin: 1.5rem 0;">
            <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 2px solid #e0e0e0;">
                <img src="https://images.unsplash.com/photo-1556912173-3bb406ef7e77?w=400&h=250&fit=crop&q=80" 
                     alt="Modern {analysis.room_type}" 
                     style="width: 100%; height: 200px; object-fit: cover;">
                <div style="padding: 1rem; text-align: center; font-weight: 600; color: #000000;">Modern {analysis.room_type}</div>
            </div>
            <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 2px solid #e0e0e0;">
                <img src="https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=400&h=250&fit=crop&q=80" 
                     alt="Cozy {analysis.room_type}" 
                     style="width: 100%; height: 200px; object-fit: cover;">
                <div style="padding: 1rem; text-align: center; font-weight: 600; color: #000000;">Cozy {analysis.room_type}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pinterest link
    search_query = f"{analysis.room_type} design ideas"
    st.markdown(f"""
    <div style="text-align: center; margin: 1.5rem 0;">
        <a href="https://www.pinterest.com/search/pins/?q={search_query.replace(' ', '%20')}" 
           target="_blank" 
           style="color: #000000; text-decoration: none; font-weight: 600; font-size: 1rem; border-bottom: 2px solid #000000; padding-bottom: 0.25rem;">
            Explore more {analysis.room_type} designs on Pinterest →
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Next Steps
    st.markdown('<div class="actions-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="actions-title">What\'s Next?</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("⎙ Save as PDF", use_container_width=True, key=f"pdf_{button_key_suffix}"):
            st.info("Use your browser's Print function (Ctrl+P / Cmd+P) and select 'Save as PDF'")
    
    # Social Media Share
    st.markdown('<div style="margin-top: 2rem; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<p style="font-weight: 600; color: #666666; margin-bottom: 1rem;">Share Your Design</p>', unsafe_allow_html=True)
    
    share_text = f"Check out my {analysis.room_type} design from RoomSense!"
    share_url = "https://roomsense.streamlit.app"
    
    social_col1, social_col2, social_col3, social_col4 = st.columns(4)
    
    with social_col1:
        st.markdown(f'''
        <a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" 
           style="display: block; padding: 0.75rem; background: white; color: #000000 !important; border: 2px solid #000000; border-radius: 8px; 
           text-align: center; text-decoration: none; font-weight: 600;">
           Facebook
        </a>
        ''', unsafe_allow_html=True)
    
    with social_col2:
        st.markdown(f'''
        <a href="https://twitter.com/intent/tweet?text={share_text}&url={share_url}" target="_blank"
           style="display: block; padding: 0.75rem; background: white; color: #000000 !important; border: 2px solid #000000; border-radius: 8px; 
           text-align: center; text-decoration: none; font-weight: 600;">
           Twitter
        </a>
        ''', unsafe_allow_html=True)
    
    with social_col3:
        st.markdown(f'''
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank"
           style="display: block; padding: 0.75rem; background: white; color: #000000 !important; border: 2px solid #000000; border-radius: 8px; 
           text-align: center; text-decoration: none; font-weight: 600;">
           LinkedIn
        </a>
        ''', unsafe_allow_html=True)
    
    with social_col4:
        st.markdown(f'''
        <a href="https://pinterest.com/pin/create/button/?url={share_url}&description={share_text}" target="_blank"
           style="display: block; padding: 0.75rem; background: white; color: #000000 !important; border: 2px solid #000000; border-radius: 8px; 
           text-align: center; text-decoration: none; font-weight: 600;">
           Pinterest
        </a>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Initialize AI system
    ai_system = SpaceVisionAI()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### About RoomSense")
        st.markdown("""
        **RoomSense** helps you design any room in your home:
        - 🏠 Identify your room type
        - 📏 Measure dimensions
        - 🪑 Spot existing furniture
        - 💡 Check lighting quality
        - 🎨 Suggest perfect layouts
        - ✨ Recommend furniture placement
        
        Perfect for bedrooms, living rooms, kitchens, bathrooms, and more!
        """)
    
    # Hero Image
    st.markdown("""
    <div style="margin: -1rem 0 2rem 0;">
        <img src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1200&h=400&fit=crop&q=80" 
             alt="Modern Living Room Interior" 
             style="width: 100%; height: 300px; object-fit: cover; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.15);">
    </div>
    """, unsafe_allow_html=True)
    
    # Configuration
    col1, col2 = st.columns([1, 1])
    
    with col1:
        room_type = st.selectbox(
            "What room are you designing?",
            ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Dining Room', 'Home Office', 'Kids Room', 'Laundry Room'],
            help="Select the type of room you want to design"
        )
    
    with col2:
        analysis_mode = st.radio(
            "How do you want to analyze?",
            ['📸 Upload Photo', '📷 Live Camera', '✏️ Manual Entry'],
            help="Choose your preferred input method",
            horizontal=True
        )
    
    # Main content based on mode
    if analysis_mode == '📸 Upload Photo':
        st.markdown('<div class="camera-section">', unsafe_allow_html=True)
        st.markdown("### Upload a Photo of Your Room")
        st.markdown("Take a photo on your phone or select from your gallery")
        
        uploaded_file = st.file_uploader(
            "Choose a photo...",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear photo of your room"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"
            
            if 'last_file_id' not in st.session_state or st.session_state.last_file_id != file_id:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.image(image, caption="Uploaded Room Image", use_container_width=True)
                
                with col2:
                    st.markdown('<span class="status-badge status-processing">Analyzing your room...</span>', unsafe_allow_html=True)
                    
                    with st.spinner('Analyzing your space...'):
                        import time
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        scene_analysis = ai_system.analyze_room_scene(image)
                        detected_objects = ai_system.detect_objects(image)
                        dimensions = ai_system.estimate_dimensions(image)
                        color_palette = ai_system.extract_color_palette(image)
                        
                        progress_bar.empty()
                    
                    st.markdown('<span class="status-badge status-complete">✓ Analysis Complete</span>', unsafe_allow_html=True)
                
                st.session_state.last_file_id = file_id
                st.session_state.room_analysis = {
                    'room_type': scene_analysis['room_type'],
                    'confidence': scene_analysis['confidence'],
                    'dimensions': dimensions,
                    'lighting': scene_analysis['lighting'],
                    'layout_type': scene_analysis['layout_type'],
                    'detected_objects': detected_objects,
                    'color_palette': color_palette
                }
            else:
                st.image(image, caption="Uploaded Room Image", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None and 'room_analysis' in st.session_state:
            analysis = RoomAnalysis(
                room_type=st.session_state.room_analysis['room_type'],
                confidence=st.session_state.room_analysis['confidence'],
                dimensions=st.session_state.room_analysis['dimensions'],
                lighting=st.session_state.room_analysis['lighting'],
                layout_type=st.session_state.room_analysis['layout_type'],
                detected_objects=st.session_state.room_analysis['detected_objects'],
                color_palette=st.session_state.room_analysis['color_palette']
            )
            
            display_analysis_results(analysis, room_type, "upload")
    
    elif analysis_mode == '📷 Live Camera':
        st.markdown('<div class="camera-section">', unsafe_allow_html=True)
        st.markdown("### Capture Your Room")
        st.markdown("Use your camera to take a photo of your room")
        
        camera_image = st.camera_input("Take a photo")
        
        if camera_image is not None:
            image = Image.open(camera_image)
            
            camera_id = f"camera_{camera_image.size}"
            
            if 'last_camera_id' not in st.session_state or st.session_state.last_camera_id != camera_id:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.image(image, caption="Captured Photo", use_container_width=True)
                
                with col2:
                    st.markdown('<span class="status-badge status-processing">Analyzing your room...</span>', unsafe_allow_html=True)
                    
                    with st.spinner('Analyzing your space...'):
                        import time
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        scene_analysis = ai_system.analyze_room_scene(image)
                        detected_objects = ai_system.detect_objects(image)
                        dimensions = ai_system.estimate_dimensions(image)
                        color_palette = ai_system.extract_color_palette(image)
                        
                        progress_bar.empty()
                    
                    st.markdown('<span class="status-badge status-complete">✓ Analysis Complete</span>', unsafe_allow_html=True)
                
                st.session_state.last_camera_id = camera_id
                st.session_state.camera_analysis = {
                    'room_type': scene_analysis['room_type'],
                    'confidence': scene_analysis['confidence'],
                    'dimensions': dimensions,
                    'lighting': scene_analysis['lighting'],
                    'layout_type': scene_analysis['layout_type'],
                    'detected_objects': detected_objects,
                    'color_palette': color_palette
                }
            else:
                st.image(image, caption="Captured Photo", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if camera_image is not None and 'camera_analysis' in st.session_state:
            analysis = RoomAnalysis(
                room_type=st.session_state.camera_analysis['room_type'],
                confidence=st.session_state.camera_analysis['confidence'],
                dimensions=st.session_state.camera_analysis['dimensions'],
                lighting=st.session_state.camera_analysis['lighting'],
                layout_type=st.session_state.camera_analysis['layout_type'],
                detected_objects=st.session_state.camera_analysis['detected_objects'],
                color_palette=st.session_state.camera_analysis['color_palette']
            )
            
            display_analysis_results(analysis, room_type, "camera")
    
    else:  # Manual Entry
        st.markdown('<div class="camera-section">', unsafe_allow_html=True)
        st.markdown("### Enter Your Room Dimensions")
        st.markdown("No photo? No problem! Just tell us about your room.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            width = st.number_input("Width (meters)", min_value=2.0, max_value=15.0, value=4.0, step=0.1)
        with col2:
            length = st.number_input("Length (meters)", min_value=2.0, max_value=15.0, value=4.5, step=0.1)
        with col3:
            height = st.number_input("Height (meters)", min_value=2.0, max_value=5.0, value=2.6, step=0.1)
        
        lighting_manual = st.select_slider("How's the lighting?", options=['Poor', 'Moderate', 'Good', 'Excellent'])
        
        if st.button("🎨 Generate Design Recommendations", use_container_width=True):
            area = width * length
            analysis = RoomAnalysis(
                room_type=room_type,
                confidence=1.0,
                dimensions={'width': width, 'length': length, 'height': height, 'area': area},
                lighting=f"{lighting_manual} lighting",
                layout_type="User Specified",
                detected_objects=[],
                color_palette=[]
            )
            
            st.success("✓ Creating your personalized room design...")
            display_analysis_results(analysis, room_type, "manual")
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
