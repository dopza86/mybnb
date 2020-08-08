# Generated by Django 3.1 on 2020-08-08 12:56

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': '편의시설',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': '시설',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HouseRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': '이용규칙',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('caption', models.CharField(max_length=80, verbose_name='설명')),
                ('file', models.ImageField(blank=True, upload_to='room_photos', verbose_name='파일')),
            ],
            options={
                'verbose_name': '사진',
                'verbose_name_plural': '사진',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': '객실종류',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='추가 일시')),
                ('name', models.CharField(max_length=140, verbose_name='이름')),
                ('description', models.TextField(verbose_name='설명')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='국가')),
                ('city', models.CharField(max_length=80, verbose_name='도시')),
                ('price', models.IntegerField(verbose_name='가격')),
                ('address', models.CharField(max_length=140, verbose_name='주소')),
                ('guests', models.IntegerField(default=0, verbose_name='숙박인원')),
                ('beds', models.IntegerField(verbose_name='침대')),
                ('bedrooms', models.IntegerField(verbose_name='침실')),
                ('baths', models.IntegerField(verbose_name='욕실')),
                ('check_in', models.TimeField(verbose_name='체크인 시간')),
                ('check_out', models.TimeField(verbose_name='체크아웃 시간')),
                ('instant_book', models.BooleanField(default=False, verbose_name='즉시예약')),
                ('amenities', models.ManyToManyField(blank=True, related_name='rooms', to='rooms.Amenity', verbose_name='편의시설')),
                ('facilities', models.ManyToManyField(blank=True, related_name='rooms', to='rooms.Facility', verbose_name='시설')),
            ],
            options={
                'verbose_name': '객실',
                'verbose_name_plural': '객실',
            },
        ),
    ]