def print_flattened(flattened):
    # Recursively print all terms in a flattened list maintaining nested structures
    output=[]
    for term in flattened:
        if isinstance(term,list):
            output.append(print_flattened(term))
        else:
            output.append(str(term))
    return output