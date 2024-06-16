class Users:
  @staticmethod
  def auth(auth_data) -> bool:
    return True


class Commands:
  @staticmethod
  def ping() -> str:
    return 'pong'

  @staticmethod
  def is_valid(command) -> bool:
    return True if command in VALID_COMMANDS else False

  @staticmethod
  def validate(command) -> str:
    if Commands.is_valid(command):
      return VALID_COMMANDS[command]

  @staticmethod
  def process(data):
    command = data['command']
    auth_data = data['auth']
    return {'auth': Users.auth(auth_data), 'command': Commands.validate(command)}


VALID_COMMANDS = {
  'ping': Commands.ping(),
}
