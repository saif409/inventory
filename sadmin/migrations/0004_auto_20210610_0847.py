# Generated by Django 3.1.6 on 2021-06-10 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sadmin', '0003_auto_20210407_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyor',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'Users')], default=3, null=True),
        ),
    ]