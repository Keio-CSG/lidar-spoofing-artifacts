U = r"G:/共有ドライブ/吉岡研-共有ドライブ/002-共同研究/UCI共同研究"
W = U + "/website用素材"
P = U + "/0_過去のLiDAR測距データ"
V16 = P + "/Velodyne VLP-16"
N25 = r"G:/共有ドライブ/吉岡研-共有ドライブ/004-Paper Submission/NDSS2025"
NAG = r"G:/共有ドライブ/吉岡研-共有ドライブ/011-個人ファイル/Nagata"
ICRA_TALK = "pptx:" + r"G:/共有ドライブ/吉岡研-共有ドライブ/009-学会発表資料/ICRA2025/ICAR_slide_2_Eng (2).pptx" + "|ppt/media/media1.mp4"

PAPERS = {
  "ndss24": dict(short="NDSS 2024", release="v1.0", url="https://sites.google.com/keio.jp/keio-csg/projects/new-gen-lidar-sec",
                 title="LiDAR Spoofing Meets the New-Gen: Capability Improvements, Broken Assumptions, and New Attack Strategies"),
  "icra25": dict(short="ICRA 2025", release="icra25-v1.0", url="https://arxiv.org/abs/2502.13641", code="https://github.com/Keio-CSG/slamspoof",
                 title="SLAMSpoof: Practical LiDAR Spoofing Attacks on Localization Systems Guided by Scan Matching Vulnerability Analysis"),
  "ndss25": dict(short="NDSS 2025", release="ndss25-v1.0", url="https://sites.google.com/keio.jp/keio-csg/projects/AttackonDrivingVehicle",
                 title="On the Realism of LiDAR Spoofing Attacks against Autonomous Driving Vehicle at High Speed and Long Distance"),
}

# Each set: attack/benign captures; each capture: pcap + optional recorded video(s)
SETS = [
  dict(paper="ndss24", id="cpi-text-ieeesp", group="CPI", title="Text injection: “IEEE S&P”", lidar="VLP-16", scene="Indoor, static", date="2022-07-13",
       note="Chosen Pattern Injection writes the letters “IEEE S&P” into free space in front of the sensor.",
       caps=[dict(role="attack", label="CPI", pcap=W+"/PCAP/IEEES&P.pcap", video=W+"/CPI/IEEES&P.mp4")]),
  dict(paper="ndss24", id="cpi-text-oakland", group="CPI", title="Text injection: “Oakland”", lidar="VLP-16", scene="Indoor, static", date="2022-08-01",
       note="The same CPI spoofer drawing the word “Oakland” as a floating point pattern.",
       caps=[dict(role="attack", label="CPI", pcap=W+"/PCAP/oakland.pcap", video=W+"/CPI/oakland.mp4")]),
  dict(paper="ndss24", id="cpi-3d-objects", group="CPI", title="3D object injection: pedestrian and car", lidar="VLP-16", scene="Indoor, static", date="2022-10-17",
       note="Injected 3D pedestrian and vehicle point patterns, including a replayed copy of a real car captured by the same LiDAR. Recorded videos are matched to captures by timestamp.",
       caps=[dict(role="attack", label="CPI · pedestrian", pcap=V16+"/2022-10-17_3D_Spoofing/human.pcap", video=V16+"/2022-10-17_3D_Spoofing/VeloView 4.1.3 64-bit 2022-10-17 15-45-31.mp4"),
             dict(role="attack", label="CPI · pedestrian, moving", pcap=V16+"/2022-10-17_3D_Spoofing/human_bure_sukuname.pcap", video=V16+"/2022-10-17_3D_Spoofing/VeloView 4.1.3 64-bit 2022-10-17 17-30-51.mp4"),
             dict(role="attack", label="CPI · car at 10 m", pcap=V16+"/2022-10-17_3D_Spoofing/car_10m.pcap", video=V16+"/2022-10-17_3D_Spoofing/VeloView 4.1.3 64-bit 2022-10-17 16-12-45.mp4"),
             dict(role="attack", label="CPI · car, oblique", pcap=V16+"/2022-10-17_3D_Spoofing/car_naname.pcap"),
             dict(role="attack", label="CPI · CAD car at 2 m", pcap=V16+"/2022-10-17_3D_Spoofing/blender_car_2m.pcap"),
             dict(role="attack", label="CPI · real-car copy at 4 m", pcap=V16+"/2022-10-17_3D_Spoofing/real_car_copy_4m_2.pcap")]),
  dict(paper="ndss24", id="cpi-walking", group="CPI", title="Dynamic injection: walking pedestrian", lidar="VLP-16", scene="Indoor, dynamic", date="2022-11-12",
       note="A real walking person is captured, then replayed as a moving injected pedestrian. The capture of the real person is the benign reference.",
       caps=[dict(role="benign", label="Real walking person (source)", pcap=V16+"/2022-11-12_CPI_jitter/2022-11-12-16-46-53_Velodyne-VLP-16-Data_capture_real_human.pcap"),
             dict(role="attack", label="CPI · walking pedestrian", pcap=V16+"/2022-11-12_CPI_jitter/2022-11-12-15-27-07_Velodyne-VLP-16-Data_walking_man_op_5v.pcap", video=V16+"/2022-11-12_CPI_jitter/VeloView 4.1.3 64-bit 2022-11-12 15-27-27.mp4"),
             dict(role="attack", label="CPI · wall pattern", pcap=V16+"/2022-11-12_CPI_jitter/2022-11-12-14-11-50_Velodyne-VLP-16-Data_wall_op_5v.pcap", video=V16+"/2022-11-12_CPI_jitter/VeloView 4.1.3 64-bit 2022-11-12 14-12-14.mp4")]),
  dict(paper="ndss24", id="rm-human-room-vlp32c", group="Removal", title="Pedestrian removal: PRA vs HFR", lidar="VLP-32C", scene="Indoor room, dynamic", date="2022-08-17",
       note="A person walks in front of the LiDAR. The synchronized Physical Removal Attack (PRA) and the High-Frequency Removal (HFR) attack are compared with a benign run.",
       camera=W+"/human_removal_attack/human_remove_camera.MOV",
       caps=[dict(role="benign", label="Benign", pcap=P+"/2022-08-17/VLP32c/benign_strongest_remove_human.pcap", video=W+"/human_removal_attack/benign_remove_human.mp4"),
             dict(role="attack", label="PRA (synchronized)", pcap=P+"/2022-08-17/VLP32c/sync_strongest_remove_human.pcap", video=W+"/human_removal_attack/PRA_human.mp4"),
             dict(role="attack", label="PRA (synchronized), run 2", pcap=P+"/2022-08-17/VLP32c/sync_strongest_remove_human2.pcap"),
             dict(role="attack", label="HFR", pcap=P+"/2022-08-17/VLP32c/HFA_strongest_remove_human.pcap", video=W+"/human_removal_attack/HFR_human.mp4")]),
  dict(paper="ndss24", id="rm-human-corridor-vlp16", group="Removal", title="Pedestrian removal in a corridor", lidar="VLP-16", scene="Indoor corridor, dynamic", date="2022-08-10",
       note="A person walks down a corridor towards the LiDAR, recorded benign, under a synchronized PRA, and under HFR.",
       camera=P+"/2022-08-10/カメラ/20220810_180944.mp4",
       caps=[dict(role="benign", label="Benign walk", pcap=P+"/2022-08-10/VLP16_outdoor/nospoof_walk.pcap"),
             dict(role="attack", label="PRA (synchronized)", pcap=P+"/2022-08-10/VLP16_outdoor/sync_remove_human.pcap"),
             dict(role="attack", label="HFR", pcap=P+"/2022-08-10/VLP16_outdoor/HFA_remove_human.pcap")]),
  dict(paper="ndss24", id="rm-car-outdoor-vlp16", group="Removal", title="Vehicle removal in a parking lot", lidar="VLP-16", scene="Outdoor, static", date="2022-08-10",
       note="HFR removes a parked car at about 5 m. No benign capture of this exact placement was found; the attack captures include periods with the spoofer off.",
       caps=[dict(role="attack", label="HFR · dual return", pcap=P+"/2022-08-10/VLP16_outdoor/car_remove_dual.pcap", video=W+"/car_removal_attack/car_HFR.mp4"),
             dict(role="attack", label="HFR · strongest return", pcap=P+"/2022-08-10/VLP16_outdoor/car_remove.pcap")]),
  dict(paper="ndss24", id="rm-human-outdoor-vlp16", group="Removal", title="Pedestrian removal in a parking lot", lidar="VLP-16", scene="Outdoor, dynamic", date="2022-08-10",
       note="HFR against a person walking between parked cars.",
       camera=P+"/2022-08-10/カメラ/20220810_164402.mp4",
       caps=[dict(role="attack", label="HFR · dual return", pcap=P+"/2022-08-10/VLP16_outdoor/human_remove_dual.pcap")]),
  # ---- NDSS 2025: Moving Vehicle Spoofing (MVS) ----
  dict(paper="ndss25", id="mvs-wall-40kmh", group="CPI", title="Ghost-wall injection at 40 km/h", lidar="VLP-32C", scene="Test track, dynamic", date="2024-03-13",
       note="The VLP-32C rides on a vehicle driving towards the roadside MVS system, which tracks the LiDAR and injects a ghost wall ahead of the vehicle. The camera clip starts two seconds before the capture.",
       camera=P+"/2024-03-13-K2実験/CPI_40kph.MOV",
       caps=[dict(role="attack", label="Synchronized injection · 40 km/h", pcap=P+"/2024-03-13-K2実験/2024-03-13-16-41-02_Velodyne-VLP-32C-Data_injection.pcap")]),
  dict(paper="ndss25", id="mvs-wall-30kmh", group="CPI", title="Ghost-wall injection at 30 km/h", lidar="VLP-32C", scene="Test track, dynamic", date="2024-03-15",
       note="Same setup as the 40 km/h run, with the vehicle at 30 km/h.",
       caps=[dict(role="attack", label="Synchronized injection · 30 km/h", pcap=P+"/2024-03-15-K2実験/LiDARデータ/2024-03-15-16-44-06_Velodyne-VLP-32C-Data_experiment1_wall_30km.pcap")]),
  dict(paper="ndss25", id="mvs-injection-runs", group="CPI", title="Injection runs on the test track", lidar="VLP-32C", scene="Test track, dynamic", date="2024-04-10",
       note="Six consecutive injection runs against the vehicle-mounted VLP-32C. Run speeds were not recorded in the file names.",
       caps=[dict(role="attack", label=f"Injection run {i}", pcap=P+f"/2024-04-10-K2/vlp32c_20240410_CPItest{'' if i == 1 else '_' + str(i)}.pcap") for i in range(1, 7)]),
  dict(paper="ndss25", id="mvs-cart-injection", group="CPI", title="Injection against a moving LiDAR on a cart", lidar="VLP-32C", scene="Outdoor, dynamic", date="2024-02-08",
       note="An early outdoor test of the auto-aiming spoofer: the VLP-32C is pushed on a cart towards the MVS system.",
       camera=[P+"/2024-02-08 屋外台車実験/実験風景ビデオ/cpi_1.MOV", P+"/2024-02-08 屋外台車実験/実験風景ビデオ/cpi_2.MOV"],
       caps=[dict(role="attack", label="Injection with auto-aiming", pcap=P+"/2024-02-08 屋外台車実験/cpi/2024-02-08-vlp32c-2.pcap")]),
  dict(paper="ndss25", id="mvs-indoor-car", group="CPI", title="Indoor injection of a captured car", lidar="VLP-32C", scene="Indoor, static", date="2024-03-22 / 04-04",
       note="A real car and a real pedestrian are first captured with the VLP-32C; the car trace is then injected as a spoofed vehicle. The captures of the real objects are the benign references.",
       caps=[dict(role="benign", label="Real car (source trace)", pcap=P+"/Velodyne VLP-32c/2024-03-22-16-30-00_Velodyne-VLP-32C-Data_real_car_capture.pcap"),
             dict(role="benign", label="Real pedestrian (source trace)", pcap=P+"/Velodyne VLP-32c/2024-03-22-16-33-21_Velodyne-VLP-32C-Data_real_pedestrian_capture.pcap"),
             dict(role="attack", label="Injected car", pcap=P+"/2024-04-04 屋内車注入・A-HFR角度特性/2024-04-04-19-39-48_Velodyne-VLP-32C-Data_indoor_car_injection.pcap")]),
  dict(paper="ndss25", id="mvs-autoware", group="Removal", title="End-to-end attack on an Autoware vehicle", lidar="VLP-32C", scene="Outdoor, dynamic", date="2024-08",
       note="PIXKIT with a VLP-32C, driven by Autoware.ai, benign vs. under attack (paper Fig. 16). Only the video is available; the LiDAR data of this run was not archived as pcap.",
       camera=N25+"/autoware.mp4", caps=[]),
  # ---- NDSS 2025: A-HFR against pulse-fingerprinting LiDARs (Hesai AT128 / XT32) ----
  dict(paper="ndss25", id="ahfr-at128-pedestrian", group="Removal", title="A-HFR vs. HFR on AT128: pedestrian at 3 m", lidar="AT128", scene="Indoor, static", date="2023-11-23",
       note="AT128 has pulse fingerprinting, which defeats the plain HFR attack; the adaptive HFR (A-HFR) at 15 MHz still removes almost all points (paper Fig. 11).",
       caps=[dict(role="benign", label="Benign", pcap=P+"/Hesai AT128/at128_remove_human_3m.pcap"),
             dict(role="attack", label="A-HFR · 15 MHz", pcap=P+"/Hesai AT128/at128_remove_human_3m_adphfr_15mhz_take2.pcap")]),
  dict(paper="ndss25", id="ahfr-at128-width", group="Removal", title="A-HFR attack width sweep on AT128", lidar="AT128", scene="Indoor, static", date="2024-04-04",
       note="A-HFR at 15 MHz with horizontal attack ranges from 10 to 60 degrees (paper Table VI).",
       caps=[dict(role="benign", label="Benign", pcap=P+"/2024-04-04 屋内車注入・A-HFR角度特性/2024-04-04_at128_benign.pcap")] +
            [dict(role="attack", label=f"A-HFR · {d}° wide", pcap=P+f"/2024-04-04 屋内車注入・A-HFR角度特性/2024-04-04_at128_{d}deg.pcap") for d in range(10, 70, 10)]),
  dict(paper="ndss25", id="ahfr-xt32-width", group="Removal", title="A-HFR attack width sweep on XT32", lidar="XT32", scene="Indoor, static", date="2024-04-04",
       note="A-HFR at 24 MHz with horizontal attack ranges from 10 to 60 degrees (paper Table VI). XT32 needs a higher frequency, so the removal rate drops faster as the range widens.",
       caps=[dict(role="benign", label="Benign", pcap=P+"/2024-04-04 屋内車注入・A-HFR角度特性/2024-04-04_xt32_benign.pcap")] +
            [dict(role="attack", label=f"A-HFR · {d}° wide", pcap=P+f"/2024-04-04 屋内車注入・A-HFR角度特性/2024-04-04_xt32_{d}deg.pcap") for d in range(10, 70, 10)]),
  dict(paper="ndss25", id="ahfr-at128-highspeed", group="Removal", title="A-HFR against AT128 on a moving vehicle", lidar="AT128", scene="Test track, dynamic", date="2024-04-10",
       note="The AT128 rides on a vehicle driving past a pedestrian while the MVS system tracks it and fires A-HFR at 15 MHz (paper Table IX). This is the 60 km/h run used in the paper's detection analysis, together with the benign reference drive; the vehicle is stopped for the first few seconds.",
       caps=[dict(role="benign", label="Benign drive", pcap=U+"/2025_NDSS_DATA/Adaptive HFR moving vehicle/benign.pcap")] +
            # Only the run used in the paper's detection analysis is published; the attack did not visibly take effect in
            # every other run (at128_20240410_{10,20,30}_{1-3}, {40,50}_{1-4}, 60_{1,2}), so those are left out.
            [dict(role="attack", label="A-HFR · 60 km/h", pcap=P+"/2024-04-10-K2/at128_20240410_60_3.pcap")]),
  # ---- ICRA 2025: SLAMSpoof ----
  dict(paper="icra25", id="slamspoof-primitives", group="Removal", title="Removal and injection seen by a VLP-16", lidar="VLP-16", scene="Indoor corridor, static", date="2024-09-13",
       note="The two attack primitives SLAMSpoof places along a trajectory: HFR removal, which turns the attacked sector into scattered noise, and injection of a fake wall that the scan matcher latches onto.",
       caps=[dict(role="benign", label="Benign", pcap=NAG+"/0913/2024-09-13-14-55-00_Velodyne-VLP-16-Data-benign.pcap"),
             dict(role="attack", label="HFR removal", pcap=NAG+"/0913/2024-09-13-14-55-51_Velodyne-VLP-16-Data-hfr.pcap"),
             dict(role="attack", label="Fake-wall injection", pcap=NAG+"/0913/2024-09-13-15-11-23_Velodyne-VLP-16-Data-wall2.pcap")]),
  dict(paper="icra25", id="slamspoof-whill", group="Removal", title="Attacking a moving WHILL from the roadside", lidar="VLP-32C", scene="Outdoor, dynamic", date="2024-08-20",
       note="A WHILL CR2 carrying a VLP-32C drives across a sports field towards the tracking spoofer (under the tent), which attacks it from up to 50 m. The screen recording shows the localization output under attack. The LiDAR data of these runs is not on the lab drive, so this set is video only.",
       camera=[dict(path=NAG+f"/IMG_{n}.MOV", label=f"Field camera · run {i}") for i, n in enumerate(("0123", "0128", "0136", "0141"), 1)] +
              [dict(path=NAG+"/Screencast from 2024年11月05日 13時30分10秒.webm", label="Localization under attack (screen recording)")], caps=[]),
  dict(paper="icra25", id="slamspoof-talk", group="Removal", title="Talk video: SMVS and spoofer placement", lidar="VLP-32C", scene="Outdoor, dynamic", date="2025-05",
       note="The video shown in the ICRA 2025 talk: the Scan Matching Vulnerability Score, how it picks spoofer placements, and the attack results.",
       camera=[dict(path=ICRA_TALK, label="ICRA 2025 talk video")], caps=[]),
]
SETUP_IMAGES = [W+"/setup/indoor_setup_caption.png", W+"/setup/outdoor_setup_caption.png", W+"/car_removal_attack/car_HFR_setup.jpg"]

AT128_CORR = P + "/Hesai AT128/AT128E2X_Angle_Correction_File.dat"
