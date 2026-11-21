#!/usr/bin/env python3
"""Restore the packaged Module 2 folder layout after downloading from GitHub.

Run once: python prepare_data.py
Then: python -m pip install -r requirements.txt
      python render_and_run.py
      python record_demo.py

Uses only Python's standard library. Copies the checked, flat packaged files
into assets/, configs/, images/, outputs/ and real_capture/. Existing files are
preserved. No network access, deletion, or course submission is performed.
"""
from pathlib import Path
import hashlib
import shutil

FILES = [{'source': 'module2_upload__assets__oak_surface_generated.png',
  'destination': 'assets/oak_surface_generated.png',
  'sha256': 'a23c0ab391e5c9ebf9224f9406ae72cf99c54d863d248f6e7204e5b43595e41b'},
 {'source': 'module2_upload__assets__provenance.json',
  'destination': 'assets/provenance.json',
  'sha256': 'c2abb5213a814d8ff71d1d894fee66f2095d81e4b445085779e0b02a0285d69f'},
 {'source': 'module2_upload__configs__calibration_simulation.json',
  'destination': 'configs/calibration_simulation.json',
  'sha256': 'dffbe750bdd73e71242bbe661f7b731c385a6beeae776768e7858e897afebc56'},
 {'source': 'module2_upload__configs__dimensions_simulation.json',
  'destination': 'configs/dimensions_simulation.json',
  'sha256': '4008e1ff4baf85f76146e2551311c2b68beaa00d3d283ef99eee99f48a39c225'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_01.png',
  'destination': 'images/calibration/sim_checkerboard_01.png',
  'sha256': '0e7943f276df398ffcc6fd4a50ea9c671a6931457f150dbe0c83d904474545d7'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_02.png',
  'destination': 'images/calibration/sim_checkerboard_02.png',
  'sha256': '4aae0f45a6a2846332762b98a3c130c25a56fae89a84a8bd88f660596a5d382f'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_03.png',
  'destination': 'images/calibration/sim_checkerboard_03.png',
  'sha256': 'bbec3e75bdebd2c22d68503bd8b47ebbe3581eb752894f29c8244a1e441c6211'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_04.png',
  'destination': 'images/calibration/sim_checkerboard_04.png',
  'sha256': '7482f0aba29ed7fd8b57d74e0f16389612f2e2401276fd2d5b58227212a9106a'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_05.png',
  'destination': 'images/calibration/sim_checkerboard_05.png',
  'sha256': 'b29ca6be31e84ffbef12aa375a59697b9b6b861ceaa38bb8055a675dcd60480a'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_06.png',
  'destination': 'images/calibration/sim_checkerboard_06.png',
  'sha256': '41a6ee7db64ed510172d782d179d41e4b9c13e260052d5e5c406646b660d3cd7'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_07.png',
  'destination': 'images/calibration/sim_checkerboard_07.png',
  'sha256': 'd3b7eaac1bec2e8a1efc17710ad8c2bfbb12629dfbf750f59933c2cb34815c35'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_08.png',
  'destination': 'images/calibration/sim_checkerboard_08.png',
  'sha256': '803d8508a7336b988410e3706bfe78e5597c5e8738d21ffd398419a9a07d9236'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_09.png',
  'destination': 'images/calibration/sim_checkerboard_09.png',
  'sha256': 'ba24e97b73db400a42b75aad4fbbd725a19f978f625a9fcd43fc520f928b8574'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_10.png',
  'destination': 'images/calibration/sim_checkerboard_10.png',
  'sha256': '85f3c6f0eb9c3dae754cc2de439d340db58dfc0225f52ae77e714db45fde5034'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_11.png',
  'destination': 'images/calibration/sim_checkerboard_11.png',
  'sha256': 'fc1c37e4db9019bd61e13a930a21ddd69940574e5b65d9316621118f99de4de9'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_12.png',
  'destination': 'images/calibration/sim_checkerboard_12.png',
  'sha256': '2bafb9983ef1ed1c0036848f1c8f4a3dce383d7e1781179737855d9e6dc28f3a'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_13.png',
  'destination': 'images/calibration/sim_checkerboard_13.png',
  'sha256': '54e3f40405e331534353fe4e345464693e493c57b8c08fbc4adbf6dffd2c7fd0'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_14.png',
  'destination': 'images/calibration/sim_checkerboard_14.png',
  'sha256': '77a579455a4ef02ff9ba6ed35b4d6a17e77d8e63734c771caeef15f06b1f6303'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_15.png',
  'destination': 'images/calibration/sim_checkerboard_15.png',
  'sha256': '6c7ed6039dd973c4908ce6aebc45807a3961c9f228693237c971abf4ebecc4c7'},
 {'source': 'module2_upload__images__calibration__sim_checkerboard_16.png',
  'destination': 'images/calibration/sim_checkerboard_16.png',
  'sha256': '4a1f3bea2f9162112a62687c8b4963a4e928a7133ddf688d454649c88777af48'},
 {'source': 'module2_upload__images__sim_object_at_3m.png',
  'destination': 'images/sim_object_at_3m.png',
  'sha256': 'b539b3d375bb8f887278d229adc72715f0de68bf7362da3d5534bbcceb4386c3'},
 {'source': 'module2_upload__outputs__calibration__calibration.npz',
  'destination': 'outputs/calibration/calibration.npz',
  'sha256': 'c087d933199a84d6bbfe53d4b104af8dab8d669a9e77902c4f21617ccaebb5bd'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_01.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_01.png',
  'sha256': '6d4823f39fc35dd1d6db813f1f57796985807e10ad2929b67db7428a77f112bb'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_02.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_02.png',
  'sha256': 'b73405fa5f888cf88a0643c6a8afb853c10a606f0f8187e9fc5fd39022d22a97'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_03.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_03.png',
  'sha256': 'c3eb3ebdcbf5f80f60df1c391b1e6b08d870cefafe6cbe24e3e48056710f58d7'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_04.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_04.png',
  'sha256': 'af89f3154335a7fc4cebfa51200054685c8fe57bdb01daf8318333894ad6aaf7'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_05.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_05.png',
  'sha256': 'b2dcf8213d47cd469441c94c847e9d7711b8b18beb047d46303c2219737c437d'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_06.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_06.png',
  'sha256': 'eb5ef7a19bbd47e0748650c80ee2324d1babb4d5f3ee91d95bc0e297baa2f400'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_07.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_07.png',
  'sha256': '8f99892b5919de2b8f0d6331bcb947d329bfd93a0f79e89e95c81ef2bb1b2964'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_08.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_08.png',
  'sha256': '5f5b1044bfd17b71077893718a60770710045ed3e885d07ecb311e51c172382f'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_09.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_09.png',
  'sha256': '2bbd5aa9b2bbf467fe69b944003d39ea295717e05ec0d860430f102e9073c2b8'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_10.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_10.png',
  'sha256': 'fbb67481bb552cfdd1b095eeabf332080b8e6d366a3e530898059db75f4cc2d1'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_11.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_11.png',
  'sha256': '4dcf4e2aa23f4a3e4992da25d843e23f02e8d3c7120be4bf0c0b41641d21861b'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_12.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_12.png',
  'sha256': '9d76f3f8db56c625c40e20150494353d65f361246786ed6b65ac383300215677'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_13.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_13.png',
  'sha256': '723c7d5041dc9a35980f0b8a37c233f932e41ff4339a1b3fab61f3f02092afb1'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_14.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_14.png',
  'sha256': '27925fbdea56d81dbb767125d9499d0cbaf7a69f0aecb80cfa4d89712dd510ad'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_15.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_15.png',
  'sha256': '496b86d128133370e2a578bd60ef2f99940d6f029199b5d8edd97cf228eff4e9'},
 {'source': 'module2_upload__outputs__calibration__corners_sim_checkerboard_16.png',
  'destination': 'outputs/calibration/corners_sim_checkerboard_16.png',
  'sha256': '3989757005e5df9f9e9cd780b287920943bbd58c71a0823363524c1777ee3bfd'},
 {'source': 'module2_upload__outputs__calibration__execution_report.pdf',
  'destination': 'outputs/calibration/execution_report.pdf',
  'sha256': 'fb9b27d37cd12aa0a0c4e353c19b56e9f942655c58cc70d7147f0172979fe297'},
 {'source': 'module2_upload__outputs__calibration__metrics.json',
  'destination': 'outputs/calibration/metrics.json',
  'sha256': 'b6503bec3e836097fc9af2bbb59785de13bfa79a29a1dc91575e2396e0cc62bd'},
 {'source': 'module2_upload__outputs__calibration__run_config.json',
  'destination': 'outputs/calibration/run_config.json',
  'sha256': 'dffbe750bdd73e71242bbe661f7b731c385a6beeae776768e7858e897afebc56'},
 {'source': 'module2_upload__outputs__calibration__runtime.json',
  'destination': 'outputs/calibration/runtime.json',
  'sha256': 'fa7d0b2a13a089509793a9f074a6afecebcf21ca60f8ec4c43cf7707946de05d'},
 {'source': 'module2_upload__outputs__dimensions__execution_report.pdf',
  'destination': 'outputs/dimensions/execution_report.pdf',
  'sha256': '66714e5238ad83802a3e498d255c4a6306334971f7f319340333a495c988dca6'},
 {'source': 'module2_upload__outputs__dimensions__measurement.png',
  'destination': 'outputs/dimensions/measurement.png',
  'sha256': 'e118559647f871045ef4738e7a58607eb883594e8ec131997de61e6501c5a2ad'},
 {'source': 'module2_upload__outputs__dimensions__metrics.json',
  'destination': 'outputs/dimensions/metrics.json',
  'sha256': 'b17b56b5abed15923c703e20dfe82f5afc7ea1eb20568718dd6f8f5d28333ceb'},
 {'source': 'module2_upload__outputs__dimensions__run_config.json',
  'destination': 'outputs/dimensions/run_config.json',
  'sha256': '4008e1ff4baf85f76146e2551311c2b68beaa00d3d283ef99eee99f48a39c225'},
 {'source': 'module2_upload__outputs__dimensions__runtime.json',
  'destination': 'outputs/dimensions/runtime.json',
  'sha256': 'fa7d0b2a13a089509793a9f074a6afecebcf21ca60f8ec4c43cf7707946de05d'},
 {'source': 'module2_upload__real_capture__Print_Checkerboard_20mm_Letter.pdf',
  'destination': 'real_capture/Print_Checkerboard_20mm_Letter.pdf',
  'sha256': '5cb3b2298cbc8ad7ec0f6b7bb4e9ceab1735e2e3963b459e07d44e9943fbabf1'},
 {'source': 'module2_upload__real_capture__README.md',
  'destination': 'real_capture/README.md',
  'sha256': '4752e6483f730f467fd8d66967cde9084de4930cd2d1bf0615f4411dc66f67e9'},
 {'source': 'module2_upload__real_capture__Real_Photo_Checklist_and_Measurements.pdf',
  'destination': 'real_capture/Real_Photo_Checklist_and_Measurements.pdf',
  'sha256': '4eccded0b7029e349e007383605c6b7957724fc01fcda19faeb2acdd9cc1468f'},
 {'source': 'module2_upload__real_capture__build_capture_kit.py',
  'destination': 'real_capture/build_capture_kit.py',
  'sha256': '54c24cb3f33c520771e2d9c56d005f6c59d8547b3b8d0a351ad585ab6dd995a9'},
 {'source': 'module2_upload__real_capture__measurements_to_fill.json',
  'destination': 'real_capture/measurements_to_fill.json',
  'sha256': 'a2483e822a7c104cc7cc4c87d0443ab97dff91c7b2c9e88f6286c4989c39e220'}]


def prepare(root=None):
    root = Path(root or Path(__file__).resolve().parent).resolve()
    pending = []
    # Validate every needed source before changing the output tree.
    for item in FILES:
        destination = root / item['destination']
        if destination.exists():
            if not destination.is_file():
                raise RuntimeError('Expected a file: ' + str(destination))
            continue
        source = root / item['source']
        if not source.is_file():
            raise FileNotFoundError('Download the complete repository: missing ' + source.name)
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        if actual != item['sha256']:
            raise RuntimeError('Packaged file checksum mismatch: ' + source.name)
        pending.append((source, destination))
    for source, destination in pending:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    return len(pending)


if __name__ == '__main__':
    count = prepare()
    print(f'Module 2 folders ready: restored {count} files; existing files preserved.')
