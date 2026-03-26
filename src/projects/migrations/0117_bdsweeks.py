from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0116_project_parent"),
    ]

    operations = [
        migrations.CreateModel(
            name="BDSWeek",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("anno", models.IntegerField()),
                ("data_inizio", models.DateField()),
                ("data_fine", models.DateField()),
                ("descrizione", models.TextField(blank=True, null=True)),
                ("logo", models.ImageField(blank=True, max_length=300, null=True, upload_to="images/")),
            ],
            options={
                "db_table": "bdsweeks",
            },
        ),
    ]
