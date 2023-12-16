# Generated by Django 4.2.8 on 2023-12-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g_mtg', '0002_alter_projectuser_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(
                blank=True, upload_to='media', verbose_name='Картинка продукта'
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.URLField(blank=True, verbose_name='Ссылка на продукт'),
        ),
        migrations.AddField(
            model_name='salechannel',
            name='image',
            field=models.ImageField(
                blank=True, upload_to='media', verbose_name='Картинка канала'
            ),
        ),
    ]