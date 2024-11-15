def to_text(val):
    try:
        return "{:,}".format(int(val)).replace(",", " ")
    except:
        print("Error trying to format value: ", val)
        if val:
            return val
        else:
            return "No information"
