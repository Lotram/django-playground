SELECT
    pg_tables.schemaname,
    pg_tables.tablename,
    indexname,
    pg_class.reltuples AS num_rows,
    pg_size_pretty(pg_relation_size(quote_ident(pg_tables.schemaname)::text || '.' || quote_ident(pg_tables.tablename)::text)) AS table_size,
    pg_size_pretty(pg_relation_size(quote_ident(pg_tables.schemaname)::text || '.' || quote_ident(indexrelname)::text)) AS index_size,
    CASE WHEN indisunique THEN
        'Y'
    ELSE
        'N'
    END AS UNIQUE,
    CASE WHEN indisvalid THEN
        'Y'
    ELSE
        'N'
    END AS active,
    number_of_scans,
    tuples_read,
    tuples_fetched
FROM
    pg_tables
    LEFT OUTER JOIN pg_class ON pg_tables.tablename = pg_class.relname
    LEFT OUTER JOIN (
        SELECT
            pg_class.relname AS ctablename,
            ipg.relname AS indexname,
            pg_index.indnatts AS number_of_columns,
            idx_scan AS number_of_scans,
            idx_tup_read AS tuples_read,
            idx_tup_fetch AS tuples_fetched,
            indexrelname,
            indisunique,
            indisvalid,
            schemaname
        FROM
            pg_index
            JOIN pg_class  ON pg_class.oid = pg_index.indrelid
            JOIN pg_class ipg ON ipg.oid = pg_index.indexrelid
            JOIN pg_stat_all_indexes psai ON pg_index.indexrelid = psai.indexrelid) AS foo ON pg_tables.tablename = foo.ctablename
        AND pg_tables.schemaname = foo.schemaname
WHERE
    pg_tables.schemaname NOT IN ('pg_catalog', 'information_schema')
    AND tablename ilike 'books_%'
    -- AND indisvalid
ORDER BY
    pg_relation_size(quote_ident(pg_tables.schemaname)::text || '.' || quote_ident(pg_tables.tablename)::text) desc,
    pg_relation_size(quote_ident(pg_tables.schemaname)::text || '.' || quote_ident(indexrelname)::text) desc;
