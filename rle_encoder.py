from collections import deque
from lsb_stuff import LSBStuff as Stuff


class RLEEncoder:
    def __init__(self, data: bytearray):
        self.data_to_encode = data
        self.result_data = bytearray()

    def review_the_same_bytes(self, count_of_same, prev_byte):
        if count_of_same != 0:
            while count_of_same > 127:
                self.result_data.append(255)
                self.result_data.append(prev_byte)
                count_of_same -= 127
            new_byte = '1' + bin(count_of_same)[2:].zfill(7)
            self.result_data.append(Stuff.get_int_from_bin(new_byte))
            self.result_data.append(prev_byte)
            count_of_same = 0
        return count_of_same

    def review_diff_bytes(self, diff_bytes: deque):
        if len(diff_bytes) != 0:
            while len(diff_bytes) > 127:
                self.result_data.append(127)
                for i in range(127):
                    self.result_data.append(diff_bytes.popleft())
            new_byte = Stuff.get_bin_from_int(len(diff_bytes))
            self.result_data.append(Stuff.get_int_from_bin(new_byte))
            for i in range(len(diff_bytes)):
                self.result_data.append(diff_bytes.popleft())
        return diff_bytes

    def encode(self):
        prev_byte = self.data_to_encode[0]
        count_of_same_bytes = 0
        differing_bytes = deque()
        for i in range(len(self.data_to_encode)):
            if i == 0:
                if self.data_to_encode[1] == prev_byte:
                    count_of_same_bytes += 1
                else:
                    differing_bytes.append(self.data_to_encode[i])
                continue
            if self.data_to_encode[i] == prev_byte:
                differing_bytes = self.review_diff_bytes(differing_bytes)
                count_of_same_bytes += 1
            else:
                count_of_same_bytes = \
                    self.review_the_same_bytes(count_of_same_bytes, prev_byte)
                prev_byte = self.data_to_encode[i]
                differing_bytes.append(self.data_to_encode[i])
        self.review_the_same_bytes(count_of_same_bytes, prev_byte)
        self.review_diff_bytes(differing_bytes)
        return self.result_data
