"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/python-automations/web/
"""


# Import for the Web Bot
from botcity.web import WebBot, Browser, By

#from botcity.plugins.http import BotHttpPlugin

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

from webdriver_manager.chrome import ChromeDriverManager

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def pesquisar_cidade(bot, cidade):
    while len(bot.find_elements('//*[@id="APjFqb"]', By.XPATH)) < 1:
        bot.wait(1000)
        print("carregando...")

    bot.find_element('//*[@id="APjFqb"]', By.XPATH).send_keys(cidade)

    bot.wait(1000)
    bot.enter()


def entrair_dados_clima(bot):

    count = 0

    while True:
        count+=1
        dia_semana = bot.find_element(f'//*[@id="wob_dp"]/div[{count}]/div[1]', By.XPATH).text
        print(dia_semana)

        if count == 8:
            break

def main():

    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    bot.headless = False

    bot.browser = Browser.CHROME

    bot.driver_path = ChromeDriverManager().install()

    bot.browse("https://www.google.com/")

    bot.maximize_window()

    try:
        pesquisar_cidade(bot, 'manaus clima')

        bot.wait(1000)
        entrair_dados_clima(bot)
    except Exception as ex:
        print(ex)
        bot.save_screenshot('erro.png')
    finally:
        bot.wait(5000)
        bot.stop_browser()

def not_found(label):
    print(f"Element not found: {label}")

if __name__ == '__main__':
    main()
