#!/bin/bash

src_name=final_weights.h5
tgt_name=weights.h5

gcloud compute scp instance-1:/home/ethan/project/dialect/models/${src_name} ./${tgt_name}