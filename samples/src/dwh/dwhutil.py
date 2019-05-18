## getbykeys, setbykeys
## js 26/03/2005
## Bubenorbis

def getbykeys(dict, *keys):
    """ dict is a structure of n nested dictionaries. Example:
    Let d1, d2, d3 be dictionaries. Let d1[1] = d2, d2[2] = d3, d3[3] = 4.
    getbykeys expects as many keys as there are nested dictionaries and
    returns the corresponding value of the innermost dictionary. Example:
    The call multiget(d1, 1, 2, 3) returns 4
    """
    result = dict
    for k in keys:
        result = result[k]
    return result


def setbykeys(dict, value, *keys):
    """ dict is a structure of n nested dictionaries. Example:
    Let d1, d2, d3 be dictionaries. Let d1[1] = d2, d2[2] = d3, d3[3] = 4.
    multiget expects a value and as many keys as there are nested dictionaries
    and sets the innermost dictionary at keys[-1] to the given value. Example:
    The call setbykeys(d1, 17, 1, 2, 3) sets d3[3] to 17
    """
    d = getbykeys(dict, *keys[:-1])
    d[keys[-1]] = value

    
        
        