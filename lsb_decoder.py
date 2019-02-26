import pickle
from lsb_stuff import LSBStuff as Stuff


class LSBDecoder:
    def __init__(self, path_to_the_file, index_of_start_of_data=None):
        self.main_file = Stuff.read_the_file(path_to_the_file)
        if index_of_start_of_data is None:
            self.index_of_start_of_data = \
                Stuff.find_index_of_the_start_of_data(self.main_file)
        else:
            self.index_of_start_of_data = index_of_start_of_data
        self.bits_per_sample = self._get_bits_per_sample()

    def _get_bits_per_sample(self):
        byte34 = self.main_file[34].to_bytes(1, 'little')
        byte35 = self.main_file[35].to_bytes(1, 'little')
        bits_per_sample = int.from_bytes(byte34 + byte35, 'little')
        return bits_per_sample

    def _read_the_flag(self, bytes_to_describe, index, offset):
        description = ''
        for i in range(bytes_to_describe):
            current_byte = self.main_file[index: index + 1]
            bin_repr_current_byte = Stuff.get_bin_str_from_bytearray(current_byte)
            list_of_current_chars = list(bin_repr_current_byte)
            description += list_of_current_chars[-1]
            index += offset
        return index, description

    def _read_the_content(self, buffer, length, index, offset):
        string_repr = ''
        buffer_index = 0
        for i in range(length):
            current_byte = self.main_file[index: index + 1]
            bin_repr_current_byte = Stuff.get_bin_str_from_bytearray(current_byte)
            current_pairs = list(bin_repr_current_byte)
            string_repr += current_pairs[-1]
            if len(string_repr) == 8:
                buffer[buffer_index] = Stuff.get_int_from_bin(string_repr)
                string_repr = ''
                buffer_index += 1
            index += offset
        return index

    def _read_the_hash(self, length_of_hash, index, offset):
        hash_str = ''
        for i in range(length_of_hash):
            current_byte = self.main_file[index: index + 1]
            bin_repr_current_byte = Stuff.get_bin_str_from_bytearray(current_byte)
            current_pairs = list(bin_repr_current_byte)
            hash_str += current_pairs[-1]
            index += offset
        rec_hash = Stuff.get_int_from_bin(hash_str)
        return index, rec_hash

    @staticmethod
    def _compare_the_checksum(actual_sum, rec_sum):
        if actual_sum != rec_sum:
            raise Exception('There was a distortion of information.({}!={})'
                            .format(actual_sum, rec_sum))

    def get_hidden_information(self):
        offset = bytes_per_sample = self.bits_per_sample // 8
        index = self.index_of_start_of_data + bytes_per_sample
        bytes_to_describe_length = 32
        index, length_description = self._read_the_flag(
            bytes_to_describe_length,
            index,
            offset
        )
        length = Stuff.get_int_from_bin(length_description)
        length_of_new_bytearray = length // 8
        bytes_to_describe_hash = 8
        index, length_of_hash_description = self._read_the_flag(
            bytes_to_describe_hash,
            index,
            offset
        )
        length_of_hash = Stuff.get_int_from_bin(length_of_hash_description)
        index, rec_hash = self._read_the_hash(length_of_hash, index, offset)
        content_of_recieved = bytearray(length_of_new_bytearray)
        index += self._read_the_content(content_of_recieved, length, index, offset)
        actual_hash = Stuff.get_hash(content_of_recieved)
        self._compare_the_checksum(actual_hash, rec_hash)
        self.create_files(content_of_recieved)

    @staticmethod
    def create_files(content_of_recieved):
        recieved_dict = pickle.loads(content_of_recieved)
        for element in recieved_dict:
            with open('(recieved) ' + element, 'wb') as file:
                file.write(recieved_dict[element])
