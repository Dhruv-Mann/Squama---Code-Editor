class TextEngine:
    # This class implements a **Gap Buffer**, a classic text-editor data structure.
    # The key idea: keep a contiguous "gap" (empty region) at the cursor location.
    # Insertions are O(1) near the gap; moving the cursor means moving the gap.
    def __init__(self, initial_capacity=100):
        """
        Initializes the Gap Buffer.
        
        :param initial_capacity: The initial size of the buffer (including the gap).
        """
        # The 'buffer' is our working memory (a Python list).
        # Syntax notes:
        # - `self` is the instance (like `this` in other languages).
        # - `initial_capacity=100` is a default argument.
        # - `[...] * initial_capacity` repeats the list, making a fixed-size array.
        # In C, this would be a malloc'd array. In Python, we use a list of None.
        self.buffer = [None] * initial_capacity
        
        # gap_start: The index where the gap begins (inclusive).
        # Initially 0 because the cursor starts at the beginning.
        self.gap_start = 0
        
        # gap_end: The index where the gap ends (exclusive).
        # Initially, the WHOLE buffer is the gap because it's empty.
        # So gap_end == initial_capacity.
        self.gap_end = initial_capacity

    def __repr__(self):
        # __repr__ is a Python "dunder" method used for developer-friendly display.
        # Returning a string here lets you `print(obj)` or inspect it in a debugger.
        return f"Buffer: {self.buffer}\nGap: [{self.gap_start}:{self.gap_end}]"
    def insert_char(self, char):
        """
        Inserts a character at the current cursor position (gap_start).
        """
        # 1. Check if the gap is full (start meets end).
        # In a gap buffer, a "full" gap means there is no space left to insert.
        # Syntax note: `==` checks equality, and `if` starts a conditional block.
        if self.gap_start == self.gap_end:
            self._resize() # We will implement this helper later
        
        # 2. Write the character into the 'hole'.
        # This is O(1) because we are just assigning to a list index.
        # Syntax note: `self.buffer[i] = value` writes at index i.
        self.buffer[self.gap_start] = char
        
        # 3. Move the gap start forward (the hole shrinks from the left).
        # This effectively advances the cursor by one position.
        # Syntax note: `+= 1` increments an integer in place.
        self.gap_start += 1

    def set_cursor(self, new_pos):
        """
        Moves the gap to the new position.
        This allows us to type anywhere in the text.
        """
        # This method had an indentation error before; it must be aligned
        # with other methods (same indentation as `insert_char`).
        # Syntax note: indentation defines blocks in Python.

        # Clamp the position (cannot go below 0 or past the total text size).
        # We calculate 'current_text_length' as capacity - gap_size.
        # Syntax note: `len(list)` gives the list length.
        # Syntax note: `max` and `min` are built-in functions.
        current_text_length = len(self.buffer) - (self.gap_end - self.gap_start)
        new_pos = max(0, min(new_pos, current_text_length))

        # CASE 1: Move Gap LEFT (e.g., cursor goes from 5 to 2).
        # We must move characters from the left of the gap to the right of the gap.
        # Syntax note: `while` repeats until the condition is False.
        while self.gap_start > new_pos:
            # Step the gap one position left by decrementing both indexes.
            self.gap_start -= 1
            self.gap_end -= 1
            # Move the character that was before the gap to the end of the gap.
            self.buffer[self.gap_end] = self.buffer[self.gap_start]
            # Optional: clear the old slot for easier debugging.
            self.buffer[self.gap_start] = None

        # CASE 2: Move Gap RIGHT (e.g., cursor goes from 2 to 5).
        # We must move characters from the right of the gap to the left of the gap.
        while self.gap_start < new_pos:
            # Move the character from the end of the gap to the start of the gap.
            self.buffer[self.gap_start] = self.buffer[self.gap_end]
            # Optional: clear the old slot for easier debugging.
            self.buffer[self.gap_end] = None
            # Step the gap one position right by incrementing both indexes.
            self.gap_start += 1
            self.gap_end += 1


            