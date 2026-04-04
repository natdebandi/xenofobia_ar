import pandas as pd

INPUT_PATH = "data/tweets_medios_arg.csv"
OUTPUT_PATH = "data/tweets_medios_arg_covid.csv"

COVID_KEYWORDS = [
    "coronavirus", "covid", "Wuhan", "cuarentena", "normalidad",
    "aislamiento", "encierro", "fase", "infectados", "distanciamiento",
    "fiebre", "síntomas"
]

df = pd.read_csv(INPUT_PATH)

pattern = "|".join(COVID_KEYWORDS)
df["covid"] = df["text"].str.contains(pattern, case=False, na=False).astype(int)

df.to_csv(OUTPUT_PATH, index=False)

print(f"Dataset guardado en: {OUTPUT_PATH}")
print(f"Total tweets: {len(df)}")
print(f"Con etiqueta covid=1: {df['covid'].sum()} ({df['covid'].mean():.1%})")
print(f"Con etiqueta covid=0: {(df['covid'] == 0).sum()}")
