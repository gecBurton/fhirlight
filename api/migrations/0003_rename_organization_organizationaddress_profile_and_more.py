# Generated by Django 5.1.4 on 2025-01-09 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_baseprofile_locationaddress_alter_concept_display_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organizationaddress',
            old_name='organization',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='organizationcontactpoint',
            old_name='organization',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='organizationidentifier',
            old_name='organization',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='patientaddress',
            old_name='patient',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='patientidentifier',
            old_name='patient',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='patientname',
            old_name='patient',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='patienttelecom',
            old_name='patient',
            new_name='profile',
        ),
    ]
