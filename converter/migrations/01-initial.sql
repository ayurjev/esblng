CREATE TABLE IF NOT EXISTS `rates_revisions`
(
    uuid String,
    base_currency Int8,
    value Float64,
    datetime Datetime,
    inserted Datetime DEFAULT now()
)
ENGINE MergeTree()
PARTITION BY (datetime)
ORDER BY (base_currency, datetime) SETTINGS index_granularity=8192