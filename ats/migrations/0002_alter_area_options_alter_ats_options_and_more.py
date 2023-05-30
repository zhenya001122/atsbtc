# Generated by Django 4.2 on 2023-05-29 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ats", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="area",
            options={
                "ordering": ["name"],
                "verbose_name": "Районы",
                "verbose_name_plural": "Районы",
            },
        ),
        migrations.AlterModelOptions(
            name="ats",
            options={
                "ordering": ["name"],
                "verbose_name": "АТС",
                "verbose_name_plural": "АТС",
            },
        ),
        migrations.AlterModelOptions(
            name="cable",
            options={
                "ordering": ["direction"],
                "verbose_name": "КЛС",
                "verbose_name_plural": "КЛС",
            },
        ),
        migrations.AlterModelOptions(
            name="cross",
            options={
                "ordering": ["number"],
                "verbose_name": "Кроссы",
                "verbose_name_plural": "Кроссы",
            },
        ),
        migrations.AlterModelOptions(
            name="department",
            options={
                "ordering": ["name"],
                "verbose_name": "Подразделения",
                "verbose_name_plural": "Подразделения",
            },
        ),
        migrations.AlterField(
            model_name="area",
            name="department",
            field=models.ManyToManyField(
                related_name="areas", to="ats.department", verbose_name="Подразделение"
            ),
        ),
        migrations.AlterField(
            model_name="area",
            name="name",
            field=models.CharField(max_length=20, verbose_name="Наименование района"),
        ),
        migrations.AlterField(
            model_name="ats",
            name="area",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="ats.area",
                verbose_name="Район",
            ),
        ),
        migrations.AlterField(
            model_name="ats",
            name="name",
            field=models.CharField(max_length=20, verbose_name="Наименование АТС"),
        ),
        migrations.AlterField(
            model_name="cable",
            name="ats",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="ats.ats",
                verbose_name="АТС",
            ),
        ),
        migrations.AlterField(
            model_name="cable",
            name="cross",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="ats.cross",
                verbose_name="Кросс",
            ),
        ),
        migrations.AlterField(
            model_name="cable",
            name="tag",
            field=models.CharField(max_length=40, verbose_name="Бирка на кабеле"),
        ),
        migrations.AlterField(
            model_name="cross",
            name="ats",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ats.ats",
                verbose_name="АТС",
            ),
        ),
        migrations.AlterField(
            model_name="cross",
            name="photo_cross",
            field=models.ImageField(
                blank=True, upload_to="photos/%Y/%m/%d/", verbose_name="Фото кросса"
            ),
        ),
        migrations.AlterField(
            model_name="cross",
            name="photo_insert",
            field=models.ImageField(
                blank=True, upload_to="photos/%Y/%m/%d/", verbose_name="Фото вкладыша"
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="name",
            field=models.CharField(max_length=20, verbose_name="Подразделение"),
        ),
        migrations.AlterField(
            model_name="note",
            name="cable",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="ats.cable",
                verbose_name="Направление КЛС",
            ),
        ),
        migrations.AlterField(
            model_name="note",
            name="cross",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="ats.cross",
                verbose_name="Кросс",
            ),
        ),
        migrations.AlterField(
            model_name="note",
            name="description",
            field=models.TextField(blank=True, verbose_name="Примечания"),
        ),
    ]
