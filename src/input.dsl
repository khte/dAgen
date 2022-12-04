
physical create_physarch test
physical gcs_components hmi=Human_machince_interface gcs_c2=GCS_C2_link pwr=Power_supply
physical drone_components mr=Multirotor daa=DAA_system fc=Flight_controller uav_c2=UAV_C2_link pwr=Power_system
physical transmitter yes

functional create_funcspec test
functional add_functions std
