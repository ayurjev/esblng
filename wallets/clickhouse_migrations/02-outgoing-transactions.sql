CREATE TABLE IF NOT EXISTS `outgoing_transactions`
(
    tx_uuid String,
    login String,
    base_currency Int8,
    amount Float64,
    cr_uuid String,
    datetime Datetime
)
ENGINE MergeTree()
PARTITION BY (datetime)
ORDER BY (login, datetime) SETTINGS index_granularity=8192;
