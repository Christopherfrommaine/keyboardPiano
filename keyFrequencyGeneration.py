def generateKeyFrequencies(tuning='12TET', A=440):
    """
    Generates a dict mapping keyboard charachters to frequencies.

    Params:
        tuning (str): the tuning and keyboard layout to use
        A (int|float): the frequency of A4 (usually 440Hz)

    Returns:
        dict where key value pairs relate a charachter (uppercase) to a float frequency
    """

    # Keyboard layouts for selected tunings:
    notesInOrder12 = 'zsxdcvgbhnjm,l.;/\''.upper()
    notesInOrder17 = 'zwsxedcvtgbyhnujm,'.upper()
    notesInOrder19 = 'zwsxedcfvtgbyhnujmk,'.upper()
    notesInOrder24 = 'zws3xed4cfvtg6byh7nuj8mk,'.upper()
    notesInorder12Extended = ('azsxdcvgbhnjm,l.;/\''.upper(), '`1q2w3er5t6y7ui9o0p[=]\\'.upper())

    C = A * 2 ** (3 / 12)  # C is three half-steps above A
    if tuning[-3:] == 'TET':
        notesPerOct = int(tuning[:-3])
        match notesPerOct:
            case 12:
                notesInOrder = notesInOrder12
            case 17:
                notesInOrder = notesInOrder17
            case 19:
                notesInOrder = notesInOrder19
            case 24:
                notesInOrder = notesInOrder24
            case _:
                # Custom TET tunings are mapped onto the 12TET or 24TET keyboard.
                # This won't correspond to the piano, but it works.
                if notesPerOct < 12:
                    notesInOrder = notesInOrder12[:notesPerOct]
                else:
                    notesInOrder = notesInOrder24[:notesPerOct]
        return {key: C * 2 ** (i / notesPerOct) for i, key in enumerate(notesInOrder)}

    elif tuning == 'Pythagorean':
        ratios = [1/1, 256/243, 9/8, 32/27, 81/64, 4/3, 1024/729, 3/2, 128/81, 27/16, 16/9, 243/128, 2/1]  # Sorry, no augmented fourth for you!
        return {key: C * ratios[i] for i, key in enumerate(notesInOrder12)}
    elif tuning == 'Extended':
        lowerOct = {key: (1/2) * C * 2 ** ((i - 2) / 12) for i, key in enumerate(notesInorder12Extended[1])}
        upperOct = {key: C * 2 ** ((i - 1) / 12) for i, key in enumerate(notesInorder12Extended[0])}
        upperOct.update(lowerOct)
        return upperOct
    else:
        print("Specified Tuning Not Found")
        return generateKeyFrequencies()  # Unknown tuning: Returns basic 12TET
