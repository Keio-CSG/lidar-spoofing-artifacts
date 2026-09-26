U = r"G:/共有ドライブ/吉岡研-共有ドライブ/002-共同研究/UCI共同研究"
W = U + "/website用素材"
P = U + "/0_過去のLiDAR測距データ"
V16 = P + "/Velodyne VLP-16"

# Each set: attack/benign captures; each capture: pcap + optional recorded video(s)
SETS = [
  dict(id="cpi-text-ieeesp", group="CPI", title="Text injection: “IEEE S&P”", lidar="VLP-16", scene="Indoor, static", date="2022-07-13",
       note="Chosen Pattern Injection writes the letters “IEEE S&P” into free space in front of the sensor.",
       caps=[dict(role="attack", label="CPI", pcap=W+"/PCAP/IEEES&P.pcap", video=W+"/CPI/IEEES&P.mp4")]),
  dict(id="cpi-text-oakland", group="CPI", title="Text injection: “Oakland”", lidar="VLP-16", scene="Indoor, static", date="2022-08-01",
       note="The same CPI spoofer drawing the word “Oakland” as a floating point pattern.",
       caps=[dict(role="attack", label="CPI", pcap=W+"/PCAP/oakland.pcap", video=W+"/CPI/oakland.mp4")]),
  dict(id="cpi-3d-objects", group="CPI", title="3D object injection: pedestrian and car", lidar="VLP-16", scene="Indoor, static", date="2022-10-17",
       note="Injected 3D pedestrian and vehicle point patterns, including a replayed copy of a real car captured by the same LiDAR. Recorded videos are matched to captures by timestamp.",
       caps=[dict(role="attack", label="CPI · pedestrian", pcap=V16+"/2022-10-17_3D_Spoofing/human.pcap", video=V16+"/2022-10-17_3D_Spoofing/VeloView 4.1.3 64-bit 2022-10-17 15-45-31.mp4"),
             dict(role="attack", label="CPI · pedestrian, moving", pcap=V16+"/2022-10-17_3D_Spoofing/human_bure_sukuname.pcap", video=V16+"/2022-10-17_3D_Spoofing/VeloView 4.1.3 64-bit 2022-10-17 17-30-51.mp4"),
             dict(role="attack", label="CPI · car at 10 m", pcap=V16+"/2022-10-17_3D_Spoofing/car_10m.pcap", video=V16+"/2022-10-17_3D_Spoofing/VeloView 4.1.3 64-bit 2022-10-17 16-12-45.mp4"),
             dict(role="attack", label="CPI · car, oblique", pcap=V16+"/2022-10-17_3D_Spoofing/car_naname.pcap"),
             dict(role="attack", label="CPI · CAD car at 2 m", pcap=V16+"/2022-10-17_3D_Spoofing/blender_car_2m.pcap"),
             dict(role="attack", label="CPI · real-car copy at 4 m", pcap=V16+"/2022-10-17_3D_Spoofing/real_car_copy_4m_2.pcap")]),
  dict(id="cpi-walking", group="CPI", title="Dynamic injection: walking pedestrian", lidar="VLP-16", scene="Indoor, dynamic", date="2022-11-12",
       note="A real walking person is captured, then replayed as a moving injected pedestrian. The capture of the real person is the benign reference.",
       caps=[dict(role="benign", label="Real walking person (source)", pcap=V16+"/2022-11-12_CPI_jitter/2022-11-12-16-46-53_Velodyne-VLP-16-Data_capture_real_human.pcap"),
             dict(role="attack", label="CPI · walking pedestrian", pcap=V16+"/2022-11-12_CPI_jitter/2022-11-12-15-27-07_Velodyne-VLP-16-Data_walking_man_op_5v.pcap", video=V16+"/2022-11-12_CPI_jitter/VeloView 4.1.3 64-bit 2022-11-12 15-27-27.mp4"),
             dict(role="attack", label="CPI · wall pattern", pcap=V16+"/2022-11-12_CPI_jitter/2022-11-12-14-11-50_Velodyne-VLP-16-Data_wall_op_5v.pcap", video=V16+"/2022-11-12_CPI_jitter/VeloView 4.1.3 64-bit 2022-11-12 14-12-14.mp4")]),
  dict(id="rm-human-room-vlp32c", group="Removal", title="Pedestrian removal: PRA vs HFR", lidar="VLP-32C", scene="Indoor room, dynamic", date="2022-08-17",
       note="A person walks in front of the LiDAR. The synchronized Physical Removal Attack (PRA) and the High-Frequency Removal (HFR) attack are compared with a benign run.",
       camera=W+"/human_removal_attack/human_remove_camera.MOV",
       caps=[dict(role="benign", label="Benign", pcap=P+"/2022-08-17/VLP32c/benign_strongest_remove_human.pcap", video=W+"/human_removal_attack/benign_remove_human.mp4"),
             dict(role="attack", label="PRA (synchronized)", pcap=P+"/2022-08-17/VLP32c/sync_strongest_remove_human.pcap", video=W+"/human_removal_attack/PRA_human.mp4"),
             dict(role="attack", label="PRA (synchronized), run 2", pcap=P+"/2022-08-17/VLP32c/sync_strongest_remove_human2.pcap"),
             dict(role="attack", label="HFR", pcap=P+"/2022-08-17/VLP32c/HFA_strongest_remove_human.pcap", video=W+"/human_removal_attack/HFR_human.mp4")]),
  dict(id="rm-human-corridor-vlp16", group="Removal", title="Pedestrian removal in a corridor", lidar="VLP-16", scene="Indoor corridor, dynamic", date="2022-08-10",
       note="A person walks down a corridor towards the LiDAR, recorded benign, under a synchronized PRA, and under HFR.",
       camera=P+"/2022-08-10/カメラ/20220810_180944.mp4",
       caps=[dict(role="benign", label="Benign walk", pcap=P+"/2022-08-10/VLP16_outdoor/nospoof_walk.pcap"),
             dict(role="attack", label="PRA (synchronized)", pcap=P+"/2022-08-10/VLP16_outdoor/sync_remove_human.pcap"),
             dict(role="attack", label="HFR", pcap=P+"/2022-08-10/VLP16_outdoor/HFA_remove_human.pcap")]),
  dict(id="rm-car-outdoor-vlp16", group="Removal", title="Vehicle removal in a parking lot", lidar="VLP-16", scene="Outdoor, static", date="2022-08-10",
       note="HFR removes a parked car at about 5 m. No benign capture of this exact placement was found; the attack captures include periods with the spoofer off.",
       caps=[dict(role="attack", label="HFR · dual return", pcap=P+"/2022-08-10/VLP16_outdoor/car_remove_dual.pcap", video=W+"/car_removal_attack/car_HFR.mp4"),
             dict(role="attack", label="HFR · strongest return", pcap=P+"/2022-08-10/VLP16_outdoor/car_remove.pcap")]),
  dict(id="rm-human-outdoor-vlp16", group="Removal", title="Pedestrian removal in a parking lot", lidar="VLP-16", scene="Outdoor, dynamic", date="2022-08-10",
       note="HFR against a person walking between parked cars.",
       camera=P+"/2022-08-10/カメラ/20220810_164402.mp4",
       caps=[dict(role="attack", label="HFR · dual return", pcap=P+"/2022-08-10/VLP16_outdoor/human_remove_dual.pcap")]),
]
SETUP_IMAGES = [W+"/setup/indoor_setup_caption.png", W+"/setup/outdoor_setup_caption.png", W+"/car_removal_attack/car_HFR_setup.jpg"]
