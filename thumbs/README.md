# Thumbnail generator for Election Leaflets

This is a Lambda function that produces thumbnails from raw leaflets and puts
the resulting files in a deterministic structure for compatibility with
`sorl-thumbnail`.

It uses `sorl-thumbnail` under the hood and accepts the same options as the
`thumbnail` templatetag. Output files are named as follows:

```
/thumbs/{size}/{optkey1}={optval1}/{optkey2}={optval2}/.../path/to/file.jpg
```

Example:

```
https://data.electionleaflets.org/thumbs/600/crop%3Dcenter/leaflets/2019-11-26_1.jpg
```

The Lambda function can consume either CloudFront or S3 events, so it can be
used as new leaflets are uploaded, or to backfill thumbnail URLs as they're
requested.

## Configuration

The pre-emptive processing of thumbnails from S3 events needs configuration for
the thumbnail specs we want to create. This is done in the `SPECS` constant in
the `handle_s3` function in `src/handler.py`, which expects a tuple of tuples.
The first element is the size spec, e.g `600` or `300x400`. The second element
is the options dict, eg `{"crop": "top", "upscale": True}`.

## Deployment

**❗ Currently must be built from a Linux machine, Docker support coming soon for Macs ❗**

Deployment is a four-stage process, covering S3 and CloudFront. You must have a
Democracy Club AWS profile active.

1. Run `make deploy_cf`
2. Note the `FunctionArn` returned and update it in the `thumbs/*` behaviour in
   the [data.electionleaflets.org CloudFront
   distribution](https://console.aws.amazon.com/cloudfront/home?region=us-east-1#distribution-settings:E2FHP2ULXIVMLT).
   This will take 10-15 minutes to update.
3. Run `make deploy_s3`
4. Note the `FunctionArn` returned and update it in the Events ->
   `el-resize-image` property for the [data.electionleaflets.org S3
   bucket](https://s3.console.aws.amazon.com/s3/buckets/data.electionleaflets.org/?region=eu-west-1&tab=properties)
