import os
from ai_services.comfyui import ComfyUIClient
from ai_services.comfyui.utils import load_workflow_template, build_prompt, submit_and_wait, collect_image_urls
from ai_services.coze import CozeClient

def main():
    # 初始化客户端
    comfyui_client = ComfyUIClient()
    coze_client = CozeClient()
    
    # 加载工作流模板
    workflow_template = load_workflow_template("json/图片编辑.json")
    
    # 处理图片
    with open("input.jpg", "rb") as f:
        # 上传图片
        upload_info = comfyui_client.upload_image(f)
        filename = upload_info["name"]
        
        # 准备图片 URL
        image_urls = {
            "2": {  # 图片节点 ID
                "field": "image",
                "value": filename
            }
        }
        
        # 翻译编辑文本
        edit_text = "把裙子改成红色"
        translated_text = coze_client.run_workflow(
            workflow_id=os.getenv("COZE_ZH_EN_WORKFLOW_ID"),
            inputs={"text": edit_text}
        )["output"]
        
        # 设置编辑文本
        image_urls["74"] = {  # 文本节点 ID
            "field": "text",
            "value": translated_text
        }
        
        # 构建并提交提示词
        prompt = build_prompt(workflow_template, image_urls)
        outputs = submit_and_wait(comfyui_client, prompt)
        
        # 收集结果
        image_urls = collect_image_urls(outputs, comfyui_client.base_url)
        print(f"生成的图片: {image_urls}")

if __name__ == "__main__":
    main() 