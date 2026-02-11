# MagicWord 服务端 (MagicWord Server)

这是 MagicWord 安卓 App 的后台服务端，用于管理 API 密钥、模型名称以及分发默认词库配置。

## 功能特性
- **管理后台**: 提供 Web 界面配置 AI 设置和上传默认词库。
- **API 接口**: 提供 `/api/init-config` 接口供 App 获取初始化配置。
- **配置存储**: 配置信息本地存储于 `config.json`。

## 安装与运行

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **运行服务器**:
   ```bash
   python app.py
   ```
   默认运行在 `0.0.0.0:5000`。

## API 文档

### 获取初始化配置
- **接口地址**: `/api/init-config`
- **请求方法**: `GET`
- **响应示例**:
  ```json
  {
    "api_key": "sk-...",
    "model_name": "Qwen/Qwen2.5-7B-Instruct",
    "default_library": [ ... ] // 词库数据的 JSON 对象或数组
  }
  ```

## 管理后台登录
- **访问地址**: `/login` 或 `/admin`
- **默认用户名**: `upxuu`
- **默认密码**: `lijiaxu2011`

## 部署说明 (PythonAnywhere)
本项目基于 Flask，可直接部署在 PythonAnywhere 等平台。
1. 上传代码至服务器。
2. 配置 WSGI 文件指向 `app.py` 中的 `app` 对象。
3. 确保 `templates` 目录与 `app.py` 在同一层级。
