import re
import json
import pandas as pd

from workflow.cleaning import split_months
from workflow.summary import monthly_summary
from workflow.details import split_countries,split_refunds

LANG = 'FR'

with open('utils/months.json') as f:
    months = json.load(f)

def nice_items(items:str):
    items = str(items)
    word_list = re.findall(r'[A-Z][a-z]+',items)
    item = ','.join(word_list)
    return item

def full_infos(df:pd.DataFrame) -> dict:
    data = split_months(df)
    for month in data.keys():
        monthly = {}
        monthly['summaries'] = monthly_summary(data[month])
        monthly['countries'] = split_countries(data[month])
        data[month] = monthly
        for country in data[month]['countries'].keys():
            data[month]['countries'][country]=split_refunds(data[month]['countries'][country])
    return data

def fill_lines(monthly_data:dict) -> list:
    eu_list = list(monthly_data['summaries']['eu'].index)
    eu_list.pop()
    world_list = list(monthly_data['summaries']['world'].index)
    world_list.pop()
    lines = ['\n## Tableau résumé EU\n']
    lines.append(monthly_data['summaries']['eu'].to_markdown())
    lines.append('\n## Tableau résumé hors-EU\n')
    lines.append(monthly_data['summaries']['world'].to_markdown())
    lines.append('\n## Tableau détails par pays\n')
    lines.append('\n### EU\n')
    for c in eu_list:
        lines.append(f'\n#### {c}\n')
        lines.append(f'\n##### Recettes\n')
        lines.append(monthly_data['countries'][c]['paid'].to_markdown())
        lines.append(f'\n##### Remboursements\n')
        lines.append(monthly_data['countries'][c]['refunds'].to_markdown())
    lines.append('\n### Hors-EU\n')
    for c in world_list:
        lines.append(f'\n#### {c}\n')
        lines.append(f'\n##### Recettes\n')
        lines.append(monthly_data['countries'][c]['paid'].to_markdown())
        lines.append(f'\n##### Remboursements\n')
        lines.append(monthly_data['countries'][c]['refunds'].to_markdown())
    return lines

def write_files(df:pd.DataFrame,path:str):
    data = full_infos(df)
    for month in data:
        lines = fill_lines(data[month])
        with open(f'{path}-{month}.md','w') as f:
            f.write(f'# Récapitulatif du mois de {months[LANG][month]}\n')
            f.writelines(lines)