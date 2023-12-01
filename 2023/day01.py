import re
encoded_calibrations = open('2023/data/day01.txt','r').read().split('\n')

pt1_decoder = {'0': '0', '1': '1', '2': '2', '3': '3', 
          '4': '4', '5': '5', '6': '6', '7': '7', 
          '8': '8', '9': '9' }
pt2_decoder = {'0': '0', '1': '1', '2': '2', '3': '3', 
          '4': '4', '5': '5', '6': '6', '7': '7', 
          '8': '8', '9': '9', 
          'one': '1', 'two': '2', 'three': '3',
          'four': '4', 'five': '5', 'six': '6',
          'seven': '7', 'eight': '8', 'nine': '9'}

def decode(encoded_value: str):
    decoder = pt2_decoder
    codes = re.compile(('|').join(decoder.keys()))
    # find the first code in the encoded string
    first_code = codes.search(encoded_value).group()

    # we can't use .findall to get the last code because in the string 'oneeight', it 
    # would return 'one' a the last code instead of 'eight'
    # just reversing the string and codes will find the last one tho
    reverse_codes = re.compile(('|').join([key[::-1] for key in decoder.keys()]))
    last_code = reverse_codes.search(encoded_value[::-1]).group()[::-1]

    decoded_value = int(decoder[first_code] + decoder[last_code])

    return decoded_value

calibrations = map(decode, encoded_calibrations)
print(sum(calibrations))
