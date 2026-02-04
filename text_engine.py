import copy

class TextEngine:
    def __init__(self, initial_capacity=100):
        self.buffer = [None] * initial_capacity
        self.gap_start = 0
        self.gap_end = initial_capacity
        self.undo_stack = []
        self.redo_stack = []

    def insert_char(self, char):
        if char in [" ", "\n"] or len(self.undo_stack) == 0:
            self._snapshot()
            self.redo_stack.clear()

        if self.gap_start == self.gap_end:
            new_capacity = len(self.buffer) * 2
            new_buffer = [None] * new_capacity
            new_buffer[:self.gap_start] = self.buffer[:self.gap_start]
            new_gap_end = new_capacity - (len(self.buffer) - self.gap_end)
            new_buffer[new_gap_end:] = self.buffer[self.gap_end:]
            self.buffer = new_buffer
            self.gap_end = new_gap_end
        
        self.buffer[self.gap_start] = char
        self.gap_start += 1

    def set_cursor(self, new_pos):
        current_text_length = len(self.buffer) - (self.gap_end - self.gap_start)
        new_pos = max(0, min(new_pos, current_text_length))

        while self.gap_start > new_pos:
            self.gap_start -= 1
            self.gap_end -= 1
            self.buffer[self.gap_end] = self.buffer[self.gap_start]
            self.buffer[self.gap_start] = None 

        while self.gap_start < new_pos:
            self.buffer[self.gap_start] = self.buffer[self.gap_end]
            self.buffer[self.gap_end] = None 
            self.gap_start += 1
            self.gap_end += 1

    def get_text(self):
        clean_prefix = [c for c in self.buffer[:self.gap_start] if c is not None]
        clean_suffix = [c for c in self.buffer[self.gap_end:] if c is not None]
        return "".join(clean_prefix + ["|"] + clean_suffix)

    def __repr__(self):
        return f"Buffer: {self.buffer}\nGap: [{self.gap_start}:{self.gap_end}]"
    
    def delete_char(self):
        if self.gap_start == 0:
            return
        self._snapshot()
        self.redo_stack.clear()
        self.gap_start -= 1
        self.buffer[self.gap_start] = None

    def _snapshot(self):
        state = {
            'buffer': list(self.buffer),
            'gap_start': self.gap_start,
            'gap_end': self.gap_end
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            return
        current_state = {
            'buffer': list(self.buffer),
            'gap_start': self.gap_start,
            'gap_end': self.gap_end
        }
        self.redo_stack.append(current_state)
        prev_state = self.undo_stack.pop()
        self.buffer = prev_state['buffer']
        self.gap_start = prev_state['gap_start']
        self.gap_end = prev_state['gap_end']

    def redo(self):
        if not self.redo_stack:
            return
        current_state = {
            'buffer': list(self.buffer),
            'gap_start': self.gap_start,
            'gap_end': self.gap_end
        }
        self.undo_stack.append(current_state)
        next_state = self.redo_stack.pop()
        self.buffer = next_state['buffer']
        self.gap_start = next_state['gap_start']
        self.gap_end = next_state['gap_end']

    @property
    def cursor_pos(self):
        return self.gap_start
    
    def load_text(self, text):
        capacity = max(len(text) * 2, 100)
        self.buffer = [None] * capacity
        for i, char in enumerate(text):
            self.buffer[i] = char
        self.gap_start = len(text)
        self.gap_end = capacity
        self.undo_stack.clear()
        self.redo_stack.clear()

    def delete_from_cursor(self, count):
        """
        Deletes 'count' characters starting from the current cursor position (Forward deletion).
        Used for deleting selections.
        """
        if count <= 0:
            return

        self._snapshot()
        self.redo_stack.clear()
        
        # To delete forward in a Gap Buffer, we just increase the gap_end pointer.
        # This "swallows" the text into the gap.
        
        # Ensure we don't delete past the end of the file
        max_deletable = len(self.buffer) - self.gap_end
        count = min(count, max_deletable)
        
        # Clear data for debugging (optional, but cleaner)
        for i in range(self.gap_end, self.gap_end + count):
            self.buffer[i] = None
            
        # The Magic: Just move the end pointer!
        self.gap_end += count
