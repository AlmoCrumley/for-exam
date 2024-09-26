from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
##from lexicon.lexicon import LEXICON_RU
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from db.users import new_user, get_next_question
from lexicon.lexicon import lexicon

# Инициализируем роутер уровня модуля
router = Router()

btn_next = KeyboardButton(text='Get the next question')
keyboard = ReplyKeyboardMarkup(keyboard=[[btn_next]], resize_keyboard=True)


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    new_user(message.from_user.id)
    await message.answer(text='ЕБАННЫЙ РОТ ПОГНАЛИ НАХУЙ', reply_markup=keyboard)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='Зачем???')

@router.message(F.text == 'Get the next question')
async def get_next(message: Message):
    txt = lexicon[get_next_question(message.from_user.id)]
    await message.answer(text=txt)  
  