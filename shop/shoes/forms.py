from django import forms


class FormOrderBy(forms.Form):
    order_by = forms.ChoiceField(
        label="Сортировка",
        required=False,
        choices=[
            ["price", "По возрастанию цены ↑"],
            ["-price", "По убыванию цены ↓"],
            ["realise_date", "Сначала старые товары"],
            ["-realise_date", "Сначала новые товары"],
        ],
    )
