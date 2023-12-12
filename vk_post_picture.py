import vk_api
from vk_api import VkUpload
from auth_data import enter_api

# Авторизация
vk_session = vk_api.VkApi(token=enter_api)
vk = vk_session.get_api()

upload = VkUpload(vk_session)  # Для загрузки изображений

# Загрузка картинок на сервера вк и получение их id
photos = ['evgen.jpg'] #Сюда фотку
photo_list = upload.photo_wall(photos)
attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

# Добавление записи на стену
vk_session.method("wall.post", {
    'owner_id': '-222174679',  # Посылаем себе на стену
    'message': 'ЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕ!!!!!!!!!!!!!!!!!!',
    'attachment': attachment,
})
