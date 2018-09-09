#!/bin/bash

# scp -r ./*.py ethan-ai-desktop.local:/home/ethan/playground/NOISES/dialect2mandarin/

gcloud compute scp --recurse ./*.py instance-1:/home/ethan/project/dialect/