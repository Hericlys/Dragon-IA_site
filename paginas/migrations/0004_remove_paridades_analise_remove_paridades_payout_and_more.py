# Generated by Django 4.0.5 on 2022-08-26 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0003_paridades'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paridades',
            name='analise',
        ),
        migrations.RemoveField(
            model_name='paridades',
            name='payout',
        ),
        migrations.AlterField(
            model_name='paridades',
            name='call',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='paridades',
            name='paridade',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='paridades',
            name='put',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]