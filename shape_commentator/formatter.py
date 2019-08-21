def tuple_format(tpl_input, length = 10):
    class SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_TUPLE:
        pass
    class SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_LIST:
        pass
    result = ""
    
    too_long = False
    too_long_dot_yet = False
    tpl_stack = [tpl_input]
    while len(tpl_stack) > 0:
        tpl = tpl_stack.pop()
        if isinstance(tpl,SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_TUPLE):
            result += "),"
        elif isinstance(tpl,SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_LIST):
            result += "],"
        elif too_long:
            if too_long_dot_yet:
                result += " ... "
                too_long_dot_yet = False
            continue
        elif type(tpl) == tuple or type(tpl) == list:
            if type(tpl) == tuple:
                result += "("
                tpl_stack.append(SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_TUPLE())
            elif type(tpl) == list:
                result += "["
                tpl_stack.append(SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_LIST())
            tmp = list(tpl)
            tmp.reverse()
            for t in tmp:
                tpl_stack.append(t)
        elif hasattr(tpl, "shape"):
            result += str(tpl.shape) + ","
        else:
            result += type(tpl).__name__ + ","
        length -= 1
        if not too_long and length <= 0:
            too_long = True
            too_long_dot_yet = True
    result = result[:-1]
    return result