import sqlite3
import csv

query = """
SELECT
  'MOUTH',
  p.cldf_id,
  COUNT(*) AS n
FROM
  formtable AS f,
  parametertable AS p
WHERE
  f.cldf_parameterReference = p.cldf_id
    AND
  ' ' || f.partial_cognacy || ' ' LIKE '% 121 %'
GROUP BY
  p.cldf_id
ORDER BY
  n DESC
;
"""

db = sqlite3.connect('ppt.sqlite3')
cursor = db.cursor()

# Execute query
cursor.execute(query)
table = cursor.fetchall()

for row in table:
    print(row)

# Write results to tsv
with open('mouth.tsv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['CORE', 'CONCEPT', 'COUNT'])
    writer.writerows(table)
