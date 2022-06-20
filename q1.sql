WITH 
    calendar_month
     AS (SELECT calendar_year_month
         FROM   CALENDAR c
         WHERE  calendar_day_of_month = 1),

     member_start
     AS (SELECT member_id,
                MIN(activity_year_month) AS start_month
         FROM   REVENUE_ANALYSIS
         WHERE  bank_type_id = 0
         GROUP  BY member_id),

     crossed
     AS (SELECT member_id,
                start_month,
                calendar_year_month
         FROM   member_start
                CROSS JOIN calendar_month
         WHERE  calendar_year_month >= start_month),

     monthly_wagers
     AS (SELECT member_id,
                activity_year_month,
                SUM(wager_amount) AS sum_wager
         FROM   REVENUE_ANALYSIS
         WHERE  bank_type_id = 0
         GROUP  BY member_id,
                   activity_year_month),
    
     calendar_lagged_wagers
     AS (SELECT c.member_id,
                c.calendar_year_month,
                w.sum_wager,
                c.start_month,
                LAG(sum_wager, 1)
                  OVER (
                    partition BY c.member_id
                    ORDER BY c.calendar_year_month) AS previous_wager
         FROM   crossed c
                LEFT JOIN monthly_wagers w
                       ON c.calendar_year_month = w.activity_year_month
                          AND ( c.member_id = w.member_id ))

SELECT member_id,
       calendar_year_month,
       CASE
         WHEN start_month = calendar_year_month THEN "new"
         WHEN sum_wager IS NOT NULL
              AND previous_wager IS NOT NULL THEN "retained"
         WHEN sum_wager IS NULL
              AND previous_wager IS NOT NULL THEN "unretained"
         WHEN sum_wager IS NOT NULL
              AND previous_wager IS NULL THEN "reactivated"
         WHEN sum_wager IS NULL
              AND previous_wager IS NULL THEN "lapsed"
       END                                   AS member_lifecycle_status,
       ROW_NUMBER()
         OVER (
           partition BY member_id, grp
           ORDER BY calendar_year_month) - 1 AS lapsed_months
FROM   (SELECT *,
               SUM(CASE
                     WHEN sum_wager IS NULL
                          AND previous_wager IS NULL THEN 0
                     ELSE 1
                   END)
                 OVER (
                   partition BY member_id
                   ORDER BY calendar_year_month) AS grp
        FROM   calendar_lagged_wagers) grp_table
ORDER  BY member_id,
          calendar_year_month 