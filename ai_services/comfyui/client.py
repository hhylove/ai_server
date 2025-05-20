import requests
import json
import logging
from typing import Optional, Dict, Any, List, BinaryIO
from ..config import Config

logger = logging.getLogger(__name__)

class ComfyUIClient:
    """ComfyUI API 客户端"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化 ComfyUI 客户端
        
        参数:
            base_url: ComfyUI 服务器地址
            api_key: API 密钥
        """
        self.base_url = (base_url or Config.COMFYUI_API_BASE).rstrip('/')
        self.api_key = api_key if api_key is not None else Config.COMFYUI_API_KEY

    def _headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def submit_prompt(self, prompt: dict, client_id: Optional[str] = None) -> str:
        """
        提交提示词到 ComfyUI
        
        参数:
            prompt: 提示词数据
            client_id: 可选的客户端 ID
            
        返回:
            提示词 ID 或任务 ID
        """
        url = f"{self.base_url}/prompt"
        data = {"prompt": prompt}
        if client_id:
            data["client_id"] = client_id
            
        resp = requests.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        response_data = resp.json()
        return response_data.get("prompt_id") or response_data.get("task_id")

    def get_history(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务历史记录
        
        参数:
            task_id: 任务 ID
            
        返回:
            任务历史数据
        """
        url = f"{self.base_url}/history/{task_id}"
        logger.info(f"获取任务历史记录: {task_id}")
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def upload_image(self, image_file: BinaryIO, filename: Optional[str] = None) -> dict:
        """
        上传图片到 ComfyUI
        
        参数:
            image_file: 图片文件对象
            filename: 可选的文件名
            
        返回:
            上传结果信息
        """
        url = f"{self.base_url}/upload/image"
        files = {"image": (filename or "image.jpg", image_file, "image/jpeg")}
        
        resp = requests.post(url, files=files)
        resp.raise_for_status()
        return resp.json()

    def get_image(self, filename: str) -> bytes:
        """
        根据文件名获取图片
        
        参数:
            filename: 图片文件名
            
        返回:
            图片数据
        """
        url = f"{self.base_url}/view/{filename}"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.content

    def list_files(self) -> List[Dict[str, Any]]:
        """
        列出已上传的文件
        
        返回:
            文件信息列表
        """
        url = f"{self.base_url}/upload"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def delete_file(self, filename: str) -> Dict[str, Any]:
        """
        删除文件
        
        参数:
            filename: 要删除的文件名
            
        返回:
            删除结果
        """
        url = f"{self.base_url}/upload/{filename}"
        resp = requests.delete(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_system_stats(self) -> Dict[str, Any]:
        """
        获取系统统计信息
        
        返回:
            系统统计信息
        """
        url = f"{self.base_url}/system/stats"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json() 