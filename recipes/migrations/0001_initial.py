from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True, help_text='Method, tips, fermentation times, etc.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=3, help_text='Amount in the chosen unit', max_digits=10)),
                ('unit', models.CharField(choices=[('g', 'Grams (g)'), ('lb', 'Pounds (lb)'), ('oz', 'Ounces (oz)')], default='g', max_length=2)),
                ('bakers_percentage', models.DecimalField(blank=True, decimal_places=2, help_text="Baker's percentage", max_digits=7, null=True)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe_uses', to='inventory.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.recipe')),
            ],
            options={'ordering': ['order', 'ingredient__name'], 'unique_together': {('recipe', 'ingredient')}},
        ),
    ]
