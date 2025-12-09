import re

class FileWriter:
    def replace_value_in_file(file_path, variable_name, context, new_value):
        if context is None:
            return # there exist vars in the GUI that are not in the config file
        with open(file_path, 'r') as file:
            content = file.read()

        if isinstance(new_value, float): # for C syntax
            new_value = f"{new_value}f"
        elif isinstance(new_value, bool): # for C syntax
            new_value = "true" if new_value else "false"
        elif isinstance(new_value, int): # for C syntax
            new_value = str(new_value)

        context_block = FileWriter.extract_context_block(content, context)

        if not context_block:
            print(f"Could not extract block for '{context}'.")
            return

        print(f"Matched Context Block:\n{context_block}\n")

        variable_regex = rf"(\.\s*{re.escape(variable_name)}\s*=\s*)(-?\d+\.?\d*f?|true|false)" # find var 
        
        if not re.search(variable_regex, context_block):
            print(f"Variable '{variable_name}' not found inside '{context}'.")
            return

        updated_context_block = re.sub(variable_regex, lambda match: match.group(1) + str(new_value), context_block) # sub in new val

        content_new = content.replace(context_block, updated_context_block) # swap context

        # write to file
        if content == content_new:
            print("No changes made.")
        else:
            with open(file_path, 'w') as file:
                file.write(content_new)
            print(f"Updated '{variable_name}' in '{context}' to {new_value}.")


    def extract_context_block(content, context):
        pattern = re.escape(context) + r"\s*=\s*\{" # find the regex that matches opening brace
        match = re.search(pattern, content) ## find in file

        if not match:
            print(f"Context '{context}' not found.")
            return None

        start = match.start() # index of match
        brace_count = 0 # counter for brace balance
        end = start # counter for index

        for i in range(start, len(content)): # from start to EOF
            if content[i] == '{':
                brace_count += 1 # increment on open
            elif content[i] == '}':
                brace_count -= 1 # decrement on close
                if brace_count == 0: # balance found and context reached
                    end = i + 1
                    break

        return content[start:end] if brace_count == 0 else None
    
# replace_value_in_file('vcu/src/SUFST/Src/config.c', 'fully_pressed_fraction', ".bps", 0.0345)

