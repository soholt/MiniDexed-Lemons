#!/bin/sh

cd ./tools
./extract_minidexed.py
./extract_performances.py
./extract_voices_from_DX7_syx.py
cd ..
