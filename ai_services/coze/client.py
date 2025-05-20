import requests
import json
import logging
from typing import Dict, Any, Optional, List
from ..config import Config

logger = logging.getLogger(__name__)

class CozeClient:
    """Coze API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Coze 客户端
        
        参数:
            api_key: API 密钥
        """
        self.api_key = api_key or Config.COZE_API_KEY
        self.base_url = Config.COZE_API_BASE

    def _headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def run_workflow(self, workflow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行工作流
        
        参数:
            workflow_id: 工作流 ID
            inputs: 输入参数
            
        返回:
            工作流结果
        """
        url = f"{self.base_url}/workflows/{workflow_id}/run"
        data = {"inputs": inputs}
        
        resp = requests.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        获取工作流信息
        
        参数:
            workflow_id: 工作流 ID
            
        返回:
            工作流信息
        """
        url = f"{self.base_url}/workflows/{workflow_id}"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        列出可用的工作流
        
        返回:
            工作流信息列表
        """
        url = f"{self.base_url}/workflows"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json() 