from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0117_bdsweeks"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="bdsweek",
            table="projects_bdsweeks",
        ),
    ]
