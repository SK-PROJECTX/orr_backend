from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("client", "0006_onboardingquestionnaire"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onboardingquestionnaire",
            name="communication_tone",
            field=models.JSONField(default=list),
        ),
    ]
