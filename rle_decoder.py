from lsb_stuff import LSBStuff as Stuff


class RLEDecoder:
    def __init__(self, data_to_decode: bytearray):
        self.data = data_to_decode
        self.result = bytearray()

    def decode(self):
        index = 0
        while index != len(self.data):
            if Stuff.get_bin_from_int(self.data[index]).startswith('1'):
                bound = int(Stuff.get_bin_from_int(self.data[index])[1:], 2)
                for i in range(bound):
                    self.result.append(self.data[index + 1])
                index += 2
            else:
                for i in range(self.data[index]):
                    index += 1
                    self.result.append(self.data[index])
                index += 1
        return self.result
