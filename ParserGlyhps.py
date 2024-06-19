from glyphsLib import GSFont
"""
metricRight, metricLeft, если None, то значение ритма
width = площадка, delta x = width - (LSB + RSB)
"""
font = GSFont('TT Interphases Pro.glyphs')
master = font.masters[0]
master_kerning = font.kerning[master.id]
#print(master_kerning["@MMK_L_A"])

# Найти нужный глиф
#print(len(font.masters))
#a = font.glyphs['H'].layers[0]
#print(a.metricLeft)
#print(int("-20"))
#print(font.masters[0])
"""
def convert_to_int(metric_value: str, default: int) -> int:
    try:
        return int(metric_value)
    except (ValueError, TypeError):
        return default
"""

def get_info_glyphs_one_font(font: GSFont) -> dict:
    """
    Return LSB, RSB, width, delta x for Glyphs of All Masters One Font
    for characters A-Z and a-z.
    """
    result = {}
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    
    for char in characters:
        result[char] = {}
        
        for master in font.masters:
            if "Italic" in master.name:
                continue
            ritm = font.glyphs["H"].layers[master.id].metricLeft
            glyph = font.glyphs[char].layers[master.id]

            LSB = glyph.metricLeft  # return str
            LSB = ritm if LSB is None else LSB
            
            RSB = glyph.metricRight  # return str
            RSB = ritm if RSB is None else RSB
            
            width = glyph.width
            #delta = width - (LSB + RSB)

            result[char][master.name] = {
                'LSB': LSB,
                'RSB': RSB,
                'width': width,
                #'delta': delta
            }
    
    return result

print(get_info_glyphs_one_font(font))
def get_kern_value(font: GSFont, left_glyph_name: str, right_glyph_name: str) -> dict:
    """
    Return the kerning value between two glyphs if it exists, otherwise return 0 for all masters without Italic of one font.
    """
    kerning = {}
    left_glyph_name = "@MMK_L_" + left_glyph_name
    right_glyph_name = "@MMK_R_" + right_glyph_name
    for master in font.masters:
        if "Italic" in master.name:
            continue

        master_kerning = font.kerning[master.id]
        if left_glyph_name in master_kerning:
            if right_glyph_name in master_kerning[left_glyph_name]:
                kerning[master.name] = master_kerning[left_glyph_name][right_glyph_name]
            else:
                kerning[master.name] = 0
        else:
            kerning[master.name] = 0     
    
    return kerning

def get_kern_all_values_one_font(font: GSFont) -> dict:
    """
    Return a dictionary with kerning values for each pair of characters A-Z and a-z for all masters of one font.
    """
    result = {}
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    
    for left_char in characters:
        for right_char in characters:
            pair = left_char + right_char
            kern_value = get_kern_value(font, left_char, right_char)
            result[pair] = kern_value
                
    return result
