from typing import Optional, Dict
from dataclasses import dataclass
from enum import Enum

class RecordingState(Enum):
    IDLE = "idle"
    CALIBRATING = "calibrating"
    RECORDING = "recording"
    PROCESSING = "processing"
    RECOGNIZING = "recognizing"
    ERROR = "error"
    SUCCESS = "success"

@dataclass
class RecordingStatus:
    state: RecordingState
    message: str
    error: Optional[str] = None
    data: Optional[Dict] = None

class StateManager:
    def __init__(self):
        self.current_status = RecordingStatus(RecordingState.IDLE, "Ready")
        self.observers = []
    
    def update_state(self, state: RecordingState, message: str, error: str = None, data: Dict = None):
        self.current_status = RecordingStatus(state, message, error, data)
        self._notify_observers()
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def _notify_observers(self):
        for observer in self.observers:
            observer(self.current_status) 