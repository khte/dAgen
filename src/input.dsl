
physical create_physarch test
physical gcs_components hmi=Human_machince_interface gcs_c2=GCS_C2_link pwr=Power_supply
physical uav_components mr=Multirotor fc=Flight_controller pwr=Power_system
physical transmitter true

functional create_funcspec test
functional aviate_functions est_alt=Estimate_altitude est_pos=Estimate_position ctrl_alt=Control_altitude ctrl_lat=Control_lateral_position
functional navigate_functions follow_route=Follow_route
functional communicate_functions c2=C2_link_communication hmi=HMI_system pilot=Remote_pilot_control daa=Detect_and_avoid
functional allocate ctrl_lat=test.uas.uav.fc ctrl_alt=test.uas.uav.mr est_pos=test.uas.uav.fc est_alt=test.uas.uav.fc follow_route=test.uas.uav.fc c2=test.uas.uav.uav_c2 hmi=test.uas.gcs.hmi pilot=test.uas.tx
