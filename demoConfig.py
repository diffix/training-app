# We use python here instead of JSON so that we have the convenience of writing queries verbatim.
exampleList = [
  {
    "heading": "Welcome",
    "description": '''
    <p class="desc">
Welcome to the Diffix for PostgreSQL Training App. Use this app to understand the capabilities and limitations of pg_diffix, the PostgreSQL extension that implements Diffix Fir. Follow the prepared queries in the topics on the left, or write your own queries.
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
A series of examples are listed on the left. Each example provides SQL queries for both pg_diffix and the native data. The blue SQL window below on the left is for pg_diffix, while the green one on the right is for the raw (non-anonymized) output. You may modify the queries or write new ones. Note that the SQL syntax for pg_diffix and native SQL can be different.
    <p class="desc">
    For users new to the system, it is useful to take the examples in the order provided.
    <p class="desc">
    The app displays the results of a cached query. Click "Run" to re-execute the query for both pg_diffix and native, or to execute any changes you make to the SQL.
    <p class="desc">
    This app has access to several different databases; <a target=_blank href="https://www.gda-score.org/resources/databases/czech-banking-data/">banking0</a>, <a target=_blank href="https://www.gda-score.org/resources/databases/usa-census-database/">census</a>, <a target=_blank href="https://www.gda-score.org/resources/databases/database-2/">scihub</a>, and <a target=_blank href="https://www.gda-score.org/resources/databases/database-1/">taxi</a>. You must select the appropriate database from the pull-down menu if you write a query.
    <p class="desc">
    The app indicates how many rows are in each answer, and the query execution time for each. However, the app displays only the first 100 rows of data
    <p class="desc">
    In addition to the query results for both pg_diffix and native queries, the app usually displays the absolute and relative error between the noisy pg_diffix and correct native answers. The error is not displayed in cases where there is no matching column value between the cloak and the native output for the displayed rows.
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
    "heading": "<u>PART 1: BASICS</u>",
    "description": '''
    <p class="desc">
This first set of examples introduces the basic pg_diffix features, and the concepts of data distortion (noise and suppression). This is enough to get started with pg_diffix and produce simple but useful anonymized data.
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
    "description": '''<p class="desc">The PostgreSQL commands for listing tables and columns work in pg_diffix.''',
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
pg_diffix accepts common PostgreSQL methods of listing tables. Note that '\d' works in psql.
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
pg_diffix accepts common PostgreSQL methods of listing columns. Note that '\d table_name' works in psql.
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
    "heading": "Basic queries",
    "description": '''<p class="desc">
    pg_diffix allows a tiny but useful subset of SQL. pg_diffix allows analysts to build multi-column histograms of counts with generalization.
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
    "heading": "Sums",
    "description": '''
<p class="desc">
Histogram over type of operation of sum of transactions amounts.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT operation,
       sum(amount)
FROM transactions
GROUP BY 1
ORDER BY 2
'''
    },
    "native": {
      "sql": '''
SELECT operation,
       sum(amount)
FROM transactions
GROUP BY 1
ORDER BY 2
'''
    }
  },
  {
    "heading": "Averages",
    "description": '''
<p class="desc">
Histogram over type of operation of average of transactions amounts.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT operation,
       avg(amount)
FROM transactions
GROUP BY 1
ORDER BY 2
'''
    },
    "native": {
      "sql": '''
SELECT operation,
       avg(amount)
FROM transactions
GROUP BY 1
ORDER BY 2
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
pg_diffix cannot return any useful information with this query, because it filters out any information related to one or a few users. Rather than attempt to run the query (which would take a very long time), pg_diffix recognizes that the answer would contain nothing and returns an error message to that effect.
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
    "heading": "Distortion",
    "description": '''
<p class="desc">
Diffix Fir distorts data in two ways. First, it adds noise to counts. Second, it suppresses output bins that pertain to too few protected entities (e.g. individual persons).
<p class="desc">
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
pg_diffix has a unique way of adding noise which we call "sticky noise".  Sticky means that the same query produces the same noise. Try re-running this query, and you will see that you get the same noisy answer every time.
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
pg_diffix adds enough noise to hide the influence of individual users. When counting the number of distinct persons (or whatever the protected entity is), then each person contributes exactly one to the count, and so the amount noise is both small and predictable.
<p class="desc">
When counting the number of rows for time-series data, then some persons contribute more than others. The amount of noise inserted by pg_diffix increases to effectively hide heavy contributors.
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
    "heading": "Suppression (text)",
    "description": '''
<p class="desc">
This example queries for the number of clients with each last name and displays them in descending order.
<p class="desc">
Simply adding noise to an answer is not enough to preserve anonymity. If there is only one user in the database with a given last name, then merely displaying this last name would single out that person and therefore be considered personal data by GDPR criteria.
<p class="desc">
The native answer here shows that there are over 3000 distinct last names in the database. pg_diffix, however, reveals only a fraction of these names: those that are shared by enough clients. The remaining names are hidden.
<p class="desc">
To inform the analyst that last names have been suppressed, and to give an indication of how much data has been suppressed, pg_diffix places all of the suppressed rows in a bucket labeled
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
    "heading": "Suppression (numbers)",
    "description": '''
<p class="desc">
This query similarly has substantial suppression, but this time displaying numbers instead of text.
<p class="desc">
In this case, rather than return
&nbsp<span style="font-family:'Courier New'">*</span>&nbsp
as the default symbol for identifying the suppression bucket, pg_diffix returns
&nbsp<span style="font-family:'Courier New'">NULL</span>&nbsp
(which here is displayed as 'None' because of the python implementation of this training program). pg_diffix can't return
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
    "heading": "Generalization",
    "description": '''
<p class="desc">
The key to avoiding excessive suppression or noise is to generalize data (or select fewer columns). Larger bins are less likely to be suppressed, and the relative noise is also less.
<p class="desc">
Fundamentally, Diffix Fir lets the analyst trade-off precision for distortion. Data with less generalization or more columns is more precise, but suffers from increased relative noise and more suppression. Data with more generalization or fewer columns has less distortion, but is also less precise.
<p class="desc">
pg_diffix supports text and numeric columns.
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
    "heading": "Heatmap example",
    "description": '''
<p class="desc">
This query counts the number of taxi rides in each hour in a square grid of roughly 1km by 1km. This query could be used to build a set of space/time heatmaps showing how the number of taxi rides differs in different locations, and changes over the course of the day. (See
<a target=_blank href="
https://taxi-heatmap.open-diffix.org/
">here</a> for a demo of just this kind of heatmap.)
<p class="desc">
This example demonstrates the use of both text and numeric generalization.
<p class="desc">
The native column type for the pickup_datetime column is datetime, so it must be cast as text for the substring() function. (The native query could have used date_trunc(), but we use substring() here as well to produce identical values.)
<p class="desc">
The amount of suppression is relatively small (slightly over 5000 of 440K rows, or roughly 1%)
<p class="desc">
The 99% of the original data that is not suppressed constitutes less than half of the native output bins (around 2000 output bins from Diffix versus over 4500 from the native query). In other words, the 1% of suppressed data is spread over a long tail of bins with very small counts.
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
    "heading": "<u>PART 2: ADVANCED</u>",
    "description": '''
    <p class="desc">
zzzz
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
    "heading": "Post-processing",
    "description": '''
    <p class="desc">
    Nested queries are possible with pg_diffix, but only the inner-most query is anonymized. Correspondly, the inner-most query is very limited in its SQL syntax, mainly what is described in Part 1, plus a few additional functions described in Part 2.
    <p class="desc">
    The outer query or queries, however, have no SQL restrictions. These outer queries can act as a kind of post-processing for the purpose of formatting data, computing aggregates, or applying logic filters. Examples using post-processing are sprinkled throughout this part.
    <p class="desc">
    Note that there are a number of functions that are effectively post-processing even without a nested query. These include ORDER BY, LIMIT, and HAVING.
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
  { "heading": "Data formatting",
    "description": '''
<p class="desc">
Here we give a simple data formatting example.  In this query, the age column is post-processed to make it clear what the age ranges are.
<p class="desc">
<font color="red">Note query takes several 10s of seconds.</font>
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
    "heading": "WHERE filter",
    "description": '''
    <p class="desc">
    The queries shown in Part 1 of this training app do not filter data: histograms from all of the data are built from each query. This can lead to very slow queries for large tables. To improve performance, pg_diffix supports WHERE clauses with AND logic and simple expressions.
    <p class="desc">
    WHERE clauses in pg_diffix are implemented as a pre-processing step (that is, it occurs before anonymization). The rows of data that pass the WHERE filter are presented to Diffix as a table over which Diffix operates.
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
    "heading": "Without WHERE",
    "description": '''
<p class="desc">
Suppose we would like to count the total number of distinct IP addresses for SciHub queries originating in the city of Aachen, Germany. We can get that without the WHERE clause by requesting a histogram over all cities, and post-processing for just Aachen.
<p class="desc">
This takes several 10s of seconds.
<p class="desc">
(Note that HAVING is a post-processing filter. It operates on the anonymized output of the city histogram.)
''',
    "dbname": "scihub",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT city, count(DISTINCT uid)
FROM sep2015
GROUP BY 1
HAVING city = 'Aachen'
'''
    },
    "native": {
      "sql": '''
SELECT city, count(DISTINCT uid)
FROM sep2015
GROUP BY 1
HAVING city = 'Aachen'
'''
    }
  },
  {
    "skip": False,
    "expectErr": True,
    "heading": "With WHERE",
    "description": '''
<p class="desc">
Here is the same query, but this time pre-filtering for city. Note that the query runs much faster (less than 2 seconds, versus several 10s of seconds without the WHERE).
''',
    "dbname": "scihub",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT city, count(DISTINCT uid)
FROM sep2015
WHERE city = 'Aachen'
GROUP BY 1
'''
    },
    "native": {
      "sql": '''
SELECT city, count(DISTINCT uid)
FROM sep2015
WHERE city = 'Aachen'
GROUP BY 1
'''
    }
  },
  {
    "skip": False,
    "expectErr": True,
    "heading": "With generalization",
    "description": '''
<p class="desc">
WHERE expressions are limited to the forms 'col = val' or 'gen_func() = val', where 'gen_func()' is a generalization function. This example shows the latter case using 'diffix.floor_by()'.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT count(*)
FROM loans
WHERE diffix.floor_by(amount,10000) = 20000
'''
    },
    "native": {
      "sql": '''
SELECT count(*)
FROM loans
WHERE diffix.floor_by(amount,10000) = 20000
'''
    }
  },
  {
    "heading": "Histograms of Counts",
    "description": '''
    <p class="desc">
    Suppose a query showed that 100 clients had 100000 transactions. We would like to know how those transactions were distributed among the 100 clients. Did all 100 clients have 1000 transactions each? Did 10 clients have 9100 transactions each while the other 90 had 100 each?
    <p class="desc">
    In normal SQL, one way to generate a count distribution would be with a nested query:
    <pre>
SELECT cnts, count(*) FROM (
  SELECT client, count(*) AS cnts
  FROM table GROUP BY 1 ) t
    </pre>
    In Diffix Fir, this query would produce garbage, because in anonymizing the inner query, everything would be suppressed. While a future version of Diffix may handle this properly by postponing anonymization to the outer query, Diffix Fir has a special function, 'diffix.count_histogram()', to compute a histogram of counts.
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
    "heading": "count_histogram()",
    "description": '''
<p class="desc">
This query gives the number of accounts that have had so many loans. From this, we see that about 20% of the accounts have had two loans, while the rest only one (unless a very small number of accounts have had more than two loans and have been suppressed, though the native result shows us that this is not the case).
<p class="desc">
The Diffix SQL on the left implements the Native SQL on the right. The Diffix SQL is rather complex and needs explanation.
<p class="desc">
The innermost query executes the 'diffix.count_histogram()' function. It produces an anonymized result in the form of an ARRAY (actually, an ARRAY of ARRAYs). The special function 'diffix.unnest_histogram()' returns a table of ARRAYs each with two values. The first value is the count of events, and the second value is the number of protected entities (e.g. individuals) with the corresponding count.
<p class="desc">
Note that 'diffix.count_histogram()' only takes columns tagged as AID columns as its argument (i.e. columns that identify the protected entity).
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT unnested[1] AS num_loans,
       unnested[2] AS num_accounts
FROM (
  SELECT 
    diffix.unnest_histogram(cnt_hist)
    AS unnested
  FROM (
    SELECT
      diffix.count_histogram(account_id)
      AS cnt_hist
    FROM loans
  ) t1
) t2
ORDER BY num_loans
'''
    },
    "native": {
      "sql": '''
SELECT num_loans,
       count(*) as num_accounts
FROM (
  SELECT account_id,
         count(*) AS num_loans
  FROM loans
  GROUP BY 1
) t
GROUP BY 1
ORDER BY num_loans
'''
    }
  },
  {
    "heading": "With generalization",
    "description": '''
<p class="desc">
The 'diffix.count_histogram()' function can also generalize counts. This is done with a second argument which acts identically to the `diffix.floor_by()` generalization function.
<p class="desc">
This query gives the number of accounts that have had so many transactions, generalized as bins of 100 transactions.

''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT unnested[1] AS num_trans,
       unnested[2] AS num_accounts
FROM (
  SELECT 
    diffix.unnest_histogram(cnt_hist)
    AS unnested
  FROM (
    SELECT
      diffix.count_histogram(account_id,100)
      AS cnt_hist
    FROM transactions
  ) t1
) t2
ORDER BY num_trans
'''
    },
    "native": {
      "sql": '''
SELECT (floor(num_trans/100)*100)::integer
         AS num_trans,
       count(*) as num_accounts
FROM (
  SELECT account_id,
         count(*) AS num_trans
  FROM transactions
  GROUP BY 1
) t
GROUP BY 1
ORDER BY num_trans
'''
    }
  },
  {
    "heading": "As 2D histogram",
    "description": '''
<p class="desc">
As expected, the 'diffix.count_histogram()' function also works in conjunction with other selected columns.
<p class="desc">
This query returns a histogram of the number of rides taken by drivers for each of the two taxi vendors.
''',
    "dbname": "taxi",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT vendor_id,
       unnested[1] AS num_rides,
       unnested[2] AS num_drivers
FROM (
  SELECT vendor_id,
    diffix.unnest_histogram(cnt_hist)
    AS unnested
  FROM (
    SELECT vendor_id,
      diffix.count_histogram(hack,5)
      AS cnt_hist
    FROM jan08
    GROUP BY 1
  ) t1
) t2
ORDER BY 1,2
'''
    },
    "native": {
      "sql": '''
SELECT vendor_id,
       (floor(num_rides/5)*5)::integer
         AS num_rides,
       count(*) as num_drivers
FROM (
  SELECT vendor_id, hack,
         count(*) AS num_rides
  FROM jan08
  GROUP BY 1,2
) t
GROUP BY 1,2
ORDER BY 1,2
'''
    }
  },
  {
    "heading": "Microdata (synthetic data)",
    "description": '''
    <p class="desc">
    While Diffix Fir can and should be thought of as producing aggregates, technically it is capable of producing microdata (i.e. one output row per input row).
    If a query has no aggregate function and corresponding GROUP BY, pg_diffix automatically assumes an aggregate of 'count(*)', and then simply expands each implied aggregate into its corresponding number of rows by repeating the set of values 'count(*)' times.
    <p class="desc">
    Note that this microdata is also a form of synthetic data.
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
    "heading": "With count(*)",
    "description": '''
<p class="desc">
By way of example, this query has the count(*) aggregate.
<p class="desc">
Note that for clarity the queries are filtered to have only three output bins, each with small counts.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT acct_district_id AS act,
       duration AS dur,
       count(*)
FROM loans
GROUP BY 1,2
HAVING acct_district_id IN (1,52,54)
       AND duration = 60
ORDER BY 3 
'''
    },
    "native": {
      "sql": '''
SELECT acct_district_id AS act,
       duration AS dur,
       count(*)
FROM loans
GROUP BY 1,2
HAVING acct_district_id IN (1,52,54)
       AND duration = 60
ORDER BY 3 
'''
    }
  },
  {
    "heading": "Without count(*)",
    "description": '''
<p class="desc">
This is the same query, but this time without the 'count(*)' aggregate and corresponding GROUP BY.
<p class="desc">
The microdata produced by pg_diffix tracks the original data very closely. The only difference is that the pg_diffix microdata may have a few more or less rows for each combination of values than the original data.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT act_d, dur_d
FROM (
  SELECT acct_district_id AS act_d,
         duration AS dur_d
  FROM loans
) t
WHERE act_d IN (1,52,54) AND dur_d = 60
ORDER BY 1,2
'''
    },
    "native": {
      "sql": '''
SELECT act_n, dur_n
FROM (
  SELECT acct_district_id AS act_n,
         duration AS dur_n
  FROM loans
) t
WHERE act_n IN (1,52,54) AND dur_n = 60
ORDER BY 1,2
'''
    }
  },
  {
    "heading": "Synthetic data",
    "description": '''
<p class="desc">
pg_diffix can be used to generate statistically accurate synthetic data.
<p class="desc">
This query generates synthetic data that captures the correlation between transaction amount and balance. The round_by() aggregate ensures that there is a minimal amount of suppression.
<p class="desc">
Note that LIMIT and OFFSET are used here to show a "window" of values in an otherwise much larger dataset (roughly 1.2M rows). The rows shown for Diffix and native are not meant to perfectly line up 1-to-1.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT amt, bal
FROM (
  SELECT diffix.round_by(amount,1000)
           AS amt,
         diffix.round_by(balance,1000)
           AS bal
  FROM transactions
  ORDER BY 1 DESC,2 DESC
) t
LIMIT 100 OFFSET 100000
'''
    },
    "native": {
      "sql": '''
SELECT amount AS amt,
       balance AS bal
FROM transactions
ORDER BY 1 DESC,2 DESC
LIMIT 100 OFFSET 100000
'''
    }
  },
  {
    "heading": "Statistics (1-column)",
    "description": '''
<p class="desc">
Given the ability to generate microdata, we can run all kinds of statistical functions on that data. Some of these are offered by PostgreSQL, and can be run as post-processing. Alternatively, one could import the microdata into a variety of programming tools with statistics packages such as R or Python. 
<p class="desc">
This section highlights PostgreSQL statistics tools that operate on a single column.
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
    "heading": "Measuring suppression",
    "description": '''
<p class="desc">
To produce high-quality microdata, we want to minimize suppression while maximizing precision through small bin widths.
<p class="desc">
This query presents a simple way to measure the amount of data lost through suppression. We can increase or decrease the amount of suppression by shrinking or growing the round_by amount. Here we see that less than 1/10 of 1% of the data is suppressed using a bin size of 100.
<p class="desc">
Note that this query assumes that suppressed bins are assigned a value of NULL. It is possible to configure a different value. The amount columns has no native NULL values (as demonstrated by the query on the right), and so using NULL to identify suppressed bins works well in this case.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT round(100*((count(*)-sum(status))/count(*)::numeric),2)
         AS percent_suppressed
FROM (
  SELECT CASE
        WHEN amount IS NULL THEN 0
        ELSE 1
        END AS status
  FROM (
    SELECT diffix.round_by(amount,100)
          AS amount
    FROM transactions
  ) t1
) t2
      '''
    },
    "native": {
      "sql": '''
SELECT count(*) as number_of_NULL_values
FROM transactions
WHERE amount IS NULL
      '''
    }
  },
  {
    "heading": "Percentile",
    "description": '''
<p class="desc">
The PostgreSQL PERCENTILE_CONT() function can compute any percentile.
<p class="desc">
This query computes the median of all transaction amounts. The basis for computing the PERCENTILE_CONT() function is the microdata from bin sizes of 100.
<p class="desc">
The noisy median is off by about 5%.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT PERCENTILE_CONT(0.5) WITHIN 
GROUP(ORDER BY amount)
FROM (
  SELECT diffix.round_by(amount,100)
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
    "heading": "Max",
    "description": '''
<p class="desc">
To compute max, we use diffix.ceil_by instead of diffix.round_by, because the Diffix estimate will tend to under-estimate the true max because high values tend to be sparse and therefore suppressed. We also used larger bins (1000 instead of 100) because this produced a higher value. Even so, the estimated max is off by roughly 10%.
<p class="desc">
In general, distortion is high for max because Diffix tends to hide outlier values.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT PERCENTILE_CONT(1.0) WITHIN 
GROUP(ORDER BY amount)
FROM (
  SELECT diffix.ceil_by(amount,1000)
         AS amount
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT PERCENTILE_CONT(1.0) WITHIN 
GROUP(ORDER BY amount)
FROM transactions
      '''
    }
  },
  {
    "heading": "Min",
    "description": '''
<p class="desc">
To compute max, we use diffix.floor_by instead of diffix.round_by. Diffix produces an exact answer in this case because a large number of accounts have transactions with amount 0.0. (Note that Max can also produce an exact answer when a large number of individuals share the maximum value.)
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT PERCENTILE_CONT(0.0) WITHIN 
GROUP(ORDER BY amount)
FROM (
  SELECT diffix.floor_by(amount,100)
         AS amount
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT PERCENTILE_CONT(0.0) WITHIN 
GROUP(ORDER BY amount)
FROM transactions
      '''
    }
  },
  {
    "heading": "Standard deviation",
    "description": '''
<p class="desc">
Standard deviation is well within 10% of the true value.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT stddev(amount)
FROM (
  SELECT diffix.floor_by(amount,100)
         AS amount
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT stddev(amount)
FROM transactions
      '''
    }
  },
  {
    "heading": "Statistics (2-column)",
    "description": '''
<p class="desc">
This section highlights PostgreSQL statistics tools that operate on column pairs.
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
    "heading": "Measuring suppression",
    "description": '''
<p class="desc">
This measures suppression for two columns (here assuming both return NULL for suppressed rows). Suppression is less than 1%, so we'll assume that this is good enough (though this needs to be studied).
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT round(100*((count(*)-sum(status))/count(*)::numeric),2)
         AS percent_suppressed
FROM (
  SELECT CASE
        WHEN amount IS NULL AND
             balance IS NULL
        THEN 0
        ELSE 1
        END AS status
  FROM (
    SELECT diffix.round_by(amount,1000)
              AS amount,
           diffix.round_by(balance,1000)
              AS balance
    FROM transactions
  ) t1
) t2
      '''
    },
    "native": {
      "sql": '''
SELECT count(*) as number_of_NULL_rows
FROM transactions
WHERE amount IS NULL AND
      balance IS NULL
      '''
    }
  },
  {
    "heading": "Correlation coefficient",
    "description": '''
<p class="desc">
The PostgreSQL corr() function implements the Pearson Correlation Coefficient. This returns a real value between -1 and 1. The higher the absolute value of the value, the stronger the correlation (positive or negative). Zero means no correlation whatsoever.
<p class="desc">
The pg_diffix estimate of the correlation is off by about 5%. Both it and the true value suggest a weak to moderate correlation between amount and balance.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT corr(amount,balance)
FROM (
  SELECT diffix.round_by(amount,1000)
            AS amount,
          diffix.round_by(balance,1000)
            AS balance
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT corr(amount,balance)
FROM transactions
      '''
    }
  },
  {
    "heading": "Covariance",
    "description": '''
<p class="desc">
The PostgreSQL covar_pop() function implements the Population Covariance. It returns a real value between plus and minus infinity. It is not scale free.
<p class="desc">
The pg_diffix estimate of the covariance is off by about 20%.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT covar_pop(amount,balance)
FROM (
  SELECT diffix.round_by(amount,1000)
            AS amount,
          diffix.round_by(balance,1000)
            AS balance
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT covar_pop(amount,balance)
FROM transactions
      '''
    }
  },
  {
    "heading": "Least squares fit (y-intercept)",
    "description": '''
<p class="desc">
The PostgreSQL regr_intercept(X,Y) function returns y-intercept of the least-squares-fit linear equation determined by the (X,Y) pairs.
<p class="desc">
The pg_diffix estimate of the y-intercept is off by slightly over 20%.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT regr_intercept(amount,balance)
FROM (
  SELECT diffix.round_by(amount,1000)
            AS amount,
          diffix.round_by(balance,1000)
            AS balance
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT regr_intercept(amount,balance)
FROM transactions
      '''
    }
  },
  {
    "heading": "Least squares fit (slope)",
    "description": '''
<p class="desc">
The PostgreSQL regr_slope(X,Y) function returns slope of the least-squares-fit linear equation determined by the (X,Y) pairs.
<p class="desc">
The pg_diffix estimate of the slope is off by around 10%.
''',
    "dbname": 'banking0',
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT regr_slope(amount,balance)
FROM (
  SELECT diffix.round_by(amount,1000)
            AS amount,
          diffix.round_by(balance,1000)
            AS balance
  FROM transactions
) t
      '''
    },
    "native": {
      "sql": '''
SELECT regr_slope(amount,balance)
FROM transactions
      '''
    }
  },
  {
    "heading": "Noise",
    "description": '''
<p class="desc">
Part 1 of this training app gives examples of proportional sticky noise.
<p class="desc">
Here we describe how pg_diffix zzzz
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
    "heading": "Noise magnitude",
    "description": '''
<p class="desc">
When different protected entities contribute different amounts to an aggregate (i.e. more rows if count(*)), pg_diffix adds proportionally more noise. It is helpful to the analyst to know how much noise is being added.
<p class="desc">
pg_diffix provides several functions that convey the standard deviation of the noise. They have the format 'aggr_noise()', where 'aggr' is 'count', 'sum', or 'avg'.
<p class="desc">
This example counts banking clients, which are protected entities. Since each client contributes only one to the count, the noise magnitude is small (SD=1) and the same for every bin.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT acct_district_id,
       count(DISTINCT client_id1),
       diffix.count_noise(DISTINCT client_id1)
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
    "heading": "Proportional",
    "description": '''
<p class="desc">
This example gives the sum of all transaction amounts per client district. Since different clients contributes different amounts to the sums, the proportional noise varies from district to district, and is very large.
<p class="desc">
Note that the sums are conveyed as millions (and so is the absolute error), but the noise magnitude is not. (This is why the noise appears so high relative to the sum.)
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT cdist,
       round((sm/1000000)::numeric,2) 
         AS sum_in_mil,
         noise
FROM (
  SELECT cli_district_id1 AS cdist,
        sum(amount) AS sm,
        diffix.sum_noise(amount) AS noise
  FROM transactions
  GROUP BY 1
) t
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT cdist,
       round((sm/1000000)::numeric,2) 
         AS sum_in_mil
FROM (
  SELECT cli_district_id1 AS cdist,
        sum(amount) AS sm
  FROM transactions
  GROUP BY 1
) t
ORDER BY 1
      '''
    }
  },
  {
    "heading": "Flattening",
    "description": '''
<p class="desc">
Sometimes data has extreme contributors; one or a few individuals that contribute far more than any other individual. Proportional noise, naively implemented, could reveal the presence or absence of these individuals simply by the amount of distortion. To prevent this, pg_diffix reduces the contribution of extreme contributors so that they are in line with other heavy contributors. We call this "flattening".
<p class="desc">
While flattening hides extreme contributors, it has the unfortunate effect of adding a systematic negative bias to row counts (though not to counts of individuals).
<p class="desc">
Here is the same query from the proportional noise example with sums. Looking at the "abs:rel" column, we see that the distortion is not zero mean: it is negative far more often than positive. 
<p class="desc">
(Note that a future release is expected to reduce this bias by distributing some of the flattened value among the sums.)
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT cdist,
       round((sm/1000000)::numeric,2) 
         AS sum_in_mil,
         noise
FROM (
  SELECT cli_district_id1 AS cdist,
        sum(amount) AS sm,
        diffix.sum_noise(amount) AS noise
  FROM transactions
  GROUP BY 1
) t
ORDER BY 1
'''
    },
    "native": {
      "sql": '''
SELECT cdist,
       round((sm/1000000)::numeric,2) 
         AS sum_in_mil
FROM (
  SELECT cli_district_id1 AS cdist,
        sum(amount) AS sm
  FROM transactions
  GROUP BY 1
) t
ORDER BY 1
'''
    }
  },
  {
    "heading": "Counting distinct (no noise)",
    "description": '''
<p class="desc">
pg_diffix supports counting distinct values for any column. pg_diffix does not necessarily add noise to dictinct counts. In particular, if the values being counted would normally not be suppressed, pg_diffix gives an exact count.
<p class="desc">
In the example below, the exact number of card types is displayed.
''',
    "dbname": "banking0",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT count(DISTINCT card_type)
       diffix.count_noise(
           DISTINCT card_type)
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
This is another way to count the number of distinct card types. Since no suppression takes place, an exact count is in any event allowed. Adding noise to 'count(DISTINCT card_type)' would in any event not prevent the user from learning the exact distinct count. Note of course that learning the exact count when there is no suppression does not weaken anonymity.
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
SELECT count(DISTINCT loan_date),
       diffix.count_noise(
           DISTINCT loan_date)
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
Part 1 contains two examples of suppression. We revisit that topic here to demonstrate how generalization can be used to reduce the amount of suppression.
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
    "heading": "A lot of suppression",
    "description": '''
<p class="desc">
This example measures the amount of suppression when exact pickup location (longitude and latitude) is queried. Over 98% of the data has been suppressed!
''',
    "dbname": "taxi",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT round(100*((count(*)-sum(status))/count(*)::numeric),2)
         AS percent_suppressed
FROM (
  SELECT CASE
        WHEN lat IS NULL
             AND lon IS NULL
        THEN 0
        ELSE 1
        END AS status
  FROM (
    SELECT pickup_latitude AS lat,
           pickup_longitude AS lon
    FROM jan08
  ) t1
) t2
'''
    },
    "native": {
      "sql": '''
SELECT count(*)
FROM jan08
WHERE pickup_latitude IS NULL OR
      pickup_longitude IS NULL
'''
    }
  },
  {
    "heading": "A little suppression",
    "description": '''
<p class="desc">
This example shows how generalizing locations into roughly 100m boxes eliminates most suppression.
''',
    "dbname": "taxi",
    "mode": "trusted",
    "diffix": {
      "sql": '''
SELECT round(100*((count(*)-sum(status))/count(*)::numeric),2)
         AS percent_suppressed
FROM (
  SELECT CASE
        WHEN lat IS NULL
             AND lon IS NULL
        THEN 0
        ELSE 1
        END AS status
  FROM (
    SELECT diffix.floor_by(
           pickup_latitude,0.001) AS lat,
           diffix.floor_by(
           pickup_longitude,0.001) AS lon
    FROM jan08
  ) t1
) t2
'''
    },
    "native": {
      "sql": '''
SELECT count(*)
FROM jan08
WHERE pickup_latitude IS NULL OR
      pickup_longitude IS NULL
'''
    }
  },
  {
    "heading": "Diffix Metadata",
    "description": '''
    <p class="desc">
    pg_diffix provides several commands that display how pg_diffix is configured and what its anonymization parameters are.
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
    "heading": "Personal tables",
    "description": '''
<p class="desc">
pg_diffix labels tables as either "personal" or "public". 
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
For pg_diffix to anonymize properly, it must recognize which column (or columns) in each personal table identifies the protected entity (or entities).
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
pg_diffix has a variety of anonymization parameters that determine for instance how much noise is added, the threshold for suppression, and how suppressed bins are labeled.
<p class="desc">
The command
<span style="font-family:'Courier New'">diffix.show_settings()</span>
displays the parameter settings.
<p class="desc">
The 
<a target=_blank href="
https://arxiv.org/abs/2201.04351
">full pg_diffix specification</a>
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
    "heading": "Protected Entities (PE)",
    "description": '''
<p class="desc">
All personal tables must have one or more columns that identify the entities whose privacy is being protected. At a minimum, the individual person must be protected, but pg_diffix can protect multiple different kinds of entities.
<p class="desc">
It is useful to for the analyst to know what columns identify the protected entities. This is because the amount of noise is more predictable for these columns (there is no flattening, and the noise is not proportional because each protected entity contributes the same amount).
<p class="desc">
pg_diffix offers a function, 
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
pg_diffix can protect multiple entities of different types. An example of this can be found in the Banking database, where both individual clients (persons) and bank accounts are protected. Some accounts are joint accounts (two persons). Even though strictly speaking two persons is not a singled-out individual, and does not necessarily require protection by GDPR criteria, it is certainly desirable that accounts be protected as well as inidividual clients.
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
    "heading": "Trusted and Untrusted",
    "description": '''
<p class="desc">
pg_diffix operates in two modes, Trusted Analyst and Untrusted Analyst.
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
    "heading": "Custom generalization",
    "description": '''
<p class="desc">
Diffix Fir allows only rudimentary generalization: numeric ranges and substrings. It lacks any native datetime or geolocation capabilities. To deal with datetime, it is necessary to convert the datetime values to text and use substring. Geolocation can be generalized as latitude/longitude numbers.
<p class="desc">
Future versions of Diffix may deal with datetime or geolocation natively.
<p class="desc">
More generally, it can be useful to generalize through categorization: pizza, carbonara, and lasagne as italian food. Categorization can be supported in PostgreSQL with for instance CASE statements or IN, but pg_diffix does not support these operations.
<p class="desc">
At this point in time, it is necessary to pre-process data before querying with pg_diffix, for instance as a materalized view or simply a new table.
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
  },
]

def getExampleList():
    return exampleList

