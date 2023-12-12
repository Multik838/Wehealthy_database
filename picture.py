from django.db import models
import requests
import vk_api
from vk_api import VkUpload
from auth_data import enter_api
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=255, unique=False)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='subcategories',
                                        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_subcategories(self):
        return Category.objects.filter(parent_category=self)

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    introduction = models.TextField()
    content = models.TextField()
    is_posted = models.BooleanField()
    image = models.ImageField(upload_to='3ooUhJWg338.jpg', blank=True, null=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Проверяем, является ли запись новой

        super().save(*args, **kwargs)


        # filename = '3ooUhJWg338.jpg'
        # with Image.open(filename) as image:
        #     image.load()

        # Если статья является новой или is_posted изменяется на True, отправляем статью на Telegram-канал
        if is_new or self.is_posted:
            bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
            chat_id = '@wehealthyru'
            message = f'Новая статья: {self.title}\n\n{self.introduction}\n\nПолная статья: http://your_website.com/post/{self.id}'
            requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}')

            # Если у статьи есть изображение, отправляем его на Telegram-канал
            if self.image:
                image_path = self.image.path
                with open(image_path, 'rb') as image_file:
                    files = {'photo': image_file}
                    requests.post(f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}', files=files)

            # Отправляем статью и изображение на стену вашего собственного сообщества ВКонтакте
            if self.image:
                vk_session = vk_api.VkApi(token= enter_api)  # Здесь нужно указать ключ доступа вашего сообщества ВКонтакте
                vk = vk_session.get_api()
                upload = VkUpload(vk_session)
                try:
                    photo = upload.photo_wall(self.image.path)[0]  # Загружаем фото на стену сообщества
                    attachments = f'photo{photo["owner_id"]}_{photo["id"]}'
                except vk_api.exceptions.VkApiError as e:
                    print(f"Ошибка при загрузке фото на стену ВКонтакте: {e}")
                    attachments = ''
            else:
                attachments = ''

            try:
                vk.wall.post(owner_id='-222174679', from_group=1, message=message, attachments=attachments)  # Здесь нужно указать ID вашего собственного сообщества ВКонтакте
            except vk_api.exceptions.VkApiError as e:
                print(f"Ошибка при публикации на стене ВКонтакте: {e}")

    class Meta:
        app_label = 'blog'