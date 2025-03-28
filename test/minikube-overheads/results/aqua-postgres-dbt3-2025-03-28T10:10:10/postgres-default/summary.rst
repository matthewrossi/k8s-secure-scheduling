Power Test
----------

* Seed: 328101034

+--------------------+------------------------+------------------------+------------------------+
| Duration (seconds) |    Query Start Time    |     RF1 Start Time     |     RF2 Start Time     |
|                    +------------------------+------------------------+------------------------+
|                    |     Query End Time     |      RF1 End Time      |      RF2 End Time      |
+====================+========================+========================+========================+
|            1001.42 | 2025-03-28 09:10:37.02 | 2025-03-28 09:10:34.84 | 2025-03-28 09:27:16.20 |
|                    +------------------------+------------------------+------------------------+
|                    | 2025-03-28 09:27:16.19 | 2025-03-28 09:10:37.01 | 2025-03-28 09:27:16.24 |
+--------------------+------------------------+------------------------+------------------------+

=======  =========================  
 Query    Response Time (seconds)
=======  =========================  
      1                       0.74
      2                       0.09
      3                       0.17
      4                       0.07
      5                       0.17
      6                       0.12
      7                       0.19
      8                       0.29
      9                       0.21
     10                       0.21
     11                       0.04
     12                       0.21
     13                       0.27
     14                       0.14
     15                       0.27
     16                       0.17
     17                     310.11
     18                       2.14
     19                       0.19
     20                     682.82
     21                       0.14
     22                       0.05
    RF1                       2.17
    RF2                       0.03
=======  =========================

Throughput Test
---------------

Stream execution summary:

+-----------+-----------+------------------------+------------------------+------------------------+
|  Stream   | Duration  |    Query Start Time    |     RF1 Start Time     |     RF2 Start Time     |
+-----------+ (seconds) +------------------------+------------------------+------------------------+
|   Seed    |           |     Query End Time     |      RF1 End Time      |      RF2 End Time      |
+===========+===========+========================+========================+========================+
|         1 |   1138.48 | 2025-03-28 09:27:16.65 | 2025-03-28 09:27:16.28 | 2025-03-28 09:27:18.59 |
+-----------+           +------------------------+------------------------+------------------------+
| 328101035 |           | 2025-03-28 09:46:15.10 | 2025-03-28 09:27:18.58 | 2025-03-28 09:27:18.62 |
+-----------+-----------+------------------------+------------------------+------------------------+
|         2 |   1081.53 | 2025-03-28 09:27:16.65 | 2025-03-28 09:27:18.65 | 2025-03-28 09:27:20.84 |
+-----------+           +------------------------+------------------------+------------------------+
| 328101036 |           | 2025-03-28 09:45:18.14 | 2025-03-28 09:27:20.83 | 2025-03-28 09:27:20.88 |
+-----------+-----------+------------------------+------------------------+------------------------+

Query execution duration (seconds):

========  ========  ========  ========  ========  ========  ========  ========
 Stream      Q1        Q2        Q3        Q4        Q5        Q6        Q7   
========  ========  ========  ========  ========  ========  ========  ========
       1      0.73      0.08      0.17      0.06      0.19      0.14      0.20
       2      0.72      0.08      0.17      0.06      0.17      0.13      0.19
     Min      0.72      0.08      0.17      0.06      0.17      0.13      0.19
     Max      0.73      0.08      0.17      0.06      0.19      0.14      0.20
     Avg      0.73      0.08      0.17      0.06      0.18      0.14      0.20
========  ========  ========  ========  ========  ========  ========  ========

========  ========  ========  ========  ========  ========  ========  ========
 Stream      Q8        Q9        Q10       Q11       Q12       Q13       Q14  
========  ========  ========  ========  ========  ========  ========  ========
       1      0.22      0.22      0.21      0.04      0.21      0.26      0.12
       2      0.24      0.22      0.22      0.04      0.21      0.28      0.13
     Min      0.22      0.22      0.21      0.04      0.21      0.26      0.12
     Max      0.24      0.22      0.22      0.04      0.21      0.28      0.13
     Avg      0.23      0.22      0.21      0.04      0.21      0.27      0.13
========  ========  ========  ========  ========  ========  ========  ========

========  ========  ========  ========  ========  ========  ========  ========
 Stream      Q15       Q16       Q17       Q18       Q19       Q20       Q21  
========  ========  ========  ========  ========  ========  ========  ========
       1      0.24      0.16    419.01      2.24      0.19    713.22      0.13
       2      0.27      0.10    363.51      2.15      0.20    711.77      0.13
     Min      0.24      0.10    363.51      2.15      0.19    711.77      0.13
     Max      0.27      0.16    419.01      2.24      0.20    713.22      0.13
     Avg      0.25      0.13    391.26      2.20      0.19    712.49      0.13
========  ========  ========  ========  ========  ========  ========  ========

========  ========  ========  ========
 Stream      Q22       RF1       RF2  
========  ========  ========  ========
       1      0.05      2.29      0.03
       2      0.05      2.18      0.04
     Min      0.05      2.18      0.03
     Max      0.05      2.29      0.04
     Avg      0.05      2.23      0.04
========  ========  ========  ========
