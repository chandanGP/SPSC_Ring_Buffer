"""
Version 2.0
"""
import queue


class SPSC_Ring_Buffer :
    """
    Version 2.0
    """
    
    def __init__(
        this,
        buffer_size : int = -1,
        enable_get_wait : bool = True,
        replace_with_none : bool = False
    ) :
        """
        * arguments are not used, they are there just for backward compatability.
        """
        
        this.__buffer = queue.SimpleQueue()
    
    def put(
        this,
        x
    ) :
        this.__buffer.put(
            x
        )
        return True
    
    def get_with_wait(
        this,
        timeout : float | None = None
    ) :
        try :
            x = this.__buffer.get(
                timeout = timeout
            )
        except queue.Empty :
            x = None
        return x
    
    def get_without_wait(
        this
    ) :
        try :
            x = this.__buffer.get_nowait()
        except queue.Empty :
            x = None
        return x