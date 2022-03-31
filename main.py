from _csv import reader
from _pydecimal import Decimal
from enum import Enum
import math

import numpy as np


class Star:
    def __init__(self, apparent_magnitude, distance, spectral_type, hostname):
        self.apparent_magnitude = apparent_magnitude
        self.distance = distance
        self.spectral_type = spectral_type
        self.hostname = hostname

    def calculate_habitable_zone(self):
        absolute_magnitude = self.apparent_magnitude - (5 * math.log10(self.distance / 10))
        bolometric_magnitude = absolute_magnitude + self.spectral_type.value
        absolute_luminosity = math.pow(10, (bolometric_magnitude - 4.72) / -2.5)
        inner_border = math.sqrt(absolute_luminosity / 1.1)
        outer_border = math.sqrt(absolute_luminosity / 0.53)
        return Decimal(inner_border), Decimal(outer_border)


class Planet:
    def __init__(self, planet_name, semi_major_axis, in_habitable_zone):
        self.planet_name = planet_name
        self.semi_major_axis = semi_major_axis
        self.in_habitable_zone = in_habitable_zone


class SpectralType(Enum):
    B = -2
    M = -2
    A = -0.3
    F = -0.15
    G = -0.4
    K = -0.8

    @staticmethod
    def find_by_name(name):
        for spectral_type_name, value in SpectralType.__members__.items():
            if spectral_type_name == name:
                return value
        raise Exception


if __name__ == '__main__':
    with open('Resources/info/stat_csv.txt', 'r') as file:
        csv_reader = reader(file)
        header = next(csv_reader)
        # Check file as empty
        if header != None:
            # Iterate over each row after the header in the csv
            stars = dict()
            planets = dict()
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                star = Star(
                    apparent_magnitude=float(row[4]),
                    distance=float(row[3]),
                    spectral_type=SpectralType.find_by_name(row[6][:1]),
                    hostname=row[0]
                )
                star_habitable_zone = star.calculate_habitable_zone()
                stars[star.hostname] = star_habitable_zone

                # planet = Planet(
                #     planet_name=row[0] + row[1],
                #     semi_major_axis=row[2],
                #     in_habitable_zone=
                #
                # )

                # if star_habitable_zone[0] <= Decimal(row[2]) <= star_habitable_zone[1]:
                #   print("FROM %s  TO  %s   VALUE-->> %s" % (star_habitable_zone[0], star_habitable_zone[1], Decimal(row[2])))
                planets[row[0] + ' ' + row[1]] = star_habitable_zone[0] <= Decimal(row[2]) <= star_habitable_zone[1]

            for hostname, habitable_range in stars.items():
               print('Habitable zone for star %s is from %s to %s' % (hostname, habitable_range[0], habitable_range[1]))

            for planet_name, in_habitable_zone in planets.items():
                print('Planet %s is in habitable zone -> %s' % (planet_name, in_habitable_zone))


            habitable = 0
            not_habitable = 0
            for planet_name, in_habitable_zone in planets.items():
                if(in_habitable_zone):
                    habitable += 1
                else:
                    not_habitable += 1

            print("Habitable -> %s \nUnhabitable -> %s" %(habitable, not_habitable))

            p = {'Is it habitable': ['yes', 'no'], 'Habitation': [69, 1222], 'Name': ['Habitable', 'Not habitable']}
            df = pn.DataFrame(data=p)

            print(df)

            print('Total number of stars is %s' % len(stars))

            print('Total number of planets is %s' % len(planets))

            fig, ax = pyl.subplots(figsize=(6, 6))
            pyl.rcParams['font.sans-serif'] = 'Arial'
            pyl.rcParams['font.family'] = 'sans-serif'
            pyl.rcParams['text.color'] = '#909090'
            pyl.rcParams['axes.labelcolor'] = '#909090'
            pyl.rcParams['xtick.color'] = '#909090'
            pyl.rcParams['ytick.color'] = '#909090'
            pyl.rcParams['font.size'] = 12
            color_palette_list = ['#009ACD', '#ADD8E6', '#63D1F4', '#0EBFE9',
                                  '#C1F0F6', '#0099CC']
            ind = np.arange(len(df['Is it habitable']))
            bars1 = ax.bar(ind, df['Habitation'],

                           color=color_palette_list,
                           label='Name')

            ax.set_title("Habitable zone")
            ax.set_ylabel("Number of planets")
            ax.set_ylim((0, 1300))
            ax.set_xticks(range(len(ind)))
            ax.set_xticklabels(['Habitable', 'Not Habitable'])
            ax.set_xlabel("Zones")

            pyl.show()

