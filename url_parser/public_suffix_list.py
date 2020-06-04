class PublicSuffixList:
    _public_suffix_list = None

    @staticmethod
    def get_list():
        if PublicSuffixList._public_suffix_list is not None:
            return PublicSuffixList._public_suffix_list

        public_suffix_list = []

        with open('public_suffix_list.dat', encoding='utf-8') as file:
            data = file.readlines()

            for line in data:
                if line[0:2] == '//':
                    continue

                line = line.replace('\n', '')
                line = line.replace('\r', '')

                if line == '':
                    continue

                public_suffix_list.append(line)

        PublicSuffixList._public_suffix_list = public_suffix_list

        return PublicSuffixList._public_suffix_list
