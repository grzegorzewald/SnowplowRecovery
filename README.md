# Snowplow Real-time data pipeline S3 Recovery/data fix
A repository with Snowplow recovery mechanism for Real-time data pipeline S3 backup file.

## How to use
Recovery mechanism can either emit base64 encoded records to stdout or write directly to the Kinesis stream.

Backup raw files may be picked up either form S3 bucket (with file name prefix or not) or form a local file (currently only a single one supported).

## How to fix bad records?

Line 48 is the answer.

## Notes
_Thrift_ schema is taken from official Snowplow repo: [collector-payload.thrift](https://github.com/snowplow/snowplow/blob/master/2-collectors/thrift-schemas/collector-payload-1/src/main/thrift/collector-payload.thrift)
