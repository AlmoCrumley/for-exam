from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, URLInputFile
##from lexicon.lexicon import LEXICON_RU
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, CallbackQuery)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.users import new_user, get_next_question, get_next_in_row
from lexicon.lexicon import lexicon, answers
from db.db import get_question_by_id

# Инициализируем роутер уровня модуля
router = Router()

btn_next = KeyboardButton(text='Get the next question')
btn_row = KeyboardButton(text='Get the next in a row')
btn_all = KeyboardButton(text='Get all questions')
decision_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='get text', callback_data='get_text_pressed')]])
keyboard = ReplyKeyboardMarkup(keyboard=[[btn_next], [btn_row], [btn_all]], resize_keyboard=True)
number = 0


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    image = URLInputFile(
        "https://avatars.dzeninfra.ru/get-zen_brief/6488213/pub_62d159f2ebe438762b152033_62d159f2ebe438762b152034/scale_1200",
        filename="python-logo.png"
    )
    new_user(message.from_user.id)
    await message.answer_photo(image)
    await message.answer(text='ЕБАННЫЙ РОТ ПОГНАЛИ НАХУЙ', reply_markup=keyboard)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='Зачем???')


@router.message(F.text == 'Get the next question')
async def get_next(message: Message):
    global number
    # txt = lexicon[get_next_question(message.from_user.id)]
    number = get_next_question(message.from_user.id)
    txt = lexicon[number]
    await message.answer(text=txt, reply_markup=decision_kb)


@router.message(F.text == 'Get the next in a row')
async def get_row(message: Message):
    global number
    # txt = lexicon[get_next_question(message.from_user.id)]
    number = get_next_in_row(message.from_user.id)
    txt = lexicon[number]
    await message.answer(text=txt, reply_markup=decision_kb)


@router.callback_query(F.data == 'get_text_pressed')
async def get_text_pressed(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'{number} {lexicon[number]}\n {answers[number]}',
        # text = answers_2['1'],
        reply_markup=callback.message.reply_markup)

class MyCallbackFactory(CallbackData, prefix='any'):
    key: str


@router.message(F.text == 'Get all questions')
async def get_all(message: Message):
    def create_kb(**kwargs):
        #width = len(kwargs)
        kb_builder = InlineKeyboardBuilder()
        buttons = []
        for k, v in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=f'{k}: {v}',
                callback_data=MyCallbackFactory(key=k).pack()))
        kb_builder.row(*buttons, width=1)
        return kb_builder.as_markup()
    questions = create_kb(**lexicon)

    await message.answer(text='all questions', reply_markup=questions)

@router.callback_query(MyCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: MyCallbackFactory):
    await callback.message.answer(
        text=f'{callback_data.key}: {lexicon[callback_data.key]}\n'
             f'{answers[callback_data.key]}'
    )
    await callback.answer()
