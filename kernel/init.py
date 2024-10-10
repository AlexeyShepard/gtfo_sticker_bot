import os, logging, importlib, inspect
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from kernel.base_handler import *

def init():
    load_dotenv()
    TOKEN = os.getenv('TOKEN') 

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application = ApplicationBuilder().token(TOKEN).build()

    print('Резултат: ' + str(deploy_handlers()))

    for make in deploy_handlers():
        application.add_handler(make())

    application.run_polling()

def deploy_handlers():
    handlers_directory = os.getenv('handlers_directory')

    print(handlers_directory)

    all_methods = []

    for filename in os.listdir(handlers_directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            # Импортируем модуль
            module_name = f"{handlers_directory}.{filename[:-3]}"  # Убираем .py
            module = importlib.import_module(module_name)

            # Получаем все функции из модуля
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name.endswith('_handler'):
                    if issubclass(obj, base_handler) and not obj.__abstractmethods__:
                        instance = obj()  # Safe to instantiate now
                        if hasattr(instance, 'make') and callable(getattr(instance, 'make')):
                            if instance.make.__code__ is not base_handler.make.__code__:
                                all_methods.append(instance.make)

    return all_methods