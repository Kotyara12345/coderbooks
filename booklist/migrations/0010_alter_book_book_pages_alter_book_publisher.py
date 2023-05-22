# Generated by Django 4.1.3 on 2023-03-15 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklist', '0009_book_book_pages_book_codes_book_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_pages',
            field=models.CharField(max_length=200, verbose_name='Количество страниц'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=200, verbose_name='Издательство'),
        ),
    ]
