from typing import Dict


packet_tag = str

packet = Dict[str, str | Dict]

auth_packet = Dict[str, str]

game_packet = Dict[str, str]

gateway_packet = Dict[packet_tag, auth_packet | game_packet]
