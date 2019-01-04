# Generated by Django 2.1.2 on 2019-01-04 08:50

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('body', models.TextField()),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=None, null=True, size=None)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
                ('time_to_read', models.IntegerField()),
                ('time_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('time_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('average_rating', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
            ],
            options={
                'ordering': ('time_created', 'time_updated'),
            },
        ),
        migrations.CreateModel(
            name='ArticleStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Highlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_start', models.IntegerField(default=0)),
                ('index_stop', models.IntegerField()),
                ('highlighted_article_piece', models.CharField(blank=True, max_length=200)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('time_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('time_updated', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
                'ordering': ('time_updated',),
            },
        ),
        migrations.CreateModel(
            name='LikesDislikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('tag', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
