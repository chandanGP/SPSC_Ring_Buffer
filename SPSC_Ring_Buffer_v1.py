"""
Veriosn 1.0
* This is the first version of SPSC ring buffer I created, which is fast and good but 
  I observed a very rare bug when both producer and consumer threads exchanging data 
  at very high speed , that bug is resolved in second version.
"""

import threading


class SPSC_Ring_Buffer :
    """
    Veriosn 1.0
    """
    
    def __init__(
        this,
        buffer_size : int,
        enable_get_wait : bool = True,
        replace_with_none : bool = False
    ) :
        this.__buffer_size = buffer_size
        this.__buffer = [
            None for _ in range(this.__buffer_size)
        ]
        
        this.__last_idx = len(this.__buffer) - 1
        this.__head_idx = 0
        this.__tail_idx = 0
        
        this.__get_event = threading.Event()
        
        if enable_get_wait :
            this.get = this.get_with_wait
        else :
            this.get = this.get_without_wait
        
        this.__replace_with_none = replace_with_none
    
    def put(
        this,
        x
    ) :
        if this.__head_idx < this.__last_idx :
            next_head_idx = this.__head_idx + 1
        else :
            next_head_idx = 0
        
        if next_head_idx == this.__tail_idx :
            return False
        
        this.__buffer[this.__head_idx] = x
        this.__head_idx = next_head_idx
        this.__get_event.set()
        return True
    
    def get_with_wait(
        this,
        timeout : float | None = None
    ) :
        while this.__tail_idx == this.__head_idx :
            this.__get_event.clear()
            if not this.__get_event.wait(timeout) :
                return 
        
        if this.__tail_idx < this.__last_idx :
            next_tail_idx = this.__tail_idx + 1
        else :
            next_tail_idx = 0
        
        x = this.__buffer[this.__tail_idx]
        if this.__replace_with_none :
            this.__buffer[this.__tail_idx] = None
        this.__tail_idx = next_tail_idx
        return x
    
    def get_without_wait(
        this
    ) :
        if this.__tail_idx == this.__head_idx :
            return None
        
        if this.__tail_idx < this.__last_idx :
            next_tail_idx = this.__tail_idx + 1
        else :
            next_tail_idx = 0
        
        x = this.__buffer[this.__tail_idx]
        if this.__replace_with_none :
            this.__buffer[this.__tail_idx] = None
        this.__tail_idx = next_tail_idx
        return x
        