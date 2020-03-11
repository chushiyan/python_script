#!/usr/bin/env bash
nohup python3 run_cls.py &> cls.log &
nohup python3 run_cninfo.py &> cninfo.log &
nohup python3 run_cnstock.py &> cnstock.log &
nohup python3 run_cs.py &> cs.log &
nohup python3 run_egs.py &> egs.log &
nohup python3 run_nbd.py &> nbd.log &
nohup python3 run_sseinfo.py &> sseinfo.log &
nohup python3 run_xuangubao.py &> xuangubao.log &
nohup python3 run_yicai.py &> yicai.log &





