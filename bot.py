import vk_api
import time
from datetime import datetime, timedelta
from vk_api.longpoll import VkLongPoll, VkEventType
import traceback

# Ваш токен доступа
TOKEN = 'vk1.a.goTp9VaoSbQd4h8S9r-y2oItpxs1xgekIJZgTI8ga3_tjcQ2oOImL0kZnV2pqrTuRLwPTlDOvPu3LOC8ne8AZIYu0WGGldgDotbwXvX_3rUiLTdW2UCoWNaSZ_h8NBojnlv6BycS5KbeTO8eQZsk5Xp0rDa5Hz79y4w6l7z_NE8e22t7caZToyRCB3xknZePpZk-CKRH09Do9MmZ5VCQIg'

# Начальная дата и время, с которого начинается ускоренное время
start_time = datetime(1922, 2, 1, 0, 0, 0)

# Временной шаг для ускоренного времени (в виртуальных секундах за одну реальную секунду)
time_step_seconds = 30  # 1 реальная секунда = 30 виртуальных секунд

# Авторизация в ВКонтакте
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()


# Функция для отправки сообщения в ВКонтакте
def send_message(peer_id, message):
    vk.messages.send(random_id=int(time.time()),
                     peer_id=peer_id,
                     message=message)


def start_longpoll():
    longpoll = VkLongPoll(vk_session)
    real_start_time = datetime.now()  # Время начала реального времени

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.text.lower() == '!время':
                        real_elapsed_time = datetime.now(
                        ) - real_start_time  # Прошедшее реальное время
                        accelerated_current_time = start_time + timedelta(
                            seconds=real_elapsed_time.total_seconds() *
                            time_step_seconds)
                        formatted_time = accelerated_current_time.strftime(
                            '%d.%m.%Y %H:%M:%S')
                        send_message(
                            event.peer_id,
                            f"#время \nТекущее виртуальное время: {formatted_time}"
                        )
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            print(traceback.format_exc())
            time.sleep(5)  # Задержка перед повторной попыткой


if __name__ == '__main__':
    while True:
        try:
            start_longpoll()
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            print(traceback.format_exc())
            time.sleep(5)  # Задержка перед повторной попыткой
