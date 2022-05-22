# Generated by Django 3.2.12 on 2022-05-20 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('overview', models.TextField()),
                ('release_date', models.DateField()),
                ('poster_path', models.TextField(null=True)),
                ('backdrop_path', models.TextField(null=True)),
                ('popularity', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('vote_average', models.FloatField()),
                ('adult', models.BooleanField(null=True)),
                ('original_language', models.CharField(max_length=50, null=True)),
                ('runtime', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('tagline', models.TextField(null=True)),
                ('budget', models.IntegerField()),
                ('revenue', models.IntegerField()),
                ('homepage', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('content', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('like_users', models.ManyToManyField(related_name='like_reviews', to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovieKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.keyword')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(through='movies.MovieGenre', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='keywords',
            field=models.ManyToManyField(through='movies.MovieKeyword', to='movies.Keyword'),
        ),
        migrations.AddField(
            model_name='movie',
            name='like_users',
            field=models.ManyToManyField(related_name='like_movies', to=settings.AUTH_USER_MODEL),
        ),
    ]
