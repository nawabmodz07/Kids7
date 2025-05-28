import asyncio
import os
import re
from telebot import TeleBot, types
from telebot.async_telebot import AsyncTeleBot
from pyrogram import Client as UserClient

API_ID = 21845583
API_HASH = "081a3cc51a428ad292be0be4d4f4f975"
BOT_TOKEN = "7671610944:AAH2TxpFytq-c9pfrRutLapvdG8wa4DZpsI"
SESSION_NAME = "my_account"
TARGET_BOT = "@dopayu_bot"

userbot = UserClient(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
bot = AsyncTeleBot(BOT_TOKEN)

# Extract valid CC from a line
def extract_cc(text):
    pattern = r"(\d{12,16})[^\d\n]?(\d{2})[^\d\n]?(\d{2,4})[^\d\n]?(\d{3,4})"
    match = re.search(pattern, text.replace(" ", "").replace("\n", ""))
    if match:
        cc, mm, yy, cvv = match.groups()
        if len(yy) == 4: yy = yy[2:]  # Convert YYYY to YY
        return f"{cc}|{mm}|{yy}|{cvv}"
    return None

# === /start Command ===
@bot.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await bot.reply_to(
        message,
        "⟡ Wᴇʟᴄᴏᴍᴇ 𝘿𝘼𝙍𝙆 𝘟 𝘾𝙃𝙀𝘾𝙆𝙀𝙍 ⟡\n\n⟡ 𝗨𝗦𝗔𝗚𝗘 ⟡ \n"
        "⟡ /bt → 𝘽𝙍𝘼𝙄𝙉𝙏𝙍𝙀𝙀 𝘼𝙐𝙏𝙃 (𝙎𝙄𝙉𝙂𝙇𝙀)\n"
        "⟡ /mbt → 𝘽𝙍𝘼𝙄𝙉𝙏𝙍𝙀𝙀 𝘼𝙐𝙏𝙃 (𝙈𝘼𝙎𝙎)\n"
        "⟡ /stop ⟶ 𝙎𝙏𝙊𝙋 𝙈𝘼𝙎𝙎 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂",
        parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
async def stop_handler(message: types.Message):
    task = bot.current_task
    if task and not task.done():
        task.cancel()
        await bot.reply_to(message, "⟡ 𝙈𝘼𝙎𝙎 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 𝙎𝙏𝙊𝙋𝙋𝙀𝘿 𝘽𝙔 𝙐𝙎𝙀𝙍.")
    else:
        await bot.reply_to(message, "⟡ 𝙉𝙊 𝘼𝘾𝙏𝙄𝙑𝙀 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 𝙏𝘼𝙎𝙆 𝙏𝙊 𝙎𝙏𝙊𝙋.")

# === /bt Command ===
@bot.message_handler(commands=['bt'])
async def bt_handler(message: types.Message):
    raw = ' '.join(message.text.split()[1:]) if len(message.text.split()) > 1 else (
        message.reply_to_message.text if message.reply_to_message else '')
    cc = extract_cc(raw)

    if not cc:
        await bot.reply_to(message, "⟡ 𝗨𝗦𝗘 𝗟𝗜𝗞𝗘 ⟡  \n. ⫷ /bt cc|mm|yy|cvv", parse_mode="Markdown")
        return

    sent = await userbot.send_message(TARGET_BOT, f"/bt {cc}")
    await bot.reply_to(message, "⟡ 𝗣𝗟𝗘𝗔𝗦𝗘 𝗪𝗔𝗜𝗧 ⟡\n⟡ 𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗖𝗖...")

    for _ in range(5):
        await asyncio.sleep(10)
        msg_ = await userbot.get_messages(TARGET_BOT, sent.id + 1)
        if msg_ and msg_.text != "Processing...":
            await bot.reply_to(message, f"💳 𝙍𝙀𝙎𝙐𝙇𝙏:\n\n{msg_.text}")
            return

    await bot.reply_to(message, "⚠️ 𝗘𝗥𝗥𝗢𝗥: 𝗔𝗣𝗜 𝗙𝗔𝗜𝗟𝗘𝗗")

@bot.message_handler(commands=['mbt'])
async def mbt_handler(message: types.Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await bot.reply_to(message, "⟡ 𝗥𝗘𝗣𝗟𝗬 ⟡ /mbt 𝗜𝗡 𝗔 .txt 𝗙𝗜𝗟𝗘")

    file_info = await bot.get_file(message.reply_to_message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    
    with open('temp_cc.txt', 'wb') as f:
        f.write(downloaded_file)
    
    with open('temp_cc.txt', "r", encoding="utf-8", errors="ignore") as f:
        raw_lines = f.readlines()
    os.remove('temp_cc.txt')

    # Extract valid CCs (max 100)
    ccs = []
    for line in raw_lines:
        cc = extract_cc(line)
        if cc:
            ccs.append(cc)
        if len(ccs) == 100:
            break

    total = len(ccs)
    if total == 0:
        return await bot.reply_to(message, "⟡ 𝙉𝙊 𝙑𝘼𝙇𝙄𝘿 𝘾𝘾𝙨 𝙁𝙊𝙐𝙉𝘿 𝙄𝙉 𝙏𝙃𝙀 𝙁𝙄𝙇𝙀")

    approved = 0
    declined = 0

    def build_keyboard():
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton(f"𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅: {approved}", callback_data="noop"),
            types.InlineKeyboardButton(f"𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌: {declined}", callback_data="noop")
        )
        markup.row(
            types.InlineKeyboardButton(f"𝙏𝙊𝙏𝘼𝙇 📊: {total}", callback_data="noop")
        )
        return markup

    status_msg = await bot.reply_to(
        message,
        "⟡ 𝗣𝗟𝗘𝗔𝗦𝗘 𝗪𝗔𝗜𝗧 ⟡\n⟡ 𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗖𝗖...",
        reply_markup=build_keyboard()
    )

    # Define async task
    async def process_ccs():
        nonlocal approved, declined
        for cc in ccs:
            try:
                sent = await userbot.send_message(TARGET_BOT, f"/bt {cc}")
                result = None

                # Wait for result
                for _ in range(10):
                    await asyncio.sleep(27)
                    reply = await userbot.get_messages(TARGET_BOT, sent.id + 1)
                    if reply and reply.text and "Processing..." not in reply.text:
                        result = reply.text
                        break

                if result and "Approved ✅" in result:
                    approved += 1
                    await bot.reply_to(message, f"𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅\n\n{result}")
                else:
                    declined += 1

                await bot.edit_message_reply_markup(
                    chat_id=message.chat.id,
                    message_id=status_msg.message_id,
                    reply_markup=build_keyboard()
                )

            except asyncio.CancelledError:
                await bot.reply_to(message, "⟡ 𝙈𝘼𝙎𝙎 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 𝙒𝘼𝙎 𝙎𝙏𝙊𝙋𝙋𝙀𝘿")
                break

            except Exception:
                declined += 1
                await bot.edit_message_reply_markup(
                    chat_id=message.chat.id,
                    message_id=status_msg.message_id,
                    reply_markup=build_keyboard()
                )
                continue

    # Store task so it can be cancelled
    task = asyncio.create_task(process_ccs())
    bot.current_task = task

# === Startup ===
async def main():
    print("🔁 Logging in userbot...")
    await userbot.start()
    
    print("✅ Starting Telegram bot...")
    await bot.set_my_commands([
        types.BotCommand("start", "𝙎𝙏𝘼𝙍𝙏 𝙏𝙃𝙀 𝘽𝗢𝙏"),
        types.BotCommand("stop", "𝙎𝙏𝙊𝙋 𝙈𝘼𝙎𝙎 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂"),
        types.BotCommand("bt", "𝘽𝙍𝘼𝙄𝙉𝙏𝙍𝙀𝙀 𝘼𝙐𝙏𝙃 (𝙎𝙄𝙉𝙂𝙇𝙀)"),
        types.BotCommand("mbt", "𝘽𝙍𝘼𝙄𝙉𝙏𝙍𝙀𝙀 𝘼𝙐𝙏𝙃 (𝙈𝘼𝙎𝙎)"),
    ])
    
    print("🤖 Bot is running...")
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())