from flask import Flask, render_template
import os
import pandas as pd
import json

app = Flask(__name__)

def load_json_files(directory):
    json_data = []
    for i in range(1, 82):
        filename = f"SecimSonucIlce-{i}.json"
        with open(os.path.join(directory, filename), 'r') as file:
            data = json.load(file)
            json_data.append(data)
    return json_data

def merge_dataframes(json_data):
    dfs = []
    for data in json_data:
        df = pd.DataFrame(data)
        df = df[df["İlçe Id"] != "Voting Rate"]
        df_filtered = df.drop(columns=["Number of Registred Voters", "Voter Turnout", "Valid Total Number of Votes","Download Data by Neighborhood"])
        dfs.append(df_filtered)
    merged_df = pd.concat(dfs)
    return merged_df

@app.route("/")
def main():
    # Read the primary JSON file
    with open('static/json/SecimSonucIl.json', 'r') as file:
        json_data_primary = json.load(file)

    df = pd.DataFrame(json_data_primary)

    # Merge the JSON files
    json_directory = 'static/json'
    json_data = load_json_files(json_directory)
    merged_df = merge_dataframes(json_data)

    # Filter and process data for stacked column chart
    df = df[df["İl Id"] != "Voting Rate"]
    df_filtered = df.drop(columns=["Number of Registred Voters", "Voter Turnout", "Valid Total Number of Votes"])

    x_data = df_filtered["Name of Province"].tolist()
    y_data_muharrem = df_filtered[" MUHARREM İNCE "].str.replace('.', '').tolist()
    y_data_meral = df_filtered[" MERAL AKŞENER "].str.replace('.', '').tolist()
    y_data_recep = df_filtered[" RECEP TAYYİP ERDOĞAN "].str.replace('.', '').tolist()
    y_data_selahattin = df_filtered[" SELAHATTİN DEMİRTAŞ "].str.replace('.', '').tolist()
    y_data_temel = df_filtered[" TEMEL KARAMOLLAOĞLU "].str.replace('.', '').tolist()
    y_data_dogu = df_filtered[" DOĞU PERİNÇEK "].str.replace('.', '').tolist()

    # Sort and process data for line chart
    merged_df = merged_df.sort_values(by="Name of District")
    x_data_line = merged_df["Name of District"].tolist()
    y_data_muharrem_line = pd.to_numeric(merged_df[' MUHARREM İNCE '].str.replace('.', ''), errors='coerce').fillna(0).tolist()
    y_data_meral_line = pd.to_numeric(merged_df[' MERAL AKŞENER '].str.replace('.', ''), errors='coerce').fillna(0).tolist()
    y_data_recep_line = pd.to_numeric(merged_df[' RECEP TAYYİP ERDOĞAN '].str.replace('.', ''), errors='coerce').fillna(0).tolist()
    y_data_selahattin_line = pd.to_numeric(merged_df[' SELAHATTİN DEMİRTAŞ '].str.replace('.', ''), errors='coerce').fillna(0).tolist()
    y_data_temel_line = pd.to_numeric(merged_df[' TEMEL KARAMOLLAOĞLU '].str.replace('.', ''), errors='coerce').fillna(0).tolist()
    y_data_dogu_line = pd.to_numeric(merged_df[' DOĞU PERİNÇEK '].str.replace('.', ''), errors='coerce').fillna(0).tolist()

    return render_template('index.html', data_table=df_filtered.to_html(index=False), merged_table=merged_df.to_html(index=False), x_data=x_data, y_data_muharrem=y_data_muharrem, y_data_meral=y_data_meral, y_data_recep=y_data_recep, y_data_selahattin=y_data_selahattin, y_data_temel=y_data_temel, y_data_dogu=y_data_dogu,
    x_data_line=x_data_line, y_data_muharrem_line=y_data_muharrem_line, y_data_meral_line=y_data_meral_line,
    y_data_recep_line=y_data_recep_line, y_data_selahattin_line=y_data_selahattin_line,
    y_data_temel_line=y_data_temel_line, y_data_dogu_line=y_data_dogu_line)

if __name__ == '__main__':
    app.run(debug=True)

   