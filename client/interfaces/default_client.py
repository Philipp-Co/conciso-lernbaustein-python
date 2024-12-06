"""Implementation of a default Client which can be used in any situation."""
# ---------------------------------------------------------------------------------------------------------------------
from interfaces.iclient import IClient
from logging import Logger
from typing import Dict

# ---------------------------------------------------------------------------------------------------------------------
class DefaultClient(IClient):
    """Implementation of a default Client. 
    
    Does not execute anything. Just returns 0 and logs its input arguments. 
    """
    def __init__(self):
        super().__init__()
        pass

    def run(self, args: Dict[str, str]) -> int:
        """Does nothing."""
        self.logger().info(f'Run DefaulClient with Arguments {args}')   
        return 0
    pass
# ---------------------------------------------------------------------------------------------------------------------
