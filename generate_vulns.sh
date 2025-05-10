#!/bin/bash

mkdir -p sboms_vulns

for file in sboms/*.json; do
  base=$(basename $file .json)
  grype sboms/$base.json -o cyclonedx-json > sboms_vulns/$base-vulns.json
  echo "✅ Grype scan completed for $base"
done
