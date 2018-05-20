#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Expected output file-name as argument"
	exit 1
	fi

name=$1-private.pem

openssl genrsa -out $name 2048
openssl rsa -in $name -outform PEM -pubout -out $1-public.pem