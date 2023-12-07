import enum


class InferenceStatus(enum.Enum):
    """Inference status enum"""
    PROCESSING = 'processing'
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
