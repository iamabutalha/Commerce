# Generated by Django 5.0.3 on 2024-04-13 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlisting_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='image_url',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='description',
            field=models.TextField(default=1, max_length=90),
            preserve_default=False,
        ),
    ]
