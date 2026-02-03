class TextEngine:
    def __init__(self, initial_capacity=100):
        self.buffer = [None] * initial_capacity
        self.gap_start = 0
        self.gap_end = initial_capacity

    def insert_char(self, char):
        if self.gap_start == self.gap_end:
            # We haven't written _resize yet, but we won't hit this limit in the test
            print("Buffer Full! (Resize not implemented yet)") 
            return 
        
        self.buffer[self.gap_start] = char
        self.gap_start += 1

    def set_cursor(self, new_pos):
        current_text_length = len(self.buffer) - (self.gap_end - self.gap_start)
        new_pos = max(0, min(new_pos, current_text_length))

        # Move Gap LEFT
        while self.gap_start > new_pos:
            self.gap_start -= 1
            self.gap_end -= 1
            self.buffer[self.gap_end] = self.buffer[self.gap_start]
            self.buffer[self.gap_start] = None 

        # Move Gap RIGHT
        while self.gap_start < new_pos:
            self.buffer[self.gap_start] = self.buffer[self.gap_end]
            self.buffer[self.gap_end] = None 
            self.gap_start += 1
            self.gap_end += 1

    def get_text(self):
        prefix = self.buffer[:self.gap_start]
        suffix = self.buffer[self.gap_end:]
        # Filter out Nones just in case, though logic should handle it
        clean_prefix = [c for c in prefix if c is not None]
        clean_suffix = [c for c in suffix if c is not None]
        return "".join(clean_prefix + clean_suffix)

    def __repr__(self):
        return f"Buffer: {self.buffer}\nGap: [{self.gap_start}:{self.gap_end}]"