import vk_api
from auth_data import enter_api
message = '"Hola como estas"?'
vk_session = vk_api.VkApi(
                token=enter_api)  # Здесь нужно указать токен доступа пользователя ВКонтакте
vk = vk_session.get_api()

try:
    vk.wall.post(owner_id='-222174679', from_group=1,
                 message=message)  # Здесь нужно указать ID вашей группы ВКонтакте с минусом (-)

except vk_api.exceptions.VkApiError as e:
    print(f"Ошибка при публикации на стене ВКонтакте: {e}")
