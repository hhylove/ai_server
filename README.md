# AI 服务库

一个用于与 AI 服务（包括 ComfyUI 和 Coze）交互的 Python 库。

## 安装

```bash
pip install ai-services
```

## 使用方法

### ComfyUI 客户端

```python
from ai_services.comfyui import ComfyUIClient

# 初始化客户端
client = ComfyUIClient(base_url="http://your-comfyui-server")

# 上传图片
with open("image.jpg", "rb") as f:
    result = client.upload_image(f)

# 提交提示词
prompt_id = client.submit_prompt({"your": "prompt"})

# 获取历史记录
history = client.get_history(prompt_id)
```

### Coze 客户端

```python
from ai_services.coze import CozeClient

# 初始化客户端
client = CozeClient(api_key="your-api-key")

# 运行工作流
result = client.run_workflow(
    workflow_id="your-workflow-id",
    inputs={"text": "你好，世界！"}
)
```

## 开发指南

1. 克隆仓库
2. 安装开发依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行测试：
   ```bash
   pytest
   ```

## 许可证

MIT 许可证 