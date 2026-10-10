# BioGENext 2026 dashboard

Локальний Streamlit-дашборд для дослідження переходу від biomedical data до clinical decision.

## Запуск

```bash
cd "stage-two-research/biogenext-dashboard"
python -m pip install -r requirements.txt
streamlit run app.py
```

Інтерфейс має темну тему з неоновими mint/blue/violet accents і містить:

- масштаб metagenomics study;
- mapped / unmapped reads;
- benchmark швидкості Bakta vs Pannotator;
- Boltz: tested compounds vs positive results;
- fastLBP та інші validation notes;
- український oncology / UBI Hub roadmap;
- рівні доказовості та обмеження метрик.

Дані вбудовані у `app.py` на основі слайдів BioGENext 2026 та позначені за типом доказовості. Це дослідницька візуалізація, не клінічний інструмент.
