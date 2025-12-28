from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0002_contactinfo_faq_servicecard_sitesettings_testimonial_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategicadvisorypagecontent',
            name='process_description',
            field=models.TextField(default='Like your Business GP, we diagnose compliance challenges and prescribe strategic solutions tailored to your organization\'s unique context.'),
        ),
        migrations.AddField(
            model_name='operationalsystemspagecontent',
            name='process_description',
            field=models.TextField(default='Just like your Business GP, we follow a systematic diagnostic and treatment approach to restore operational health.'),
        ),
        migrations.AddField(
            model_name='livingsystemspagecontent',
            name='process_description',
            field=models.TextField(default='At the heart of our work, we take a systems approach to understanding and regenerating living systems. We observe the current state, design regenerative solutions, and implement systems that restore ecological health while creating economic value.'),
        ),
    ]