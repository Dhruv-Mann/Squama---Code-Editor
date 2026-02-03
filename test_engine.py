# THIS IS THE MISSING MAGIC LINE
from text_engine import TextEngine 

if __name__ == "__main__":
    editor = TextEngine(initial_capacity=10)
    
    print("1. Inserting 'H', 'i'")
    editor.insert_char('H')
    editor.insert_char('i')
    print(editor) 
    print("Text:", editor.get_text()) 
    
    print("\n2. Moving Cursor to index 1 (between 'H' and 'i')")
    editor.set_cursor(1)
    print(editor) 
    
    print("\n3. Inserting 'e' at index 1")
    editor.insert_char('e')
    print("Text:", editor.get_text()) 

    # Verification
    if editor.get_text() == "Hei":
        print("\n✅ GREEN: Logic is solid.")
    else:
        print("\n❌ RED: Logic failed.")