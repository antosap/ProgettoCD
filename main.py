import os
import time


class Solution:
    # Funzione per applicare BWT
    def BWT_Encode(self, s):
        # inizio BWT con parola presa da input
        table = [input_string[i:] + input_string[:i] for i in range(len(input_string))]  # Table of rotations of string
        # print('table = ', table)
        table = sorted(table)
        # print('sorted table = ', table)
        last_column = [row[-1:] for row in table]  # Last characters of each row

        bwt = ''.join(last_column)
        pos = bwt.find("$")

        return (bwt, pos)

    def iBWT(self, bwt):
        table = [""] * len(bwt)  # Make empty table

        for i in range(len(bwt)):
            table = [bwt[i] + table[i] for i in range(len(bwt))]  # Add a column of r
            # print('unsorted = ', table)
            table = sorted(table)
            # print('sorted    =', table)

        inverse_bwt = [row for row in table if row.endswith("$")][0]  # Find the correct row (ending in $)
        inverse_bwt = inverse_bwt.rstrip("$")  # Get rid of start and end markers

        return inverse_bwt

    # Funzione per applicare LZW

    def LZW_Encode(self, rle_output):
        """Compress a string to a list of output symbols."""

        # Build the dictionary.
        dict_size = 256
        dictionary = dict((chr(i), i) for i in range(dict_size))
        # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}
        uncompressed = rle_output[0]
        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                # Add wc to the dictionary.
                dictionary[wc] = dict_size
                dict_size += 1
                w = c

        # Output the code for w.
        if w:
            result.append(dictionary[w])
        return result, rle_output[1]

    # Funzione per applicare iLZW

    def iLZW_Decode(self, iHuffmanOutput):
        """Decompress a list of output ks to a string."""
        from io import StringIO

        # Build the dictionary.
        dict_size = 256
        dictionary = dict((i, chr(i)) for i in range(dict_size))
        # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

        # use StringIO, otherwise this becomes O(N^2)
        # due to string concatenation in a loop
        result = StringIO()
        w = chr(iHuffmanOutput.pop(0))
        result.write(w)
        for k in iHuffmanOutput:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result.write(entry)

            # Add w+entry[0] to the dictionary.
            dictionary[dict_size] = w + entry[0]
            dict_size += 1

            w = entry
        return result.getvalue()

    # Funzione per applicare RLE
    def RLE_Encode(self, bwt_output):
        input_list = bwt_output[0]
        # inizio RLE con passaggio da bwt
        res = ""
        tmp = input_list[0]
        count = 1
        for i in range(1, len(input_list)):
            if input_list[i] != tmp:
                res += str(count) + tmp
                tmp = input_list[i]
                count = 1
            else:
                count += 1
        return (res + str(count) + tmp), bwt_output[1]

    # Funzione per applicare iRLE

    def iRLE(self, huffmanOutput):
        output = ""
        num = ""
        for i in huffmanOutput:
            if i.isalpha():
                output += i * int(num)
                num = ""
            else:
                num += i
        return output

    # Funzione per applicare Huffman

    def HuffmanEncoding(self, the_data):
        ob = Solution()
        symbolWithProbs = ob.CalculateProbability(the_data)
        the_symbols = symbolWithProbs.keys()
        the_probabilities = symbolWithProbs.values()
        # print("symbols: ", the_symbols)
        # print("probabilities: ", the_probabilities)

        the_nodes = []

        # converting symbols and probabilities into huffman tree nodes
        for symbol in the_symbols:
            the_nodes.append(ob.Nodes(symbolWithProbs.get(symbol), symbol))

        while len(the_nodes) > 1:
            # sorting all the nodes in ascending order based on their probability
            the_nodes = sorted(the_nodes, key=lambda x: x.probability)
            # for node in nodes:
            #      print(node.symbol, node.prob)

            # picking two smallest nodes
            right = the_nodes[0]
            left = the_nodes[1]

            left.code = 0
            right.code = 1

            # combining the 2 smallest nodes to create new node
            newNode = ob.Nodes(left.probability + right.probability, left.symbol + right.symbol, left, right)

            the_nodes.remove(left)
            the_nodes.remove(right)
            the_nodes.append(newNode)

        huffmanEncoding = ob.CalculateCodes(the_nodes[0])
        # print("symbols with codes", huffmanEncoding)
        ob.TotalGain(the_data, huffmanEncoding)
        encodedOutput = ob.OutputEncoded(the_data, huffmanEncoding)
        return encodedOutput, the_nodes[0]

    # Funzione per applicare inversa Huffman

    def HuffmanDecoding(self, encodedData, huffmanTree):
        treeHead = huffmanTree
        decodedOutput = []
        for x in encodedData:
            if x == '1':
                huffmanTree = huffmanTree.right
            elif x == '0':
                huffmanTree = huffmanTree.left
            try:
                if huffmanTree.left.symbol == None and huffmanTree.right.symbol == None:
                    pass
            except AttributeError:
                decodedOutput.append(huffmanTree.symbol)
                huffmanTree = treeHead

        # string = ''.join([str(item) for item in decodedOutput])
        return decodedOutput

    # Dipendenze Huffman

    # Node of a Huffman Tree
    class Nodes:
        def __init__(self, probability, symbol, left=None, right=None):
            # probability of the symbol
            self.probability = probability

            # the symbol
            self.symbol = symbol

            # the left node
            self.left = left

            # the right node
            self.right = right

            # the tree direction (0 or 1)
            self.code = ''

    """ A supporting function in order to calculate the probabilities of symbols in specified data """

    def CalculateProbability(self, the_data):
        the_symbols = dict()
        for item in the_data:
            if the_symbols.get(item) == None:
                the_symbols[item] = 1
            else:
                the_symbols[item] += 1
        return the_symbols

    """ A supporting function in order to print the codes of symbols by travelling a Huffman Tree """
    the_codes = dict()

    def CalculateCodes(self, node, value=''):
        ob = Solution()
        # a huffman code for current node
        newValue = value + str(node.code)

        if (node.left):
            ob.CalculateCodes(node.left, newValue)
        if (node.right):
            ob.CalculateCodes(node.right, newValue)

        if (not node.left and not node.right):
            ob.the_codes[node.symbol] = newValue

        return ob.the_codes

    """ A supporting function in order to get the encoded result """

    def OutputEncoded(self, the_data, coding):
        encodingOutput = []
        for element in the_data:
            # print(coding[element], end = '')
            encodingOutput.append(coding[element])

        the_string = ''.join([str(item) for item in encodingOutput])
        return the_string

    """ A supporting function in order to calculate the space difference between compressed and non compressed data"""

    def TotalGain(self, the_data, coding):
        # total bit space to store the data before compression
        beforeCompression = len(the_data) * 8
        afterCompression = 0
        the_symbols = coding.keys()
        for symbol in the_symbols:
            the_count = the_data.count(symbol)
            # calculating how many bit is required for that symbol in total
            afterCompression += the_count * len(coding[symbol])
        # print("Space usage before compression (in bits):", beforeCompression)
        # print("Space usage after compression (in bits):", afterCompression)

    '''
        Funzione che prende una stringa in input.
        Controlla se è alfanumerica, altrimenti ritorna False.
        Se è alfanumerica, controlla se ci sono numeri.
        Anche in questo caso ritorna False, altrimenti True.
    '''

    def checkAlphanumeric(self, s):
        if s.isalnum():
            if any(char.isdigit() for char in s):
                return False
            else:
                return True
        else:
            return False

    '''
        Funzione che prende in input una stringa.
        Cicla sulla stringa per esaminare ogni carattere.
        Controlla se ogni carattere è una lettera.
        Se trova un numero, lo rimuove e restituise la stringa pulita.
    '''

    def deleteSpecialCharacters(self, s):
        for char in s:
            if not char.isalpha():
                s = s.replace(str(char), "")
        return s

    def saveToBin(self, the_tree):
        import pickle

        with open("nodes.bin", "wb") as f:
            pickle.dump(the_tree, f)

    def readFromBin(self):
        import pickle

        with open("nodes.bin", "rb") as f:
            return pickle.load(f)


# Controllo esistenza compressed.txt

while True:
    # Chiedi all'utente di scegliere un'azione
    action = input("Vuoi comprimere o decomprimere? (c/d): ")

    # Esegui l'azione scelta dall'utente
    if action == "c":

        if os.path.isfile('compressed.txt'):
            os.remove('compressed.txt')

        file_url = input("\nSpecify file location: ")

        with open(file_url + ".txt", 'r+') as fd:
            lines = fd.readlines()
            fd.seek(0)
            fd.writelines(line for line in lines if line.strip())
            fd.truncate()

        with open(file_url + ".txt", "r") as file:
            lines = file.readlines()
            lines = [line.replace(' ', '') for line in lines]

        ob = Solution()
        start_time = time.time()

        nodi = []

        # ------------------------------------------------------------
        # -                                                          -
        # -                   FASE DI COMPRESSIONE                   -
        # -                                                          -
        # ------------------------------------------------------------

        for input_string in lines:
            compelapsed_time = time.time() - start_time
            if input_string.endswith("\n"):
                input_string = input_string[:-1]

            # Controllo Alfanumerico
            if not ob.checkAlphanumeric(input_string):
                input_string = ob.deleteSpecialCharacters(input_string)

            assert "$" not in input_string
            input_string = input_string + "$"
            print("\nInput: " + input_string)

            bwt_result = ob.BWT_Encode(input_string)
            print("BWT: ", bwt_result[0])
            no_dollar_string = bwt_result[0].replace("$", "")
            tmp = list(bwt_result)
            tmp[0] = no_dollar_string
            bwt_result = tuple(tmp)
            print("BWT No-Dollar: ", no_dollar_string)

            if not no_dollar_string:
                continue

            # Chiamata funzione RLE
            rle_result = ob.RLE_Encode(bwt_result)
            print("RLE: ", rle_result)

            # Chiamata funzione LZW
            lzw_result = ob.LZW_Encode(rle_result)
            print("LZW: ", lzw_result)

            # Chiamata funzione Huffman
            the_data = lzw_result[0]
            encoding, the_tree = ob.HuffmanEncoding(lzw_result[0])

            nodi.append(the_tree)

            print("Final Encoded output with Huffman:", encoding)

            # Vecchio formato stringa
            output_string = str(encoding) + "," + str(lzw_result[1])

            # Nuovo formato, versione tupla, richiamare elementi con [i]
            # output_tuple = (str(encoding), str(the_tree), str(lzw_result[1]))

            # print("Output Tuple: ", output_tuple)

            with open('compressed.txt', "a+", ) as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(output_string)

        ob.saveToBin(nodi)

        print("\n" + str(compelapsed_time) + " -> Compression elapsedTime")
        break

# ------------------------------------------------------------
# -                                                          -
# -                  FASE DI DECOMPRESSIONE                  -
# -                                                          -
# ------------------------------------------------------------



    if action == "d":

        if os.path.isfile('decompressed.txt'):
            os.remove('decompressed.txt')

        ob = Solution()
        start_time = time.time()

        nodes = ob.readFromBin()
        compressed_output = []
        dollar_pos = []
        couples = []

        with open("compressed.txt", "r") as file:
            for line in file.readlines():
                x = line.split(",")
                compressed_output.append(x[0])
                dollar_pos.append(x[1])

        for x in range(0, len(nodes)):
            couples.append((compressed_output[x], nodes[x]))

        count = 0

        for x in couples:
            decompelapsed_time = time.time() - start_time

            huff_decode = ob.HuffmanDecoding(x[0], x[1])
            print("Huffman Decoding: ", huff_decode)

            # Chiamata funzione iLZW
            ilzw_result = ob.iLZW_Decode(huff_decode)
            print("iLZW result: ", ilzw_result)

            # Chiamata funzione iRLE
            irle_result = ob.iRLE(ilzw_result)
            print("iRLE result: ", irle_result)

            string_with_dollar = irle_result[:int(dollar_pos[count])] + "$" + irle_result[int(dollar_pos[count]):]

            ibtw_result = ob.iBWT(string_with_dollar)
            print("iBWT result: ", ibtw_result)
            print("\n")

            with open('decompressed.txt', "a+", ) as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(ibtw_result)

            count = count + 1

        print("\n" + str(decompelapsed_time) + " -> Decompression elapsedTime")
        break
    else:
        # Se l'utente inserisce un'opzione non valida, mostra un errore e ricomincia
        print("Opzione non valida. Per favore scegli c o d.")