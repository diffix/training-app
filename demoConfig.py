# We use python here instead of JSON so that we have the convenience of writing queries verbatim.
exampleList = [
  {
    "heading": "Welcome",
    "description": '''
    <p class="desc">
Welcome to the Diffix for PostgreSQL Training App. Use this app to understand the capabilities and limitations of Diffix Elm, and how to get the most out of Diffix Elm. Follow the prepared queries in the topics on the left, or write your own queries.
    <p class="desc">
For more information, visit the Open Diffix project website at <a target=_blank href="https:/open-diffix.org">open-diffix.org</a>, or contact us at hello@open-diffix.org.''',
    "dbname": "",
    "mode": "trusted",
    "diffix": {
      "sql": ""
    },
    "native": {
      "sql": ""
    }
  },
  {
    "heading": "Using the app",
    "description": '''
    <p class="desc">
A series of examples are listed on the left. Each example provides SQL queries for both Diffix Elm and the native data. The blue SQL window below on the left is for Diffix Elm, while the green one on the right is for the raw (non-anonymized) output. You may modify the queries or write new ones. Note that the SQL syntax for Diffix Elm and native SQL can be different.
    <p class="desc">
    For users new to the system, it is useful to take the examples in the order provided.
    <p class="desc">
    The app displays the results of a cached query. Click "Run" to re-execute the query for both Diffix Elm and native, or to execute any changes you make to the SQL.
    <p class="desc">
    This app has access to several different databases; <a target=_blank href="https://www.gda-score.org/resources/databases/czech-banking-data/">banking0</a>, <a target=_blank href="https://www.gda-score.org/resources/databases/usa-census-database/">census</a>, <a target=_blank href="https://www.gda-score.org/resources/databases/database-2/">scihub</a>, and <a target=_blank href="https://www.gda-score.org/resources/databases/database-1/">taxi</a>. You must select the appropriate database from the pull-down menu if you write a query.
    <p class="desc">
    The app indicates how many rows are in each answer, and the query execution time for each. However, the app displays only the first 100 rows of data
    <p class="desc">
    In addition to the query results for both Diffix Elm and native queries, the app usually displays the absolute and relative error between the noisy Diffix Elm and correct native answers. The error is not displayed in cases where there is no matching column value between the cloak and the native output for the displayed rows.
    ''',
    "dbname": "",
    "mode": "trusted",
    "diffix": {
      "sql": ""
    },
    "native": {
      "sql": ""
    }
  },
  {
    "heading": "Schema exploration",
    "description": '''<p class="desc">The PostgreSQL commands for listing tables and columns work in Diffix Elm.''',
    "dbname": "",
    "mode": "trusted",
    "diffix": {
      "sql": ""
    },
    "native": {
      "sql": ""
    }
  },
  {
    "heading": "Tables",
    "description": '''
<p class="desc">
Diffix Elm accepts common PostgreSQL methods of listing tables. Note that '\d' works in psql.
''',
    
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';
'''
    },
    "native": {
      "sql": '''
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';
'''
    }
  },
  {
    "heading": "Columns",
    "description": '''
<p class="desc">
Diffix Elm accepts common PostgreSQL methods of listing columns. Note that '\d table_name' works in psql.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'accounts'
'''
    },
    "native": {
      "sql": '''
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'accounts' '''
    }
  },
  {
    "heading": "Personal tables",
    "description": '''
<p class="desc">
Diffix Elm labels tables as either "personal" or "public". 
Personal tables contain personal information (data about persons), and are therefore anonymized. Public tables do not contain personal data, and are not anonymized.
<p class="desc">
The command
<span style="font-family:'Courier New'">diffix.show_labels()</span>
can be used to display table labels.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT objname AS table, label
FROM diffix.show_labels()
WHERE objtype = 'table'
'''
    },
    "native": {
      "sql": '''
'''
    }
  },
  {
    "heading": "AID columns",
    "description": '''
<p class="desc">
For Diffix Elm to anonymize properly, it must recognize which column (or columns) in each personal table identifies the protected entity (or entities).
These columns are given the label "AID" (for Anonymization ID).
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT objname AS aid_column, label
FROM diffix.show_labels()
WHERE objtype = 'column'
'''
    },
    "native": {
      "sql": '''
'''
    }
  },
  {
    "heading": "Anonymization settings",
    "description": '''
<p class="desc">
Diffix Elm has a variety of anonymization parameters that determine for instance how much noise is added, the threshold for suppression, and how suppressed bins are labeled.
<p class="desc">
The command
<span style="font-family:'Courier New'">diffix.show_settings()</span>
displays the parameter settings.
<p class="desc">
The 
<a target=_blank href="
https://arxiv.org/abs/2201.04351
">full Diffix Elm specification</a>
describes how these parameters are used.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT diffix.show_settings()
       AS anonymization_parameters
'''
    },
    "native": {
      "sql": '''
'''
    }
  },
  {
    "heading": "Basic queries",
    "description": '''<p class="desc">
    Diffix Elm allows a tiny but useful subset of SQL. Diffix Elm allows analysts to build multi-column histograms of counts with generalization.
    ''',
    "dbname": "",
    "mode": "trusted",
    "diffix": {
      "sql": ""
    },
    "native": {
      "sql": ""
    }
  },
  {
    "heading": "Counting distinct values",
    "description": '''
        <p class="desc">Count the number of bank accounts.
        ''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT count(DISTINCT account_id)
FROM accounts'''
    },
    "native": {
      "sql": '''
SELECT count(DISTINCT account_id)
FROM accounts'''
    }
  },
  {
    "heading": "Counting events (in time series data)",
    "description": '''<p class="desc">Count the number of rides in the taxi database (one ride per row).''',
    "dbname": "taxi",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT count(*)
FROM jan08'''
    },
    "native": {
      "sql": '''
SELECT count(*)
FROM jan08'''
    }
  },
  {
    "heading": "Histogram of values",
    "description": '''<p class="desc">Count the number of clients in each Client District.''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT acct_district_id AS district,
       count(DISTINCT client_id1)
FROM accounts
GROUP BY 1
ORDER BY 1'''
    },
    "native": {
      "sql": '''
SELECT acct_district_id AS district,
       count(DISTINCT client_id1)
FROM accounts
GROUP BY 1
ORDER BY 1'''
    }
  },
  {
    "heading": "2D Histogram (heat map)",
    "description": '''
<p class="desc">
Histogram of counts of individuals by number of marriages per 5-year age group.
<p class="desc">
Note the use of floor() to generalize the age column.
<p class="desc">
<font color="red">Note query takes around 1/2 minute</font>
''',
    "dbname": "census0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT diffix.floor_by(age,5) AS age, 
       marrno AS marriages,
       count(*)
FROM uidperhousehold
GROUP BY 1,2
ORDER BY 1,2
'''
    },
    "native": {
      "sql": '''
SELECT floor(age/5)*5 as age,
       marrno AS marriages,
       count(*)
FROM uidperhousehold
GROUP BY 1,2
ORDER BY 1,2
'''
    }
  },
  {
    "heading": "Subqueries",
    "description": '''<p class="desc">Average number of transactions per account.
    <p class="desc">
    <font color="red">Note query takes around seven seconds.</font>
    ''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT trans / accounts AS average_trans
FROM (
  SELECT count(*) AS trans,
    count(DISTINCT account_id) AS accounts
  FROM transactions
) t
'''
    },
    "native": {
      "sql": '''
SELECT trans / accounts AS average_trans
FROM (
  SELECT count(*) AS trans,
    count(DISTINCT account_id) AS accounts
  FROM transactions
) t
'''
    }
  },
  {
    "heading": "A common mistake",
    "description": '''
<p class="desc">
SELECT * FROM table LIMIT X
''',
    "dbname": "",
    "mode": "trusted",
    "diffix": {
      "sql": ""
    },
    "native": {
      "sql": ""
    }
  },
  {
    "skip": False,
    "expectErr": True,
    "heading": "SELECT * ... LIMIT X",
    "description": '''
<p class="desc">
TODO: One of the first things an analyst may do when presented with a new database is:
<p class="desc">
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<span style="font-family:'Courier New'">SELECT * ... LIMIT X</span>
<p class="desc">
This gives the analyst an immediate impression of what data he or she is dealing with.
<p class="desc">
Diffix Elm cannot return any useful information with this query, because it filters out any information related to one or a few users. Rather than attempt to run the query (which would take a very long time), Diffix Elm recognizes that the answer would contain nothing and returns an error message to that effect.
<p class="desc">
''',
    "dbname": "scihub",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT *
FROM sep2015
ORDER BY uid
LIMIT 10
'''
    },
    "native": {
      "sql": '''
SELECT *
FROM sep2015
LIMIT 10
'''
    }
  },
  {
    "heading": "Noise",
    "description": '''
<p class="desc">
Diffix Elm adds noise to answers. The following set of examples illustrate how noise is added and potential pitfalls.
<p class="desc">
The following examples are best selected in order.
Read more 
<a target=_blank href="
https://www.open-diffix.org/blog/diffix-elm-automates-what-statistics-offices-have-been-doing-for-decades
">here</a>.
''',
    "dbname": "",
    "mode": "trusted",
    "diffix": {
      "sql": ""
    },
    "native": {
      "sql": ""
    }
  },
  {
    "heading": "Sticky noise",
    "description": '''
<p class="desc">
Diffix Elm has a unique way of adding noise which we call "sticky noise".  Sticky means that the same query produces the same noise. Try re-running this query, and you will see that you get the same noisy answer every time.
<p class="desc">
Note that the absolute noise (the "abs" column in red) is relatively small; rarely more than plus or minus 5. This is always the case when counting persons (the protected entity).
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT acct_district_id,
       count(DISTINCT client_id1)
FROM accounts
GROUP BY 1
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT acct_district_id,
       count(DISTINCT client_id1)
FROM accounts
GROUP BY 1
ORDER BY 1
'''
    }
  },
  {
    "heading": "Proportional noise",
    "description": '''
<p class="desc">
Diffix Elm adds enough noise to hide the influence of individual users. When counting the number of distinct persons (or whatever the protected entity is), then each person contributes exactly one to the count, and so the amount noise is both small and predictable.
<p class="desc">
When counting the number of rows for time-series data, then some persons contribute more than others. The amount of noise inserted by Diffix Elm increases to effectively hide heavy contributors.
<p class="desc">
In this query, noise levels are much higher; absolute error is easily plus or minus 1500. Relative error varies substantially from less than a percent to 10% or more.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT cli_district_id1, count(*)
FROM transactions
GROUP BY 1
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT cli_district_id1, count(*)
FROM transactions
GROUP BY 1
ORDER BY 1
'''
    }
  },
  {
    "heading": "Flattening",
    "description": '''
<p class="desc">
Sometimes data has extreme contributors; one or a few individuals that contribute far more than any other individual. Proportional noise, naively implemented, could reveal the presence or absence of these individuals simply by the amount of distortion. To prevent this, Diffix Elm reduces the contribution of extreme contributors so that they are in line with other heavy contributors. We call this "flattening".
<p class="desc">
While flattening hides extreme contributors, it has the unfortunate effect of adding a systematic negative bias to row counts (though not to counts of individuals).
<p class="desc">
Here is the same query from the proportional noise example. Looking at the "abs:rel" column, we see that the noise is not zero mean: it is negative far more often than positive. 
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT cli_district_id1, count(*)
FROM transactions
GROUP BY 1
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT cli_district_id1, count(*)
FROM transactions
GROUP BY 1
ORDER BY 1
'''
    }
  },
  {
    "heading": "Counting distinct (no noise)",
    "description": '''
<p class="desc">
Diffix Elm supports counting distinct values for any column. Diffix Elm does not necessarily add noise to dictinct counts. In particular, if the values being counted would normally not be suppressed, Diffix Elm gives an exact count.
<p class="desc">
In the example below, the exact number of card types is displayed.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT count(DISTINCT card_type)
FROM cards
'''
    },
    "native": {
      "sql": '''
SELECT count(DISTINCT card_type)
FROM cards
'''
    }
  },
  {
    "heading": "Counting distinct (no noise)",
    "heading": "-&nbsp&nbsp&nbspEquivalent Histogram",
    "description": '''
<p class="desc">
This is another way to count the number of distinct card types. Since no suppression takes place, an exact count is in any event allowed.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT card_type, count(*)
FROM cards
GROUP BY 1
'''
    },
    "native": {
      "sql": '''
SELECT card_type, count(*)
FROM cards
GROUP BY 1
'''
    }
  },
  {
    "heading": "Counting distinct (with noise)",
    "description": '''
<p class="desc">
When suppression would prevent viewing all column values, counting distinct values does add noise.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT count(DISTINCT loan_date)
FROM loans
'''
    },
    "native": {
      "sql": '''
SELECT count(DISTINCT loan_date)
FROM loans
'''
    }
  },
  {
    "heading": "Suppression",
    "description": '''
<p class="desc">
Diffix Elm suppresses answers that pertain to too few individuals. The following set of example illustrate this anonymization mechanism.
Read more 
<a target=_blank href="
https://www.open-diffix.org/blog/diffix-elm-automates-what-statistics-offices-have-been-doing-for-decades
">here</a>.
''',
    "dbname": "",
    "mode": "trusted",
    "diffix": {
      "sql": ""
    },
    "native": {
      "sql": ""
    }
  },
  {
    "heading": "Text",
    "description": '''
<p class="desc">
This example queries for the number of clients with each last name and displays them in descending order.
<p class="desc">
Simply adding noise to an answer is not enough to preserve anonymity. If there is only one user in the database with a given last name, then merely displaying this last name would single out that person and therefore be considered personal data by GDPR criteria.
<p class="desc">
The native answer here shows that there are over 3000 distinct last names in the database. Diffix Elm, however, reveals only a fraction of these names: those that are shared by enough clients. The remaining names are hidden.
<p class="desc">
To inform the analyst that last names have been suppressed, and to give an indication of how much data has been suppressed, Diffix Elm places all of the suppressed rows in a bucket labeled
&nbsp<span style="font-family:'Courier New'">*</span>&nbsp
and then displays the anonymized aggregate for that bucket.
<p class="desc">
For this query, essentially what happens is that all suppressed last names are replaced with the value
&nbsp<span style="font-family:'Courier New'">*</span>&nbsp
and then displayed as though
&nbsp<span style="font-family:'Courier New'">*</span>&nbsp
is a last name. From this we see that there are nearly 4000 clients whose last names have been suppressed.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT lastname1,
       count(DISTINCT client_id1)
FROM accounts
GROUP BY 1
ORDER BY 2 DESC
'''
    },
    "native": {
      "sql": '''
SELECT lastname1,
       count(DISTINCT client_id1)
FROM accounts
GROUP BY 1
ORDER BY 2 DESC
'''
    }
  },
  {
    "heading": "Numbers",
    "description": '''
<p class="desc">
This query similarly has substantial suppression, but this time displaying numbers instead of text.
<p class="desc">
In this case, rather than return
&nbsp<span style="font-family:'Courier New'">*</span>&nbsp
as the default symbol for identifying the suppression bucket, Diffix Elm returns
&nbsp<span style="font-family:'Courier New'">NULL</span>&nbsp
(which here is displayed as 'None' because of the python implementation of this training program). Diffix Elm can't return
&nbsp<span style="font-family:'Courier New'">*</span>&nbsp
for numbers because
&nbsp<span style="font-family:'Courier New'">*</span>&nbsp
is a string and therefore the wrong type.
<p class="desc">
Note however that NULL values may represent both suppressed data and true NULL entries in the data.
''',
    "dbname": "taxi",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT pickup_latitude,
       count(*)
FROM jan08
GROUP BY 1
ORDER BY 2 DESC
'''
    },
    "native": {
      "sql": '''
SELECT pickup_latitude,
       count(*)
FROM jan08
GROUP BY 1
ORDER BY 2 DESC
'''
    }
  },
  {
    "heading": "-&nbsp&nbsp&nbspSmarter query (generalization)",
    "description": '''
<p class="desc">
In cases where there is substantial suppression, the analyst may use generalization (in this case, the 'diffix.floor_by()' function) to avoid excessive suppression.
<p class="desc">
In the example below, the Diffix Elm output does show a suppression bin (row labeled 'None'), but there are relatively few rows in this bin: very little of the data is being suppressed.
''',
    "dbname": "taxi",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT diffix.floor_by(pickup_latitude,
                   0.0001) AS latitude,
       count(*)
FROM jan08
GROUP BY 1
ORDER BY 2 DESC
'''
    },
    "native": {
      "sql": '''
SELECT floor(pickup_latitude*10000)/10000
           AS latitude,
       count(*)
FROM jan08
GROUP BY 1
ORDER BY 2 DESC
'''
    }
  },
  {
    "heading": "Protected Entities (PE)",
    "description": '''
<p class="desc">
All personal tables must have one or more columns that identify the entities whose privacy is being protected. At a minimum, the individual person must be protected, but Diffix Elm can protect multiple different kinds of entities.
<p class="desc">
It is useful to for the analyst to know what columns identify the protected entities. This is because the amount of noise is more predictable for these columns (there is no flattening, and the noise is not proportional because each protected entity contributes the same amount).
<p class="desc">
Diffix Elm offers a function, 
<span style="font-family:'Courier New'">diffix.show_labels()</span>,
that shows which columns identify protected entities.
Such columns are labeled 'aid' (for Anonymization ID). 
''',
    "dbname": '',
    "mode": "trusted",
    "diffix": {
      "sql": ''
    },
    "native": {
      "sql": ''
    }
  },
  {
    "heading": "Taxi Driver (hack)",
    "description": '''
<p class="desc">
The NYC Taxi table does not contain data about riders. If it did, these would certainly be protected entities. It does, however, identify the driver (the 'hack' column). To protect drivers' anonymity, the 'hack' column is labeled as the protected entity ('aid').
''',
    "dbname": "taxi",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT objname, label FROM 
diffix.show_labels()
WHERE label = 'aid';
'''
    },
    "native": {
      "sql": ''''''
    }
  },
  {
    "heading": "Multiple PE types",
    "description": '''
<p class="desc">
Diffix Elm can protect multiple entities of different types. An example of this can be found in the Banking database, where both individual clients (persons) and bank accounts are protected. Some accounts are joint accounts (two persons). Even though strictly speaking two persons is not a singled-out individual, and does not necessarily require protection by GDPR criteria, it is certainly desirable that accounts be protected as well as inidividual clients.
<p class="desc">
This query displays the two protected entity types for the banking 'accounts' table.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT objname, label FROM 
diffix.show_labels()
WHERE label = 'aid' AND
      objname LIKE '%accounts%';
'''
    },
    "native": {
      "sql": ''''''
    }
  },
  {
    "heading": "Multiple PE roles",
    "description": '''
<p class="desc">
When data describes interactions between persons, all persons in the interaction must be protected. This can be found in the 'orders' table of the Banking data, where both the sending account ('account_id') and receiving account ('account_to') are included. The 'client_id1' is the client associated with the 'account_id', and is also protected.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT objname, label FROM 
diffix.show_labels()
WHERE label = 'aid' AND
      objname LIKE '%orders%';
'''
    },
    "native": {
      "sql": ''''''
    }
  },
  {
    "heading": "Generalization",
    "description": '''
<p class="desc">
The key to avoiding excessive suppression or noise is to generalize data. Larger bins are less likely to be suppressed, and the relative noise is also less.
<p class="desc">
Diffix Elm supports text and numeric columns.
<p class="desc">
The generalization function for text is:
<p class="desc">-  substring(col,offset,length)</p>
<p class="desc">
The generalization functions for numeric are:
<p class="desc">-  diffix.floor_by(col,bin_size)</p>
<p class="desc">-  diffix.round_by(col,bin_size)</p>
<p class="desc">-  diffix.ceil_by(col,bin_size)</p>
<p class="desc">-  width_bucket(col,low,high,count)</p>
''',
    "dbname": '',
    "mode": "trusted",
    "diffix": {
      "sql": ''
    },
    "native": {
      "sql": ''
    }
  },
  {
    "heading": "Example 1",
    "description": '''
<p class="desc">
This query counts the number of taxi rides in each hour in a square grid of roughly 1km by 1km. It demonstrates the use of both text and numeric generalization.
<p class="desc">
The native column type for the pickup_datetime column is datetime, so it must be cast as text for the substring() function. (The native query could have used date_trunc(), but we use substring() here as well to produce identical values.)
<p class="desc">
The amount of suppression is relatively small (roughly 5000 of 440K rows, or roughly 1%)
''',
    "dbname": "taxi",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT substring(cast(pickup_datetime
      AS text),1,13) AS hour,
    diffix.round_by(pickup_latitude,0.01)
      AS lat,
    diffix.round_by(pickup_longitude,0.01)
      AS lon,
    count(*)
FROM jan08
GROUP BY 1,2,3
ORDER BY 1,2,3
'''
    },
    "native": {
      "sql": '''
SELECT substring(cast(pickup_datetime
      AS text),1,13) AS hour,
    diffix.round_by(pickup_latitude,0.01)
      AS lat,
    diffix.round_by(pickup_longitude,0.01)
      AS lon,
    count(*)
FROM jan08
GROUP BY 1,2,3
ORDER BY 1,2,3
'''
    }
  },
  {
    "heading": "Example 2",
    "description": '''
<p class="desc">
This query counts the number of transactions for 11 equal-sized buckets for the column amount in the range from 0 to 80000.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT width_bucket(amount,0,80000,10),
       count(*)
FROM transactions
GROUP BY 1
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT width_bucket(amount,0,80000,10),
       count(*)
FROM transactions
GROUP BY 1
ORDER BY 1
'''
    }
  },
  {
    "heading": "Trusted and Untrusted",
    "description": '''
<p class="desc">
Diffix Elm operates in two modes, Trusted Analyst and Untrusted Analyst.
<p class="desc">
Trusted Analyst mode prevents accidental release of personal data.
<p class="desc">
Untrusted Analyst mode prevents intentional release of personal data.
<p class="desc">
Untrusted Analyst mode places additional restrictions on the generalization functions. Otherwise, the two modes behave identically (i.e. the same amount of noise and suppression).
''',
    "dbname": '',
    "mode": "trusted",
    "diffix": {
      "sql": ''
    },
    "native": {
      "sql": ''
    }
  },
  {
    "heading": "Floor, round, ceil",
    "description": '''
<p class="desc">
Whereas Trusted Analyst mode allows any bucket width in the floor(), round(), and ceil() functions, Untrusted Analyst mode constrains the allowed widths to values in the sequence <... 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50 ...>
<p class="desc">
This query allows bucket sizes of three in Trusted Analyst mode.
''',
    "dbname": "census0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT diffix.floor_by(age,3) AS age,
       count(*)
FROM uidperhousehold
GROUP BY 1
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT floor(age/3)*3 AS age,
       count(*)
FROM uidperhousehold
GROUP BY 1
ORDER BY 1
'''
    }
  },
  {
    "heading": "-&nbsp&nbsp&nbspFails for untrusted",
    "description": '''
<p class="desc">
The same query fails in Untrusted Analyst mode.
''',
    "dbname": "census0",
    "mode": "untrusted",
    "diffix": {
      "sql": '''
SELECT diffix.floor_by(age,3) AS age,
       count(*)
FROM uidperhousehold
GROUP BY 1
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT floor(age/3)*3 AS age,
       count(*)
FROM uidperhousehold
GROUP BY 1
ORDER BY 1
'''
    }
  },
  {
    "heading": "Substring",
    "description": '''
<p class="desc">
Whereas Trusted Analyst mode allows substrings at any offset, Untrusted Analyst mode allows substrings only from the left.
<p class="desc">
This query allows substrings from the third text character
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT substring(lastname1,3,2) AS snippet,
       count(*)
FROM accounts
GROUP BY 1
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT substring(lastname1,3,2) AS snippet,
       count(*)
FROM accounts
GROUP BY 1
ORDER BY 1
'''
    }
  },
  {
    "heading": "-&nbsp&nbsp&nbspFails for untrusted",
    "description": '''
<p class="desc">
The same query fails in Untrusted Analyst mode.
''',
    "dbname": "banking0",
    "mode": "untrusted",
    "diffix": {
      "sql": '''
SELECT substring(lastname1,3,2) AS snippet,
       count(*)
FROM accounts
GROUP BY 1
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT substring(lastname1,3,2) AS snippet,
       count(*)
FROM accounts
GROUP BY 1
ORDER BY 1
'''
    }
  },
  {
    "heading": "More functions",
    "description": '''
<p class="desc">
The SQL features that work with Diffix Elm are powerful but limited. Diffix Elm, however, does allow for post-processing with SQL through the use of nested queries. The inner query is anonymized (and has limited SQL), while the outer query has no SQL limitations. zzzz
''',
    "dbname": '',
    "mode": "trusted",
    "diffix": {
      "sql": ''
    },
    "native": {
      "sql": ''
    }
  },
  {
    "heading": "Text processing",
    "description": '''
<p class="desc">
In this query, the age column is post-processed to make it clear what the age ranges are.
''',
    "dbname": 'census0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT concat(age,'-',age+4) AS age,
       num_persons FROM
( SELECT diffix.floor_by(age,5) AS age,
         count(*) AS num_persons
  FROM uidperhousehold
  GROUP BY 1
  ORDER BY 1
) t
      '''
    },
    "native": {
      "sql": '''
SELECT concat(age,'-',age+4) AS age,
       num_persons FROM
( SELECT diffix.floor_by(age,5) AS age,
         count(*) AS num_persons
  FROM uidperhousehold
  GROUP BY 1
  ORDER BY 1
) t
      '''
    }
  },
  {
    "heading": "Average events per protected entity",
    "description": '''
<p class="desc">
This query computes the average number of transactions per person.
<p class="desc">
Diffix Elm anonymizes the inner query (or "anonymizing query"), and the division operation is done as post processing.
<p class="desc">
Note that the native query could have been written the same way, but instead we use the PostgreSQL avg() function (which is not yet natively available in Diffix Elm). The native query would fail under Diffix Elm because account_id is a protected entity, and would produce no output in the anonymizing query.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT num_trans::float/num_accounts AS avg
FROM (
  SELECT count(*) AS num_trans,
         count(DISTINCT account_id)
             AS num_accounts
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT avg(act_cnt) AS avg
FROM (
  SELECT account_id,
         count(*) AS act_cnt
  FROM transactions
  GROUP BY 1
) t
      '''
    }
  },
  {
    "heading": "-&nbsp&nbsp&nbspAs a histogram",
    "description": '''
<p class="desc">
This likewise computes the average number of transactions per account, but this time as a histogram on transaction type.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT trans_type,
       num_trans::float/num_accounts
           AS avg
FROM (
  SELECT trans_type,
         count(*) AS num_trans,
         count(DISTINCT account_id)
             AS num_accounts
  FROM transactions
  GROUP BY 1
) t
      '''
    },
    "native": {
      "sql": '''
SELECT trans_type,
       avg(act_cnt) AS avg
FROM (
  SELECT trans_type, account_id,
         count(*) AS act_cnt
  FROM transactions
  GROUP BY 1,2
) t
GROUP BY 1
      '''
    }
  },
  {
    "heading": "Sum of column",
    "description": '''
<p class="desc">
This query computes the sum of all transaction amounts.
<p class="desc">
The technique used here is to avoid suppression by zzzz
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT sum(rounded_amount)
FROM (
  SELECT diffix.round_by(amount,1000)
         AS rounded_amount
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT sum(amount)
FROM transactions
      '''
    }
  },
  {
    "heading": "Max",
    "description": '''
<p class="desc">
This query computes the maximum of all transaction amounts.
<p class="desc">
Diffix Elm does not have a built-in max() function, but a maximum can be approximated by taking the highest value of a histogram that has little or no suppression.
<p class="desc">
This requires fine tuning: the analyst must discover the largest bucket size that nevertheless leads to little or not suppression, and then use that bucket size in the SQL expression shown here.
<p class="desc">
Note that often the max value is often unique to one individual, and so reporting a max would in any event constitute singling-out and be regarded as personal data by GDPR criteria.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT max(amount)
FROM (
  SELECT diffix.ceil_by(amount,1000)
         AS amount,
         count(*)
  FROM transactions
  GROUP BY 1
) t
      '''
    },
    "native": {
      "sql": '''
SELECT max(amount)
FROM transactions
      '''
    }
  },
  {
    "heading": "Min",
    "description": '''
<p class="desc">
This query computes the minimum of all transaction amounts.
<p class="desc">
As with max, Diffix Elm approximates the min() function by taking the lowest value of a histogram that has little or no suppression.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT min(amount)
FROM (
  SELECT diffix.floor_by(amount,1000)
         AS amount,
         count(*)
  FROM transactions
  GROUP BY 1
) t
      '''
    },
    "native": {
      "sql": '''
SELECT min(amount)
FROM transactions
      '''
    }
  },
  {
    "heading": "Median",
    "description": '''
<p class="desc">
This query computes the median of all transaction amounts.
<p class="desc">
Here again, Diffix Elm approximates median() using a histogram that has little or no suppression. Unlike the min() and max() examples, however, here the anonymizing query does not have an aggregate count and associated GROUP BY. When there is no GROUP BY, Diffix Elm internally adds count(*), computes the corresponding buckets, and then outputs the number of rows corresponding to the noisy counts.
<p class="desc">
The resulting table can then be read diretly into PostgreSQL's PERCENTILE_CONT() function to estimate the median (or any other percentile).
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT PERCENTILE_CONT(0.5) WITHIN 
GROUP(ORDER BY amount)
FROM (
  SELECT diffix.round_by(amount,1000)
         AS amount
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT PERCENTILE_CONT(0.5) WITHIN 
GROUP(ORDER BY amount)
FROM transactions
      '''
    }
  },
  {
    "heading": "Visit again!",
    "description": '''
<p class="desc">
We are constantly adding new examples, so visit again from time to time!
''',
    "dbname": "",
    "mode": "trusted",
    "diffix": {
      "sql": ""
    },
    "native": {
      "sql": ""
    }
  }
]

def getExampleList():
    return exampleList

