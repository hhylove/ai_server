import os
from typing import Optional

class Config:
    """AI 服务配置"""
    
    # ComfyUI 配置
    COMFYUI_API_BASE: str = os.getenv("COMFYUI_API_BASE", "http://localhost:8188")
    COMFYUI_API_KEY: Optional[str] = os.getenv("COMFYUI_API_KEY")
    
    # Coze 配置
    COZE_API_BASE: str = os.getenv("COZE_API_BASE", "https://api.coze.cn")
    COZE_API_KEY: Optional[str] = os.getenv("COZE_API_KEY")
    COZE_ZH_EN_WORKFLOW_ID: str = os.getenv("COZE_ZH_EN_WORKFLOW_ID", "") 