#!/bin/bash

mkdir -p sboms

images=(
  alpine:latest
  ubuntu:latest
  nginx:latest
  redis:latest
  node:latest
  python:latest
  golang:latest
  postgres:latest
  mysql:latest
  mongo:latest
  debian:latest
  centos:latest
  httpd:latest
  memcached:latest
  elasticsearch:latest
  rabbitmq:latest
  cassandra:latest
  influxdb:latest
  busybox:latest
)

for img in "${images[@]}"; do
  name=$(echo $img | tr ':/' '-')
  syft $img -o cyclonedx-json > sboms/$name.json
  echo "✅ Generated SBOM for $img"
done
