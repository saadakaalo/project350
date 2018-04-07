# Generated by Django 2.0.1 on 2018-04-07 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('add_content', '0011_logtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='add_content.Course')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='userdetail',
            name='user_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='add_content.UserGroup'),
        ),
    ]