import json
import copy
import time
import os
from typing import Dict, Any, List, Optional
from .client import ComfyUIClient

def load_workflow_template(json_filename: str) -> dict:
    """
    从 JSON 文件加载工作流模板
    
    参数:
        json_filename: JSON 文件路径
        
    返回:
        工作流模板
    """
    with open(json_filename, "r", encoding="utf-8") as f:
        return json.load(f)

def build_prompt(template: dict, image_urls: dict, extra_params: Optional[dict] = None) -> dict:
    """
    根据模板和参数构建提示词
    
    参数:
        template: 工作流模板
        image_urls: 图片 URL 映射
        extra_params: 额外参数
        
    返回:
        构建的提示词
    """
    prompt = copy.deepcopy(template)
    for node_id, data in image_urls.items():
        field = data.get("field", "url")
        value = data.get("value")
        prompt[node_id]["inputs"][field] = value
        
    if extra_params:
        for node_id, params in extra_params.items():
            prompt[node_id]["inputs"].update(params)
            
    return prompt

def submit_and_wait(client: ComfyUIClient, prompt: dict, timeout: int = 300) -> dict:
    """
    提交提示词并等待完成
    
    参数:
        client: ComfyUI 客户端
        prompt: 要提交的提示词
        timeout: 最大等待时间（秒）
        
    返回:
        输出数据
        
    异常:
        TimeoutError: 如果处理时间过长
    """
    prompt_id = client.submit_prompt(prompt)
    start_time = time.time()
    
    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError("处理超时")
            
        time.sleep(1)
        history = client.get_history(prompt_id)
        result = history.get(prompt_id, {})
        status = result.get("status", {})
        outputs = result.get("outputs", {})
        
        if status.get("status_str") == "success" and outputs:
            return outputs

def collect_image_urls(outputs: dict, base_url: str) -> List[str]:
    """
    从输出中收集图片 URL
    
    参数:
        outputs: 输出数据
        base_url: 图片基础 URL
        
    返回:
        图片 URL 列表
    """
    image_filenames = []
    for node in outputs.values():
        if 'images' in node and isinstance(node['images'], list):
            for img in node['images']:
                if 'filename' in img:
                    image_filenames.append(img['filename'])
    return [f"{base_url}/view?filename={fname}" for fname in image_filenames]

def collect_video_urls(outputs: dict, base_url: str) -> List[Dict[str, Any]]:
    """
    从输出中收集视频 URL
    
    参数:
        outputs: 输出数据
        base_url: 视频基础 URL
        
    返回:
        视频信息列表
    """
    video_urls = []
    for node in outputs.values():
        if 'gifs' in node and isinstance(node['gifs'], list):
            for video in node['gifs']:
                if 'filename' in video:
                    video_urls.append({
                        'url': f"{base_url}/view?filename={video['filename']}",
                        'format': video.get('format', 'video/h264-mp4'),
                        'frame_rate': video.get('frame_rate', 16.0),
                        'filename': video['filename']
                    })
    return video_urls 