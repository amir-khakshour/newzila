# Generated by Django 2.2.10 on 2020-02-21 13:05

from django.db import migrations, models
import newzila.newsletter.utils


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='verification_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Verification date'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='verification_token',
            field=models.CharField(default=newzila.newsletter.utils.make_verification_token, max_length=40, verbose_name='verification_token'),
        ),
    ]
