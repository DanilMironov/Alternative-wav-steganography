import argparse
import sys
from lsb_encoder import LSBEncoder
from lsb_decoder import LSBDecoder


class Main:
    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser(description='LSB')
        parser.add_argument('-en', '--encode', action='store_true',
                            help='if you want to put information into WAV.')
        parser.add_argument('-dec', '--decode', action='store_true',
                            help='if you want to pull out information from WAV.')
        parser.add_argument('-f', '--file', default='', type=str,
                            help='Enter the path to the file'
                                 'you want to inscribe.', nargs='*')
        parser.add_argument('-w', '--wav', default='', type=str,
                            help='Enter the path to the WAV-file', nargs='*')
        return parser.parse_args(args)

    def main(self):
        parser = self.parse_args(sys.argv[1:])
        if parser.encode and parser.decode:
            raise Exception("This keys shouldn't be used at the same time")
        if parser.encode:
            files = parser.file
            wav_path = ' '.join(parser.wav)
            if len(files) == 0 or len(wav_path) == 0:
                raise Exception('Not all arguments are specified. Try again!')
            lsb = LSBEncoder(files, wav_path)
            lsb.inscribe()
            lsb.create_new_wav()
            return
        if parser.decode:
            wav_path = ' '.join(parser.wav)
            if len(wav_path) == 0:
                raise Exception('Not all arguments are specified. Try again!')
            lsb = LSBDecoder(wav_path)
            lsb.get_hidden_information()


if __name__ == '__main__':
    main = Main()
    main.main()
