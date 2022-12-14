from enum import Enum


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    UPLOADING = "uploading"
    DONE = "done"
    FAILED = "failed"
