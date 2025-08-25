rm -rf STACKS MWCS DTT db.ini msnoise.sqlite

msnoise db init --tech 1

msnoise config set startdate=2018-01-01
msnoise config set enddate=2018-12-31
msnoise config set components_to_compute=ZZ
msnoise config set remove_response='Y'
msnoise config set response_format=inventory
msnoise config set response_path='./station'
msnoise config set response_prefilt=0.01,0.05,24.9,24.95

msnoise config set preprocess_lowpass=49.9
msnoise config set preprocess_highpass=0.01
msnoise config set cc_sampling_rate=100
msnoise config set preprocess_max_gap=86400 

msnoise config set mov_stack=1,5
msnoise config set stack_method='linear'

msnoise config set data_structure=custom.py   # script reads .xml files for all stations
msnoise config set data_folder=station   # folder includes .xml files
msnoise populate


msnoise config set maxlag=40  # second
msnoise config set overlap=0.5
msnoise config set keep_days=Y
msnoise config set analysis_duration=86400  # second
msnoise config set corr_duration=1800  # second
msnoise config set hpc='Y'

msnoise db execute 'insert into filters (ref, low, mwcs_low, high, mwcs_high, rms_threshold, mwcs_wlen, mwcs_step, used) values (1, 0.01, 0.01, 49.9, 49.9, 0.0, 12.0, 4.0, 1)'

# --path: path to folder that includes raw waveform data
msnoise scan_archive --path ./Data --recursively --init
msnoise new_jobs

msnoise -t 8 compute_cc

msnoise reset -a STACK
msnoise new_jobs --hpc CC:STACK
msnoise stack -r
msnoise reset STACK
msnoise stack -m


