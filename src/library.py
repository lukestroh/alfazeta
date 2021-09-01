# https://blogfonts.com/fonts/s/373/49373/img/slide-segment7-0.png
def library():
    pos = dict(
        top = 0b00000001,
        bottom = 0b00001000,
        middle = 0b01000000,
        top_left = 0b00100000,
        bottom_left = 0b00010000,
        bottom_right = 0b00000100,
        top_right = 0b00000010
    )

    alphabet = dict(
        # lowercase
        a = 0b01110111,
        b = 0b01111100,
        c = 0b01011000,
        d = 0b01011110,
        e = 0b01111001,
        f = 0b01110001,
        g = 0b00111101,
        h = 0b01110100, # for uppercase, 0b01110110 (This will be confused with 'X' though)
        i = 0b00010000, # for uppercase, 0b00110000
        j = 0b00011110,
        k = 0b01110101,
        l = 0b00110000,
        m = 0b01010101,
        n = 0b01010100, # for uppercase, 0b00110111
        o = 0b01011100, # for uppercase, 0b00111111
        p = 0b01110011,
        q = 0b01100111,
        r = 0b01010000, # for uppercase, 0b00110001
        s = 0b01101101,
        t = 0b01111000,
        u = 0b00011100, # for uppercase, 0b00111110
        v = 0b00111100, # this might look bad
        w = 0b01111110,
        x = 0b01110110,
        y = 0b01101110,
        z = 0b01001011,

        # uppercase
        A = 0b01110111,
        B = 0b01111100,
        C = 0b00111001,
        D = 0b01011110,
        E = 0b01111001,
        F = 0b01110001,
        G = 0b00111101,
        H = 0b01110110,
        I = 0b00110000,
        J = 0b00011110,
        K = 0b01110101,
        L = 0b00111000,
        M = 0b00010101,
        N = 0b00110111,
        O = 0b00111111,
        P = 0b01110011,
        Q = 0b01100111,
        R = 0b00110011,
        S = 0b01101101,
        T = 0b01111000,
        U = 0b00111110,
        V = 0b01100110, # this might look bad
        W = 0b01111110,
        X = 0b01110110,
        Y = 0b01101110,
        Z = 0b01011011
    )

    numbers = {
        '0':  0b00111111,
        '1':  0b00000110,
        '2':  0b01011011,
        '3':  0b01001111,
        '4':  0b01100110,
        '5':  0b01101101,
        '6':  0b01111101,
        '7':  0b00000111,
        '8':  0b01111111,
        '9':  0b01101111
    }

    symbols = {
        '?': 0b01010011,
        ' ': 0b00000000,
        ':': 0b01001000,
        "'": 0b00000010,
        '"': 0b00100010,
        '-': 0b01000000,
        '_': 0b00001000,
        '/': 0b01010010,
        '\\': 0b01100100,
        '*': 0b01100011,
        ',': 0b00001100,
    }

    combined = alphabet | numbers | symbols | pos
    return combined

def flipped():
    flipped_alphabet = dict(
        # lowercase
        a = 0b01111110,
        b = 0b01100111,
        c = 0b01000011,
        d = 0b01110011,
        e = 0b01001111,
        f = 0b01001110,
        g = 0b01011111,
        h = 0b01100110, # for uppercase, 0b01110110 (This will be confused with 'X' though)
        i = 0b00000010, # for uppercase, 0b00110000
        j = 0b00110001,
        k = 0b01101110,
        l = 0b00000110,
        m = 0b01101010,
        n = 0b01100010, # for uppercase, 0b00110111
        o = 0b01100011, # for uppercase, 0b00111111
        p = 0b01011110,
        q = 0b01111100,
        r = 0b01000010, # for uppercase, 0b00110001
        s = 0b01101101,
        t = 0b01000111,
        u = 0b00100011, # for uppercase, 0b00111110
        v = 0b00100111, # this might look bad
        w = 0b01110111,
        x = 0b01110110,
        y = 0b01110101,
        z = 0b01001011,

        # # uppercase
        A = 0b01111110,
        B = 0b01111111,
        C = 0b00001111,
        D = 0b00111111,
        # E = 0b01001111,
        F = 0b01110001,
        G = 0b00111101,
        H = 0b01110110,
        I = 0b00110000,
        J = 0b00011110,
        K = 0b01110101,
        L = 0b00111000,
        M = 0b00010101,
        N = 0b00110111,
        O = 0b00111111,
        P = 0b01110011,
        Q = 0b01100111,
        R = 0b00110011,
        S = 0b01101101,
        T = 0b01111000,
        U = 0b00111110,
        V = 0b01100110, # this might look bad
        W = 0b01111110,
        X = 0b01110110,
        Y = 0b01101110,
        Z = 0b01011011
    )

    numbers_flipped = {
        '0':  0b00111111,
        '1':  0b00110000,
        '2':  0b01011011,
        '3':  0b01111001,
        '4':  0b01110100,
        '5':  0b01101101,
        '6':  0b01101111,
        '7':  0b00111000,
        '8':  0b01111111,
        '9':  0b01111100
    }

    symbols_flipped = {
        '?': 0b01011010,
        ' ': 0b00000000,
        ':': 0b01000001,
        "'": 0b00010000,
        '"': 0b00010100,
        '-': 0b01000000,
        '_': 0b00000001,
        '/': 0b01010010,
        '\\': 0b01100100,
        '*': 0b01011100,
        ',': 0b00100001,
    }
    combined_flipped = flipped_alphabet | numbers_flipped | symbols_flipped

    return combined_flipped
