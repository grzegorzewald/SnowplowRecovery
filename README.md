# Snoplow Realtime data pipeline S3 Recovery/data fix
A repository with Snowplow recovery mechanism for Realtime data pipeline S3 backup file.

## How to use
The Python code itself process gzipped backup files and prints to stdout bas64 encoded records. Thic cna be piped into stream enrich, working on pipe stream and writing to Enriched steram.

Backup raw files may be picked up either form S3 bucket (with file name prefix or not) or form a local file (currently only a single one supported).

## Notes
_Thrift_ schema is taken from official Snowplow repo: [collector-payload.thrift](https://github.com/snowplow/snowplow/blob/master/2-collectors/thrift-schemas/collector-payload-1/src/main/thrift/collector-payload.thrift)
