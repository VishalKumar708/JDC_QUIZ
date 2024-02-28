
def convert_str_to_bool(value):
    if isinstance(value, str):
        value = value.strip().lower()  # Convert to lowercase and remove leading/trailing whitespace
        if value == 'true':
            return True
        elif value == 'false':
            return False
    elif isinstance(value, bool):
        return value  # If already a boolean value, return it directly
    raise ValueError("Invalid boolean value")

