
from camera import Camera
from grid import Grid
from vcamera import Vcamera
from scenarioRunner import ScenarioRunner
from scenarioGenerator import ScenarioGenerator
import argparse
from stat_indicator import StatIndicator




parser          = argparse.ArgumentParser()

args            = parser.parse_args()

grid            = Grid(arg_host_ip = "192.168.0.1",arg_host_http_path = '/var/www/html')

hard_cam        = Camera(username = 'root',host_ip = '192.168.0.202',ssh_passwd = '',web_port = 8042,arduino_port = '/dev/ARDUINO',linux_port = '/dev/LINUX',rtos_port = '/dev/RTOS',grid = grid ,control_mode= 'complete' )

vcam            = Vcamera(hard_cam,'spherical')

sce_runner      = ScenarioRunner(vcam)

sc_gen          = ScenarioGenerator()

stat_indicator  = StatIndicator(sce_runner,sc_gen)

stat_indicator.run_status()

#parser.add_argument('-sc' , help = 'the name of the scenario , which can be : enduance ,stitching or sni' , type = str)





# # --functional tests --#
# sce_runner.run_test('./scenarios/still_pano.json',arg_result_path='~/Desktop/status/functionnal/still_pano/func_still_pano.json')
# sce_runner.run_test('./scenarios/S0.json',arg_result_path='~/Desktop/status/functionnal/S0/func_still_S0.json')
# sce_runner.run_test('./scenarios/C0.json',arg_result_path='~/Desktop/status/functionnal/C0/func_still_C0.json')
# sce_runner.run_test('./scenarios/func_spheric_video_30_fps.json',arg_result_path='~/Desktop/status/functionnal/v30/func_spheric_video_30_fps.json')
# sce_runner.run_test('./scenarios/func_spheric_video_25_fps.json',arg_result_path='~/Desktop/status/functionnal/v25/func_spheric_video_25_fps.json')
# sce_runner.run_test('./scenarios/func_spheric_video_24_fps.json',arg_result_path='~/Desktop/status/functionnal/v24/func_spheric_video_24_fps.json')
# sce_runner.run_test('./scenarios/func_spheric_video_15_fps.json',arg_result_path='~/Desktop/status/functionnal/v15/func_spheric_video_15_fps.json')
#
# # -- unitary tests --#
# sce_runner.run_test('./scenarios/unitary_spheric_video_30_fps_1min.json',arg_result_path='~/Desktop/status/unitary/v15/unitary_spheric_video_30_fps_1min.json')
# sce_runner.run_test('./scenarios/unitary_spheric_video_30_fps_10min.json',arg_result_path='~/Desktop/status/unitary/v15/unitary_spheric_video_30_fps_1min.json')
# sce_runner.run_test('./scenarios/unitary_spheric_video_30_fps_30min.json',arg_result_path='~/Desktop/status/unitary/v15/unitary_spheric_video_30_fps_1min.json')
#
# # -- robustness tests --#
# sc_gen.generate_sceanrio(arg_sceanrio = 'v30,pano,s0',arg_result_path = '~/Desktop/status/robustness/robus1/robustness1.json',min_duration=2,max_duration=4)
# #sc_gen.generate_sceanrio(arg_sceanrio = 'v25,v24,pano,s0*2',arg_result_path = '~/Desktop/status/robustness/robus2/robustness2.json',min_duration=2,max_duration=4)
# sce_runner.run_test('~/Desktop/status/robustness/robus1/robustness1.json',arg_result_path='~/Desktop/status/robustness/robus1/result_robustness1.json')
# #sce_runner.run_test('~/Desktop/status/robustness/robus2/robustness2.json',arg_result_path='~/Desktop/status/robustness/robus2/result_robustness2.json')

# -- robustness tests --#


# sce_runner.run_test('./scenarios/scenario1.json')


