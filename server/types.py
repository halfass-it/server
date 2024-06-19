from typing import Dict

# auth_packet = {'token': '$TOKEN', 'username': '$USERNAME'}
AuthPacketStructure = Dict[str, Dict[str, str]]

# gameplay_packet = {'action': '$ACTION', 'data': '$DATA'}
GameplayPacketStructure = Dict[str, Dict[str, str]]

# command = {'auth': auth_packet, 'gameplay': gameplay_packet}
CommandPacketStruct = Dict[str, Dict[str, Dict[str, str]]]
