# Generated by Django 3.2 on 2023-10-25 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0003_auto_20231011_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['id'], 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='recipies/images/', verbose_name='Изображение рецепта'),
        ),
    ]