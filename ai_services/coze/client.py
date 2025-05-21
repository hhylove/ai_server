import requests
import json
import logging
from typing import Dict, Any, Optional, List
from ..config import Config
from fastapi import UploadFile, HTTPException

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
        url = f"{self.base_url}/v1/workflow/run"
        data = {
        "parameters": {
            "input": inputs
        },
        "workflow_id": workflow_id
    }
        
        resp = requests.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return resp.json()
    


        
    def upload_file_to_coze(self, file: UploadFile) -> str:
        files = {'file': (file.filename, file.file, file.content_type)}
        url = f"{self.base_url}/v1/files/upload"
        response = requests.post(url, files=files, hheaders=self._headers())
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="上传到Coze失败")
        resp_json = response.json()
        if resp_json.get("code") != 0:
            raise HTTPException(status_code=500, detail=f"Coze上传失败: {resp_json.get('msg')}")
        return resp_json["data"]["id"]

    def run_file_workflow(self, file_id: str, workflow_id: str, input_key: str = "file_id") -> str:
        payload = {
            "parameters": {
                "input": f'{{\"{input_key}\": \"{file_id}\"}}'
            },
            "workflow_id": workflow_id
        }
        url = f"{self.base_url}/v1/workflow/run"
        response = requests.post(url, json=payload, headers=self._headers())
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="调用Coze工作流失败")
        resp_json = response.json()
        if resp_json.get("code") != 0:
            raise HTTPException(status_code=500, detail=f"Coze工作流失败: {resp_json.get('msg')}")
        import json as pyjson
        output = pyjson.loads(resp_json["data"])["output"]
        return output
