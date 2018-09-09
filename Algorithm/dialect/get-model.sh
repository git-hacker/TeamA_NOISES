#!/bin/bash

src_name=tmp.h5
tgt_name=tmp.h5

gcloud compute scp instance-1:/home/ethan/project/dialect/models/${src_name} ./models/${tgt_name}