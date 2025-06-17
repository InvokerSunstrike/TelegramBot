import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '7638188374:AAHyAP7znIM-X_QioGiyPQ2KUFhbRkQ7PbQ'

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

start_text = (
    "<b>Ассаламу Алейкум, Зулейха 💙</b>\n\n"
    "Этот бот мы создали для нас двоих. Чтобы ближе узнавать друг друга, "
    "сближаться сердцами, укреплять любовь и веру. Пусть каждый вопрос станет шагом "
    "к лучшему взаимопониманию и к спокойствию в сердце.\n\n"
    "<i>Выбери раздел ниже и начни с любого, что зовёт твоё сердце.</i> 🤍"
)

quiz_data = {
    "heart": [
        {"q": "Почему ислам считают религией, очищающей сердца?", "options": ["Потому что запрещено всё вредное", "Потому что призывает к очищению как внешнему, так и внутреннему", "Потому что религия строгости", "Потому что обязывает поститься"], "a": 1},
        {"q": "Что происходит с сердцем, если оно лишено истины?", "options": ["Оно покрывается ржавчиной", "Оно начинает ускоренно биться", "Оно забывает память", "Оно перестаёт работать"], "a": 0},
        {"q": "Чем являются Коран и Сунна для сердец?", "options": ["Источник вдохновения", "Исцелением и милостью для верующих", "Руководством только для правителей", "Историческими записями"], "a": 1},
        {"q": "К чему зовёт Аллах в суре «аль-Анфаль», когда призывает уверовать?", "options": ["К жизни сердца через веру", "К знанию истории уммы", "К поиску богатства", "К силе разума"], "a": 0},
        {"q": "Что спасает человека в Судный день согласно суре «аш-Шу’ара»?", "options": ["Чистое сердце", "Число поклонений", "Знания и наука", "Хорошее происхождение"], "a": 0}
    ],
    "heart_summary": """<b>📖 Аят для укрепления сердца</b>
رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا
<em>"Господь наш! Не уклоняй наши сердца после того, как Ты наставил нас!"</em>
— Сура Али Имран, 3:8

🔹 Учится быстро, читай каждый день, особенно после намаза.

❤️ Основной хадис о сердце
«Поистине, в теле есть кусочек мяса: если он исправен — исправно всё тело; если он испорчен — испорчено всё тело. Это — сердце».
— аль-Бухари, Муслим

🔹 Хорошо заходит наизусть, легко понять. Подходит для напоминания себе и другим.

🌪 Хадис о переменчивости сердца
«Сердце — как перо в пустыне: ветер переворачивает его то в одну, то в другую сторону».
— Ахмад 4/408

🔹 Очень образное, сразу отпечатывается в сознании.

🕊️ Мольба Пророка ﷺ
اللَّهُمَّ إِنِّي أَسْأَلُكَ قَلْبًا سَلِيمًا
"О Аллах, я прошу у Тебя здравое сердце!"

🔹 Очень короткая, искренняя. Повторяй в дуа, легко учить и детям, и взрослым.

🔒 Часто повторяемая дуа Пророка ﷺ
يَا مُقَلِّبَ الْقُلُوبِ ثَبِّتْ قَلْبِي عَلَى دِينِكَ
"О Переворачивающий сердца! Утверди моё сердце на Твоей религии!"

🔹 Это одно из самых сильных прошений — проси с хошу‘ (смирением).

✨ Аят, наполняющий душу радостью
مَنْ عَمِلَ صَالِحًا مِّن ذَكَرٍ أَوْ أُنثَى وَهُوَ مُؤْمِنٌ فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً
"Кто бы ни совершал праведные дела, будь то мужчина или женщина, и будет верующим — Мы непременно даруем ему прекрасную жизнь".
— Сура ан-Нахль, 16:97"""
}

user_progress = {}

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧼 Очищение сердца", callback_data="start_heart")],
    [InlineKeyboardButton(text="📘 Итог / Выучить", callback_data="heart_summary")]
])

@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_progress[message.from_user.id] = {"section": None, "index": 0}
    await message.answer(start_text, reply_markup=menu_keyboard)

@dp.callback_query(F.data == "heart_summary")
async def show_summary(callback: CallbackQuery):
    await callback.message.answer(quiz_data["heart_summary"])

@dp.callback_query(F.data.startswith("start_"))
async def start_quiz(callback: CallbackQuery):
    section = callback.data.split("_")[1]
    user_id = callback.from_user.id
    user_progress[user_id] = {"section": section, "index": 0}
    await send_question(callback.message, user_id)

async def send_question(message, user_id):
    progress = user_progress[user_id]
    section = progress["section"]
    index = progress["index"]

    if index >= len(quiz_data[section]):
        await message.answer("✅ Викторина завершена! Спасибо за участие! 🙌")
        return

    item = quiz_data[section][index]
    buttons = [InlineKeyboardButton(text=opt, callback_data=f"answer_{index}_{i}_{item['a']}_{section}") for i, opt in enumerate(item["options"])]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn] for btn in buttons])
    await message.answer(f"<b>{item['q']}</b>", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: CallbackQuery):
    _, index, chosen, correct, section = callback.data.split("_")
    index, chosen, correct = int(index), int(chosen), int(correct)

    result = "✅ Правильно!" if chosen == correct else "❌ Неправильно. Попробуй ещё."
    await callback.answer(result, show_alert=True)

    user_id = callback.from_user.id
    user_progress[user_id]["index"] += 1
    await send_question(callback.message, user_id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
