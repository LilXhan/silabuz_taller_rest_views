# Generated by Django 4.1.6 on 2023-02-08 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('done_at', models.DateField(null=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('deleted_at', models.DateField(null=True)),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'todo',
            },
        ),
    ]
