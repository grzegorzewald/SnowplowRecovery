#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import gzip
import base64
import boto3
import thriftpy
from thriftpy.protocol import TCyBinaryProtocolFactory
from thriftpy.utils import deserialize, serialize

RECORD_START_SEQUENCE = b'\x0b\x00\x64\x00\x00\x00'
TMP_FILE_NAME = 'tmp.gz'

client = boto3.client('kinesis')

collector = thriftpy.load("collector-payload.thrift")
collector_payload = collector.CollectorPayload()

def emit_to_stdout(record, key):
    print base64.b64encode(str(record))

def emit_to_kinesis(record, key):
    resp = client.put_record(
        StreamName = emiter_stream_name,
        Data = record,
        PartitionKey = key
    )

emiters = {
    "stdout": emit_to_stdout,
    "kinesis": emit_to_kinesis
}

emiter = 'stdout'
emiter_stream_name = ''

def emit(record, key):
    emiters[emiter](record, key)

def eprint(args):
    print >> sys.stderr, args

def process_record(record):
    decoded_record = deserialize(collector_payload, record, TCyBinaryProtocolFactory())
    ipAddress = str(decoded_record.ipAddress)
    decoded_record.collector = 'S3-recovery-0.0.2'
    record_to_emit = serialize(decoded_record, TCyBinaryProtocolFactory())
    emit(record_to_emit, ipAddress)

def process_gzfile(gz_file_name):
    with gzip.open(gz_file_name,'rb') as f:
        record = bytearray(f.read(6))
        byte = f.read(1)
        while byte != "":
            record.append(byte)
            if record.endswith(RECORD_START_SEQUENCE):
                process_record(record[:-6])
                record = bytearray(RECORD_START_SEQUENCE)
            byte = f.read(1)
        process_record(record)

def process_s3(s3_bucket, s3_prefix):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)
    for obj in bucket.objects.filter(Prefix = s3_prefix):
        eprint(obj.key)
        bucket.download_file(obj.key, TMP_FILE_NAME)
        process_gzfile(TMP_FILE_NAME)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", type=str,  help="S3 bucket", required=False)
    parser.add_argument("-p", "--prefix", type=str,  help="S3 file prefix", required=False)
    parser.add_argument("-f", "--local_file", type=str,  help="Local file name", required=False)
    parser.add_argument("-o", "--output", type=str,  help="Output stream type", required=False)
    parser.add_argument("-s", "--output_stream", type=str,  help="Output stream name", required=False)
    args = parser.parse_args()
    if args.output in emiters.keys():
        emiter = args.output
    else:
        eprint("Invalid output type!")
        sys.exit(1)
    if isinstance(args.output_stream, str) and (len(args.output_stream) > 0):
        emiter_stream_name = args.output_stream
    if args.local_file and (args.bucket or args.prefix):
        eprint("Cant use local file and s3 files at the same time!")
        sys.exit(2)
    if args.bucket:
        process_s3(s3_bucket = args.bucket, s3_prefix = args.prefix or '')
        sys.exit(0)
    if args.local_file:
        process_gzfile(args.local_file)
        sys.exit(0)
    eprint("No required parameter set!")
    sys.exit(1)
