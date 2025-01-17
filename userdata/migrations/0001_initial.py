# Generated by Django 3.2.3 on 2024-07-08 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('marital_status', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('contact_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('social_security_number', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_contact_name', models.CharField(max_length=100)),
                ('emergency_contact_relationship', models.CharField(max_length=50)),
                ('emergency_contact_number', models.CharField(max_length=20)),
                ('medical_history', models.TextField()),
                ('current_medications', models.TextField()),
                ('allergies', models.TextField()),
                ('primary_care_physician', models.CharField(max_length=100)),
                ('primary_care_physician_contact', models.CharField(max_length=20)),
                ('specialist_physicians', models.TextField(blank=True, null=True)),
                ('health_insurance_information', models.TextField()),
                ('daily_living_assistance_requirements', models.TextField()),
                ('dietary_preferences_restrictions', models.TextField()),
                ('preferred_activities_hobbies', models.TextField()),
                ('religious_cultural_preferences', models.TextField()),
                ('communication_preferences', models.TextField()),
                ('power_of_attorney', models.CharField(max_length=100)),
                ('power_of_attorney_contact', models.CharField(max_length=20)),
                ('advance_directives', models.TextField(blank=True, null=True)),
                ('financial_information', models.TextField()),
                ('payment_method', models.CharField(max_length=50)),
                ('family_members', models.TextField()),
                ('social_network', models.TextField()),
                ('previous_living_arrangements', models.TextField()),
                ('special_equipment_needs', models.TextField()),
                ('transportation_needs', models.TextField()),
                ('behavioral_cognitive_assessments', models.TextField()),
                ('mental_health_history', models.TextField()),
            ],
        ),
    ]
