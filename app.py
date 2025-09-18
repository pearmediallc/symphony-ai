# app.py
import os
import requests
from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for, render_template_string
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TIKTOK_BASE = "https://business-api.tiktok.com/open_api/v1.3"

app = Flask(__name__, static_url_path="", static_folder="static")
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here-change-this')

# Get auth credentials and API settings from environment
AUTH_USERNAME = os.getenv('AUTH_USERNAME', 'admin')
AUTH_PASSWORD = os.getenv('AUTH_PASSWORD', 'password')
TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_ACCESS_TOKEN', '')
TIKTOK_ADVERTISER_ID = os.getenv('TIKTOK_ADVERTISER_ID', '')

def tt_headers(access_token: str, content_type="application/json"):
    return {
        "Access-Token": access_token,
        "Content-Type": content_type
    }

# Login HTML template
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>Login - TikTok Symphony AI Studio</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            width: 90%;
            max-width: 400px;
        }
        h1 {
            font-size: 2rem;
            background: linear-gradient(135deg, #FF004F, #00F2EA);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 32px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e1e1e2;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #FF004F;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #FF004F, #00F2EA);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(255, 0, 79, 0.3);
        }
        .error {
            background: #fee;
            color: #c00;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        .icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #FF004F, #00F2EA);
            border-radius: 15px;
            margin: 0 auto 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="icon">🎬</div>
        <h1>TikTok Symphony AI</h1>
        <p class="subtitle">Sign in to continue</p>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="post">
            <label for="username">Username</label>
            <input type="text" id="username" name="username" required autofocus />

            <label for="password">Password</label>
            <input type="password" id="password" name="password" required />

            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>
'''

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(force=True) if request.is_json else request.form
        username = data.get('username', '')
        password = data.get('password', '')

        if username == AUTH_USERNAME and password == AUTH_PASSWORD:
            session['logged_in'] = True
            if request.is_json:
                return jsonify({"success": True, "message": "Login successful"}), 200
            return redirect(url_for('home'))
        else:
            if request.is_json:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401
            return render_template_string(LOGIN_HTML, error="Invalid username or password")

    return render_template_string(LOGIN_HTML)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route("/")
@login_required
def home():
    return send_from_directory("static", "index.html")

@app.route("/script_generator")
@app.route("/script_generator/")
@login_required
def script_generator():
    return send_from_directory("static/script_generator", "index.html")

@app.route("/avatar")
@app.route("/avatar/")
@login_required
def avatar():
    return send_from_directory("static/avatar", "index.html")

@app.route('/api/get_config')
@login_required
def get_config():
    """Return configuration values from environment"""
    return jsonify({
        "access_token": TIKTOK_ACCESS_TOKEN,
        "advertiser_id": TIKTOK_ADVERTISER_ID
    }), 200

@app.post("/api/create_task")
@login_required
def create_task():
    """
    Body JSON:
    {
      "access_token": "...",
      "mode": "CUSTOM" | "PRODUCT",
      "custom_prompt": "...",                # when CUSTOM
      "script_generation_count": 3,          # 1..8
      "script_info": { ... },                # tone/style/pov/lang/industry (optional)
      "product_info": { ... },               # when PRODUCT
      "media_list": { "video_id_list": [], "image_url_list": [] },  # optional for PRODUCT
      "video_duration": "15S" | "30S"        # optional
    }
    """
    data = request.get_json(force=True) or {}

    # Debug logging
    print(f"Received data: {data}")

    # Use access token from environment if not provided
    access_token = data.get("access_token", "").strip() or TIKTOK_ACCESS_TOKEN
    mode = data.get("mode", "CUSTOM")

    if not access_token:
        return jsonify({"error": "Missing access_token"}), 400

    payload = {
        "script_generation_count": data.get("script_generation_count", 3),
    }

    # Attach mode-specific fields
    if mode.upper() == "CUSTOM":
        payload["script_source"] = "CUSTOM"
        custom_prompt = data.get("custom_prompt", "").strip()

        print(f"Custom prompt received: {custom_prompt}")

        if not custom_prompt:
            return jsonify({
                "error": "custom_prompt is required for CUSTOM mode",
                "details": f"Received data keys: {list(data.keys())}"
            }), 400
        payload["custom_prompt"] = custom_prompt
        # Note: script_info is NOT allowed for CUSTOM mode per TikTok API
    else:
        payload["script_source"] = "PRODUCT"
        # script_info is only used for PRODUCT mode
        payload["script_info"] = data.get("script_info") or {
            "tone": "Friendly",
            "style": "Product focused",
            "point_of_view": "From consumer",
            "script_language": "en",
            "relevant_industry": "All"
        }
        product_info = data.get("product_info")
        if not product_info:
            return jsonify({"error": "product_info is required for PRODUCT mode"}), 400
        payload["product_info"] = product_info
        media_list = data.get("media_list")
        if media_list:
            payload["media_list"] = media_list
        vd = data.get("video_duration")
        if vd in ("15S", "30S"):
            payload["video_duration"] = vd

    try:
        print(f"Sending payload to TikTok API: {payload}")
        r = requests.post(
            f"{TIKTOK_BASE}/creative/aigc/script_generation/task/create/",
            headers=tt_headers(access_token),
            json=payload,
            timeout=30,
        )
        response_data = r.json()
        print(f"TikTok API response: {response_data}")

        # If TikTok API returns an error, provide more context
        # TikTok API returns code as string "0" for success
        if r.status_code != 200 or str(response_data.get("code")) != "0":
            error_response = {
                "error": "TikTok API Error",
                "message": response_data.get("message", "Unknown error"),
                "code": response_data.get("code"),
                "details": f"Status: {r.status_code}, Code: {response_data.get('code')}",
                "request_payload": payload,
                "tiktok_response": response_data
            }
            return jsonify(error_response), r.status_code if r.status_code != 200 else 400

        return jsonify(response_data), r.status_code
    except requests.RequestException as e:
        print(f"Request exception: {str(e)}")
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.get("/api/task_status")
@login_required
def task_status():
    """
    Query params:
      access_token=...
      task_id=...
    """
    access_token = (request.args.get("access_token") or "").strip() or TIKTOK_ACCESS_TOKEN
    task_id = (request.args.get("task_id") or "").strip()
    if not access_token or not task_id:
        return jsonify({"error": "access_token and task_id are required"}), 400

    try:
        r = requests.get(
            f"{TIKTOK_BASE}/creative/aigc/script/task/get/",
            headers={"Access-Token": access_token},
            params={"task_id": task_id},
            timeout=30,
        )
        return jsonify(r.json()), r.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/list_scripts")
@login_required
def list_scripts():
    """
    Query params:
      access_token=...
      page=1
      page_size=20
    """
    access_token = (request.args.get("access_token") or "").strip() or TIKTOK_ACCESS_TOKEN
    if not access_token:
        return jsonify({"error": "access_token is required"}), 400
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))

    try:
        r = requests.get(
            f"{TIKTOK_BASE}/creative/aigc/script/list/",
            headers={"Access-Token": access_token},
            params={"page": page, "page_size": page_size},
            timeout=30,
        )
        return jsonify(r.json()), r.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/get_avatars")
@login_required
def get_avatars():
    """
    Get available digital avatars.
    Query params:
      access_token=...
      page=1 (optional)
      page_size=10 (optional)
    """
    access_token = (request.args.get("access_token") or "").strip() or TIKTOK_ACCESS_TOKEN
    if not access_token:
        return jsonify({"error": "access_token is required"}), 400

    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))

    try:
        r = requests.get(
            f"{TIKTOK_BASE}/creative/digital_avatar/get/",
            headers={"Access-Token": access_token},
            params={"page": page, "page_size": page_size},
            timeout=30,
        )
        return jsonify(r.json()), r.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/create_avatar_video_task")
@login_required
def create_avatar_video_task():
    """
    Create digital avatar video tasks.
    Body JSON:
    {
      "access_token": "...",
      "material_packages": [
        {
          "avatar_id": "...",
          "script": "...",
          "video_name": "..." (optional),
          "package_id": "..." (optional)
        }
      ]
    }
    """
    data = request.get_json(force=True) or {}
    access_token = data.get("access_token", "").strip() or TIKTOK_ACCESS_TOKEN
    material_packages = data.get("material_packages", [])

    if not access_token:
        return jsonify({"error": "Missing access_token"}), 400
    if not material_packages:
        return jsonify({"error": "material_packages is required"}), 400

    # Validate material packages
    for package in material_packages:
        if not package.get("avatar_id"):
            return jsonify({"error": "avatar_id is required in material_packages"}), 400
        if not package.get("script"):
            return jsonify({"error": "script is required in material_packages"}), 400

    payload = {"material_packages": material_packages}

    try:
        r = requests.post(
            f"{TIKTOK_BASE}/creative/digital_avatar/video/task/create/",
            headers=tt_headers(access_token),
            json=payload,
            timeout=30,
        )
        return jsonify(r.json()), r.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/get_avatar_video_task_status")
@login_required
def get_avatar_video_task_status():
    """
    Get the results of digital avatar video tasks.
    Query params:
      access_token=...
      task_ids=["task1","task2",...] (JSON array as string)
    """
    access_token = (request.args.get("access_token") or "").strip() or TIKTOK_ACCESS_TOKEN
    task_ids_str = (request.args.get("task_ids") or "").strip()

    if not access_token:
        return jsonify({"error": "access_token is required"}), 400
    if not task_ids_str:
        return jsonify({"error": "task_ids is required"}), 400

    try:
        # Parse task_ids JSON array
        import json
        task_ids = json.loads(task_ids_str)
        if not isinstance(task_ids, list):
            return jsonify({"error": "task_ids must be a JSON array"}), 400
    except (json.JSONDecodeError, Exception) as e:
        return jsonify({"error": f"task_ids must be a valid JSON array: {str(e)}"}), 400

    try:
        r = requests.get(
            f"{TIKTOK_BASE}/creative/digital_avatar/video/task/get/",
            headers={"Access-Token": access_token},
            params={"task_ids": task_ids_str},
            timeout=30,
        )
        return jsonify(r.json()), r.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/list_avatar_videos")
@login_required
def list_avatar_videos():
    """
    Get digital avatar videos under your account.
    Query params:
      access_token=...
      avatar_id=... (optional)
      start_date=YYYY-MM-DD (optional)
      end_date=YYYY-MM-DD (optional)
      page=1 (optional)
      page_size=10 (optional)
    """
    access_token = (request.args.get("access_token") or "").strip() or TIKTOK_ACCESS_TOKEN
    if not access_token:
        return jsonify({"error": "access_token is required"}), 400

    # Build filtering object
    filtering = {}
    avatar_id = request.args.get("avatar_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if avatar_id:
        filtering["avatar_id"] = avatar_id
    if start_date:
        filtering["start_date"] = start_date
    if end_date:
        filtering["end_date"] = end_date

    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))

    params = {"page": page, "page_size": page_size}
    if filtering:
        params["filtering"] = filtering

    try:
        r = requests.get(
            f"{TIKTOK_BASE}/creative/digital_avatar/video/list/",
            headers={"Access-Token": access_token},
            params=params,
            timeout=30,
        )
        return jsonify(r.json()), r.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/update_avatar_video_name")
@login_required
def update_avatar_video_name():
    """
    Update the name of a digital avatar video.
    Body JSON:
    {
      "access_token": "...",
      "avatar_video_id": "...",
      "file_name": "..."
    }
    """
    data = request.get_json(force=True) or {}
    access_token = data.get("access_token", "").strip() or TIKTOK_ACCESS_TOKEN
    avatar_video_id = data.get("avatar_video_id", "").strip()
    file_name = data.get("file_name", "").strip()

    if not access_token:
        return jsonify({"error": "Missing access_token"}), 400
    if not avatar_video_id:
        return jsonify({"error": "Missing avatar_video_id"}), 400
    if not file_name:
        return jsonify({"error": "Missing file_name"}), 400

    payload = {
        "avatar_video_id": avatar_video_id,
        "file_name": file_name
    }

    try:
        r = requests.post(
            f"{TIKTOK_BASE}/file/video/ad/update/",
            headers=tt_headers(access_token),
            json=payload,
            timeout=30,
        )
        return jsonify(r.json()), r.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/get_video_info")
@login_required
def get_video_info():
    """
    Get detailed information about specific videos including thumbnail URLs
    Query params:
      access_token=...
      advertiser_id=...
      video_ids=["video_id1","video_id2"] (JSON array as string)
    """
    access_token = (request.args.get("access_token") or "").strip() or TIKTOK_ACCESS_TOKEN
    advertiser_id = (request.args.get("advertiser_id") or "").strip() or TIKTOK_ADVERTISER_ID
    video_ids_str = (request.args.get("video_ids") or "").strip()

    if not access_token or not advertiser_id or not video_ids_str:
        return jsonify({"error": "access_token, advertiser_id and video_ids are required"}), 400

    try:
        import json
        video_ids = json.loads(video_ids_str)
        if not isinstance(video_ids, list):
            return jsonify({"error": "video_ids must be a JSON array"}), 400
    except:
        return jsonify({"error": "video_ids must be a valid JSON array"}), 400

    try:
        # v1.3 endpoint for video info
        r = requests.get(
            f"{TIKTOK_BASE}/file/video/ad/info/",
            headers={"Access-Token": access_token},
            params={
                "advertiser_id": advertiser_id,
                "video_ids": json.dumps(video_ids)
            },
            timeout=30,
        )

        response_data = r.json()
        print(f"Video info response: {response_data}")

        return jsonify(response_data), r.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/get_assets_videos")
@login_required
def get_assets_videos():
    """
    Get videos from TikTok Ads assets library.
    Query params:
      access_token=...
      advertiser_id=...
      page=1 (optional)
      page_size=20 (optional)
    """
    access_token = (request.args.get("access_token") or "").strip() or TIKTOK_ACCESS_TOKEN
    advertiser_id = (request.args.get("advertiser_id") or "").strip() or TIKTOK_ADVERTISER_ID

    if not access_token:
        return jsonify({"error": "access_token is required"}), 400
    if not advertiser_id:
        return jsonify({"error": "advertiser_id is required"}), 400

    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))

    try:
        params = {
            "advertiser_id": advertiser_id,
            "page": page,
            "page_size": page_size
        }

        print(f"Fetching videos with params: {params}")

        r = requests.get(
            f"{TIKTOK_BASE}/file/video/ad/search/",
            headers={"Access-Token": access_token},
            params=params,
            timeout=30,
        )

        response_data = r.json()
        print(f"TikTok video search response: {response_data}")

        return jsonify(response_data), r.status_code
    except requests.RequestException as e:
        print(f"Request error in get_assets_videos: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Video/Image upload endpoints have been removed as per requirements




if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
