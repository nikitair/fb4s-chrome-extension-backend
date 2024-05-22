class MySQLQueries:
    sent_weekly_outreach_emails = """
SELECT
  *
FROM
  (
    SELECT
      fub.external_id,
      fub.broker_external_id,
      q1.customer_id,
      q1.name,
      q1.url,
      q1.email,
      q1.mls,
      q1.created_at
    FROM
      (
        SELECT
          customers.id as customer_id,
          CONCAT(customers.firstname, ' ', customers.lastname) as name,
          listings.internal_url AS url,
          outreach.subscriber_email AS email,
          outreach.mls_number AS mls,
          outreach.created_at
        FROM
          tbl_customer_outreach_campaign_sent_listings outreach
          LEFT JOIN tbl_advertisement listings on listings.DDF_ID = outreach.mls_number
          LEFT JOIN tbl_customers customers on customers.email = outreach.subscriber_email
      ) q1
      LEFT JOIN tbl_external_crm_leads fub ON fub.customer_id = q1.customer_id
  ) q2
WHERE
  created_at >= NOW() - INTERVAL 12 HOUR
  AND external_id IS NOT NULL && external_id != ''
  AND url IS NOT NULL && url != ''
ORDER BY
  created_at DESC
"""
