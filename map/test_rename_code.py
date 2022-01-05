from common.models import ValueObject, Reader


class RenameCode(object):
    def __init__(self):
        pass

    def excute(self):
        vo = ValueObject()
        reader = Reader()
        vo.context = 'data/'
        vo.fname = 'iso_countries'
        self.csvfile = reader.new_file(vo)
        df = reader.csv(self.csvfile)
        # print(df)
        df.loc[(df.name == 'United States of America'), 'name'] = 'USA'
        df.loc[(df.name == 'United Kingdom of Great Britain and Northern Ireland'), 'name'] = 'UK'
        df.loc[(df.name == 'Russian Federation'), 'name'] = 'Russia'
        df.loc[(df.name == 'Iran (Islamic Republic of)'), 'name'] = 'Iran'
        df.loc[(df.name == 'Viet Nam'), 'name'] = 'Vietnam'
        df.loc[(df.name == 'South Georgia and the South Sandwich Islands'), 'name'] = 'Georgia'
        df.loc[(df.name == 'United Arab Emirates'), 'name'] = 'UAE'
        df.loc[(df.name == 'Bolivia (Plurinational State of)'), 'name'] = 'Bolivia'
        df.loc[(df.name == 'Palestine, State of'), 'name'] = 'Palestine'
        df.loc[(df.name == 'Venezuela (Bolivarian Republic of)'), 'name'] = 'Venezuela'
        df.loc[(df.name == 'Korea, Republic of'), 'name'] = 'S. Korea'
        df.loc[(df.name == 'Moldova, Republic of'), 'name'] = 'Moldova'
        df.loc[(df.name == "Côte d'Ivoire"), 'name'] = 'Ivory Coast'
        df.loc[(df.name == "Congo, Democratic Republic of the"), 'name'] = 'DRC'
        df.loc[(df.name == "Lao People's Democratic Republic"), 'name'] = 'Laos'
        df.loc[(df.name == "Syrian Arab Republic"), 'name'] = 'Syria'
        df.loc[(df.name == "Tanzania, United Republic of"), 'name'] = 'Tanzania'
        df.loc[(df.name == "Taiwan, Province of China"), 'name'] = 'Taiwan'
        df.loc[(df.name == "Jersey"), 'name'] = 'Channel Islands'
        df.loc[(df.name == "Brunei Darussalam"), 'name'] = 'Brunei'
        df.loc[(df.name == "Central African Republic"), 'name'] = 'CAR'
        df.loc[(df.name == "Saint Vincent and the Grenadines"), 'name'] = 'St. Vincent Grenadines'
        df.loc[(df.name == "Sint Maarten (Dutch part)"), 'name'] = 'Sint Maarten'
        df.loc[(df.name == "Saint Martin (French part)"), 'name'] = 'Saint Martin'
        df.loc[(df.name == "Turks and Caicos Islands"), 'name'] = 'Turks and Caicos'
        df.loc[(df.name == "Faroe Islands"), 'name'] = 'Faeroe Islands'
        df.loc[(df.name == "Virgin Islands (British)"), 'name'] = 'British Virgin Islands'
        df.loc[(df.name == "Saint Barthélemy"), 'name'] = 'St. Barth'
        df.loc[(df.name == "Falkland Islands (Malvinas)"), 'name'] = 'Falkland Islands'
        df.loc[(df.name == "Saint Pierre and Miquelon"), 'name'] = 'Saint Pierre Miquelon'
        df.loc[(df.name == "Saint Helena, Ascension and Tristan da Cunha"), 'name'] = 'Saint Helena'
        df.loc[(df.name == "Micronesia (Federated States of)"), 'name'] = 'Micronesia'
        df.to_csv(vo.context + 'new_data/new_iso_countries.csv', index=False)


if __name__ == '__main__':
    r = RenameCode()
    r.excute()