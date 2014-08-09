#!/usr/bin/env python
#
# Script to pull down US Census data for the ASA Hackathon
# By Pete Warden <pete@petewarden.com> 2014
# Released under the MIT License

from us import states
from census import Census

# You'll need to get your own key at http://www.census.gov/developers/
CENSUS_API_KEY='b4e8add27414d5f6165ff485a6503b168cdf0c59'

# Each row of this table is <readable label>, <2010 code>, <2000 code>
WANTED_CODES = [
  ['Population', 'P0030001', 'P003001'],
  ['White', 'P0030002', 'P003002'],
  ['Black or African American', 'P0030003', 'P003003'],
  ['American Indian and Alaska Native', 'P0030004', 'P003004'],
  ['Asian', 'P0030005', 'P003005'],
  ['Native Hawaiian and Other Pacific Islander', 'P0030006', 'P003006'],
  ['Other Race', 'P0030007', 'P003007'],
  ['Two or More Races', 'P0030008', 'P003008'],
  ['Not Hispanic or Latino', 'P0040002', 'P004002'],
  ['Hispanic or Latino', 'P0040003', 'P004003'],
  ['Male', 'P0120002', 'P012002'],
  ['Female', 'P0120026', 'P012026'],
  ['Median Age', 'P0130001', 'P013001'],
  ['Households', 'P0180001', 'P018001'],
  ['Family Households', 'P0180002', 'P018002'],
  ['Husband-wife family', 'P0180003', 'P018003'],
  ['Male no wife present', 'P0180005', 'P018005'],
  ['Female no husband present', 'P0180006', 'P018006'],
  ['Living alone', 'P0180008', 'P018008'],
  ['Living with roommates', 'P0180008', 'P018008'],
  ['Households with over-60\'s', 'P0240002', 'P024002'],
]
WANTED_YEARS = [2010, 2000]
STATE_FIPS = states.CA.fips
COUNTY_FIPS = '075' # 075 is San Francisco County

c = Census(CENSUS_API_KEY)

statistics_by_tract = {}

for code_info in WANTED_CODES:
  label = code_info[0]
  for index, year in enumerate(WANTED_YEARS):
    code = code_info[index + 1]
    statistics_for_code = c.sf1.state_county_tract(code, STATE_FIPS, COUNTY_FIPS, Census.ALL, year=year)
    if len(statistics_for_code) == 0:
      print "Bad result for " + code
      exit(1)
    for row in statistics_for_code:
      tract_id = row['tract']
      if len(tract_id) == 5:
        tract_id = '0' + tract_id
      if tract_id not in statistics_by_tract:
        statistics_by_tract[tract_id] = {}
      key = label + ' ' + str(year)
      statistics_by_tract[tract_id][key] = row[code]

headers = ['Tract ID']
for code_info in WANTED_CODES:
  label = code_info[0]
  for year in WANTED_YEARS:
    key = label + ' ' + str(year)
    headers.append(key)

print ','.join(headers)

for tract_id, tract_statistics in statistics_by_tract.items():
  values = [tract_id]
  for code_info in WANTED_CODES:
    label = code_info[0]
    for index, year in enumerate(WANTED_YEARS):
      key = label + ' ' + str(year)
      if key in tract_statistics:
        value = tract_statistics[key]
      else:
        value = ''
      values.append(value)
  print ','.join(values)
