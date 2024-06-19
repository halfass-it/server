from typing import Dict

# auth_packet = {'token': '$TOKEN', 'username': '$USERNAME'}
AuthPacketStructure = Dict[str, Dict[str, str]]

# game_packet = {'action': '$ACTION', 'data': '$DATA'}
GamePacketStructure = Dict[str, Dict[str, str]]

# command = {'auth': auth_packet, 'gameplay': game_packet}
CommandPacketStruct = Dict[str, Dict[str, Dict[str, str]]]
