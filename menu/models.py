from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """
    Модель для представления меню.
    """
    name = models.CharField(
        'Меню', unique=True, max_length=100, db_index=True
    )
    order = models.IntegerField(
        'Порядок отображения меню на странице', default=0
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    """
    Модель для представления элементов меню.
    """
    title = models.CharField('Заголовок элемента меню', max_length=256)
    url = models.CharField(
        'Прямой URL для пункта меню',
        max_length=256, null=True, blank=True
    )
    named_url = models.CharField(
        'Имнованный URL для пункта меню',
        max_length=256, null=True, blank=True
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='Родительский элемент'
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE,
        related_name='item',
        verbose_name='Меню'
    )
    order = models.IntegerField(
        'Порядок отображения элемента внутри своего уровня вложенности', 
        default=0
    )

    def get_absolute_url(self):
        if self.url:
            return self.url
        elif self.named_url:
            return reverse(self.named_url)
        return ''

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        constraints = [
            models.UniqueConstraint(
                fields=('parent', 'title'),
                name='unique_item_for_parent'
            ),
            models.CheckConstraint(
                check=~models.Q(id=models.F('parent')),
                name='not_self_parent'
            )
        ]

    def __str__(self) -> str:
        if self.parent:
            return f'{str(self.parent)}. {self.title}'
        return f'{self.menu.name}. {self.title}'
