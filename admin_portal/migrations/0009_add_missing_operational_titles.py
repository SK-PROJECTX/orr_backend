from django.db import migrations
import admin_portal.fields

class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0008_operationalsystemspagecontent_process_step_4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationalsystemspagecontent',
            name='process_step_1_title',
            field=admin_portal.fields.RichTextField(default=admin_portal.fields._default),
        ),
        migrations.AddField(
            model_name='operationalsystemspagecontent',
            name='process_step_2_title',
            field=admin_portal.fields.RichTextField(default=admin_portal.fields._default),
        ),
        migrations.AddField(
            model_name='operationalsystemspagecontent',
            name='process_step_3_title',
            field=admin_portal.fields.RichTextField(default=admin_portal.fields._default),
        ),
        migrations.AddField(
            model_name='operationalsystemspagecontent',
            name='process_step_4_title',
            field=admin_portal.fields.RichTextField(default=admin_portal.fields._default),
        ),
    ]
